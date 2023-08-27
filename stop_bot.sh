#!/bin/sh
tmux send-keys -t bot_cashia 'C-c' Enter
tmux kill-session -t bot_cashia

pkill -9 -f main.py