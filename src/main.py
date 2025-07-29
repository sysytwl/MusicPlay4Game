import ctypes
import sys
import os
import time
import json
from mido import MidiFile
import keyboard
import ctypes
from music21 import converter, key

# ------------------- MIDI Key Detection -------------------
def detect_midi_key(midi_path):
    print(f"[AutoKey] Detecting key for MIDI file: {midi_path}, based on the size of the file, this may take a while...")
    try:
        score = converter.parse(midi_path)
        key_obj = score.analyze('key')
        print(f"[AutoKey] Detected key: {key_obj.tonic.name} {key_obj.mode}")
        return key_obj
    except Exception as e:
        print(f"[!] Key detection failed: {e}")
        return None

# ------------------- Window focus detection (Windows) -------------------
def get_foreground_window_title():
    """
    Return the title of the current foreground window (Windows).
    """
    user32 = ctypes.windll.user32
    hwnd = user32.GetForegroundWindow()
    if hwnd == 0:
        return ""
    length = user32.GetWindowTextLengthW(hwnd)
    buff = ctypes.create_unicode_buffer(length + 1)
    user32.GetWindowTextW(hwnd, buff, length + 1)
    return buff.value

DEFAULT_FOCUS_LIST = [
    "原神",      # Genshin Impact
    "Honkai",     # Honkai Impact 3rd
    "Synthesia",    # Synthesia piano tutor
    "Minecraft",
]

# ------------------- Admin Elevation (Windows) -------------------
def run_as_admin():
    if os.name != 'nt':
        return
    if ctypes.windll.shell32.IsUserAnAdmin():
        return
    script = os.path.abspath(sys.argv[0])
    params = ' '.join([f'"{arg}"' for arg in sys.argv[1:]])
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, f'"{script}" {params}', None, 1)
    sys.exit()

# ------------------- Load Keymap -------------------
def load_keymap(file_path):
    if not os.path.exists(file_path):
        print(f"[!] Keymap file '{file_path}' not found.")
        sys.exit(1)

    with open(file_path, 'r') as f:
        if file_path.endswith('.json'):
            try:
                raw = json.load(f)
            except json.JSONDecodeError as e:
                print(f"[!] Failed to parse JSON keymap: {e}")
                sys.exit(1)
            # Ensure keys and values are strings
            keymap = {}
            for k, v in raw.items():
                sk = str(k)
                if v is None:
                    sv = ""
                else:
                    sv = str(v)
                keymap[sk] = sv
        else:
            print("Error: Keymap file must be in JSON format. Now using default keymap.")
            keymap = {
                "60": "a", "61": "s", "62": "d", "63": "f",
                "64": "g", "65": "h", "66": "j", "67": "k",
                "68": "l"
            }
    return keymap

# ------------------- Load MIDI File -------------------
def load_midi_file(path):
    """
    Try loading the MIDI file normally; if data-byte errors occur,
    retry with clip=True. If still fails, raise.
    """
    try:
        mid = MidiFile(path)
        return mid
    except OSError as e:
        print(f"[!] Warning: failed to load MIDI normally: {e}")
        print("[*] Retrying with clip=True (will attempt to clip out-of-range data bytes)...")
        try:
            mid = MidiFile(path, clip=True)
            print("[+] Loaded MIDI with clip=True")
            return mid
        except OSError as e2:
            print(f"[!] Error: failed to load MIDI even with clip=True: {e2}")
            raise

# ------------------- trans to C Major -------------------
def transpose_note(note, semitone_shift):
    new_note = note + semitone_shift
    return max(0, min(127, new_note))  # clamp to valid MIDI range

# ------------------- Find closest mapped note -------------------
def find_closest_note(note_int, mapped_notes):
    """
    Given an integer note and a sorted list of mapped_notes (integers),
    return the mapped note int that is closest in absolute difference.
    If tie, returns the smaller note.
    """
    if not mapped_notes:
        return None
    # Linear search for min difference (list is usually small)
    closest = mapped_notes[0]
    min_diff = abs(note_int - closest)
    for mn in mapped_notes[1:]:
        diff = abs(note_int - mn)
        if diff < min_diff or (diff == min_diff and mn < closest):
            min_diff = diff
            closest = mn
    return closest

