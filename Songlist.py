import gc

from Song import Song


class Songlist:
    ''' A doubly linked list that contains numerous songs
    '''

    class ListNode:
        ''' A single node in the list
        '''
        def __init__(self, song):
            self.song = song

        def __eq__(self, other):
            return (self.song.artist == other.song.artist) \
                    and \
                   (self.song.title == other.song.title)

        def __lt__(self, other):
            if (self.song.artist > other.song.artist):
                return True
            elif (self.song.artist == other.song.artist):
                return (self.song.title > other.song.title)
            else:
                return False


    def __init__(self, name):
        ''' Init a new list
        '''
        self.name = name
        self.data = []

        # Reference to user interface
        self.main_screen = None

    def add_song(self, song):
        ''' Add a new song to the list
        '''
        new_node = self.ListNode(song)
        self.data.append( new_node )
        song.list_links[self.name] = len(self.data)-1
        print("Add new song to {:}: <{:}-{:}>".format(
            self.name, song.artist, song.title))

    def remove_song(self, song):
        ''' Removes a song from the list
        '''
        # Remove link to this list from the song
        try:
            i_node = song.list_links.pop(self.name)
        except:
            print("Song <{:}-{:}> not found in {:}".format(
                song.artist, song.title, self.name))
            return

        # Clear that node
        node = self.data.pop( i_node )
        node.song = None
        del node

        # Update indices of remaning list nodes
        self.update_list_links()

        # User output
        print("<{:}-{:}> has been removed from {:}".format(song.artist, song.title, self.name))


    def sort(self, reverse=True):
        ''' Sort the list alphabetically
        '''
        sorted_data = sorted(self.data, reverse=reverse)
        self.data = sorted_data
        self.update_list_links()

    def update_list_links(self):
        ''' Update the connection of the list songs
            to their respective list nodes
        '''
        for i, node in enumerate(self.data):
            node.song.list_links[self.name] = i

    def clear(self):
        ''' Clears all entries in the songlist
        '''
        for node in self.data[::-1]:
            i_node = node.song.list_links.pop(self.name)
            node = self.data.pop( i_node )
            node.song = None
            del node

        gc.collect()

    def get_head(self):
        ''' Return the head of the list
        '''
        if len(self.data) < 1:
            return None
        return self.data[0]








