# music player, conv mid to keys for games (ReBuild)

> test: genshin -> working

# TL;DR
1. open terminal and run: `file_location/MiDiConvPlayer.exe [mid file] [keymap.json]`
example:
```terminal
MiDiConvPlayer.exe ./mid_music/bwv988.mid ./keymaps/keymap.json --closest
 ```

2. midi web recommend: https://onlinesequencer.net/

# use method:
1. install python
2. install libs
```bat
pip install -r requirements.txt
```
3. run
```bat
python ./src/main.py ./mid_music/bwv988.mid ./keymaps/keymap.json --closest
```
4. help msg
```bat
python ./src/main.py
```

# log 
1. RBV1 rebuild v1
2. RBV1.1 error fix:
```txt
The error OSError: data byte must be in range 0..127 indicates that mido encountered a byte outside the valid MIDI data range while parsing the file. Some MIDI files may contain unexpected or slightly nonstandard bytes
```
3. RBV1.2 function add:
```txt
window -> stop/play
speed change
```

4. RBV1.3 function add:
```txt
Supports Simultaneous Notes and long notes
```

5. RB1.4 function add:
``` 
transfer tone
transfer major
```
bug fix:
```
zero intervial node, e.g. rush e, eeeeeeeeeeeeeeee
minium time 35ms for 30fps
```

6. 1.5&1.6
解决停顿感问题
解决重叠（按下没放开，又按下）

# FAQ

## Q: How can I add a GUI without making the Python EXE too large (e.g. 500MB)?

- **Why is the EXE so big?**  
  Packaging Python apps (with PyInstaller, etc.) bundles the Python interpreter and all dependencies, which increases size, especially with GUI libraries (like PyQt, Tkinter, etc.).

- **Advice to reduce EXE size:**
  1. **Use a lightweight GUI library:**  
     - `tkinter` (built-in, smallest),  
     - `customtkinter` (modern look, still small),  
     - Avoid PyQt/PySide unless you need advanced features.
  2. **Minimize dependencies:**  
     - Remove unused packages from your project and requirements.
  3. **PyInstaller options:**  
     - Use `--onefile` and `--noconsole` for a single EXE.  
     - Use `--exclude-module` to skip unused modules.
     - Use UPX (if available) to compress binaries: `pyinstaller --onefile --upx-dir=upx_folder ...`
  4. **Consider a web-based GUI:**  
     - Use `flask` or `fastapi` + `HTML/JS` for a browser-based interface.  
     - This keeps the EXE smaller and more portable.
  5. **Distribute as a Python script:**  
     - If possible, ask users to install Python and run the script directly.

- **Typical EXE sizes:**  
  - Minimal Tkinter GUI: ~30-60MB  
  - PyQt/PySide: 100MB+  
  - Web UI (Flask): ~30-60MB

- **Summary:**  
  For smallest EXE, use Tkinter, minimize dependencies, and use PyInstaller with UPX.

## Q: For Web UI, does that mean I need to open localhost:80 at runtime?

- Yes, a web-based GUI means your Python app will start a local web server (e.g., on `localhost:5000` or `localhost:80`).
- You interact with the app by opening a browser and visiting the local address (e.g., `http://localhost:5000`).
- You can choose the port (80, 5000, 8080, etc.) in your code. Port 80 may require admin rights; 5000/8080 are common defaults.
- The web server only runs on your computer (not public), unless you configure it otherwise.