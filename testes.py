import cv2
import numpy as np


img = cv2.imread("C:/Users/Brunno Santos/Downloads/HOUGH/4Pixel.png")
k = np.empty(3)
for l in range(0, img.shape[0]):
    for c in range(0, img.shape[1]):
        #print(img[l][c])  o padrao de saida é azul, verde e vermelho (BGR)
        if(img[l][c][2] > 0):
            print('1')