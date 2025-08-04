from playlist_engine import Playlist, SongNode
from playback_history import PlaybackHistory
from SongRating_tree import RatingBST
from snapshot import SnapshotDashboard
from instant_song_lookup import SongLookup

class VolumeNormalizer:
    def __init__(self, playlist):
        self.playlist = playlist

    def normalize(self):
        # Step 1: Collect all volumes
        current = self.playlist.head
        volumes = []
        while current:
            volumes.append(current.volume)
            current = current.next

        # Step 2: Compute average volume
        if not volumes:
            print("No songs to normalize.")
            return

        avg_volume = sum(volumes) / len(volumes)

        # Step 3: Normalize each song
        current = self.playlist.head
        while current:
            current.adjusted_volume = avg_volume
            current = current.next

        print(f"[Normalized] All songs adjusted to average volume: {round(avg_volume, 2)}")

    def print_volumes(self):
        current = self.playlist.head
        print("\n🎚️  Volume Levels:")
        while current:
            print(f"- {current.title}: Original {current.volume}, Adjusted {round(current.adjusted_volume, 2) if current.adjusted_volume else 'Not Normalized'}")
            current = current.next




#----------------test--------------------------------

def main():
    lookup = SongLookup()
    history = PlaybackHistory()
    rating_tree = RatingBST()
    playlist = Playlist(history)



    # Assign varying volumes while adding songs
    songs_with_ratings_and_volumes = [
        ("Chaiyya Chaiyya", "Sukhwinder Singh", "4:48", 5, 60),
        ("Kesariya", "Arijit Singh", "4:30", 4, 80),
        ("Tum Hi Ho", "Arijit Singh", "4:20", 5, 40),
        ("Kal Ho Naa Ho", "Sonu Nigam", "5:00", 3, 50),
        ("Agar Tum Saath Ho", "Alka Yagnik", "5:42", 4, 70),
    ]

    for title, artist, duration, rating, volume in songs_with_ratings_and_volumes:
        playlist.add_song(title, artist, duration)
        playlist.tail.volume = volume  # assign custom volume
        rating_tree.insert_song(playlist.tail, rating)
        lookup.add_song(playlist.tail)

    # Normalize volumes
    volume_normalizer = VolumeNormalizer(playlist)
    volume_normalizer.normalize()
    volume_normalizer.print_volumes()

# main()
