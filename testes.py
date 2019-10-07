import cv2
import numpy as np

#sorted - ordena lista


img = cv2.imread("C:/Users/Brunno Santos/Downloads/HOUGH/4Pixel.png")
'''x_y = []
pontos = []
x_y.append('2')
x_y.append('3')
pontos.append(x_y.copy())
x_y.clear()
x_y.append('4')
x_y.append('382')
pontos.append(x_y.copy())
print(pontos)'''

'''ponts = [1 , 2]

cir = []
cir.append(ponts.copy())
ponts[0] = 4
ponts[1] = 3
cir.append(ponts.copy())
ponts[0] = 5
ponts[1] = 7
cir.append(ponts.copy())
print(cir)'''



matriz = [[1, 2, 3], [654, 323, 531], [3432, 434, 456]]
min = 100000000
index = 0

for lin in range(0, len(matriz)):
    if (min > matriz[lin][2]):
        min = matriz[lin][2]
        index = lin

print(index)






'''max([valor for linha in matriz for valor in linha])'''
