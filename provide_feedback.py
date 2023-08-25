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

    thumb_collector = FeedbackCollector(
        component_name='yt_feedback_comp_thumbs',
        email=trubrics_credentials['email'], # Store your Trubrics credentials in st.secrets:
        password=trubrics_credentials['password'], # https://blog.streamlit.io/secrets-in-sharing-apps/
    )

    thumbs_feedback = thumb_collector.st_feedback(
        feedback_type='thumbs',
        model='my_model', # TODO: what to put here?
        open_feedback_label="What do you think of the web app?",
        align='flex-start',
    )
