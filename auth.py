#!/usr/local/bin/python

import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
from sqlalchemy import create_engine, text
import yaml
from yaml.loader import SafeLoader

def auth_from_db():
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
    preauth_df = pd.read_sql(sql = text("select email from user_profile where preauth = True"), con=dbEngine.connect())

    userdetails_df['password'] =  userdetails_df['password'].apply(lambda x: stauth.Hasher([x]).generate()[0])

    user_dict = {}
    for idx, row in username_df.iterrows():
        #print(row['username'])
        #print(userdetails_df[userdetails_df['username'] == row['username']][['name', 'email']].to_dict('records')[0])
        user_dict[row['username']] = userdetails_df[userdetails_df['username'] == row['username']][['name', 'email', 'password']].to_dict('records')[0]
    #print(user_dict)
    credentials_dict = {}
    credentials_dict['usernames'] = user_dict
    print(credentials_dict)
    #print(credentials_dict['usernames']['krishch']['email'])

    preauth_dict = {}
    preauth_dict['emails'] = preauth_df['email'].to_list()
    #print(preauth_dict)

    #print(cookie_df['name'].values[0])

    authenticator = stauth.Authenticate(
        credentials_dict,
        cookie_df['name'].values[0],
        cookie_df['key'].values[0],
        int(cookie_df['expiry_days'].values[0]),
        preauth_dict
    )   

    return authenticator

def auth_from_yaml():
    hashed_passwords = stauth.Hasher(['abc', 'def', 'test']).generate()
    print("hashed_passwords ", hashed_passwords)

    with open('./config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)

    print(config['credentials'])
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )
    return authenticator

authenticator = auth_from_db()
name, authentication_status, username = authenticator.login('Login', 'main')

print("name ", name, "auth ", authentication_status, "username ", username)

if authentication_status:
    authenticator.logout('Logout', 'main', key='unique_key')
    st.write(f'Welcome *{name}*')
    st.title('Some content')
elif authentication_status is False:
    st.error('Username/password is incorrect')
elif authentication_status is None:
    st.warning('Please enter your username and password')