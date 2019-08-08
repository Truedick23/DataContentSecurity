from struct import unpack

class BMPFile:

    def __init__(self, path):
        file = open(path, 'rb')

        # BITMAPFILEHEADER
        self.bfType = file.read(2)
        self.bfSize = file.read(4)
        self.bfReserved1 = file.read(2)
        self.bfReserved2 = file.read(2)
        self.bfOffBits = file.read(4)

        # BITMAPINFOHEADER
        self.biSize = file.read(4)
        self.biWidth = file.read(4)
        self.biHeight = file.read(4)
        self.biPlanes = file.read(2)
        self.biBitCount = file.read(2)

        self.height = unpack('i', self.biHeight)[0]
        self.width = unpack('i', self.biWidth)[0]

        self.biCompression = file.read(4)
        self.biSizeImage = file.read(4)
        self.biXPelsPerMeter = file.read(4)
        self.biYPelsPerMeter = file.read(4)
        self.biClrUsed = file.read(4)
        self.biClrImportant = file.read(4)

        #IMAGEDATA
        self.image_data = []
        self.redundant_data = []

        for h in range(self.height):
            data_row = []
            count = 0
            for w in range(self.width):
                data_row.append(
                    [file.read(1), file.read(1), file.read(1)])
                count = count + 3
            while count % 4 != 0:
                self.redundant_data.append(file.read(1))
                count = count + 1
            self.image_data.append(data_row)

        self.image_data.reverse()
        file.close()

        self.R = []
        self.G = []
        self.B = []
        for row in range(self.height):
            R_row = []
            G_row = []
            B_row = []
            for col in range(self.width):
                B_row.append(int.from_bytes(self.image_data[row][col][0], 'big'))
                G_row.append(int.from_bytes(self.image_data[row][col][1], 'big'))
                R_row.append(int.from_bytes(self.image_data[row][col][2], 'big'))
            self.R.append(R_row)
            self.B.append(B_row)
            self.G.append(G_row)


    def set_pixel(self, h, w, r, g, b):
        self.image_data[h][w][0] = b.to_bytes(1, byteorder='big')
        self.image_data[h][w][1] = g.to_bytes(1, byteorder='big')
        self.image_data[h][w][2] = r.to_bytes(1, byteorder='big')

    def save_file(self, path):
        file = open(path, 'wb+')

        file.write(self.bfType)
        file.write(self.bfSize)
        file.write(self.bfReserved1)
        file.write(self.bfReserved2)
        file.write(self.bfOffBits)

        file.write(self.biSize)
        file.write(self.biWidth)
        file.write(self.biHeight)
        file.write(self.biPlanes)
        file.write(self.biBitCount)

        file.write(self.biCompression)
        file.write(self.biSizeImage)
        file.write(self.biXPelsPerMeter)
        file.write(self.biYPelsPerMeter)
        file.write(self.biClrUsed)
        file.write(self.biClrImportant)

        red = 0
        for h in range(self.height):
            count = 0
            for w in range(self.width):

                file.write(self.image_data[self.height - 1 - h][w][0])
                file.write(self.image_data[self.height - 1 - h][w][1])
                file.write(self.image_data[self.height - 1 - h][w][2])

                count = count + 3
            while count % 4 != 0:
                file.write(self.redundant_data[red])
                red = red + 1
                count = count + 1

        file.close()

if __name__ == '__main__':
    BMP = BMPFile('logo.bmp')
    width = BMP.width
    height = BMP.height
    # print(width, height)
    for h in range(height):
        for w in range(width):
            # print(BMP.R[h][w], BMP.G[h][w], BMP.B[h][w])
            if BMP.R[h][w] < 40 and BMP.G[h][w] < 40 and BMP.B[h][w] < 40:
                print(h, w)
                BMP.set_pixel(h, w, 0, 0, 255)
    BMP.save_file('logo1.bmp')