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


def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])

conn = init_connection()

st.set_page_config(layout="wide")

# Embed a youtube video
st_player("https://youtu.be/CmSKVW1v0xM")

if "n_clicks" not in st.session_state:
    st.session_state["n_clicks"] = "0"

with st.sidebar:
    choice = st.radio("Radio", [1, 2, 3])

id = str(int(st.session_state["n_clicks"]) + 1)

content = f"<a href='#' id='{id}'><img src='https://icons.iconarchive.com/icons/custom-icon-design/pretty-office-7/256/Save-icon.png'></a>"

clicked = click_detector(content, key="click_detector")

if clicked != "" and clicked != st.session_state["n_clicks"]:
    st.session_state["n_clicks"] = clicked
    st.subheader("Saving Report..")
else:
    st.subheader(f"Choice: #{choice}")

#st.header("Youtube Recommendation App")
app_header = "<h1 style='text-align: center; color: black;'>Youtube Recommendation App</h1>"
st.markdown(app_header, unsafe_allow_html=True)

st.markdown('<style>' + open('./components/style.css').read() + '</style>', unsafe_allow_html=True)

tabs = sidebar()

if tabs == 'Dashboard':
    all_words = st.text_input("Enter Search Words(seperated by comma if multiple)")
    search_words = all_words.split(',')
    print(search_words)
    search_words = [x.strip() for x in search_words if x]
    print("search_words", search_words)

    session.slider_count = st.slider(label="video_count", min_value=1, max_value=50)
    st.text("")

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
        cols = cycle(st.columns(4)) # st.columns here since it is out of beta at the time I'm writing this
        for idx, converted_img in enumerate(converted_imgs):
            next(cols).image(converted_img, width=150, caption=video_ids[idx])
elif tabs == 'Upload':
    topics = ["streamlit", "education"]
    load_images(conn, topics)