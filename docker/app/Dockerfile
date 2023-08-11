# app/Dockerfile

FROM python:3.9-slim

RUN mkdir /app

WORKDIR /app

ADD .gitconfig $HOME/.gitconfig
ADD .git-credentials $HOME/.git-credentials

RUN apt-get update && apt-get install -y \
    build-essential \
    curl vim \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

#HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

#ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]

# keeps container running
ADD start.sh /start.sh
CMD ["/start.sh"]
