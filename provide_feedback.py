# provide_feedback.py

import numpy as np
import pandas as pd

import streamlit as st
from sqlalchemy import create_engine
from trubrics.integrations.streamlit import FeedbackCollector



def write_feedback(conn):
    r"""
    Provide an anonymous feedback form for users of the web app. Loosely following this guide:
    https://blog.streamlit.io/collecting-user-feedback-on-ml-in-streamlit/

    TODO: follow the updated guide https://blog.streamlit.io/trubrics-a-user-feedback-tool-for-your-ai-streamlit-apps/
    """

    dbcredentials = st.secrets["postgres"]

    dbEngine = create_engine('postgresql+psycopg2://' +
        dbcredentials['user'] + ':' +
        dbcredentials['password'] + '@' +
        dbcredentials['host'] + ':' +
        str(dbcredentials['port']) + '/' +
        dbcredentials['dbname'])

    with st.form("feedback_form"):

        collector = FeedbackCollector()

        feedback_sentiment = collector.st_feedback(
            feedback_type='thumbs'
        )
        feedback_text = collector.st_feedback(
            feedback_type='issue'
        )

        submitted = st.form_submit_button("Submit")
        if submitted:
            # TODO: write response to database
            st.write(f"You felt: {feedback_sentiment}")
            st.write(f"You wrote: {feedback_text}")
