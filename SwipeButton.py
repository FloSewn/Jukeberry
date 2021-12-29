from kivy.uix.carousel import Carousel

class SwipeButton(Carousel):
    ''' This class defines a swipe button in the
        songpool
    '''

    def __init__(self, data, *args, **kwargs):
        ''' Initialize a new swipe button
        '''
        super().__init__(*args, **kwargs)
        self.main_screen = data['main_screen']
        self.song        = data['song']
        self.playlist    = data['playlist']
        self.songpool    = data['songpool']

        self.text = self.song.song_str
        self.marked_time = 0

    def add_song_to_playlist(self, take_out=True):
        ''' Add song to playlist and update the
            songpool preview
        '''
        # If too many songs in playlist
        # -> send message to user
        if not self.playlist.is_taking_songs():
            return

        # Queue song
        self.song.queue( self.playlist )

        # Take out song
        if take_out:
            self.song.hide()
            self.songpool.remove_song( self.song )

        # Update main screen
        self.main_screen.update_playlist_layout()
        self.main_screen.remove_songpool_layout_widget( self )


    def press_add_button(self):
        ''' Handle the pressing of the main button in
            caroussel, which adds songs to the playlist.
            If too many songs are currently in the playlist,
            a message is printed to the user.
        '''
        if self.playlist.is_taking_songs():
            self.load_slide(self.slides[1])
        else:
            self.load_slide(self.slides[2])
