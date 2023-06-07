create table video_topics (video_id text primary key, topics text[], video_url text)

create table video_thumbnails(video_id text references video_topics(video_id), thumbnail bytea)

insert into video_topics values ('streamlit1', '{"stremlit",  "education"}', 'https://www.youtube.com/watch?v=3egaMfE9388')
insert into video_topics values ('streamlit2', '{"stremlit",  "education", "capstone"}', 'https://youtube.com/watch?v=_s0bcrHO0Nk')

insert into video_thumbnails values('streamlit1', bytea('/images/3egaMfE9388.jpg'))
insert into video_thumbnails values('streamlit2', bytea('/images/_s0bcrHO0Nk-SD.jpg'))