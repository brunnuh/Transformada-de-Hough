import cv2
import numpy as np

#sorted - ordena lista


#img = cv2.imread("C:/Users/Brunno Santos/Downloads/HOUGH/4Pixel.png")
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

matriz = np.array(((5,2,-1),(3,12,-4),(5,52,6,9)))

'''valor = min(valor for linha in matriz for valor in linha)
index = matriz[][:].index(valor)'''
print(np.argmin(matriz[:][1]))#np.argmin(self.coord_center[:,3])