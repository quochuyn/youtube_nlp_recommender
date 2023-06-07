#!/usr/local/bin/python

import streamlit as st
import psycopg2
# from dataservice.query import run_query
from components.sidebar import sidebar
from dataservice.load_images import load_images, fetch_images
from io import BytesIO


def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])

conn = init_connection()

# load_images(conn)

# st.set_page_config(layout="wide")

# st.header("Custom tab component for on-hover navigation bar")
# st.markdown('<style>' + open('./components/style.css').read() + '</style>', unsafe_allow_html=True)

# tabs = sidebar()

# if tabs == 'Dashboard':
#     input_terms = st.text_input("Enter keywords")

image_bytes = fetch_images(conn)
# # # Create a binary stream
image_stream = BytesIO(image_bytes)
st.image(image_stream, caption='My Image')