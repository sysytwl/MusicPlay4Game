import ctypes
import sys
import os
import time
import json
from mido import MidiFile
import keyboard
import ctypes

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

run_as_admin()

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
def play_midi(midi_file, keymap, use_closest=False, verbose=False, speed=1.0, focus_list=None):
    """
    Play the MIDI file.
    focus_list: list of window-title substrings. Before sending each note, wait until
                the foreground window title contains any one of these substrings.
                If focus_list is None or empty, no focus checking is done.
    """
    # Prepare mapped_notes list as before...
    mapped_notes = []
    for k, v in keymap.items():
        if v:
            try:
                mapped_notes.append(int(k))
            except ValueError:
                pass
    mapped_notes.sort()

    print(f"[+] Playing: {midi_file}  (use_closest={'ON' if use_closest else 'OFF'}, speed={speed})")
    try:
        mid = load_midi_file(midi_file)
    except OSError:
        print("[!] Aborting playback due to MIDI load failure.")
        return

    for msg in mid:
        # Adjust timing by speed
        delay = msg.time / speed if speed and speed > 0 else msg.time
        time.sleep(max(0,delay-0.05))#keypress correction for keyboard lag

        if msg.type == 'note_on' and msg.velocity > 0:
            note_int = msg.note
            note_str = str(note_int)

            # --- Focus check: wait until any substring in focus_list matches ---
            if focus_list:
                while True:
                    title = get_foreground_window_title()
                    # Check if any substring matches (case-insensitive)
                    matched = False
                    for substr in focus_list:
                        if substr.lower() in title.lower():
                            matched = True
                            if verbose:
                                print(f"[Focused] Window '{title}' matches '{substr}', proceeding with Note {note_int}")
                            break
                    if matched:
                        break
                    # Not matched yet: print and wait
                    print(f"[Waiting] Note {note_int}: current window '{title}' not in focus list; waiting...")
                    time.sleep(2)

            # --- Mapping / replacement logic as before ---
            mapped = keymap.get(note_str, "")
            if mapped:
                if verbose:
                    print(f"Note {note_int} → Key '{mapped}'")
                keyboard.press(mapped)
                time.sleep(0.05)
                keyboard.release(mapped)
            else:
                if use_closest and mapped_notes:
                    closest_note = find_closest_note(note_int, mapped_notes)
                    if closest_note is not None:
                        key = keymap.get(str(closest_note))
                        if key:
                            print(f"[Replaced] Note {note_int} unmapped; using closest mapped note {closest_note} → Key '{key}'")
                            keyboard.press(key)
                            time.sleep(0.05)
                            keyboard.release(key)
                            continue
                print(f"[Ignored] Note {note_int} has no key mapping")


# ------------------- Main Entry -------------------
def print_usage():
    print("Usage: python midi_to_keyboard.py <your.mid> <keymap.json> [--print] [--closest] [--speed <float>] [--focus <window_substring>] [--list-windows]")
    print("  --print           : print every mapped key press (verbose).")
    print("  --closest         : replace unmapped/empty notes by the closest available mapped note.")
    print("  --speed <num>     : playback speed multiplier (>1 faster, <1 slower).")
    print("  --focus <substring> : only send keys when foreground window title contains the given substring.")
    print("                       If omitted, uses all default substrings in the list.")
    print("  --list-windows    : list available default window substrings.")
    time.sleep(5)
    sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print_usage()

    midi_file = sys.argv[1]
    keymap_file = sys.argv[2]

    verbose_mode = False
    use_closest = False
    speed = 1.0

    focus_substr = None

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
                    sys.exit(1)
                i += 2
            else:
                print("[!] --speed requires a numeric argument, e.g. --speed 1.5")
                sys.exit(1)
        elif arg == "--focus":
            if i + 1 < len(sys.argv):
                focus_substr = sys.argv[i + 1]
                print(f"[Info] Using focus substring: '{focus_substr}'")
                i += 2
            else:
                print("[!] --focus requires a window title substring argument.")
                sys.exit(1)
        elif arg == "--list-windows":
            print("Available default window substrings:")
            for substr in DEFAULT_FOCUS_LIST:
                print(f"  '{substr}'")
            sys.exit(0)
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

    # Load keymap and call play_midi with focus_list
    keymap = load_keymap(keymap_file)
    play_midi(
        midi_file,
        keymap,
        use_closest=use_closest,
        verbose=verbose_mode,
        speed=speed,
        focus_list=focus_list
    )