# ------------------- Play MIDI -------------------
def play_midi(midi_file, keymap, use_closest=False, verbose=False, speed=1.0, focus_list=None, transpose_offset=0):
    #import threading

    print(f"[+] Playing: {midi_file}  (use_closest={'ON' if use_closest else 'OFF'}, speed={speed}), transpose_offset={transpose_offset}")

    try:
        mid = load_midi_file(midi_file)
    except OSError:
        print("[!] Aborting playback due to MIDI load failure.")
        return

    mapped_notes = sorted(int(k) for k, v in keymap.items() if v)

    note_last_release_time = {}  # note: timestamp of last release
    REPEAT_NOTE_DELAY_THRESHOLD = 0.03  # 30ms
    for msg in mid:
        if msg.time > 0:
            time.sleep(msg.time / speed)

        if msg.type in ['note_on', 'note_off']:
            note = transpose_note(msg.note, transpose_offset)
            note_str = str(note)

            # Handle focus wait
            if focus_list:
                while True:
                    title = get_foreground_window_title()
                    if any(substr.lower() in title.lower() for substr in focus_list):
                        break
                    print(f"[Waiting] Note {note}: current window '{title}' not in focus list; waiting...")
                    time.sleep(2)

            key = keymap.get(note_str, "")

            # Find replacement key if missing
            if not key and use_closest:
                numeric_note = int(note_str)
                mapped_notes = sorted(int(k) for k in keymap)
                min_note = mapped_notes[0]
                max_note = mapped_notes[-1]

                if min_note <= numeric_note <= max_note:
                    closest_note = find_closest_note(note, mapped_notes)
                    if closest_note is not None:
                        key = keymap.get(str(closest_note))
                        if key:
                            print(f"[Replaced] Note {note} unmapped; using closest mapped note {closest_note} → Key '{key}'")

            if not key:
                print(f"[Ignored] Note {note} has no key mapping")
                continue

            if msg.type == 'note_on' and msg.velocity > 0:
                now = time.time()
                last_release = note_last_release_time.get(note, 0)
                if now - last_release < REPEAT_NOTE_DELAY_THRESHOLD:
                    time.sleep(REPEAT_NOTE_DELAY_THRESHOLD-(now - last_release))
                keyboard.press(key)
                if verbose:
                    print(f"[Pressed] Note {note} → Key '{key}'", end=" ")
            elif msg.type == 'note_off':
                keyboard.release(key)
                note_last_release_time[note] = time.time()
                keyboard.release(key)
                if verbose:
                    print(f"[Released] Note {note} → Key '{key}'", end=" ")
            else:
                print(f"[!] Unknown MIDI message type: {msg.type} for note {note}")

# ------------------- Main Entry -------------------
def print_usage():
    print("Usage: python midi_to_keyboard.py <your.mid> <keymap.json> [--print] [--closest] [--speed <float>] [--focus <window_substring>] [--list-windows]")
    print("  --print           : print every mapped key press (verbose).")
    print("  --closest         : replace unmapped/empty notes by the closest available mapped note.")
    print("  --speed <num>     : playback speed multiplier (>1 faster, <1 slower).")
    print("  --focus <substring> : only send keys when foreground window title contains the given substring.")
    print("                       If omitted, uses all default substrings in the list.")
    print("  --list-windows    : list available default window substrings.")
    print("  --transpose <to> <from/auto> : transpose the MIDI to C major from the given key.")
    print("'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3,'E': 4, 'F': 5, 'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8, 'Ab': 8,'A': 9, 'A#': 10, 'Bb': 10, 'B': 11,")
    print("  --transtone <-offest value>")
    time.sleep(10)
    sys.exit(1)

