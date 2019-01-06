#!/bin/bash

function ln-cfg {
  [[ -e "$2" ]] && mv -i "$2" "$2.bak"

  mkdir -p "$(dirname $2)"

  ln -s "$(pwd)/$1" "$2"
}


cd $(dirname $(readlink -f $0)) # jump to the script directory


# xinitrc
if [ -z "$XINITRC" ]; then
  echo "XINITRC not defined, skipping...";
else
  ln-cfg xinitrc "$XINITRC"
fi

# xmodmap
if [ -z "$XMODMAP" ]; then
  echo "XMODMAP not defined, skipping...";
else
  ln-cfg xmodmap "$XMODMAP"
fi

# xcompose
if [ -z "$XCOMPOSEFILE" ]; then
  echo "XCOMPOSEFILE not defined, skipping...";
else
  ln-cfg xcompose "$XCOMPOSEFILE"
fi
