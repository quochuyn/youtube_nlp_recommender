#!/usr/local/bin/python
import streamlit as st
import psycopg2
from components.sidebar import sidebar
from streamlit import session_state as session
from itertools import cycle
from streamlit_player import st_player
from auth_app import auth_from_db, auth_from_yaml
from user_profile import modify_profile
from provide_feedback import write_feedback
from sqlalchemy import create_engine, text
import pandas as pd
import youtube.get_youtube_data as get_youtube_data
from sentence_transformers import SentenceTransformer
import machine_learning.embedding as embedding
from components.footer import  my_footer

YOUTUBE_API_KEY = st.secrets["api"]["key1"]
MAX_VIDS = 50

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

@st.cache_resource
def init_BERT_model():
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    return model

def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])

def app_layout():
    st.set_page_config(layout="wide")
    app_header = "<h1 style='text-align: center; color: black;'>Youtube Recommendation App</h1>"
    st.markdown(app_header, unsafe_allow_html=True)

    st.markdown('<style>' + open('./components/style.css').read() + '</style>', unsafe_allow_html=True)
    my_footer()

@st.cache_data
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
    filter_model = init_BERT_model()

    if tabs == 'Videos':
        profile_df = pd.read_sql(sql = text("select search_words, filtered_words " + \
                                    " from user_profile where username = '" + username + "'"), 
                                    con=dbEngine.connect())

        profile_searchwords = profile_df['search_words'].values[0]
        profile_filtered_words = profile_df['filtered_words'].values[0]

        print("profile searchwords ", profile_searchwords, type(profile_searchwords))
        print("profile filtered_words ", profile_filtered_words, type(profile_filtered_words))

        input_query = st.text_input("$Enter\;Query$", value = ','.join(profile_searchwords))
        input_filter = st.text_input("$Enter\;Filters$", value = ','.join(profile_filtered_words))

        print("input_query ", input_query, type(input_query))
        print("input_filter ", input_filter, type(input_filter))

        session.slider_count = st.slider(label="video_count", min_value=1, max_value=50)
        st.text("")

        if len(input_query) > 0:
            cols = cycle(st.columns(3))

            # no need to call api if results are alearedy fetched for the search words
            if st.session_state.search_words != input_query:
                st.session_state.search_words = input_query
                st.session_state.youtube_df = get_youtube_videos(input_query)

            if len(input_filter) > 0:
                titles = st.session_state.youtube_df['title'].values
                #print("Titles ", titles, type(titles))
                filtered_titles = embedding.filter_out_embed(filter_model, input_filter, titles)
                filtered_df = st.session_state.youtube_df[st.session_state.youtube_df['title'].isin(filtered_titles)]
                for idx, row in filtered_df.head(session.slider_count).iterrows():
                    with next(cols):
                        # Embed a youtube video
                        st_player(url="https://youtu.be/" + row['video_id'], controls=True)
                        #video_title = "<b style='max-width: 500px; display: inline-block; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; \
                        #                font-family: serif; text-align: center; color: black;'>" + row['title'] + "</b>"
                        #st.markdown(video_title, unsafe_allow_html=True)
            else:
                for idx, row in st.session_state.youtube_df.head(session.slider_count).iterrows():
                    with next(cols):
                        # Embed a youtube video
                        st_player(url="https://youtu.be/" + row['video_id'], controls=True)
                        #st.caption(row['title'])
                        #video_title = "<b style='max-width: 500px; display: inline-block; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; \
                        #                font-family: serif; text-align: center; color: black;'>" + row['title'] + "</b>"
                        #st.markdown(video_title, unsafe_allow_html=True)
    elif tabs == 'Account Setting':
        modify_profile(conn, username)
        
app_layout()

# authenticator = auth_from_db()
# name, authentication_status, username = authenticator.login('Login \n Username Hint: guest \n Password Hint: test', 'main')

# cheat for removing authentication/login friction
name = 'guest'
authentication_status = True
username = 'guest'

if authentication_status:
    # authenticator.logout('Logout', 'main', key='unique_key')
    st.write(f'$Welcome\;*{name}*$')
    youtube_app(username)
elif authentication_status is False:
    st.error('Username/password is incorrect')
elif authentication_status is None:
    st.warning('Please enter your username and password')