# from playback_history import PlaybackHistory
from mergesort import merge_sort
import uuid

class SongNode:
    def __init__(self, title, artist, duration, volume=50):
        self.id = str(uuid.uuid4()) #unique identifier for each song
        self.title = title
        self.artist = artist
        self.duration = duration
        self.volume = volume  # 0–100 scale
        self.adjusted_volume = None  # After normalization
        self.prev = None
        self.next = None

class Playlist:
    def __init__(self, history , name="Untitled"):
        # Time: O(1), Space: O(1)
        self.id = str(uuid.uuid4())
        self.name = name
        self.head = None
        self.tail = None
        self.current = None
        self.length = 0
        self.history = history


    def add_song(self, title, artist, duration):
        # Time: O(1), Space: O(1)
        new_node = SongNode(title, artist, duration)
        if not self.head:
            self.head = self.tail = new_node
            self.current = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        self.length += 1

    #to add a song at the start of the playlist(stack-undo functionality)
    def add_song_at_start(self, title, artist, duration):
        # Time: O(1), Space: O(1)
        new_node = SongNode(title, artist, duration)
        if not self.head:
            self.head = self.tail = self.current = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self.length += 1

    def delete_song(self, index):
        # Time: O(n), Space: O(1)
        if index < 0 or index >= self.length:
            print("Invalid index.")
            return

        curr = self.head
        for _ in range(index):
            curr = curr.next

        if curr.prev:
            curr.prev.next = curr.next
        else:
            self.head = curr.next

        if curr.next:
            curr.next.prev = curr.prev
        else:
            self.tail = curr.prev

        self.length -= 1

    def move_song(self, from_index, to_index):
        # Time: O(n), Space: O(1)
        if from_index == to_index or from_index < 0 or to_index < 0 or from_index >= self.length or to_index >= self.length:
            print("Invalid move.")
            return

        # Remove song from original position
        curr = self.head
        for _ in range(from_index):
            curr = curr.next

        # Detach node
        if curr.prev:
            curr.prev.next = curr.next
        else:
            self.head = curr.next
        if curr.next:
            curr.next.prev = curr.prev
        else:
            self.tail = curr.prev


        # Re-insert at new position
        if to_index == 0:
            curr.next = self.head
            curr.prev = None
            if self.head:
                self.head.prev = curr
            self.head = curr
            if not self.tail:
                self.tail = curr
        else:
            temp = self.head
            for _ in range(to_index - 1):#as i have removed one node so using -1
                temp = temp.next
            curr.next = temp.next
            curr.prev = temp
            if temp.next:
                temp.next.prev = curr
            else:
                self.tail = curr
            temp.next = curr


    def reverse_playlist(self):
        # Time: O(n), Space: O(1)
        curr = self.head
        self.tail = self.head

        while curr:
            curr.prev, curr.next = curr.next, curr.prev
            if not curr.prev:  #as we have  reached last node 
                self.head = curr #we can set it as head
            curr = curr.prev

    def play_next(self):
        # Time: O(1), Space: O(1)
        if not self.current:
            print("No song to play.")
            return
        print(f"Now playing: {self.current.title} by {self.current.artist}")
        self.history.push(self.current)
        self.current = self.current.next

    def play_previous(self):
        # Time: O(1), Space: O(1)
        if self.current and self.current.prev:
            self.current = self.current.prev
            print(f"Now playing: {self.current.title} by {self.current.artist}")
            self.history.push(self.current)
        else:
            print("No previous song.")

    def sort_playlist(self, criteria="title", ascending=True):
        # Time: O(n log n), Space: O(n)
        # Convert linked list to array for sorting
        songs = []
        current = self.head
        while current:
            songs.append(current)
            current = current.next

        if criteria == "title":
            key_func = lambda song: song.title.lower()
        elif criteria == "duration":
            key_func = lambda song: int(song.duration.split(":")[0]) * 60 + int(song.duration.split(":")[1])
        elif criteria == "recent":
            print("[Info] Playlist is already in recently added order.")
            # self.print_playlist()
            return
        else:
            print(f"[Error] Unknown sorting criteria: {criteria}")
            return

        # Sort using custom Merge Sort
        songs = merge_sort(songs, key=key_func, ascending=ascending)

        # Rebuild doubly linked list from sorted songs
        self.head = self.tail = None
        self.length = 0
        for song in songs:
            song.prev = song.next = None  # Reset links
            if not self.head:
                self.head = self.tail = song
            else:
                self.tail.next = song
                song.prev = self.tail
                self.tail = song
            self.length += 1

        print(f"[Sorted by {criteria}, {'ascending' if ascending else 'descending'}]")



    def print_playlist(self):
        # Time: O(n), Space: O(1)
        current = self.head
        index = 0
        print("\n--- Playlist ---")
        while current:
            marker = " ← current" if current == self.current else ""
            print(f"{index}: [{current.id[:8]}] {current.title} by {current.artist} ({current.duration}){marker}")

            current = current.next
            index += 1
        print("----------------\n")

class PlaylistSwitcher:
    def __init__(self):
        self.playlist_stacks = {}  # playlist_id → stack of SongNode
        self.current_playlist = None

    def switch_to(self, playlist):
        # Save current position
        # Time: O(1), Space: O(p) p - number of playlists
        if self.current_playlist and self.current_playlist.current:
            pid = self.current_playlist.id
            if pid not in self.playlist_stacks:
                self.playlist_stacks[pid] = []
            self.playlist_stacks[pid].append(self.current_playlist.current)

        # Switch to new playlist
        self.current_playlist = playlist
        pid = playlist.id
        if pid in self.playlist_stacks and self.playlist_stacks[pid]:
            # Resume from last saved song
            playlist.current = self.playlist_stacks[pid].pop()
            print(f"[Resumed] {playlist.name} from '{playlist.current.title}'")
        else:
            # Start from beginning
            playlist.current = playlist.head
            print(f"[Started] {playlist.name} from beginning.")




#----------------test--------------------------------



def test1():
    
    playlist = Playlist(None)
    playlist.add_song("Chaiyya Chaiyya", "Sukhwinder Singh", "4:48")
    playlist.add_song("Kesariya", "Arijit Singh", "4:30")
    playlist.add_song("Tum Hi Ho", "Arijit Singh", "4:20")
    playlist.print_playlist()

    print("deleting song at index 1")
    playlist.delete_song(1)
    playlist.print_playlist()

    print("Adding more songs to the playlist")
    playlist.add_song("Kal Ho Naa Ho", "Sonu Nigam", "5:00")
    playlist.add_song("Agar Tum Saath Ho", "Arijit Singh", "5:42")
    playlist.print_playlist()

    print("Moving song from index 2 to index 1")
    playlist.move_song(2, 1)
    playlist.print_playlist()

    print("Reversing the playlist")
    playlist.reverse_playlist()
    playlist.print_playlist()

# test1()


