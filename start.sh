#!/bin/bash

echo "

THANK YOU FOR DEPLOYING }

TOR TOOLKIT X

Version - 0.2.6-Heroku-Master-Finalised.

CREATED BY - Yash Khadse

KANGED AND MODDED BY KANGERSHUB.....

"

echo "Starting TTK-X engine in 10 seconds"

 hour=0
 min=0
 sec=10
        while [ $hour -ge 0 ]; do
                 while [ $min -ge 0 ]; do
                         while [ $sec -ge 0 ]; do
                                 echo -ne "$hour:$min:$sec\033[0K\r"
                                 let "sec=sec-1"
                                 sleep 1
                         done
                         sec=10
                         let "min=min-1"
                 done
                 min=0
                 let "hour=hour-1"
         done

echo "ttk-x engine starting now --------"


aria2c --conf-path="aria2.conf" -D
./alive.sh & gunicorn tortoolkit:start_server --bind 0.0.0.0:$PORT --worker-class aiohttp.GunicornWebWorker & qbittorrent-nox -d & python3 -m tortoolkit