from PIL import Image
import binascii
from operator import mod

def get_hidden_data():
    hide = Image.open(r"lfr-insert.bmp")  # 将路径换了，这是我们需要隐藏的图片
    c, d = hide.size
    print(c, d)
    m = ''
    for i in range(c):
        for j in range(d):
            m = m + str(bin(hide.getpixel((i, j))).lstrip('0b')).zfill(8)
    return m


if __name__ == '__main__':
    hidden_data = get_hidden_data()
    num = 0
    image = Image.open("lenna_ori.bmp")
    a, b = image.size
    print('Original Pic Size:', a, b)
    print('Length of Hidden Data:', len(hidden_data))
    if a * b < len(hidden_data):
        print("Hidden Pic is Too Big!")
    for i in range(a):
        for j in range(b):
            if (num == len(hidden_data)):
                break
            a = image.getpixel((i, j))

            a1 = a[0] - mod(a[0], 2) + int(hidden_data[num])

            image.putpixel((i, j), (a1, a[1], a[2]))
            num += 1

    image.save(r"lenna.bmp")