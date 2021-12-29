import os, sys
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

# https://codeloop.org/python-kivy-how-to-play-mp3-music/
from kivy.core.audio import SoundLoader

from SwipeButton import SwipeButton


class MainScreen(Screen):
    ''' This class defines the main window of the jukebox
        application
    '''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.songpool           = None
        self.playlist           = None
        self.settings_screen    = None

    def connect_songpool(self, songpool):
        self.songpool = songpool
        songpool.main_screen = self

    def connect_playlist(self, playlist):
        self.playlist = playlist
        playlist.main_screen = self

    def update_songpool_layout(self):
        ''' Update the songpool layout according to
            all current non-hidden songs that are available
            in the songpool
        '''
        songpool_layout = self.ids.songpool_boxlayout
        songpool_layout.clear_widgets()

        for i, node in enumerate(self.songpool.data):
            song = node.song
            if song.is_hidden: continue
            data = {
                    'main_screen': self,
                    'song'       : song,
                    'playlist'   : self.playlist,
                    'songpool'   : self.songpool,
                    }
            swipe_button = SwipeButton( data=data )
            songpool_layout.add_widget( swipe_button )


    def remove_songpool_layout_widget(self, widget):
        ''' Removes a widget in the
            songpool layout without affecting the remaining
            widgets
        '''
        songpool_layout = self.ids.songpool_boxlayout
        songpool_layout.remove_widget( widget )


    def update_playlist_layout(self):
        ''' Update the labels that show the
            current playlist
        '''
        if len(self.playlist.data) < 1: return

        self.ids.playlist_boxlayout.clear_widgets()

        cur_artist_str = self.playlist.data[0].song.artist
        cur_title_str = self.playlist.data[0].song.title
        self.ids.artist_label.text = cur_artist_str
        self.ids.title_label.text = cur_title_str

        for i, node in enumerate(self.playlist.data):

            if i == 0:
                pass
            elif node.song.is_queued:

                label = Label(text=node.song.song_str,
                              size_hint_y=None,
                              height=40)

                label.color = (251./255., 245./255., 231./255., 1.)
                label.font_name = 'BungeeInline'
                label.font_size = 14

                self.ids.playlist_boxlayout.add_widget( label )


    def play_next_song(self):
        ''' Play the next song in the playlist
        '''
        self.playlist.next_song()
        self.update_playlist_layout()

    def close_app(self):
        ''' Close the application
        '''
        sys.exit(1)


    def update_songpool_buttons(self, show_count=10):
        ''' Update the state of the songpool swipebuttons
        '''
        songpool_layout = self.ids.songpool_boxlayout
        for child in songpool_layout.children:
            if child.index > 0:
                child.marked_time += 1
            if child.marked_time > show_count:
                if (child.index == 1):
                    child.load_previous()
                if (child.index == 2):
                    child.load_next()
                child.marked_time = 0


    def show_password_screen(self):
        ''' Switch to the password screen
        '''
        # password_screen must call its own method to
        # switch the screen, in order to handle the
        # activation of the password enigma
        self.password_screen.show_password_screen()




