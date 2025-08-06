```markdown
# 🎵 PlayWise Music Engine

A sophisticated backend engine for a **smart music playlist management system**, developed as a solution for the **PlayWise DSA Hackathon**. This project showcases the practical application of core data structures and algorithms to build a **modular, performance-oriented system**.

---

## 🌟 Core Features

- **🎶 Dynamic Playlist Management**  
  Powered by a **Doubly Linked List** for efficient song addition, deletion, reordering, and reversal.

- **⏪ Playback History & Undo**  
  Uses a **Stack** to maintain playback history, enabling instant undo of last played track.

- **⭐ Song Rating System**  
  Implements a **Binary Search Tree (BST)** to index and retrieve songs by rating (1-5 stars).

- **⚡ Instant Song Lookup**  
  Achieved with a **Hash Map** (Python Dictionary) for O(1) lookups by song ID or title.

- **🧮 Advanced Sorting**  
  Employs a custom **Merge Sort** algorithm to sort playlists by title, duration, or recency.

- **🔊 Volume Normalization**  
  Normalizes song volumes to a consistent average level across the playlist.

- **🎛️ Multi-Playlist Management**  
  A **PlaylistSwitcher** allows seamless switching between playlists while retaining playback positions.

- **📊 System Snapshot Dashboard**  
  Real-time dashboard showing:
  - Top 5 longest songs
  - Recently played tracks
  - Count of songs by rating

---

## 🏗️ System Architecture

The project follows a **modular architecture**. Each core functionality is encapsulated in its own Python module, promoting scalability and maintainability.

The `main.py` script acts as the central orchestrator, initializing all components and managing the main application loop.

### 📐 Architecture Overview:

```

main.py
├── playlist\_engine.py        # Playlist & PlaylistSwitcher (Doubly Linked List)
├── playback\_history.py       # PlaybackHistory (Stack)
├── SongRating\_tree.py        # RatingBST (Binary Search Tree)
├── instant\_song\_lookup.py    # SongLookup (Hash Map)
├── mergesort.py              # Custom Merge Sort Algorithm
├── snapshot.py               # Snapshot Dashboard
├── volumecontrol.py          # Volume Normalizer

````

---

## 🛠️ Tech Stack & Concepts

- **Language**: Python 3.x

- **Core Data Structures**:
  - Doubly Linked List (`playlist_engine.py`)
  - Stack (`playback_history.py`)
  - Binary Search Tree (`SongRating_tree.py`)
  - Hash Map / Dictionary (`instant_song_lookup.py`)

- **Algorithms**:
  - Merge Sort (`mergesort.py`)
  - In-order Tree Traversal
  - Iterative node/list manipulation

---

## 🚀 Getting Started

### ✅ Prerequisites

- Python 3.x installed

### 🧩 Installation

```bash
git clone https://github.com/adarshsharma-18/playwise-music-engine-step.git
cd playwise-music-engine-step
````

### ▶️ Running the Application

```bash
python main.py
```

You’ll see an interactive menu:

```
==================================================
PlayWise: Currently playing 'Bollywood Vibes'
==================================================
1. Add a song
2. Delete a song
3. Move a song
4. Reverse playlist
5. Sort playlist
6. Play next song
7. Undo last played song
8. Search by title
9. Search by rating
10. View system snapshot (Dashboard)
11. Normalize playlist volume
12. Switch to another playlist
13. Print current playlist
0. Exit
==================================================
Enter your choice:
```

---

## 📦 Modules Overview

| Module                   | Description                                                                           |
| ------------------------ | ------------------------------------------------------------------------------------- |
| `main.py`                | Entry point of the app; runs the interactive UI loop.                                 |
| `playlist_engine.py`     | Implements `SongNode`, `Playlist`, and `PlaylistSwitcher` using a Doubly Linked List. |
| `playback_history.py`    | Implements `PlaybackHistory` using a Stack (list).                                    |
| `SongRating_tree.py`     | Defines `RatingNode` and `RatingBST` for storing songs by rating.                     |
| `instant_song_lookup.py` | Implements `SongLookup` with dictionaries for fast lookup.                            |
| `mergesort.py`           | Contains `merge_sort()` used to sort playlists.                                       |
| `snapshot.py`            | Defines the `SnapshotDashboard` for system stats.                                     |
| `volumecontrol.py`       | Contains `VolumeNormalizer` to adjust volume levels.                                  |

---

## 🔮 Future Improvements

* 🖥 **GUI Interface**: Build a GUI using **Tkinter** or **PyQt** for improved UX.
* 💾 **Data Persistence**: Save playlists and data using **SQLite** or **JSON**.
* 🌲 **Self-Balancing BST**: Upgrade to **AVL** or **Red-Black Tree** for guaranteed O(log k) operations.
* 🧯 **Robust Error Handling**: Improve user feedback with granular exceptions and error messages.

---

## 👨‍💻 Author

**Adarsh Sharma**
🔗 [GitHub Profile](https://github.com/adarshsharma-18)

