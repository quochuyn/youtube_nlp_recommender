#!/bin/bash
if [[ $1 == "-bash" ]]; then
  /bin/bash
fi


# using git pull in start.sh to get latest code
cd /app/youtube_recommender_app/ && git pull && cp /credentials/secrets.toml .streamlit/ && cp /credentials/git_push.sh .

if [[ $? == "0" ]]; then
  while true; do cat /dev/null; done
fi
