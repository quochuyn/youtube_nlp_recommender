#!/usr/local/bin/python

import streamlit as st
import psycopg2
# from dataservice.query import run_query
from components.sidebar import sidebar
from dataservice.thumbnail_images import load_images, fetch_images, select_images
from streamlit import session_state as session
from io import BytesIO
from itertools import cycle
import base64
from streamlit_player import st_player
from st_click_detector import click_detector
from auth_app import auth_from_db, auth_from_yaml
from user_profile import modify_profile
from sqlalchemy import create_engine, text
import pandas as pd
import ast
import youtube.get_youtube_data as get_youtube_data

YOUTUBE_API_KEY = get_youtube_data.get_youtube_api_key()
MAX_VIDS = 15

if 'search_words' not in st.session_state:
    st.session_state.search_words = None
    st.session_state.youtube_df = pd.DataFrame()

dbcredentials = st.secrets["postgres"]

dbEngine = create_engine('postgresql+psycopg2://' +
    dbcredentials['user'] + ':' +
    dbcredentials['password'] + '@' +
    dbcredentials['host'] + ':' +
    str(dbcredentials['port']) + '/' +
    dbcredentials['dbname'])

def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])

def app_layout():
    st.set_page_config(layout="wide")

    app_header = "<h1 style='text-align: center; color: black;'>Youtube Recommendation App</h1>"
    st.markdown(app_header, unsafe_allow_html=True)

    st.markdown('<style>' + open('./components/style.css').read() + '</style>', unsafe_allow_html=True)

def get_youtube_videos(input_query):
    print("Calling youtube_api..")
    youtube_client = get_youtube_data.make_client(YOUTUBE_API_KEY)
    youtube_df = get_youtube_data.search_youtube(
        youtube_client,
        query= input_query,
        max_vids=MAX_VIDS,        # youtube accepts 50 as the max value
        order='relevance'   # default is relevance
    )
    return youtube_df

def youtube_app(username):
    conn = init_connection()
    tabs = sidebar()

    if tabs == 'Dashboard':
        profile_searchwords = pd.read_sql(sql = text("select search_words " + \
                                    " from user_profile where username = '" + username + "'"), 
                                    con=dbEngine.connect())['search_words'].values[0]
        print("profile searchwords ", profile_searchwords, type(profile_searchwords))

        input_query = st.text_input("Enter Query", value = ','.join(profile_searchwords))

        # search_words = all_words.split(',')
        # print(search_words)
        # search_words = [x.strip() for x in search_words if x]
        # print("search_words", search_words)

        session.slider_count = st.slider(label="video_count", min_value=1, max_value=50)
        st.text("")

        if len(input_query) > 0:
            cols = cycle(st.columns(4))

            # no need to call api if results are alearedy fetched for the search words
            if st.session_state.search_words != input_query:
                st.session_state.search_words = input_query
                st.session_state.youtube_df = get_youtube_videos(input_query)

            for idx, row in st.session_state.youtube_df.head(session.slider_count).iterrows():
                with next(cols):
                    # Embed a youtube video
                    st_player(url="https://youtu.be/" + row['video_id'], controls=True)

    elif tabs == 'Upload':
        topics = ["streamlit", "education"]
        load_images(conn, topics)
    elif tabs == 'Account Setting':
        modify_profile(conn, username)
app_layout()

authenticator = auth_from_db()
name, authentication_status, username = authenticator.login('Login', 'main')

#print("name ", name, "auth ", authentication_status, "username ", username)

if authentication_status:
    authenticator.logout('Logout', 'main', key='unique_key')
    st.write(f'Welcome *{name}*')
    youtube_app(username)
elif authentication_status is False:
    st.error('Username/password is incorrect')
elif authentication_status is None:
    st.warning('Please enter your username and password')