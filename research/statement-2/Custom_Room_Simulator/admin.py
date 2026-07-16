import sys, user
ME="AdminGPU"
c = sys.argv[1:] or ["?"]

handlers = {
 # user / role
 "add":   lambda: user.add_user(ME,c[1]),
 "prom":  lambda: user.promote(ME,c[1],True),
 "dem":   lambda: user.promote(ME,c[1],False),
 "kick":  lambda: user.kick(ME,c[1]),
 # chat
 "chat":  lambda: user.chat(ME," ".join(c[1:])),
 # playlists
 "plist": lambda: user.playlist_create(ME," ".join(c[1:])),
 "padd":  lambda: user.playlist_add(ME,c[1]," ".join(c[2:])),
 "prem":  lambda: user.playlist_remove(ME,c[1],int(c[2])-1),
 "pshow": lambda: user.playlist_show(ME,c[1] if len(c)==2 else None),
 "pswitch": lambda: user.playlist_switch(ME,c[1]),
 # current playlist
 "cpadd": lambda: user.current_playlist_add(ME," ".join(c[1:])),
 "cprem": lambda: user.current_playlist_remove(ME,int(c[1])-1),
 "cpshow": lambda: user.current_playlist_show(ME),
 "cpnext": lambda: user.current_playlist_next(ME),
 # polling
 "poll":  lambda: user.poll_create(ME,c[1],c[2:]),
 "pend":  lambda: user.poll_end(ME,c[1]),
 # toggles / force / share
 "glob":  lambda: user.glob_toggle(ME,c[1],c[2]),
 "force": lambda: user.force_personal(ME,c[1],c[2],c[3]),
 "share": lambda: user.share(ME,c[1]=="on")
}

handlers.get(c[0], lambda: print("Bad admin command"))()
