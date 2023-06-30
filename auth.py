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

username_df = pd.read_sql(sql = text("select username from user_profile"), con=dbEngine.connect())
userdetails_df = pd.read_sql(sql = text("select * from user_profile"), con=dbEngine.connect())
cookie_df = pd.read_sql(sql = text("select * from session_cookie"), con=dbEngine.connect())
preauth_df = pd.read_sql(sql = text("select email from user_profile where preauth == True"), con=dbEngine.connect())

if __name__ == "__main__":
    #mydict = user_df.to_dict('records')
    # mydict = dict(zip(user_df.email, user_df.name))
    #print(mydict)

    user_dict = {}
    for idx, row in username_df.iterrows():
        print(row['username'])
        print(userdetails_df[userdetails_df['username'] == row['username']][['name', 'email']].to_dict('records')[0])
        user_dict[row['username']] = userdetails_df[userdetails_df['username'] == row['username']][['name', 'email']].to_dict('records')[0]
    print(user_dict)
    credentials_dict = {}
    credentials_dict['usernames'] = user_dict
    print(credentials_dict)
    print(credentials_dict['usernames']['krishch']['email'])

    
