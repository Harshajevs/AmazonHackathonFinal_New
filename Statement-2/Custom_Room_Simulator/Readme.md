python main.py

Admin Commands (admin.py)
Run as:

bash
python admin.py <command> [arguments...]
User & Role Management
add <username> – Add a new user to the room.

prom <username> – Promote a user to co-admin.

dem <username> – Demote a co-admin to regular user.

kick <username> – Remove a user from the room.

Chat
chat <message> – Send a message as admin.

Playlist Management
plist <playlist name> – Create a new playlist.

padd <playlist_id> <movie title> – Add a movie to a playlist.

prem <playlist_id> <movie_index> – Remove a movie from a playlist (admins/co-admins only).

pshow – Show all playlists.

pshow <playlist_id> – Show movies in a specific playlist.

pswitch <playlist_id> – Switch to another playlist (makes it the current playlist).

Current Playlist Operations
cpadd <movie title> – Add a movie to the current playlist.

cprem <movie_index> – Remove a movie from the current playlist (admins/co-admins only).

cpshow – Show the current playlist.

cpnext – Advance to the next movie in the current playlist (removes the first movie).

Polling
poll <question> <option1> <option2> ... – Create a poll.

pend <poll_id> – End a poll and show the result.

Global & Force Toggles
glob <setting> <on|off> – Toggle global settings (chat, reactions) for all users.

force <username> <setting> <on|off> – Force a personal setting for a user (admin only).

share <on|off> – Enable or disable screen sharing (admin only).

User Commands (user1.py, user2.py, ...)
Run as:

bash
python user1.py <command> [arguments...]
Communication
chat <message> – Send a message.

react <emoji_number> – Send a reaction (1: 😂, 2: 👍, 3: ❤️, 4: 👏).

Personal Controls
toggle <setting> <on|off> – Toggle personal settings (video, audio, reactions, screen_lock).

hand – Raise hand.

Polling
vote <poll_id> <option> – Vote in a poll.

Playlist Viewing
cpshow – Show the current playlist.

plist – Show all playlists.

plist <playlist_id> – Show movies in a specific playlist.