import streamlit as st
import pandas as pd
from st_aggrid import AgGrid
from sqlalchemy import create_engine, text
from psycopg2.extensions import AsIs


def modify_profile(conn, username):
    dbcredentials = st.secrets["postgres"]

    dbEngine = create_engine('postgresql+psycopg2://' +
        dbcredentials['user'] + ':' +
        dbcredentials['password'] + '@' +
        dbcredentials['host'] + ':' +
        str(dbcredentials['port']) + '/' +
        dbcredentials['dbname'])

    username_df = pd.read_sql(sql = text("select username, array_to_string(search_words, ',') search_words, " + \
                    " array_to_string(filtered_words, ',') filtered_words " + \
                    " from user_profile where username = '" + username + "'"), con=dbEngine.connect())

    print(username_df)
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

    #print(new_df['search_words'].values[0])
    new_search_words = new_df['search_words'].values[0]

    # if not isinstance(new_search_words, list):
    #     new_search_words = new_search_words.split(',')

    new_filtered_words = new_df['filtered_words'].values[0]
    
    # if not isinstance(new_filtered_words, list):
    #     new_filtered_words = new_filtered_words.split(',')
    
    st.write(new_df)

    if st.button('Save'):
        st.write('Saving changes search {} and filter {}...'.format(new_search_words, new_filtered_words))
        with conn.cursor() as cur:
            cur.execute("update user_profile set search_words = array[%s],  filtered_words = array[%s] where username = '%s'", 
                                    (new_search_words, new_filtered_words,  AsIs(username)))
        st.write('Saving Done!')
        conn.commit()
