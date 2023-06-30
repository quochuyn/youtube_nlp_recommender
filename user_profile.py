import streamlit as st
import pandas as pd
from st_aggrid import AgGrid
from sqlalchemy import create_engine, text

def modify_profile(username):
    dbcredentials = st.secrets["postgres"]

    dbEngine = create_engine('postgresql+psycopg2://' +
        dbcredentials['user'] + ':' +
        dbcredentials['password'] + '@' +
        dbcredentials['host'] + ':' +
        str(dbcredentials['port']) + '/' +
        dbcredentials['dbname'])

    username_df = pd.read_sql(sql = text("select * from user_profile where username = '" + username + "'"), con=dbEngine.connect())

    grid_options = {
        "columnDefs": [
            {
                "headerName": "Search",
                "field": "search_words",
                "editable": True,
            },
            {
                "headerName": "Filtered",
                "field": "filtered_words",
                "editable": True,
            },
        ],
    }

    grid_return = AgGrid(username_df, grid_options)
    new_df = grid_return["data"]

    st.write(new_df)