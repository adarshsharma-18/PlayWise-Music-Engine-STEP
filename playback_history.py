from playlist_engine import Playlist, SongNode

class PlaybackHistory:
    def __init__(self):
        # Time: O(1), Space: O(1)
        self.stack = []

    def push(self, song_node):
        # Time: O(1), Space: O(1)
        self.stack.append(song_node)

    def undo_last_play(self, playlist):
        # Time: O(1), Space: O(1)
        if not self.stack:
            print("No song to undo.")
            return
        song = self.stack.pop()
        print(f"Undoing play: {song.title} by {song.artist}")
        playlist.add_song_at_start(song.title, song.artist, song.duration)




#----------------test--------------------------------

def main():
    history = PlaybackHistory()
    playlist = Playlist(history)

    playlist.add_song("Chaiyya Chaiyya", "Sukhwinder Singh", "4:48")
    playlist.add_song("Kesariya", "Arijit Singh", "4:30")
    playlist.add_song("Tum Hi Ho", "Arijit Singh", "4:20")

    playlist.print_playlist()

    playlist.play_next()
    playlist.play_next()
    playlist.play_next()
    playlist.play_next()  # No more songs

    playlist.print_playlist()

    # Undo playback
    history.undo_last_play(playlist)
    history.undo_last_play(playlist)
    playlist.print_playlist()

# main()