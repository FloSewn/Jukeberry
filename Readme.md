# Jukeberry
---------------------------
<img src="img/sample/Main.png" alt="Jukeberry-MainMenu" width="800"/>

Jukeberry is a small Python/Kivy application to use your Raspberry Pi as a jukebox.

Simply place all songs that should appear in your jukebox playlist in the `mp3_files` directory. 
All songs must be named in the following format:

`ID-ARTIST-TITLE.mp3`

The `ID` refers to an integer which is used to group songs into different playlists. 
The current implementation allows four playlists with IDs `1` to `4`.

<img src="img/sample/Settings.png" alt="Jukeberry-SettingsMenu" width="800"/>

## License
The project is licensed under the MIT License - see the LICENSE file for details.
For the used fonts the corresponding license file is given in the respective directories.
