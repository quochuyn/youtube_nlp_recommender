import streamlit as st

# from dataservice.query import run_query
from components.sidebar import sidebar

st.set_page_config(layout="wide")

st.header("Custom tab component for on-hover navigation bar")
st.markdown('<style>' + open('./components/style.css').read() + '</style>', unsafe_allow_html=True)

tabs = sidebar()

if tabs == 'Dashboard':
    input_terms = st.text_input("Enter keywords")