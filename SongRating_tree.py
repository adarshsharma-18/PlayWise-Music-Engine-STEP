from playback_history import PlaybackHistory
from playlist_engine import Playlist, SongNode

class RatingNode:
    def __init__(self, rating):
        self.rating = rating
        self.songs = []  # List of SongNode references
        self.left = None
        self.right = None

class RatingBST:
    def __init__(self):
        # Time: O(1), Space: O(1)
        self.root = None

    def insert_song(self, song_node, rating):
        # Average Time: O(log k), Worst: O(k), Space: O(1), where k is number of unique ratings
        if rating < 1 or rating > 5:
            print("Rating must be between 1 and 5.")
            return
        self.root = self._insert(self.root, song_node, rating)

    def _insert(self, node, song_node, rating):
        # Average Time: O(log k), Worst: O(k), Space: O(1)
        if not node:
            new_node = RatingNode(rating)
            new_node.songs.append(song_node)
            return new_node
        if rating < node.rating:
            node.left = self._insert(node.left, song_node, rating)
        elif rating > node.rating:
            node.right = self._insert(node.right, song_node, rating)
        else:
            node.songs.append(song_node)
        return node

    def search_by_rating(self, rating):
        # Average Time: O(log k), Worst: O(k), Space: O(1)
        node = self._search(self.root, rating)
        if node:
            return node.songs
        return []

    def _search(self, node, rating):
        # Average Time: O(log k), Worst: O(k), Space: O(1)
        if not node:
            return None
        if rating == node.rating:
            return node
        elif rating < node.rating:
            return self._search(node.left, rating)
        else:
            return self._search(node.right, rating)

    def delete_song(self, song_id):
        # Time: O(n), Space: O(h), n = total songs, h = tree height
        self._delete_song(self.root, song_id)

    def _delete_song(self, node, song_id):
        # Time: O(n), Space: O(h)
        if not node:
            return
        for i, song in enumerate(node.songs):
            if song.id[:8] == song_id:
                print(f"Deleting song: {song.title} from rating {node.rating}")
                del node.songs[i]
                break
        self._delete_song(node.left, song_id)
        self._delete_song(node.right, song_id)

    def print_all_ratings(self):
        # Time: O(n), Space: O(h)
        print("\n--- Song Ratings Tree ---")
        self._inorder_print(self.root)
        print("-------------------------\n")

    def _inorder_print(self, node):
        # Time: O(n), Space: O(h)
        if node:
            self._inorder_print(node.left)
            print(f"Rating {node.rating}:")
            for song in node.songs:
                print(f"  - [{song.id[:8]}] {song.title} by {song.artist} ({song.duration})")
            self._inorder_print(node.right)



#----------------test--------------------------------


def main():
    # Initialize components
    history = PlaybackHistory()
    rating_tree = RatingBST()
    playlist = Playlist(history)

    # Add songs to the playlist and rating tree in one step
    songs_with_ratings = [
        ("Chaiyya Chaiyya", "Sukhwinder Singh", "4:48", 5),
        ("Kesariya", "Arijit Singh", "4:30", 4),
        ("Tum Hi Ho", "Arijit Singh", "4:20", 5),
        ("Kal Ho Naa Ho", "Sonu Nigam", "5:00", 3),
        ("Agar Tum Saath Ho", "Alka Yagnik", "5:42", 4),
    ]

    for title, artist, duration, rating in songs_with_ratings:
        playlist.add_song(title, artist, duration)
        rating_tree.insert_song(playlist.tail, rating)  # playlist.tail is the newly added node

    # Initial Playlist
    print("\n[ Initial Playlist ]")
    playlist.print_playlist()

    # Playback simulation
    print("[ Playing Songs ]")
    playlist.play_next()  # Chaiyya Chaiyya
    playlist.play_next()  # Kesariya
    playlist.play_next()  # Tum Hi Ho

    # Undo last play
    print("[ Undo Last Playback ]")
    history.undo_last_play(playlist)
    playlist.print_playlist()

    # Search songs by rating
    print("[ Songs with 5-Star Rating ]")
    songs = rating_tree.search_by_rating(5)
    for song in songs:
        print(f"- {song.title} by {song.artist}")

    # Delete a song by ID
    id=input("Enter song ID to delete (first 8 characters): ")
    song_id = id
    print(f"[ Deleting Song from Rating Tree: {song_id} ]")
    rating_tree.delete_song(song_id)


    # Print updated rating BST
    print("[ Updated Rating BST ]")
    rating_tree.print_all_ratings()

    # Final Playlist View
    print("[ Final Playlist Snapshot ]")
    playlist.print_playlist()


# main()
