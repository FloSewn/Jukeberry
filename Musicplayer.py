# https://codeloop.org/python-kivy-how-to-play-mp3-music/
from kivy.core.audio import SoundLoader
import time


class Musicplayer():

    def __init__(self):
        self.playlist = None
        self.cur_player = None
        self.old_player = None

        # Time step for fading-update
        self.fade_dt    = 0.01
        # Volume-delta during fading
        self.fade_vol   = 0.0035
        # Start volume for fading
        self.min_volume = 0.05
        # Song state at which next song is called
        self.start_fade = 0.95

        # Volume last song (needed to get volume
        # of a next song right)
        self.volume     = 0.0
        # Indicator to skip a song if "next" button
        # has been pressed several times in a row
        self.skip_old   = False

        # Interface for kivy clock for consistency
        self.time_delta = self.fade_dt

    def connect_playlist(self, playlist):
        self.playlist = playlist
        playlist.musicplayer = self

    def update(self, dt):
        ''' This function is frequently called in order
            to fade in new songs and fade out old songs
        '''
        if self.old_player is None:
            return

        # "Next" has been pushed twice
        if self.skip_old:
            self.old_player.stop()
            del self.old_player
            self.old_player = None
            self.cur_player.volume = self.volume
            self.skip_old = False
            return

        # Fade out old player - fade in new player
        old_vol = self.old_player.volume - self.fade_vol

        if (old_vol >= self.min_volume):
            # Clean floating point errors
            old_vol = float("{:.5f}".format(old_vol))
            new_vol = float("{:.5f}".format(
                self.cur_player.volume + self.fade_vol))
            # Adjust volume
            self.old_player.volume = old_vol
            self.cur_player.volume = new_vol

        else:
            self.old_player.stop()
            del self.old_player
            self.old_player = None
            self.cur_player.volume = self.volume


    def play_head(self):
        ''' Plays the current head song in the
            playlist
        '''
        head = self.playlist.get_head()

        if head is None: return
        next_song = head.song

        # Mark new head as being played
        head.song.was_played = True

        # Initialization of no song is playing yet
        if self.cur_player is None:
            self.cur_player = SoundLoader().load(
                    next_song.path )
            if self.cur_player:
                self.cur_player.play()
            return

        # "Next" hast been pushed twice:
        # Next song should be player but new song
        # is still fading in
        # --> Stop fading of old song
        if self.old_player is not None:
            self.old_player.stop()
            del self.old_player
            self.old_player = None
            self.skip_old = True

        # Load new song
        self.old_player = self.cur_player
        self.cur_player = SoundLoader().load(
                next_song.path )
        self.volume = self.old_player.volume
        if self.cur_player:
            self.cur_player.play()
            self.cur_player.volume = self.min_volume


    def stop(self):
        ''' Stop the music
        '''
        if self.cur_player is not None:
            self.cur_player.stop()

    def cont(self):
        ''' Continue the music
        '''
        if self.cur_player is not None:
            self.cur_player.play()

    def adjust_volume(self, value):
        ''' Adjust the music volume
        '''
        if self.cur_player is not None:
            self.cur_player.volume = value
        if self.old_player is not None:
            self.volume = value

    def adjust_fading(self, value):
        ''' Adjust the song fading start
        '''
        self.start_fade = value

    def is_playing(self):
        ''' Check the status of the music player
        '''
        return (self.cur_player is not None) and \
                (self.cur_player.get_pos() != 0)

    def state(self):
        ''' Returns the current state in the song
            normalized to [0,1]
        '''
        pos = self.cur_player.get_pos()
        tot = self.cur_player.length
        return pos/tot

    def ready_for_next_song(self):
        ''' Returns true if the next song should be
            played
        '''
        if self.state() >= self.start_fade:
            return True
        else:
            return False




