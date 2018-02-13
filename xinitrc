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


# keyboard settings
setxkbmap -option compose:lwin
[[ -f ~/.Xmodmap ]] && xmodmap ~/.Xmodmap

# load theme for qt apps
[ "$XDG_CURRENT_DESKTOP" = "KDE" ] || [ "$XDG_CURRENT_DESKTOP" = "GNOME" ] || export QT_QPA_PLATFORMTHEME="qt5ct"

# set wallpaper
feh --bg-scale "~/.config/wallpaper"
xsetroot -cursor_name left_ptr&


exec i3
# exec gnome-session
#exec startkde
# exec startxfce4
# ...or the Window Manager of your choice
