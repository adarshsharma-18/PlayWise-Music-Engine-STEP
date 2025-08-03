from SongRating_tree import RatingBST, SongNode
from playlist_engine import Playlist, SongNode , PlaylistSwitcher
from playback_history import PlaybackHistory
from snapshot import SnapshotDashboard

class SongLookup:
    def __init__(self):
        self.id_map = {}       # song_id (UUID) → SongNode
        self.title_map = {}    # title → [SongNode, ...]

    def add_song(self, song_node):
        # Map by ID
        self.id_map[song_node.id] = song_node

        # Map by title (many songs can share the same title)
        if song_node.title not in self.title_map:
            self.title_map[song_node.title] = []
        self.title_map[song_node.title].append(song_node)

    def get_by_id(self, song_id):
        return self.id_map.get(song_id)

    def get_by_title(self, title):
        return self.title_map.get(title, [])

    def remove_song(self, song_id):
        song = self.id_map.pop(song_id, None)
        if song:
            # Remove from title map too
            if song.title in self.title_map:
                self.title_map[song.title] = [s for s in self.title_map[song.title] if s.id != song_id]
                if not self.title_map[song.title]:
                    del self.title_map[song.title]


#----------------test(lookup,sort,dasborad)------------------------
def test1():
    lookup = SongLookup()
    history = PlaybackHistory()
    rating_tree = RatingBST()
    playlist = Playlist(history) 

    # Add songs to playlist, rating tree, and lookup map in one step
    songs_with_ratings = [
        ("Chaiyya Chaiyya", "Sukhwinder Singh", "4:18", 5),
        ("Kesariya", "Arijit Singh", "4:30", 4),
        ("Tum Hi Ho", "Arijit Singh", "4:20", 5),
    ]

    for title, artist, duration, rating in songs_with_ratings:
        playlist.add_song(title, artist, duration)
        new_song_node = playlist.tail  # last added node
        rating_tree.insert_song(new_song_node, rating)
        lookup.add_song(new_song_node)  # sync lookup

    # Get by ID
    song_id = playlist.head.id
    song = lookup.get_by_id(song_id)
    if song:
        print(f"[Lookup by ID] Found: {song.title} by {song.artist}")

    # Get all songs by title
    title_query = "Tum Hi Ho"
    matches = lookup.get_by_title(title_query)
    print(f"[Lookup by Title] Matches for '{title_query}':")
    for s in matches:
        print(f"- [{s.id[:8]}] {s.title} by {s.artist}")

    playlist.print_playlist()
    #check sorting functionality

    playlist.sort_playlist(criteria="title", ascending=False)
    playlist.print_playlist()

    # Sort by duration (longest to shortest)
    playlist.sort_playlist(criteria="duration", ascending=False)
    playlist.print_playlist()

    # Restore original order (recently added)
    print("[Restoring recently added order]")
    # Could be skipped if original playlist structure was preserved elsewhere
    
    # After building playlist, history, and rating tree
    dashboard = SnapshotDashboard(playlist, history, rating_tree)
    snapshot = dashboard.export_snapshot()

    # Print Snapshot
    print("\n📊 [Dashboard Snapshot]")
    print("🔸 Top 5 Longest Songs:")
    for song in snapshot["top_5_longest_songs"]:
        print(f"- {song}")

    print("\n🔸 Recently Played Songs:")
    for song in snapshot["recently_played_songs"]:
        print(f"- {song}")

    print("\n🔸 Song Count by Rating:")
    for rating, count in snapshot["song_count_by_rating"].items():
        print(f"⭐ {rating} star(s): {count} song(s)")

    

# test1()
#-----------------test2(satck to swithch)------------------------
def test2():    
    # Create two playlists
    history = PlaybackHistory()
    playlist1 = Playlist(history, name="Bollywood Vibes")
    playlist2 = Playlist(history, name="Romantic Classics")
    switcher = PlaylistSwitcher()

    # Add songs
    playlist1.add_song("Chaiyya Chaiyya", "Sukhwinder Singh", "4:48")
    playlist1.add_song("Kal Ho Naa Ho", "Sonu Nigam", "5:00")
    playlist2.add_song("Tum Hi Ho", "Arijit Singh", "4:20")
    playlist2.add_song("Agar Tum Saath Ho", "Alka Yagnik", "5:42")

    # Simulate switching and playing
    switcher.switch_to(playlist1)
    playlist1.play_next()  # Plays Chaiyya Chaiyya
     # Plays Kal Ho Naa Ho

    switcher.switch_to(playlist2)
    playlist2.play_next()  # Plays Tum Hi Ho

    # Switch back to playlist1 and resume
    switcher.switch_to(playlist1)
    playlist1.play_next()  # Resumes from last position

# test2()