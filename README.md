# Youtube Recommender App

YouTube and Netflix give users the option to “dislike” a video. But, a dislike on a video does not tell the algorithm what specifically the user is upset about. Our project overcomes this with a **natural language filter bar** that uses **artificial intelligence** (BERT or ChatGPT) behind the scenes to make Youtube video recommendations more personalized and less manipulative. This is a research project for the Masters of Applied Data Science at the University of Michigan.

# Key Links
- [Streamlit App](https://youtube-capstone.streamlit.app/)
- [Medium Article](https://medium.com/@gabrielalon257/youtube-filtering-capstone-67f755fb6dca)
- [Research Poster](https://drive.google.com/file/d/1fbkjsChxA_kINFSDvluDN6QNpTsqON04/view?usp=sharing)
- [Video](https://www.youtube.com/watch?v=T_uKgvzt8M0)

# Getting Started

Clone the repository to a local directory:
```
git clone https://github.com/quochuyn/youtube_nlp_recommender
```

Install dependencies:
```
pip install -r requirements.txt
```

Edit `main_app.py` to customize this app to your heart's desire. :heart:

## Credentials

The key feature of this app uses Youtube's API for searching videos which can be created in Google Cloud by following the instructions on the [API overview page](https://developers.google.com/youtube/v3/getting-started).

Additionally, access to a database for user profiles is also required. There are many options and tutorials for creating a local or cloud-based database. Here, we have used the cloud-based Amazon Web Services (AWS)'s Relational Database Service (RDS) to create a free-tier Postgres database. We followed this [video tutorial](https://www.youtube.com/watch?v=I_fTQTsz2nQ). Most configuration defaults are accepted, except that you need to disable storage autoscaling so that you don't exceed the free-tier storage limitations and incur charges on your credit card.

## Plugging in Credentials

If you're using docker to perform a local run, then you will need to create a `secrets.toml` file in the `./.streamlit` directory with the below code. 

For a cloud-based run with Streamlit Cloud, you'll need to paste your Amazon RDS database and Youtube API secrets within the app root at the time of deployment which is explained [here](https://docs.streamlit.io/library/advanced-features/secrets-management).

```
[postgres]
host = "your_host"
port = 5432
dbname = "your_database_name"
user = "your_database_user"
password = "your_database_password"

[api]
key1 = "your_youtube_api_key"
```

## Docker

Installation Instructions - Local Run (Not necessary for making a Streamlit website for free)

  0. If you don't have Docker: You can get Docker Desktop here https://docs.docker.com/compose/install/index.html
  1. cd docker
  2. docker-compose build
  3. docker-compose up -d
  4. docker exec -ti app /bin/bash
  5. cd /app/youtube_recommender_app
  6. ./run_app.sh

## Streamlit

This streamlit site was setup under the Streamlit Cloud. Read [here](https://blog.streamlit.io/host-your-streamlit-app-for-free/) for more context. Deploying this app on streamlit cloud gives a url that is unique to the GitHub Repo. Streamlit will read from the current version of the associated GitHub Repo upon refresh.

Streamlit Hosting Instructions - Cloud Run

  1. Fork the Github repository
  2. Follow [app deployment instructions](https://docs.streamlit.io/streamlit-community-cloud/get-started/deploy-an-app)

# Data Access Statement

The data is accessed live through Youtube's API and belongs to Youtube and its affiliates according to its [Terms of Services](https://developers.google.com/youtube/terms/api-services-terms-of-service).

# Privacy Statement
The default version of the app does not store user searches or preferences. The user can choose to go to the Account Setting tab to enable the saving of those preferences.
