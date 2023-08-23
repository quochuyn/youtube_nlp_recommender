# provide_feedback.py

import numpy as np
import pandas as pd

import streamlit as st
from sqlalchemy import create_engine



def write_feedback(conn, username):
    r"""
    Provide a feedback form for users of the web app.
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
        feedback_text = st.text_area("$Give\;Feedback$", value=default_text)

        submitted = st.form_submit_button("Submit")
        if submitted:
            # write response to database
            st.write(f"You wrote: {feedback_text}")
