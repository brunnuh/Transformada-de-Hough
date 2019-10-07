import cv2
import numpy as np
from Converters import *
from math import radians,sin,cos



class HoughTrans:
    def __init__(self, img, rmin, rmax): # passar parametros
        #print("iniciando")
        self.img = img
        self.rmin = rmin
        self.rmax = rmax
        self.width = img.shape[0]
        self.height = img.shape[1]
        self.limSupD = 60
        self.limSupE = 120
        self.limInfE = 240
        self.limInfD = 300
        #self.px_on = np.empty(shape = [1])
        #self.circulo = np.empty(shape=[1])
        self.__acumulador = np.empty(shape=[self.height, self.width, (self.rmax - self.rmin)])  # aloca uma matriz [][][]
        self.__allocateAcumulador(self.height, self.width)  # criando acumulaador apartir da altura e largura
        self.px_on = Converters.BufferedImageToPoint(self, img, 0)

    



    def __allocateAcumulador(self, lmax, cmax): # cria um acumulador
        try:
            #print('alocando...')
            #self.__acumalador = np.empty(shape=[lmax, cmax, (self.rmax - self.rmin)])  # aloca uma matriz [][][],
            for linha in range(0, lmax):
                for coluna in range(0, cmax):
                    self.__acumulador[linha][coluna] = np.empty(shape = [self.rmax - self.rmin]) #(self.rmax - self.rmin)
            #print('alocado')

            #print('inicializando...')

            for raio in range(0, (self.rmax - self.rmin)):
                for linha in range(0, lmax):
                    for coluna in range(0, cmax):
                        self.__acumulador[linha][coluna][raio] = 0
            #print('inicializado')
        except:
            print("Hough Transform: Erro na inicializa do acumulador.")


    def applyMethod(self, qtd):
        perc = 1.03
        h_x = 0
        h_y  = 0 
                                
        for raio in range(0, (self.rmax - self.rmin)):

            circulo = []
            circulo = ((self.getCirculo((raio + self.rmin), perc).copy()))#cria o circulo modelo
            for np in range(0, len(self.px_on)):
                for coord in range(0, len(circulo)):
                    h_x = (self.px_on[np][0] + circulo[coord][0])
                    h_y = (self.px_on[np][1] + circulo[coord][1])
                    if ((h_x >= 0) and (h_x < self.width) and (h_y >= 0) and (h_y < self.height)):
                        try:
                            self.__acumulador[h_x][h_y][raio] += 1
                        except:
                            print("erro na acumulacao")
                            break

            circulo.clear() #provavel erro
        return self.getPeak(qtd)
	
    def getCirculo(self, raio, perc):

        circulo = []
        pontos = [0, 0]

        for passo in range(0, 360):
            if((passo > 0 and passo < self.limSupD) or (passo > self.limInfD and passo < 360) or (passo > self.limSupE and passo < self.limInfE)):
                angulo = radians(passo)
                Xc = round(raio * perc * cos(angulo))
                Yc = round(raio * perc * sin(angulo))
                if((passo == 0) or (Xc != pontos[0]) or (Yc != pontos[1])):
                    pontos[0] = Xc
                    pontos[1] = Yc
                    circulo.append(pontos.copy())
        return circulo


    def getPeak(self, qtd):
        coord_center = np.empty(shape=[qtd,4])
        linha = 0
        coluna = 0
        cont = 0
        trocou = True
        for raio in range(0, (self.rmax - self.rmin)):
            for lin in range(0, len(self.__acumulador)):
                for col in range(0, len(self.__acumulador[0])):
                    if(cont < len(coord_center)):
                        coord_center[cont][0] = lin
                        coord_center[cont][1] = col
                        coord_center[cont][2] = raio + self.rmin
                        coord_center[cont][3] = self.__acumulador[lin][col][raio]
                        cont += 1
                    else:
                        if(trocou == True):
                            linha, coluna = self.index_Min(coord_center)
                            #index = max([valor for linha in coord_center for valor in linha])
                            trocou = False
                        if(self.__acumulador[lin][col][raio] > coord_center[linha][coluna]): # verificar
                            coord_center[linha][0] = lin
                            coord_center[linha][1] = col
                            coord_center[linha][2] = raio + self.rmin
                            coord_center[linha][3] = self.__acumulador[lin][col][raio]
                            trocou = True
        return coord_center


    def index_Min(self, matriz):
        min = 100000000
        linha = 0
        coluna = 0
        try:
            for lin in range(0, matriz.shape[0]):
                for col in range(0,matriz.shape[1]):
                    if(min > matriz[lin][col]):
                        min = matriz[lin][col]
                        linha, coluna = lin, col
        except Exception as erro:
            print(f"Matriz sem memoria na funcao Index_min classe Hough Transform, erro {erro.__class__}")

        return linha, coluna

