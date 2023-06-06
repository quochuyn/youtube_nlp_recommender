from dataservice.query import run_query

dataframe = None

st.title("""
Netflix Recommendation System
This is an Content Based Recommender System made on implicit ratings :smile:.
 """)

st.text("")
st.text("")
st.text("")
st.text("")

session.options = st.multiselect(label="Select Movies", options=movies)

st.text("")
st.text("")

session.slider_count = st.slider(label="movie_count", min_value=5, max_value=50)

st.text("")
st.text("")

buffer1, col1, buffer2 = st.columns([1.45, 1, 1])

is_clicked = col1.button(label="Recommend")

if is_clicked:
    dataframe = recommend_table(session.options, movie_count=session.slider_count, tfidf_data=tfidf)

st.text("")
st.text("")
st.text("")
st.text("")

if dataframe is not None:
    st.table(dataframe)