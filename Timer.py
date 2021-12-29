

class Timer:

    def __init__(self, **kwargs):
        self.playlist = kwargs.get('playlist', None)
        self.songpool = kwargs.get('songpool', None)
        self.musicplayer = kwargs.get('musicplayer', None)
        self.main_screen = kwargs.get('main_screen', None)
        self.settings_screen = kwargs.get('settings_screen', None)

        # refresh time
        self.time_delta = 3.0 / 6.0

    def update(self, dt):
        ''' This functions are called perdiodically
            from the app
        '''
        # Update swipe buttons
        self.main_screen.update_songpool_buttons()

        # Add songs to playlist if it contains too less
        if self.playlist.add_random_songs():
            self.main_screen.update_playlist_layout()
            self.main_screen.update_songpool_layout()

        # Update volume
        if self.musicplayer.old_player is None:
            self.musicplayer.adjust_volume(
                    self.settings_screen.ids.volume_slider.value )

        # Update song fading
        self.musicplayer.adjust_fading(
                self.settings_screen.ids.fading_slider.value )

        # Play to next song if current one is over or
        # if curreng song is near the end
        if (self.musicplayer.old_player is None   \
            and not self.musicplayer.is_playing()   ) \
        or self.musicplayer.ready_for_next_song():
            self.playlist.next_song()
            self.main_screen.update_playlist_layout()







