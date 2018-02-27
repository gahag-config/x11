#!/bin/bash

function ln-cfg {
  [[ -e "$2" ]] && mv -i "$2" "$2.bak"
  ln -s "$(pwd)/$1" "$2"
}


cd $(dirname $(readlink -f $0)) # jump to the script directory


# xinitrc
ln-cfg xinitrc ~/.xinitrc

# xcompose
ln-cfg xcompose ~/.XCompose
