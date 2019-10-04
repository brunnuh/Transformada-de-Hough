import numpy as np
import cv2
from Converters import *
from math import radians, cos, sin
import numpy



class HoughTrans:
    def __init__(self, img, rmin, rmax): # passar parametros
        #print("iniciando")
        self.img = img
        self.rmin = rmin
        self.rmax = rmax
        self.limSupD = 60
        self.limSupE = 120
        self.limInfE = 240
        self.limInfD = 300
        self.width = img.shape[0]
        self.height = img.shape[1]
        self.px_on = np.empty(shape=[])
        #self.__acumalador = np.empty(shape=[img.shape[0], img.shape[1], (self.rmax - self.rmin)])  # aloca uma matriz [][][]
        self.Hough(img, rmin, rmax)



    def Hough(self, img, rmin, rmax):
        self.__allocateAcumulador(self.height, self.width)  # criando acumulaador apartir da altura e largura
        self.px_on = Converters.BufferedImageToPoint(self, img, 0)
        #self.applyMethod(10,10,10)

    def __allocateAcumulador(self, lmax, cmax): # cria um acumulador
        try:
            #print('alocando...')
            self.__acumalador = np.empty(shape=[lmax, cmax, (self.rmax - self.rmin)])  # aloca uma matriz [][][],
            for linha in range(0, lmax-1):
                for coluna in range(0, cmax-1):
                    self.__acumalador[linha][coluna] = np.empty(shape=[self.rmax - self.rmin]) #(self.rmax - self.rmin)
            #print('alocado')

            #print('inicializando...')

            for raio in range(0, (self.rmax - self.rmin)):
                for linha in range(0, lmax):
                    for coluna in range(0, cmax):
                        self.__acumalador[linha][coluna][raio] = 0
            #print('inicializado')
        except:
            print("Hough Transform: Erro na inicializa do acumulador.")

    def applyMethod(self, qtd, perc, fator):

            #colocar execoes

        for raio in range(0, (self.rmax - self.rmin)):

            #circulo = numpy.empty(shape=[])
            circulo = numpy.empty(shape=[self.getCirculo((raio + self.rmin), perc, fator)])

            for np in range(0, len(self.px_on)-1):
                for coord in range(0, len(circulo)):
                    h_x = (self.pxs_on[np].x + circulo[coord].x)
                    h_y = (self.pxs_on[np].y + circulo[coord].y)
                    if((h_x >= 0 and h_x < self.width) and (h_y >= 0 and h_y < self.height)):
                        self.__acumalador[h_x][h_y][raio] += 1
            return self.getPeak(qtd)

    def getCirculo(self, raio, perc, fator):
        circulo = np.empty(shape=[1]) #
        #max_div = (fator*raio)
        Xant = 0
        Yant = 0


        for passo in range(0, 360):
            if((passo > 0 and passo < self.limSupD) or (passo > self.limInfD and passo < 360) or (passo > self.limSupE and passo < self.limInfE)):
                angulo = radians(passo)
                Xc = round(raio * perc * cos(angulo))
                Yc = round(raio * perc * sin(angulo))
                if((passo == 0) or (Xc != Xant) or (Yc != Yant)):
                    Xant = Xc
                    Yant = Yc
                    circulo[0] = np.empty(shape=[Xc, Yc])
            return circulo


    def getPeak(self, qtd):
        coord_center = np.empty(shape=[qtd,4])
        index = 0
        cont = 0
        trocou = True
        for raio in range(0, (self.rmax - self.rmin)):
            for lin in range(0, len(self.__acumalador)):
                for col in range(0, len(self.__acumalador[0])):
                    if(cont < len(coord_center)):
                        coord_center[cont][0] = lin
                        coord_center[cont][1] = col
                        coord_center[cont][2] = raio + self.rmin
                        coord_center[cont][3] = self.__acumalador[lin][col][raio]
                        cont += 1
                    else:
                        if(trocou == True):
                            index = self.index_Min(coord_center)
                            trocou = False
                        if(self.__acumalador[lin][col][raio] > coord_center[index][3]):
                            coord_center[index][0] = lin
                            coord_center[index][1] = col
                            coord_center[index][2] = raio + self.rmin
                            coord_center[index][3] = self.__accumulator[lin][col][raio]
                            trocou = True
        return coord_center


    def index_Min(self, matriz):
        min = 100000000
        index = 0
        try:
            for lin in range(0, len(matriz)):
                if(min > matriz[lin][3]):
                    min = matriz[lin][3]
                    index = lin
        except Exception as erro:
            print(f"Matriz sem memoria na funcao Index_min classe Hough Transform, erro {erro.__class__}")

        return index