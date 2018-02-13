#!/bin/bash

function ensure-dir {
  [[ -f "$@" ]] && mv -i "$@" "$@.bak"
  mkdir -p "$@"
}

function ln-cfg {
  [[ -e "$2" ]] && mv -i "$2" "$2.bak"
  ln -s "$(pwd)/$1" "$2"
}


cd $(dirname $(readlink -f $0)) # jump to the script directory


# xinitrc
ln-cfg xinitrc ~/.xinitrc

# xmodmap
ln-cfg xmodmap ~/.Xmodmap

# xcompose
ln-cfg xcompose ~/.XCompose

# breeze cursor for i3
ensure-dir          ~/.icons
ensure-dir          ~/.icons/default
ln-cfg breeze.theme ~/.icons/default/index.theme

# i3/rofi/polybar
ensure-dir     ~/.config
ln-cfg i3      ~/.config/i3
ln-cfg rofi    ~/.config/rofi
ln-cfg polybar ~/.config/polybar
