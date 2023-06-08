#!/usr/local/bin/python

import streamlit as st
import psycopg2
# from dataservice.query import run_query
from components.sidebar import sidebar
from dataservice.thumbnail_images import load_images, fetch_images
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
    input_terms = st.text_input("Enter keywords")
    session.slider_count = st.slider(label="movie_count", min_value=5, max_value=50)
    # image_bytes = fetch_images(conn)
    # # # Create a binary stream
    # image_stream = BytesIO(image_bytes)
    # st.image(image_stream, caption='My Image')

    stored_imgs = fetch_images(conn) # your images here
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
    load_images(conn)