import json, secrets

STATE, CHAT = "room_state.json", "group_chat.txt"
hid  = lambda: secrets.token_hex(4)

load = lambda: json.load(open(STATE, encoding="utf-8"))
save = lambda s: json.dump(s, open(STATE, "w", encoding="utf-8"), indent=4)
_APP = lambda ln: open(CHAT, "a", encoding="utf-8").write(ln + "\n")

def log_status(msg):  _APP(msg)
def log_chat(u,t):    _APP(f"[chat] {u}: {t}")
def log_react(u,e):   _APP(f"[reaction] {u}: {e}")

EMOJI = {"1":"😂","2":"👍","3":"❤️","4":"👏"}

uid = lambda n,s: next((k for k,v in s["users"].items() if v["username"]==n), None)
adm = lambda u,s: s["users"][u]["roles"]["is_admin"]
co  = lambda u,s: s["users"][u]["roles"]["is_co_admin"]
mod = lambda u,s: adm(u,s) or co(u,s)

def _kick_allowed(kicker,target,s):
    if adm(kicker,s):
        return True
    return co(kicker,s) and not adm(target,s)

# ── PLAYLISTS ──────────────────────────────────────────
def playlist_create(actor,name):
    s=load(); aid=uid(actor,s)
    if not mod(aid,s): return log_status("Denied.")
    pid=hid()
    s["playlists"][pid]={"name":name,"movies":[]}
    if s["current_playlist"] is None:
        s["current_playlist"] = pid
    save(s); log_status(f"{actor} created playlist {pid} ({name}).")

def playlist_add(actor,pid,title):
    s=load(); aid=uid(actor,s)
    if not mod(aid,s):           return log_status("Denied.")
    if pid not in s["playlists"]: return log_status("Playlist not found.")
    s["playlists"][pid]["movies"].append(title)
    save(s); log_status(f"{actor} added '{title}' to playlist {pid}.")

def playlist_remove(actor,pid,index):
    s=load(); aid=uid(actor,s)
    if not mod(aid,s): return log_status("Denied.")
    if pid not in s["playlists"]: return log_status("Playlist not found.")
    pl = s["playlists"][pid]["movies"]
    if not (0 <= index < len(pl)): return log_status("Invalid movie index.")
    removed = pl.pop(index)
    save(s); log_status(f"{actor} removed '{removed}' from playlist {pid}.")

def playlist_show(requester,pid=None):
    s=load()
    if pid:
        pl=s["playlists"].get(pid)
        if not pl: return log_chat(requester,"Playlist not found.")
        log_chat(requester,f"{pid} – {pl['name']}")
        for i, m in enumerate(pl["movies"]):
            log_chat(requester,f"    {i+1}. {m}")
    else:
        if not s["playlists"]:
            return log_chat(requester,"No playlists yet.")
        for pid,pl in s["playlists"].items():
            mark = " (current)" if pid==s.get("current_playlist") else ""
            log_chat(requester,f"{pid} – {pl['name']} ({len(pl['movies'])} movies){mark}")

def playlist_switch(actor, pid):
    s=load(); aid=uid(actor,s)
    if not mod(aid,s): return log_status("Denied.")
    if pid not in s["playlists"]: return log_status("Playlist not found.")
    s["current_playlist"] = pid
    save(s); log_status(f"{actor} switched to playlist {pid} ({s['playlists'][pid]['name']}).")

# ── CURRENT PLAYLIST QUEUE ─────────────────────────────
def current_playlist_add(actor,title):
    s=load(); aid=uid(actor,s)
    if not mod(aid,s): return log_status("Denied.")
    cp = s.get("current_playlist")
    if not cp or cp not in s["playlists"]:
        return log_status("No current playlist.")
    s["playlists"][cp]["movies"].append(title)
    save(s); log_status(f"{actor} added '{title}' to current playlist.")

def current_playlist_remove(actor,index):
    s=load(); aid=uid(actor,s)
    if not mod(aid,s): return log_status("Denied.")
    cp = s.get("current_playlist")
    if not cp or cp not in s["playlists"]:
        return log_status("No current playlist.")
    pl = s["playlists"][cp]["movies"]
    if not (0 <= index < len(pl)): return log_status("Invalid movie index.")
    removed = pl.pop(index)
    save(s); log_status(f"{actor} removed '{removed}' from current playlist.")

def current_playlist_show(requester):
    s=load()
    cp = s.get("current_playlist")
    if not cp or cp not in s["playlists"]:
        return log_chat(requester,"No current playlist.")
    pl = s["playlists"][cp]
    if not pl["movies"]:
        return log_chat(requester,"Current playlist is empty.")
    for idx, m in enumerate(pl["movies"], 1):
        log_chat(requester, f"{idx}. {m}")

