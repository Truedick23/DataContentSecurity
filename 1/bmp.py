from PIL import Image, ImageDraw
import sys

def using_pil():
    im = Image.open('logo.bmp')
    draw = ImageDraw.Draw(im)
    size = im.size
    print(size)
    im_rgb = im.convert('RGB')
    pixel_data = im_rgb.load()

    for i in range(size[0]):
        for j in range(size[1]):
            pixel = pixel_data[i, j]
            if(pixel[0] == 0 and pixel[1] == 0 and pixel[2] == 0):
                print(i, j)
                draw.point((i, j), (0, 255, 255))
    im.save('pillowed.bmp')

if __name__ == '__main__':
    using_pil()