#!/bin/bash
if [[ $1 == "-bash" ]]; then
  /bin/bash
fi


# using git pull in start.sh to get latest code
cd /app && /credentials/git_clone.sh
cd ./youtube_recommender_app && git pull && pip3 install -r requirements.txt 
cd /app/youtube_recommender_app/ && git pull && cp /credentials/secrets.toml .streamlit/ && cp /credentials/git_push.sh .

if [[ $? == "0" ]]; then
  while true; do cat /dev/null; done
fi
