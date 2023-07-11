git config --global user.email "krishch@umich.edu"
if [ $# -eq 0 ]
  then
    echo "No arguments supplied for commit message"
    exit 1
fi
git add *;git status;git add *;git commit -am "$1";git push  https://krishch72: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@github.com/krishch72/youtube_recommender_app.git;git status
