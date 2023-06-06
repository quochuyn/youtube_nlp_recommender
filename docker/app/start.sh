#!/bin/bash
if [[ $1 == "-bash" ]]; then
  /bin/bash
fi


# using git pull in start.sh to get latest code
cd /app/youtube_recommender_app/ && git pull

if [[ $? == "0" ]]; then
  while true; do cat /dev/null; done
fi
