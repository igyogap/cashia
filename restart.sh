#!/bin/bash
NOW=$(date +"%Y-%m-%d %H:%M:%S")
echo "${NOW} : Stop Bot\n\n"
cd /home/cashia

sh stop_bot.sh

sleep 20s

NOW=$(date +"%Y-%m-%d %H:%M:%S")
echo "${NOW} : Start Bot"
sh run_bot.sh