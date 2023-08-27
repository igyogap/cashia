#!/bin/bash
tmux new-session -d -s bot_cashia
tmux send-keys -t bot_cashia '/usr/bin/python3 /home/cashia/main.py' Enter