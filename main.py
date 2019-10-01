from HoughTrans import *
import cv2

img = cv2.imread("C:/Users/Brunno Santos/Downloads/HOUGH/4Pixel.png")
#print(img.shape[0])
ob = HoughTrans(img, 2, 6) # raio minimo e raio maximo
