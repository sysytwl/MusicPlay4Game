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