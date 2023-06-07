import psycopg2

def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])

conn = init_connection()

file_path = "/images"
file_list = [f for f in listdir(file_path) if isfile(join(file_path, f))]
for img_file in file_list:
    with open(img_file, "rb") as image:
    f = image.read()
    img_bytes = bytearray(f)
    print img_bytes[0]
    with conn.cursor() as cur:
        video_id = img_file.split('.')[0]
        cur.execute("insert into video_topics values (" + video_id + ", ARRAY[['stremlit',  'education']], 'https://www.youtube.com/watch?v='" + video_id +')')
        cur.execute("insert into video_thumbnails values(" + video_id + ", " + img_bytes + ")")
