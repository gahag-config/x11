#!/usr/bin/env bash

echo -e "\e[1;34m[\e[0m$USER \e[0;93m~\e[1;34m]>\e[0m pacman -Syu"
bash --init-file <(echo ". \"$HOME/.bashrc\"; sudo pacman -Syu")
