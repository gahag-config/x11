#!/bin/bash

wallpaper=~/.config/wallpaper.png

[[ -f ~/.config ]]    && mv -i ~/.config    ~/.config.bak
[[ -e "$wallpaper" ]] && mv -i "$wallpaper" "$wallpaper.bak"

convert -format png "$@" "$wallpaper"
