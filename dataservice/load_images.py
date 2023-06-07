file_path = "/images"
file_list = [f for f in listdir(file_path) if isfile(join(file_path, f))]
for img_file in file_list:
    with open(img_file, "rb") as image:
    f = image.read()
    b = bytearray(f)
    print b[0]