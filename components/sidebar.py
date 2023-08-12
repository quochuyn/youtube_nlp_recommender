from st_on_hover_tabs import on_hover_tabs
import streamlit as st


def sidebar():
    with st.sidebar:
        tabs = on_hover_tabs(tabName=['Videos', 'Account Setting'], 
                            iconName=['Videos', 'manage_accounts'], default_choice=0)

    if tabs =='Videos':
        dashboard_title = '<p style="font-family:Courier; color:Black; font-size: 20px;">Youtube Video Search</p>'
        st.markdown(dashboard_title, unsafe_allow_html=True)
        #st.title("Youtube Video Search")
        #st.write('Name of option is {}'.format(tabs))

    elif tabs == 'Account Setting':
        account_title = '<p style="font-family:Courier; color:Black; font-size: 20px;">User Personal Settings(Click Filter Cell to Edit)</p>'
        st.markdown(account_title, unsafe_allow_html=True)
        #st.title("User Personal Settings")
        #st.write('Name of option is {}'.format(tabs))
    
    return tabs
    
