from PIL import Image
import os


def drawline(x0, y0, x1, y1, color):
    steep = False
    if abs(x1 - x0) < abs(y1 - y0):  # Prefer longer projection
        x0, y0 = y0, x0
        x1, y1 = y1, x1
        steep = True
    if x1 < x0:  # Starting coordinate must be less
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    k = 0 if (x1 - x0) == 0 else (y1 - y0) / (x1 - x0)
    for x in range(x0, x1):
        if steep:
            pixels[(x - x0) * k + y0, x] = color
        else:
            pixels[x, (x - x0) * k + y0] = color


width = 800
height = 800
img = Image.new('RGB', (width, height), "black")  # create a new black image
pixels = img.load()
white = 255 * 65536 + 255 * 256 + 255

vertices = []
faces = []
file = open(os.path.abspath('../resources/head.obj'))
for line in file:
    if line.startswith('v '):
        strValues = line.strip('v ').split()
        vertices.append(list(map(float, strValues)))
    elif line.startswith('f '):
        strValues = line.strip('f ').split()
        verticesNumbers = []
        for val in strValues:
            verticesNumbers.append(int(val.split('/')[0]) - 1)  # First integer is the number of vertex, starts from 1
        faces.append(verticesNumbers)

for face in faces:
    for i in range(0, 3):
        v0 = vertices[face[i]]
        v1 = vertices[face[(i + 1) % 3]]
        x00 = (v0[0] + 1) * (width - 10) / 2
        y00 = (v0[1] + 1) * (height - 10) / 2
        x01 = (v1[0] + 1) * (width - 10) / 2
        y01 = (v1[1] + 1) * (height - 10) / 2
        drawline(int(x00), int(y00), int(x01), int(y01), white)

img.rotate(180).show()