def current_playlist_next(actor):
    s=load(); aid=uid(actor,s)
    if not mod(aid,s): return log_status("Denied.")
    cp = s.get("current_playlist")
    if not cp or cp not in s["playlists"]: return log_status("No current playlist.")
    pl = s["playlists"][cp]["movies"]
    if pl:
        removed = pl.pop(0)
        save(s)
        log_status(f"{actor} advanced to next item in current playlist (removed '{removed}').")

# ── USER & ROLE MANAGEMENT ─────────────────────────────
def add_user(admin,new_name):
    s=load(); aid=uid(admin,s)
    if not adm(aid,s): return log_status("Permission denied.")
    if uid(new_name,s): return log_status(f"User '{new_name}' already exists.")
    s["users"][hid()]={"username":new_name,"roles":{"is_admin":False,"is_co_admin":False},
                       "personal":{"video_on":True,"audio_on":True,
                                   "reactions_on":True,"screen_lock":False,
                                   "raised_hand":False}}
    save(s); log_status(f"{new_name} joined the room.")

def promote(admin,target,make=True):
    s=load(); aid=uid(admin,s); tid=uid(target,s)
    if not adm(aid,s) or not tid: return log_status("Promotion failed.")
    s["users"][tid]["roles"]["is_co_admin"]=make; save(s)
    log_status(f"{target} {'promoted' if make else 'demoted'} to co-admin.")

def kick(actor,target):
    s=load(); aid=uid(actor,s); tid=uid(target,s)
    if not aid or not tid: return log_status("Kick failed.")
    if not _kick_allowed(aid,tid,s): return log_status("Kick denied – insufficient rights.")
    del s["users"][tid]; save(s); log_status(f"{target} left the room.")

# ── COMMUNICATION & PERSONAL CONTROLS ─────────────────
def chat(name,text):
    s=load()
    if not s["global_settings"]["chat_enabled"]: return log_status("Chat is OFF.")
    log_chat(name,text)

def react(name,val): log_react(name,EMOJI.get(val,val))

def toggle_self(name,setting,onoff):
    s=load(); tid=uid(name,s)
    key="screen_lock" if setting=="screen_lock" else f"{setting}_on"
    if key not in s["users"][tid]["personal"]: return log_status("Unknown setting.")
    s["users"][tid]["personal"][key]=(onoff=="on"); save(s)
    log_status(f"{name} turned {setting} {onoff.upper()}.")

def hand(name):
    s=load(); tid=uid(name,s)
    s["users"][tid]["personal"]["raised_hand"]=True; save(s)
    log_status(f"{name} raised a hand.")

# ── POLLING (open / vote / close) ─────────────────────
def poll_create(admin,q,opts):
    s=load(); aid=uid(admin,s)
    if not adm(aid,s): return log_status("Only admin may poll.")
    pid=hid()
    s["polls"][pid]={"q":q,"opts":opts,"votes":{o:0 for o in opts}}
    save(s); log_status(f"Poll {pid}: {q} ({', '.join(opts)})")

def vote(name,pid,opt):
    s=load(); p=s["polls"].get(pid)
    if not p or opt not in p["opts"]: return log_status("Bad vote.")
    p["votes"][opt]+=1; save(s)
    log_status(f"{name} voted for {opt} (poll {pid}).")

def poll_end(actor,pid):
    s=load(); aid=uid(actor,s)
    if not mod(aid,s): return log_status("Permission denied.")
    poll=s["polls"].pop(pid,None)
    if not poll: return log_status("Poll id not found.")
    winner=max(poll["votes"],key=poll["votes"].get)
    tally=", ".join(f"{k}={v}" for k,v in poll["votes"].items())
    save(s); log_status(f"Poll {pid} closed – {tally} (winner = {winner})")

# ── GLOBAL TOGGLES & SHARE ────────────────────────────
def glob_toggle(actor,setting,onoff):
    s=load(); aid=uid(actor,s)
    if not mod(aid,s): return log_status("Denied.")
    key=f"{setting}_enabled"
    if key not in s["global_settings"]: return log_status("Unknown setting.")
    s["global_settings"][key]=(onoff=="on"); save(s)
    log_status(f"{actor} turned {setting} {onoff.upper()} for everyone.")

def force_personal(actor,target,setting,onoff):
    s=load(); aid=uid(actor,s); tid=uid(target,s)
    if not adm(aid,s): return log_status("Only admin may force settings.")
    if setting=="screen_lock": return log_status("screen_lock is personal only.")
    s["users"][tid]["personal"][f"{setting}_on"]=(onoff=="on"); save(s)
    log_status(f"{actor} set {target}'s {setting} {onoff.upper()}.")

def share(actor,allow):
    s=load(); aid=uid(actor,s)
    if not adm(aid,s): return log_status("Denied.")
    s["screen_sharing_allowed"]=allow; save(s)
    log_status(f"Screen-sharing {'ENABLED' if allow else 'DISABLED'} by admin.")
