from datetime import datetime
import os

class Song:

    def __init__(self, song_key, song_dir='mp3_files'):
        self.group, self.artist, self.title = self.encrypt_song(song_key)
        self.song_dir   = song_dir
        self.played     = datetime.now()
        self.path       = os.path.join(self.song_dir, song_key)

        self.is_queued     = False
        self.is_hidden     = False
        self.was_played    = False

        self.list_links = {}

        self.song_str = "{:} - {:}".format(
                self.artist, self.title)

    def encrypt_song(self, key):
        (group, artist, title) = key.replace('.mp3','').replace('_',' ').split('-')
        return int(group), artist, title

    def queue(self, playlist):
        ''' Queue this song to a playlist '''
        self.is_queued = True
        playlist.add_song( self )

    def hide(self):
        ''' Hide this song '''
        self.is_hidden = True


