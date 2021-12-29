from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import NumericProperty, StringProperty, BooleanProperty
from kivy.uix.slider import Slider
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox


class SongpoolControl(BoxLayout):
    ''' This class defines a list of control boxes and
        corresponding song labels, which are utilized
        to control the available songs in the songpool
        on the main screen
    '''
    def __init__(self, **kwargs):
        super(SongpoolControl, self).__init__(**kwargs)

    def setup_rows(self, settings_screen, songpool):
        self.settings_screen = settings_screen
        self.songpool = songpool
        self.rows = []

        for node in songpool.data:
            new_row = SongpoolControlRow(self.settings_screen,node.song)
            self.add_widget( new_row )
            self.rows.append( new_row )

    def update_checkboxes(self):
        for row in self.rows:
            row.update()


class SongpoolControlRow(BoxLayout):
    ''' This class represents a row in the SongpoolControl
        structure.
        The checkbox is set active, if a corresponding song
        is available for the user in the main screen.
    '''
    title = StringProperty()
    artist = StringProperty()
    available = BooleanProperty()
    song = None

    def __init__(self, settings_screen, song, **kwargs):
        super(SongpoolControlRow, self).__init__(**kwargs)
        self.settings_screen = settings_screen
        self.title = song.title
        self.artist = song.artist
        self.available = not song.is_hidden
        self.song = song

    def update(self):
        self.available = not self.song.is_hidden

    def set_checkbox(self, is_active):
        ''' This function handles the activation / deactivation
            of songs in the settings menu
        '''
        # Pass if structure has not been initialized yet
        if (self.song is None):
            return

        # If song is currently queued, do nothing
        # --> Checkbox must remain inactive
        if (self.song.is_queued):
            self.ids.CheckBox.active = False
            self.available = False
            return

        # Update status
        self.available = is_active

        # Show song in songpool-preview
        if (self.available):
            self.song.is_hidden = False

            # Set song to "unplayed" state
            if self.song.was_played :
                self.song.was_played = False


        # Hide song from songpool-preview
        else:
            self.song.is_hidden = True

        # Set flag to update songpool on exit
        self.settings_screen.update_songpool_on_exit = True



class SettingsScreen(Screen):
    volume = NumericProperty(1.0)
    update_songpool_on_exit = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def connect_main_screen(self, main_screen):
        main_screen.settings_screen = self
        self.main_screen = main_screen

    def connect_songpool(self, songpool):
        songpool.settings_screen = self
        self.songpool = songpool
        self.ids.songpool_control.setup_rows(self, self.songpool)

    def set_song_category(self, state, index):
        ''' Handle the category checkboxes
        '''
        # Activate  / deactivate songs, that are in a single
        # category, which is specified by <index>
        if state:
            pool_str = '(song.group == {:d})'           \
                       'and (song.was_played == False)' \
                       'and (song.is_queued == False)'.format(index)
            self.songpool.show_songs(pool_str)
        else:
            pool_str = 'song.group == {:d}'.format(index)
            self.songpool.hide_songs(pool_str)

        # Update the songpool-control panel
        self.update_songpool_control()



    def update_songpool_control(self):
        ''' Update checkboxes in SongpoolControl structure
        '''
        self.ids.songpool_control.update_checkboxes()


    def show_main_screen(self):
        ''' Switch to the main screen - before going back,
            the songpool preview (and its layout in the main
            screen) always gets updated
        '''
        if self.update_songpool_on_exit:
            self.songpool.update_preview()
            self.main_screen.update_songpool_layout()
            self.update_songpool_on_exit = False

        self.manager.current = 'main_screen'
