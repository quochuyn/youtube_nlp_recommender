from st_aggrid import AgGrid
import pandas as pd

# df = pd.read_csv('https://raw.githubusercontent.com/fivethirtyeight/data/master/airline-safety/airline-safety.csv')
# AgGrid(df)

import streamlit as st
import pandas as pd
from st_aggrid import AgGrid

df = pd.DataFrame({"col1": [1, 2, 3], "col2": [4, 5, 6]})

grid_options = {
    "columnDefs": [
        {
            "headerName": "col1",
            "field": "col1",
            "editable": True,
        },
        {
            "headerName": "col2",
            "field": "col2",
            "editable": False,
        },
    ],
}

grid_return = AgGrid(df, grid_options)
new_df = grid_return["data"]

st.write(new_df)