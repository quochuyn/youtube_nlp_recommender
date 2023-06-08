from st_on_hover_tabs import on_hover_tabs
import streamlit as st


def sidebar():
    with st.sidebar:
        tabs = on_hover_tabs(tabName=['Dashboard', 'Account Setting', 'Upload'], 
                            iconName=['dashboard', 'manage_accounts', 'upload'], default_choice=0)

    if tabs =='Dashboard':
        st.title("Navigation Bar")
        st.write('Name of option is {}'.format(tabs))

    elif tabs == 'Account Setting':
        st.title("User Personal Settings")
        st.write('Name of option is {}'.format(tabs))

    elif tabs == 'Upload':
        st.title("Image Upload to Postgres")
        st.write('Name of option is {}'.format(tabs))
    
    return tabs
    