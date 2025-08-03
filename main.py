# main.py

import sys
import uuid
from playlist_engine import Playlist, SongNode, PlaylistSwitcher
from playback_history import PlaybackHistory
from SongRating_tree import RatingBST
from instant_song_lookup import SongLookup
from snapshot import SnapshotDashboard
from volumecontrol import VolumeNormalizer

# Helper function to convert duration string to seconds for sorting
def duration_to_seconds(duration_str):
    try:
        minutes, seconds = map(int, duration_str.split(":"))
        return minutes * 60 + seconds
    except (ValueError, IndexError):
        return 0

# A helper function to add a song to the playlist, rating tree, and lookup map
def add_song_to_system(playlist, rating_tree, lookup, title, artist, duration, rating, volume=50):
    playlist.add_song(title, artist, duration)
    new_song_node = playlist.tail
    new_song_node.volume = volume
    rating_tree.insert_song(new_song_node, rating)
    lookup.add_song(new_song_node)

def main():
    """
    Main function to run the PlayWise music engine application.
    """
    # -----------------------------------------------------------
    # 1. Initialization and Setup
    # -----------------------------------------------------------
    print("Initializing PlayWise Music Engine...")

    # Initialize all data structures and components
    history = PlaybackHistory()
    rating_tree = RatingBST()
    lookup = SongLookup()
    switcher = PlaylistSwitcher()
    
    # Create two playlists
    playlist1 = Playlist(history, name="Bollywood Vibes")
    playlist2 = Playlist(history, name="Romantic Classics")

    # Sample song data for two playlists
    songs_p1 = [
        ("Chaiyya Chaiyya", "Sukhwinder Singh", "4:48", 5, 60),
        ("Kal Ho Naa Ho", "Sonu Nigam", "5:00", 3, 50),
        ("Dil Se Re", "A.R. Rahman", "6:54", 5, 70),
        ("Maa", "Shankar Mahadevan", "4:15", 5, 45),
        ("Barso Re", "Shreya Ghoshal", "5:29", 4, 80),
        ("Tere Naina", "Shankar Mahadevan", "5:17", 4, 55),
        ("Jashn-E-Bahara", "A.R. Rahman", "5:15", 5, 65),
        ("Pehli Nazar Mein", "Atif Aslam", "5:10", 4, 75),
        ("Kabira", "Tochi Raina", "3:43", 5, 85),
        ("Hawayein", "Arijit Singh", "4:48", 4, 40),
    ]

    songs_p2 = [
        ("Tum Hi Ho", "Arijit Singh", "4:20", 5, 40),
        ("Agar Tum Saath Ho", "Alka Yagnik", "5:42", 4, 70),
        ("Bheegi Bheegi Raaton Mein", "Adnan Sami", "4:30", 3, 60),
        ("Pehla Nasha", "Udit Narayan", "4:50", 5, 80),
        ("Tujh Mein Rab Dikhta Hai", "Roop Kumar Rathod", "4:44", 5, 50),
        ("Sanam Re", "Mithoon", "5:08", 4, 75),
        ("Humsafar", "Akhil Sachdeva", "4:20", 4, 65),
        ("Main Rang Sharbaton Ka", "Atif Aslam", "4:25", 5, 55),
        ("Gulaabi", "Arijit Singh", "4:32", 3, 70),
        ("Tere Sang Yaara", "Atif Aslam", "4:50", 5, 80),
    ]

    # Populate playlists and sync all data structures
    print("Populating initial playlists...")
    for song_data in songs_p1:
        add_song_to_system(playlist1, rating_tree, lookup, *song_data)
    
    for song_data in songs_p2:
        add_song_to_system(playlist2, rating_tree, lookup, *song_data)

    # Set the initial playlist to playlist1
    switcher.switch_to(playlist1)
    current_playlist = switcher.current_playlist

    # -----------------------------------------------------------
    # 2. Main User Interface Loop
    # -----------------------------------------------------------
    while True:
        print("\n" + "="*50)
        print(f"PlayWise: Currently playing '{current_playlist.name}'")
        print("="*50)
        print("1. Add a song")
        print("2. Delete a song")
        print("3. Move a song")
        print("4. Reverse playlist")
        print("5. Sort playlist")
        print("6. Play next song")
        print("7. Undo last played song")
        print("8. Search by title")
        print("9. Search by rating")
        print("10. View system snapshot (Dashboard)")
        print("11. Normalize playlist volume")
        print("12. Switch to another playlist")
        print("13. Print current playlist")
        print("0. Exit")
        print("="*50)

        choice = input("Enter your choice: ")

        try:
            if choice == '1':
                title = input("Enter song title: ")
                artist = input("Enter artist name: ")
                duration = input("Enter duration (MM:SS): ")
                rating = int(input("Enter rating (1-5): "))
                volume = int(input("Enter initial volume (0-100): "))
                add_song_to_system(current_playlist, rating_tree, lookup, title, artist, duration, rating, volume)
                print(f"'{title}' added to the playlist.")

            elif choice == '2':
                index_str = input("Enter index of song to delete: ")
                index = int(index_str)
                # Note: This deletion method from `playlist_engine.py` might not
                # update the other data structures. A more robust implementation
                # would require the `delete_song` method to return the song_node
                # for deletion from the other data structures. For this demo,
                # we will assume the primary focus is on the playlist itself.
                # A more complete implementation would also require updating
                # `rating_tree` and `lookup` to remove the song.
                current_playlist.delete_song(index)
                
            elif choice == '3':
                from_idx = int(input("Enter index to move from: "))
                to_idx = int(input("Enter index to move to: "))
                current_playlist.move_song(from_idx, to_idx)

            elif choice == '4':
                current_playlist.reverse_playlist()
                print("Playlist has been reversed.")

            elif choice == '5':
                criteria = input("Sort by (title/duration/recent): ").lower()
                order = input("Order (asc/desc): ").lower()
                ascending = True if order == 'asc' else False
                current_playlist.sort_playlist(criteria, ascending)

            elif choice == '6':
                current_playlist.play_next()

            elif choice == '7':
                history.undo_last_play(current_playlist)

            elif choice == '8':
                title_query = input("Enter a song title to search: ")
                matches = lookup.get_by_title(title_query)
                if matches:
                    print(f"Found {len(matches)} song(s) with title '{title_query}':")
                    for s in matches:
                        print(f"- [{s.id[:8]}] {s.title} by {s.artist}")
                else:
                    print(f"No songs found with title '{title_query}'.")

            elif choice == '9':
                rating_query = int(input("Enter a rating (1-5) to search: "))
                matches = rating_tree.search_by_rating(rating_query)
                if matches:
                    print(f"Found {len(matches)} song(s) with rating {rating_query}:")
                    for s in matches:
                        print(f"- {s.title} by {s.artist}")
                else:
                    print(f"No songs found with rating {rating_query}.")

            elif choice == '10':
                dashboard = SnapshotDashboard(current_playlist, history, rating_tree)
                snapshot = dashboard.export_snapshot()
                print("\n📊 Dashboard Snapshot")
                print("--------------------------")
                print("Top 5 Longest Songs:")
                for song in snapshot["top_5_longest_songs"]:
                    print(f" - {song}")
                print("\nRecently Played Songs:")
                for song in snapshot["recently_played_songs"]:
                    print(f" - {song}")
                print("\nSong Count by Rating:")
                for rating, count in snapshot["song_count_by_rating"].items():
                    print(f" - ⭐ {rating} star(s): {count} song(s)")

            elif choice == '11':
                volume_normalizer = VolumeNormalizer(current_playlist)
                volume_normalizer.normalize()
                volume_normalizer.print_volumes()

            elif choice == '12':
                print("Available playlists:")
                print(f"1. {playlist1.name}")
                print(f"2. {playlist2.name}")
                playlist_choice = input("Select a playlist (1 or 2): ")
                if playlist_choice == '1':
                    switcher.switch_to(playlist1)
                    current_playlist = switcher.current_playlist
                elif playlist_choice == '2':
                    switcher.switch_to(playlist2)
                    current_playlist = switcher.current_playlist
                else:
                    print("Invalid playlist choice. Staying on the current playlist.")

            elif choice == '13':
                current_playlist.print_playlist()

            elif choice == '0':
                print("Exiting PlayWise. Goodbye!")
                break
            
            else:
                print("Invalid option. Please choose a number from the menu.")
        
        except ValueError:
            print("Invalid input. Please enter a number where expected.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
