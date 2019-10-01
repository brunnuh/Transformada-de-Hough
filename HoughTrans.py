import cv2
import numpy as np
from Converters import *



class HoughTrans:
    def __init__(self, img, rmin, rmax): # passar parametros
        #print("iniciando")
        self.img = img
        self.rmin = rmin
        self.rmax = rmax
        self.width = img.shape[0]
        self.height = img.shape[1]
        self.point = []
        #self.__acumalador = np.empty(shape=[img.shape[0], img.shape[1], (self.rmax - self.rmin)])  # aloca uma matriz [][][]
        self.Hough(img, rmin, rmax)



    def Hough(self, img, rmin, rmax):
        self.__allocateAcumulador(self.height, self.width)  # criando acumulaador apartir da altura e largura
        self.point = Converters.BufferedImageToPoint(self, img, 0)


    def __allocateAcumulador(self, lmax, cmax): # cria um acumulador
        try:
            #print('alocando...')
            self.__acumalador = np.empty(shape=[lmax, cmax, (self.rmax - self.rmin)])  # aloca uma matriz [][][],
            for linha in range(0, lmax-1):
                for coluna in range(0, cmax-1):
                    self.__acumalador[linha][coluna] = (self.rmax - self.rmin) #(self.rmax - self.rmin)
            #print('alocado')

            #print('inicializando...')

            for raio in range(0, (self.rmax - self.rmin)):
                for linha in range(0, lmax):
                    for coluna in range(0, cmax):
                        self.__acumalador[linha][coluna][raio] = 0
            #print('inicializado')
        except:
            print("Hough Transform: Erro na inicializa do acumulador.")





