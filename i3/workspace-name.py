#!/usr/bin/env python3

# This script listens for i3 events and updates workspace names to show icons
# for running programs.  It contains icons for a few programs, but more can
# easily be added by adding them to `icons` below.
#
# It also re-numbers workspaces in ascending order with one skipped number
# between monitors (leaving a gap for a new workspace to be created). By
# default, i3 workspace numbers are sticky, so they quickly get out of order.
#
# Dependencies
# * xorg-xprop  - install through system package manager
# * i3ipc       - install with pip
# * fontawesome - install with pip
#
# Installation:
# * Download this script and place it in ~/.config/i3/ (or anywhere you want)
# * Add "exec_always ~/.config/i3/i3-autoname-workspaces.py &" to your i3 config
# * Restart i3: $ i3-msg restart
#
# Configuration:
# The default i3 config's keybindings reference workspaces by name, which is an
# issue when using this script because the "names" are constantaly changing to
# include window icons.  Instead, you'll need to change the keybindings to
# reference workspaces by number.  Change lines like:
#   bindsym $mod+1 workspace 1
# To:
#   bindsym $mod+1 workspace number 1

import i3ipc
import logging
import signal
import sys
import fontawesome as fa

from util import *

# Add icons here for common programs you use.  The keys are the X window class
# (WM_CLASS) names (lower-cased) and the icons can be any text you want to
# display.
#
# Most of these are character codes for font awesome:
#   https://fontawesome.com/cheatsheet
#
# If you're not sure what the WM_CLASS is for your application, you can use
# xprop (https://linux.die.net/man/1/xprop). Run `xprop | grep WM_CLASS`
# then click on the application you want to inspect.
icons = {
  'empty'          : fa.icons['ban'],
  'default'        : fa.icons['asterisk'], # Used for any application not in the list.
  'discord'        : fa.icons['comment'],
  'dolphin'        : fa.icons['folder'],
  'emacs'          : fa.icons['code'],
  'firefox'        : fa.icons['firefox'],
  'gwenview'       : '', # fa.icons['image']
  'kate'           : fa.icons['code'],
  'kwrite'         : fa.icons['file-text-o'],
  'okular'         : fa.icons['file-pdf-o'],
  'smplayer'       : fa.icons['music'],
  'steam'          : fa.icons['steam'],
  'thunderbird'    : fa.icons['envelope'],
  'vivaldi-stable' : fa.icons['vimeo'],
  'konsole'        : fa.icons['terminal'],
  # 'cura': fa.icons['cube'],
  # 'dolphin': fa.icons['files-o'],
  # 'feh': fa.icons['picture-o'],
  # 'gpick': fa.icons['eyedropper'],
  # 'kicad': fa.icons['microchip'],
  # 'libreoffice': fa.icons['file-text-o'],
  # 'zenity': fa.icons['window-maximize'],
}


def window_icon(window):
  # Try all window classes and use the first one we have an icon for
  classes = xprop(window.window, 'WM_CLASS')
  
  if classes != None and len(classes) > 0:
    for cls in classes:
      cls = cls.lower()  # case-insensitive matching
      
      if cls in icons:
        return icons[cls]
      
  logging.info('No icon available for window with classes: %s' % str(classes))
  
  return icons['default']


def rename_workspaces(i3):
  # renames all workspaces based on the windows present
  ws_infos = i3.get_workspaces()
  
  for ws_index, workspace in enumerate(i3.get_tree().workspaces()):
    ws_info = ws_infos[ws_index]
    
    name = parse_workspace_name(workspace.name)
    name['icons'] = ' '.join([window_icon(w) for w in workspace.leaves()])
    if not name['icons']:
      name['icons'] = icons['empty']
    
    new_name = construct_workspace_name(name)
    if workspace.name == new_name:
      continue
    i3.command('rename workspace "%s" to "%s"' % (workspace.name, new_name))


# Rename workspaces to just numbers and shortnames, removing the icons.
def on_exit(i3):
  for workspace in i3.get_tree().workspaces():
    name = parse_workspace_name(workspace.name)
    name['icons'] = None
    new_name = construct_workspace_name(name)
    if workspace.name == new_name:
      continue
    i3.command('rename workspace "%s" to "%s"' % (workspace.name, new_name))
  
  i3.main_quit()
  sys.exit(0)


if __name__ == '__main__':
  logging.basicConfig(level=logging.INFO)
  
  i3 = i3ipc.Connection()
  
  # Exit gracefully when ctrl+c is pressed
  for sig in [signal.SIGINT, signal.SIGTERM]:
    signal.signal(sig, lambda signal, frame: on_exit(i3))
    
  rename_workspaces(i3)
  
  # Call rename_workspaces() for relevant window events
  def window_event_handler(i3, e):
    if e.change in ['new', 'close', 'move']:
      rename_workspaces(i3)
  
  def workspace_event_handler(i3, e):
    if e.change == 'init':
      rename_workspaces(i3)
  
  i3.on('window', window_event_handler)
  i3.on('workspace', workspace_event_handler)
  i3.main()
