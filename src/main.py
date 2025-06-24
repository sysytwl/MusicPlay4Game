import ctypes
import sys
import os
import time
import json
from mido import MidiFile, MidiFileError
import keyboard

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
    except (OSError, MidiFileError) as e:
        print(f"[!] Warning: failed to load MIDI normally: {e}")
        print("[*] Retrying with clip=True (will attempt to clip out-of-range data bytes)...")
        try:
            mid = MidiFile(path, clip=True)
            print("[+] Loaded MIDI with clip=True")
            return mid
        except Exception as e2:
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
def play_midi(midi_file, keymap, use_closest=False, verbose=False):
    """
    Play the MIDI file, using keymap dict of str(midi_note) -> key string.
    If use_closest=True, whenever a note is unmapped or maps to empty string,
    replace with the closest available mapped note. Print when replacements happen.
    If use_closest=False, unmapped notes just print "[Ignored...]".
    """
    # Prepare list of mapped notes as integers, for closest lookup
    mapped_notes = []
    for k, v in keymap.items():
        if v:  # only consider non-empty mappings
            try:
                ni = int(k)
                mapped_notes.append(ni)
            except ValueError:
                # skip keys that are not integers
                pass
    mapped_notes.sort()
    print(f"[+] Playing: {midi_file}  (use_closest={'ON' if use_closest else 'OFF'})")
    try:
        mid = load_midi_file(midi_file)
    except Exception:
        print("[!] Aborting playback due to MIDI load failure.")
        return

    for msg in mid:
        time.sleep(msg.time)
        if msg.type == 'note_on' and msg.velocity > 0:
            note_int = msg.note
            note_str = str(note_int)
            mapped = keymap.get(note_str, "")
            if mapped:
                # Direct mapping exists
                if verbose:
                    print(f"Note {note_int} → Key '{mapped}'")
                keyboard.press(mapped)
                keyboard.release(mapped)
            else:
                # Unmapped or empty
                if use_closest and mapped_notes:
                    closest_note = find_closest_note(note_int, mapped_notes)
                    if closest_note is not None:
                        key = keymap.get(str(closest_note))
                        if key:
                            print(f"[Replaced] Note {note_int} unmapped; using closest mapped note {closest_note} → Key '{key}'")
                            keyboard.press(key)
                            keyboard.release(key)
                            continue
                # If no replacement or use_closest=False:
                print(f"[Ignored] Note {note_int} has no key mapping")

# ------------------- Main Entry -------------------
def print_usage():
    print("Usage: python midi_to_keyboard.py <your.mid> <keymap.json> [--print] [--closest]")
    print("  --print    : print every mapped key press (verbose).")
    print("  --closest  : replace unmapped/empty notes by the closest available mapped note.")
    time.sleep(5)
    sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print_usage()

    midi_file = sys.argv[1]
    keymap_file = sys.argv[2]

    # Parse optional args
    verbose_mode = False
    use_closest = False
    i = 3
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "--print":
            verbose_mode = True
            i += 1
        elif arg == "--closest":
            use_closest = True
            i += 1
        else:
            print(f"[!] Unknown argument: {arg}")
            print_usage()

    if not os.path.exists(midi_file):
        print(f"[!] MIDI file '{midi_file}' not found.")
        sys.exit(1)

    keymap = load_keymap(keymap_file)
    play_midi(midi_file, keymap, use_closest=use_closest, verbose=verbose_mode)