if __name__ == "__main__":
    run_as_admin()

    if len(sys.argv) < 3:
        print_usage()

    midi_file = sys.argv[1]
    keymap_file = sys.argv[2]

    verbose_mode = False
    use_closest = False
    speed = 1.1

    focus_substr = None

    KEY_NAME_TO_MIDI = {
        'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3,
        'E': 4, 'F': 5, 'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8, 'Ab': 8,
        'A': 9, 'A#': 10, 'Bb': 10, 'B': 11,
    }
    transpose_offset = 0
    target_key = "C"  # Default
    from_key = "C"  # Default
    i = 3
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "--print":
            verbose_mode = True
            i += 1
        elif arg == "--closest":
            use_closest = True
            i += 1
        elif arg == "--speed":
            if i + 1 < len(sys.argv):
                try:
                    speed = float(sys.argv[i + 1])
                    if speed <= 0:
                        raise ValueError
                except ValueError:
                    print(f"[!] Invalid speed value: {sys.argv[i+1]}. Must be a positive number.")
                    print_usage()
                i += 2
            else:
                print("[!] --speed requires a numeric argument, e.g. --speed 1.5")
                print_usage()
        elif arg == "--focus":
            if i + 1 < len(sys.argv):
                focus_substr = sys.argv[i + 1]
                print(f"[Info] Using focus substring: '{focus_substr}'")
                i += 2
            else:
                print("[!] --focus requires a window title substring argument.")
                print_usage()
        elif arg == "--list-windows":
            print("Available default window substrings:")
            for substr in DEFAULT_FOCUS_LIST:
                print(f"  '{substr}'")
            sys.exit(0)
        elif arg == "--transpose":
            if i + 2 < len(sys.argv):
                target_key = sys.argv[i + 1].capitalize()
                from_key = sys.argv[i + 2].capitalize()

                if target_key not in KEY_NAME_TO_MIDI:
                    print(f"[!] Unknown target key: {target_key}")
                    print_usage()

                if ((from_key != "Auto") and (from_key not in KEY_NAME_TO_MIDI)):
                    print(f"[!] Unknown source key: {from_key}")
                    print_usage()
                # else:
                #     # Manual shift
                #     transpose_mode = "manual"
                #     offset = (KEY_NAME_TO_MIDI[target_key] - KEY_NAME_TO_MIDI[from_key]) % 12
                #     transpose_offset = offset
                #     print(f"[Transpose] Manually shifting {from_key} → {target_key} (offset: {offset})")

                i += 3
            else:
                print("[!] Usage: --transpose <target_key> <from_key|auto>")
                print_usage()

        elif arg == "--transtone":
            if i + 1 < len(sys.argv):
                transpose_offset = int(sys.argv[i + 1])
                i += 2
            else:
                print("[!] Usage: --transtone <offest value>")
                print_usage()

        else:
            print(f"[!] Unknown argument: {arg}")
            print_usage()

    if focus_substr:
        # Only use the one provided
        focus_list = [focus_substr]
    else:
        # Use all defaults
        focus_list = DEFAULT_FOCUS_LIST.copy()
        print(f"[Info] No --focus given; using default focus substrings: {focus_list}")

    if from_key == "Auto":
        key_obj = detect_midi_key(midi_file)
        if key_obj:
            # Normalize name (E- → Eb)
            from_key = key_obj.tonic.name.replace("-", "b")
            #from_key = KEY_NAME_TO_MIDI.get(tonic_name, 0)

            # if key_obj.mode == "major":
            #     transpose_offset = -root
            #     print(f"[AutoKey] Transposing from {tonic_name} major → C major (shift: {transpose_offset})")
            # elif key_obj.mode == "minor":
            #     if "--minor-to-major" in sys.argv:
            #         # Relative minor → relative major
            #         major_tonic = (root + 3) % 12  # A minor (9) → C major (0)
            #         transpose_offset = (KEY_NAME_TO_MIDI["C"] - major_tonic) % 12
            #         print(f"[AutoKey] Shifting from {tonic_name} minor to C major via relative major (shift: {transpose_offset})")
            #     else:
            #         transpose_offset = (KEY_NAME_TO_MIDI["A"] - root) % 12
            #         print(f"[AutoKey] Transposing from {tonic_name} minor → A minor (shift: {transpose_offset})")
            # else:
            #     print(f"[AutoKey] Unknown mode '{key_obj.mode}', skipping transpose.")
            #     transpose_offset = 0
        else:
            print("[!] Key detection failed. Playing as-is.")
            from_key = "C"

    if not transpose_offset:
        transpose_offset = (KEY_NAME_TO_MIDI[target_key] - KEY_NAME_TO_MIDI[from_key]) #% 12

    # Load keymap and call play_midi with focus_list
    keymap = load_keymap(keymap_file)
    play_midi(
        midi_file,
        keymap,
        use_closest=use_closest,
        verbose=verbose_mode,
        speed=speed,
        focus_list=focus_list,
        transpose_offset=transpose_offset
    )

