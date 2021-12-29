from kivy.uix.screenmanager import ScreenManager, Screen

from kivy.uix.carousel import Carousel
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label


PASSWORD = [1,2,3]#,4,1,4,2,1]

class EnigmaLayout(GridLayout):

    is_active = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def setup_entries(self):
        ''' Create all enigma entries
        '''
        self.entries = []
        for i in range(len(PASSWORD)):
            new_entry = EnigmaEntry( self )
            self.add_widget( new_entry )
            self.entries.append( new_entry )

    def check_password(self):
        ''' Check the enigma for a correct password
        '''
        if not self.is_active:
            return

        # Check each entry for correctness
        for i, entry in enumerate(self.entries):
            cur_index = entry.index
            if cur_index != PASSWORD[i]:
                return

        # Switch to settings screen
        self.parent.parent.show_settings_screen()


    def reset(self):
        ''' Reset the enigma
        '''
        for entry in self.entries:
            entry.load_slide( entry.buttons[0] )



class EnigmaEntry(Carousel):

    def __init__(self, enigma_layout, **kwargs):
        super().__init__(**kwargs)

        self.enigma_layout = enigma_layout
        self.buttons = []

        # Create labels from 0 to 9
        for i in range(0,10):
            new_button = EnigmaLabel( text = str(i) )
            self.add_widget( new_button )
            self.buttons.append( new_button )


class EnigmaLabel(Label):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)



class PasswordScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def connect_main_screen(self, main_screen):
        main_screen.password_screen = self
        self.main_screen = main_screen
        self.ids.enigma_layout.setup_entries()

    def connect_settings_screen(self, settings_screen):
        settings_screen.password_screen = self
        self.settings_screen = settings_screen

    def show_settings_screen(self):
        ''' Switch to the settings screen
        '''
        # Reset enigma
        self.ids.enigma_layout.reset()
        # Deactivate enigma
        self.ids.enigma_layout.is_active = False

        self.settings_screen.update_songpool_control()
        self.manager.current = 'settings_screen'

    def show_main_screen(self):
        ''' Switch to the main screen
        '''
        # Reset enigma
        self.ids.enigma_layout.reset()
        # Deactivate enigma
        self.ids.enigma_layout.is_active = False

        self.manager.current = 'main_screen'

    def show_password_screen(self):
        # Activate enigma
        self.ids.enigma_layout.is_active = True
        # Set screen
        self.manager.current = 'password_screen'
