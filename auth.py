#!/usr/local/bin/python

import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
from sqlalchemy import create_engine, text

dbcredentials = st.secrets["postgres"]


dbEngine = create_engine('postgresql+psycopg2://' +
    dbcredentials['user'] + ':' +
    dbcredentials['password'] + '@' +
    dbcredentials['host'] + ':' +
    str(dbcredentials['port']) + '/' +
    dbcredentials['dbname'])

user_df = pd.read_sql(sql = text("select * from user_profile"), con=dbEngine.connect())

if __name__ == "__main__":
    print(user_df)
