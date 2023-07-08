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
from youtube.get_youtube_data import get_youtube_api_key, make_client, search_youtube

def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])


def app_layout():
    st.set_page_config(layout="wide")

    app_header = "<h1 style='text-align: center; color: black;'>Youtube Recommendation App</h1>"
    st.markdown(app_header, unsafe_allow_html=True)

    st.markdown('<style>' + open('./components/style.css').read() + '</style>', unsafe_allow_html=True)

def utube_app(username):
    conn = init_connection()
    tabs = sidebar()

    if tabs == 'Dashboard':
        dbcredentials = st.secrets["postgres"]

        dbEngine = create_engine('postgresql+psycopg2://' +
            dbcredentials['user'] + ':' +
            dbcredentials['password'] + '@' +
            dbcredentials['host'] + ':' +
            str(dbcredentials['port']) + '/' +
            dbcredentials['dbname'])

        profile_searchwords = pd.read_sql(sql = text("select search_words " + \
                                    " from user_profile where username = '" + username + "'"), 
                                    con=dbEngine.connect())['search_words'].values[0]
        print("profile searchwords ", profile_searchwords, type(profile_searchwords))

        all_words = st.text_input("Enter Search Words(seperated by comma if multiple)", value = ','.join(profile_searchwords))

        search_words = all_words.split(',')
        print(search_words)
        search_words = [x.strip() for x in search_words if x]
        print("search_words", search_words)

        session.slider_count = st.slider(label="video_count", min_value=1, max_value=50)
        st.text("")

        
        YOUTUBE_API_KEY = get_youtube_api_key()
        youtube = make_client(YOUTUBE_API_KEY)
        youtube_df = search_youtube(
            youtube,
            #query= "'" + search_words[0] + "'",
            query='bossa nova',
            max_vids=session.slider_count,        # youtube accepts 50 as the max value
            order='relevance'   # default is relevance
        )

        if len(search_words) > 0:
            stored_imgs = select_images(conn, search_words, session.slider_count) # your images here
            converted_imgs = []
            video_ids = []
            for img in stored_imgs:
                #pyscopg2 returns tuple, extract first key, which is memoryview for the image
                mview = img[0]
                #print(type(mview))
                #print(img[1])
                video_ids.append(img[1])
                converted_imgs.append(BytesIO(base64.b64decode(mview)))

            print("total imgs", len(converted_imgs))
            caption = [] # your caption here
            cols = cycle(st.columns(4))
            for idx, converted_img in enumerate(converted_imgs):
                #next(cols).image(converted_img, width=150, caption=video_ids[idx])
                with next(cols):
                    # Embed a youtube video
                    st_player(url="https://youtu.be/" + video_ids[idx], controls=True)
                
        
        tmp_message = '<p style="font-family:Courier; color:Black; font-size: 20px;">Based on query -> bossa nova to youtube api</p>'
        st.markdown(tmp_message, unsafe_allow_html=True)
        cols = cycle(st.columns(4))
        for idx, row in youtube_df.iterrows():
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
    utube_app(username)
elif authentication_status is False:
    st.error('Username/password is incorrect')
elif authentication_status is None:
    st.warning('Please enter your username and password')