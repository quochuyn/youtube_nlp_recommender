#!/usr/local/bin/python

import psycopg2
from psycopg2 import sql
from psycopg2.extensions import AsIs
import streamlit as st
from os.path import isfile, join
from os import listdir
import base64
from io import BytesIO

def load_images(conn, topics):
    file_path = "/images/"
    file_list = [f for f in listdir(file_path) if isfile(join(file_path, f))]
    for img_file in file_list:
        with open(file_path + img_file, "rb") as image:
            f = image.read()
            img_bytes = base64.b64encode(f)
            st.text("inserting image from file {}".format(img_file))
            with conn.cursor() as cur:
                video_id = img_file.split('.')[0]
                cur.execute("insert into video_topics values (%s, %s, 'https://www.youtube.com/watch?v=%s') ON CONFLICT DO NOTHING", 
                                    (video_id, topics,  AsIs(video_id)))
                #cur.execute("insert into video_thumbnails values('" + video_id + "', " + img_bytes + ")")
                cur.execute('''INSERT INTO video_thumbnails VALUES (%s, %s) ON CONFLICT DO NOTHING''', (video_id, img_bytes))
    st.text("Image upload complete!")
    conn.commit()

def fetch_images(conn):
    with conn.cursor() as cur:
        cur.execute('''SELECT thumbnail FROM video_thumbnails''')
        return cur.fetchall()

def select_images(conn, search_words, img_count):
    with conn.cursor() as cur:
        cur.execute("SELECT thumbnail FROM video_thumbnails where " + \
                        " video_id in " + \
                            " (SELECT video_id  FROM video_topics  WHERE topics && ARRAY{})".format(search_words))

        return cur.fetchmany(img_count)