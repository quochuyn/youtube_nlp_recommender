create table video_topics (video_id text primary key, topics text[], video_url text)

create table video_thumbnails(video_id text references video_topics(video_id) primary key, thumbnail bytea)

-- upload option in app loads preset data in above tables
-- these are some sample queries since we have a complex type array
-- && means ANY value
-- @> means ALL values

SELECT video_id  FROM video_topics  WHERE  topics && ARRAY['test', 'streamlit']

SELECT video_id  FROM video_topics  WHERE  not topics @> ARRAY['streamlit']



create table user_profile (username text primary key, email text, name text, password text, preauth boolean, search_words text[], filtered_words text[])
create table session_cookie(expiry_days integer, key text, cookie_name text)

-- sample data insert
insert into user_profile values('krishch', 'krishch@umich.edu', 'krishan chawla', 'test', true, array['streamlit'], array['toxic'])
insert into session_cookie  values(30, 'test', 'test')

