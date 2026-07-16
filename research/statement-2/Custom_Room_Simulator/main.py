import json, secrets, os

STATE, CHAT = "room_state.json", "group_chat.txt"
hid   = lambda: secrets.token_hex(4)
save  = lambda s: json.dump(s, open(STATE, "w", encoding="utf-8"), indent=4)
log   = lambda m: open(CHAT, "a", encoding="utf-8").write(m + "\n")

# fresh session
for f in (STATE, CHAT):
    open(f, "w", encoding="utf-8").close()

admin_id = hid()
state = {
    "room_id": hid(),
    "global_settings": {"chat_enabled": True, "reactions_enabled": True},
    "users": {
        admin_id: {
            "username": "AdminGPU",
            "roles": {"is_admin": True, "is_co_admin": False},
            "personal": {
                "video_on": True, "audio_on": True,
                "reactions_on": True, "screen_lock": False,
                "raised_hand": False
            }
        }
    },
    "playlists": {},                   # id ➜ {name, movies}
    "current_playlist": None,          # playlist id
    "polls": {},
    "screen_sharing_allowed": False
}
save(state)
log(f"Room {state['room_id']} created by AdminGPU.")
print("Room ready – use admin.py to add users.")
