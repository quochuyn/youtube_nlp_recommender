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


def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])

conn = init_connection()

st.set_page_config(layout="wide")

st.header("Custom tab component for on-hover navigation bar")
st.markdown('<style>' + open('./components/style.css').read() + '</style>', unsafe_allow_html=True)

tabs = sidebar()

if tabs == 'Dashboard':
    input_term = st.text_input("Enter keywords")
    print("input_term", input_term)
    session.slider_count = st.slider(label="video_count", min_value=5, max_value=50)
    st.text("")

    if input_term:
        stored_imgs = select_images(conn, input_term) # your images here
        converted_imgs = []
        for img in stored_imgs:
            #pyscopg2 returns tuple, extract first key, which is memoryview for the image
            mview = img[0]
            print(type(mview))
            converted_imgs.append(BytesIO(base64.b64decode(mview)))

        print("total imgs", len(converted_imgs))
        caption = [] # your caption here
        cols = cycle(st.columns(4)) # st.columns here since it is out of beta at the time I'm writing this
        for idx, converted_img in enumerate(converted_imgs):
            next(cols).image(converted_img, width=150, caption='test')
elif tabs == 'Upload':
    topics = ["streamlit", "education"]
    load_images(conn, topics)