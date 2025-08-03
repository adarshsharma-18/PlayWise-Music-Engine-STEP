

class SnapshotDashboard:
    def __init__(self, playlist, history, rating_tree):
        self.playlist = playlist
        self.history = history
        self.rating_tree = rating_tree

    def export_snapshot(self):
        return {
            "top_5_longest_songs": self.get_top_5_longest(),
            "recently_played_songs": self.get_recently_played(),
            "song_count_by_rating": self.get_song_count_by_rating()
        }

    def get_top_5_longest(self):
        songs = []
        current = self.playlist.head
        while current:
            songs.append(current)
            current = current.next

        # Sort using duration as key (in seconds)
        songs.sort(
            key=lambda s: int(s.duration.split(":")[0]) * 60 + int(s.duration.split(":")[1]),
            reverse=True
        )
        return [f"{s.title} by {s.artist} ({s.duration})" for s in songs[:5]]
    def get_recently_played(self):
        return [
            f"{s.title} by {s.artist} ({s.duration})"
            for s in reversed(self.history.stack)
        ]

    def get_song_count_by_rating(self):
        rating_counts = {}
        self._count_ratings(self.rating_tree.root, rating_counts)
        return rating_counts

    def _count_ratings(self, node, rating_counts):
        if not node:
            return
        rating_counts[node.rating] = len(node.songs)
        self._count_ratings(node.left, rating_counts)
        self._count_ratings(node.right, rating_counts)
