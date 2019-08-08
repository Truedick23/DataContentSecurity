from PIL import Image
import binascii
from operator import mod

if __name__ == '__main__':

    img = Image.new("L", (67, 60))
    inserted_image = Image.open("lenna.bmp")
    c, d = img.size
    a, b = inserted_image.size
    print('Size of Hidden Pic:', c, d)
    print('Size of Inserted Pic:', a, b)

    num = 0
    m = ""
    s = []
    for q in range(a):
        for p in range(b):

            m = m + str(mod(inserted_image.getpixel((q, p))[0], 2))

            num += 1
            if (num == 8):
                m = "0b" + m
                s.append(eval(m))
                num = 0
                m = ""

    count = 0
    for i in range(c):
        for j in range(d):
            if (count == len(s)):
                break

            img.putpixel((i, j), s[count])
            count += 1
    img.save(r"extracted.bmp")