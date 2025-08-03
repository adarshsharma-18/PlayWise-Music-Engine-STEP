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