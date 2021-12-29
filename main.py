from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen

from Songpool import Songpool
from MainScreen import MainScreen
from SettingsScreen import SettingsScreen
from Playlist import Playlist
from Song import Song
from Timer import Timer
from Musicplayer import Musicplayer
from PasswordScreen import PasswordScreen

import sys, os

# Set window size for raspberry pi touchscreen
from kivy.config import Config
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '480')

# Hide Mouse cursor
#Config.set("graphics", "show_cursor", 0)

# Turn on fullscreen mode
from kivy.core.window import Window
#Window.fullscreen = True

# Set custom font style
from kivy.core.text import LabelBase
LabelBase.register(name='BungeeShade',
                   fn_regular='fonts/bungee/fonts/Bungee_Basic/BungeeShade-Regular.ttf')
LabelBase.register(name='Bungee',
                   fn_regular='fonts/bungee/fonts/Bungee_Basic/Bungee-Regular.ttf')
LabelBase.register(name='BungeeInline',
                   fn_regular='fonts/bungee/fonts/Bungee_Basic/BungeeInline-Regular.ttf')


class JukeboxApp(App):

    def build(self):

        # Init songpool data structure
        self.songpool = Songpool()

        for mp3_file in os.listdir("mp3_files"):
            try:
                new_song = Song( mp3_file )
                self.songpool.add_song( new_song )
            except:
                print("Failed to add {:} to {:}".format(
                    mp3_file, self.songpool.name))

        # Sort entire songpool and show songs of category 0 & 1
        # in songpool preview
        self.songpool.sort()
        self.songpool.hide_songs("song.group >= 0")
        self.songpool.show_songs("song.group == 0 or song.group == 1")
        self.songpool.update_preview()

        # Init playlist data structure
        self.playlist = Playlist(self.songpool.preview)

        # Init music player
        self.musicplayer = Musicplayer()
        self.musicplayer.connect_playlist( self.playlist )
        self.musicplayer.play_head()

        # Load kivy files
        Builder.load_file("ScreenManager.kv")
        Builder.load_file("MainScreen.kv")
        Builder.load_file("SettingsScreen.kv")
        Builder.load_file("PasswordScreen.kv")
        Builder.load_file("SwipeButton.kv")

        # Init interface
        self.screen_manager  = ScreenManager()
        self.main_screen     = MainScreen(name='main_screen')
        self.settings_screen = SettingsScreen(name='settings_screen')
        self.password_screen = PasswordScreen(name='password_screen')
        self.settings_screen.connect_main_screen( self.main_screen )
        self.settings_screen.connect_songpool( self.songpool )
        self.password_screen.connect_main_screen( self.main_screen )
        self.password_screen.connect_settings_screen( self.settings_screen )

        # Set up main screen
        self.main_screen.connect_songpool( self.songpool.preview )
        self.main_screen.connect_playlist( self.playlist )
        self.main_screen.update_songpool_layout()
        self.main_screen.update_playlist_layout()

        # Set up interval functions
        self.timer = Timer(playlist=self.playlist,
                           songpool=self.songpool,
                           musicplayer=self.musicplayer,
                           main_screen=self.main_screen,
                           settings_screen=self.settings_screen)
        Clock.schedule_interval(
                self.timer.update,
                self.timer.time_delta)

        Clock.schedule_interval(
                self.musicplayer.update,
                self.musicplayer.time_delta)

        # Finally add screens
        self.screen_manager.add_widget(self.main_screen)
        self.screen_manager.add_widget(self.settings_screen)
        self.screen_manager.add_widget(self.password_screen)

        return self.screen_manager


if __name__ == '__main__':
    JukeboxApp().run()
