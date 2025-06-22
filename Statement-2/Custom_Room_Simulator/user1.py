import sys, user
ME="User1"                                # change per copy

a = sys.argv[1:] or ["?"]
cmd = a[0]

if   cmd=="chat":   user.chat(ME," ".join(a[1:]))
elif cmd=="react":  user.react(ME,a[1])
elif cmd=="toggle": user.toggle_self(ME,a[1],a[2])
elif cmd=="hand":   user.hand(ME)
elif cmd=="vote":   user.vote(ME,a[1],a[2])
elif cmd=="cpshow": user.current_playlist_show(ME)
elif cmd=="plist":  user.playlist_show(ME, a[1] if len(a)==2 else None)
else:               print("Bad user command")
