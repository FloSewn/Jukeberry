from Songlist import Songlist
import random


class Playlist(Songlist):

    def __init__(self, songpool, n_minimum=3, n_maximum=7):
        super().__init__("Playlist")

        random.seed(539)

        self.songpool  = songpool
        self.n_minimum = min((n_minimum, len(songpool.data)))
        self.n_maximum = max((n_minimum, n_maximum))

        self.musicplayer = None

        self.add_random_songs()

    def add_random_songs(self, take_out=True):
        ''' Add randomly songs from the songpool
            until the required minimum of songs in the
            playlist is met
        '''
        # Add random songs to initialize the playlist
        n_pool = len(self.songpool.data)
        n_add  = 0

        while (len(self.data) < self.n_minimum) and (n_pool > 0):
            index = random.randint(0, n_pool-1)
            song = self.songpool.data[index].song
            song.queue( self )
            if take_out:
                song.hide()
                self.songpool.remove_song( song )
                n_pool = len(self.songpool.data)

            n_add += 1

        return (n_add > 0)


    def next_song(self):
        ''' Play the next song in the playlist
        '''
        # Remove previous head
        if len(self.data) < 1: return
        current_song = self.data[0].song
        current_song.is_queued  = False
        self.remove_song( current_song )

        # Play next song
        self.musicplayer.play_head()

        # Make new head
        if len(self.data) < 1: return
        current_song = self.data[0].song


    def is_taking_songs(self):
        ''' Returns true, if the playlist can take some
            more songs

            FADE OUT LABEL: https://stackoverflow.com/questions/35351729/having-a-label-fade-out-in-kivy/35354967
        '''
        if len(self.data) < self.n_maximum:
            return True

        return False


