#!/bin/sh
#
# ~/.xinitrc
#
# Executed by startx (run your window manager from here)

if [ -d /etc/X11/xinit/xinitrc.d ]; then
  for f in /etc/X11/xinit/xinitrc.d/*; do
    [ -x "$f" ] && . "$f"
  done
  unset f
fi


# XProfile
[[ -f "$XPROFILE" ]] && source "$XPROFILE"

# keyboard settings
[[ -f "$XMODMAP" ]] && xmodmap "$XMODMAP"

# exec i3
# exec gnome-session
exec startplasma-x11
# exec startxfce4
# ...or the Window Manager of your choice
