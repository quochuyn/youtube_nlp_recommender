#!/usr/local/bin/python

import streamlit as st
import psycopg2
# from dataservice.query import run_query
from components.sidebar import sidebar
from dataservice.load_images import load_images


def init_connection():
    secrets='../.streamlit/secrets.toml'
    return psycopg2.connect(**st.secrets["postgres"])

conn = init_connection()

load_images(conn)

# st.set_page_config(layout="wide")

# st.header("Custom tab component for on-hover navigation bar")
# st.markdown('<style>' + open('./components/style.css').read() + '</style>', unsafe_allow_html=True)

# tabs = sidebar()

# if tabs == 'Dashboard':
#     input_terms = st.text_input("Enter keywords")
