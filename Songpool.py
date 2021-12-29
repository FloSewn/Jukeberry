from Songlist import Songlist


class Songpool(Songlist):

    def __init__(self):
        super().__init__("Songpool")
        self.preview = Songlist("SongpoolPreview")
        self.settings_screen = None

    def hide_songs(self, condition="song.group > 1"):
        ''' Hide songs to the user if condition is true
        '''
        for node in self.data:
            song = node.song
            if eval(condition):
                song.is_hidden = True

    def show_songs(self, condition="song.group > 1"):
        ''' Present songs to the user if condition is true
        '''
        for node in self.data:
            song = node.song
            if eval(condition):
                song.is_hidden = False


    def update_preview(self):
        ''' Creates a preview songlist for the user
            interface. The preview does not contain
            hidden songs
        '''
        # Add songs that are not hidden
        self.preview.clear()
        for node in self.data:
            song = node.song
            if not song.is_hidden:
                self.preview.add_song( song )
        # Sort preview list
        self.preview.sort()

    def clear(self):
        ''' Clears the songpool and also its preview list '''
        super().clear()
        self.preview.clear()

