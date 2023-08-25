# provide_feedback.py

import numpy as np
import pandas as pd

import streamlit as st
from sqlalchemy import create_engine
from trubrics.integrations.streamlit import FeedbackCollector



def write_feedback(conn):
    r"""
    Provide an anonymous feedback form for users of the web app. This uses the trubrics
    tool: https://blog.streamlit.io/trubrics-a-user-feedback-tool-for-your-ai-streamlit-apps/
    """

    dbcredentials = st.secrets['postgres']

    dbEngine = create_engine('postgresql+psycopg2://' +
        dbcredentials['user'] + ':' +
        dbcredentials['password'] + '@' +
        dbcredentials['host'] + ':' +
        str(dbcredentials['port']) + '/' +
        dbcredentials['dbname'])

    trubrics_credentials = st.secrets['trubrics']

    collector = FeedbackCollector(
        component_name='feedback_component',
        email=trubrics_credentials['email'], # Store your Trubrics credentials in st.secrets:
        password=trubrics_credentials['password'], # https://blog.streamlit.io/secrets-in-sharing-apps/
    )

    text_feedback = collector.st_feedback(
        feedback_type='textbox',
        model='my_model', # TODO: what to put here?
        open_feedback_label="What do you think of the web app?",
    )

    thumbs_feedback = collector.st_feedback(
        feedback_type='thumbs',
        model='my_model', # TODO: what to put here?
        open_feedback_label=""
    )

    submitted = st.form_submit_button("Submit")
    if submitted:
        # TODO: write response to database
        st.write(f"You wrote: {text_feedback}")
        st.write(f"You gave a thumbs: {thumbs_feedback}, {type(thumbs_feedback)}")
