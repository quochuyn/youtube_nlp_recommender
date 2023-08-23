# provide_feedback.py

import numpy as np
import pandas as pd

import streamlit as st
from sqlalchemy import create_engine



def write_feedback(conn):
    r"""
    Provide an anonymous feedback form for users of the web app.

    TODO: https://blog.streamlit.io/trubrics-a-user-feedback-tool-for-your-ai-streamlit-apps/
    """

    dbcredentials = st.secrets["postgres"]

    dbEngine = create_engine('postgresql+psycopg2://' +
        dbcredentials['user'] + ':' +
        dbcredentials['password'] + '@' +
        dbcredentials['host'] + ':' +
        str(dbcredentials['port']) + '/' +
        dbcredentials['dbname'])

    with st.form("feedback_form"):

        default_text = ""
        feedback_text = st.text_area("What do you think of the web app?", value=default_text)

        submitted = st.form_submit_button("Submit")
        if submitted:
            # TODO: write response to database
            st.write(f"You wrote: {feedback_text}")
