#!/usr/local/bin/python

import psycopg2
import streamlit as st
from os.path import isfile, join
from os import listdir
import base64

def load_images(conn):
    file_path = "/images/"
    file_list = [f for f in listdir(file_path) if isfile(join(file_path, f))]
    for img_file in file_list:
        with open(file_path + img_file, "rb") as image:
            f = image.read()
            img_bytes = base64.b64encode(f)
            print("inserting image from file {}".format(img_file))
            with conn.cursor() as cur:
                video_id = img_file.split('.')[0]
                cur.execute("insert into video_topics values ('" + video_id + "', ARRAY['stremlit',  'education'], 'https://www.youtube.com/watch?v=" + \
                            video_id + "'" + ')')
                #cur.execute("insert into video_thumbnails values('" + video_id + "', " + img_bytes + ")")
                cur.execute('''INSERT INTO video_thumbnails VALUES (%s, %s)''', (video_id, img_bytes))
    conn.commit()

def fetch_images(conn):
    with conn.cursor() as cur:
        cur.execute('''SELECT thumbnail FROM video_thumbnails''')
        # cur.execute('''SELECT video_id FROM video_topics''')

        #print(cur.fetchone())
        mview = cur.fetchone()
        print(type(mview[0]))
        #print(mview.tobytes())
        #new_bin_data = bytes(mview)
        stored_img = base64.b64decode(mview[0])
        return stored_img