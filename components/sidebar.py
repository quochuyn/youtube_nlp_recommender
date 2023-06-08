from st_on_hover_tabs import on_hover_tabs
import streamlit as st


def sidebar():
    with st.sidebar:
        tabs = on_hover_tabs(tabName=['Dashboard', 'Account Setting', 'Upload'], 
                            iconName=['dashboard', 'manage_accounts', 'upload'], default_choice=0)


    if tabs =='Dashboard':
        dashboard_title = '<p style="font-family:Courier; color:Blue; font-size: 20px;">Youtube Video Search</p>'
        st.markdown(dashboard_title, unsafe_allow_html=True)
        #st.title("Youtube Video Search")
        #st.write('Name of option is {}'.format(tabs))

    elif tabs == 'Account Setting':
        account_title = '<p style="font-family:Courier; color:Blue; font-size: 20px;">User Personal Settings</p>'
        st.markdown(account_title, unsafe_allow_html=True)
        #st.title("User Personal Settings")
        #st.write('Name of option is {}'.format(tabs))

    elif tabs == 'Upload':
        upload_title = '<p style="font-family:Courier; color:Blue; font-size: 20px;">Image Upload To Postgres</p>'
        st.markdown(upload_title, unsafe_allow_html=True)
        #st.title("Image Upload to Postgres")
        #st.write('Name of option is {}'.format(tabs))
    
    return tabs
    