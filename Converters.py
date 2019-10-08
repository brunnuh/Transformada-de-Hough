import numpy as np
import cv2


class Converters(object):

        def BufferedImageToPoint(self, img, valor):
            pontos = []
            try:
                for lin in range(0, img.shape[0]):#pq de 0 ate o penultimo ??
                    for col in range(0, img.shape[1]):
                        if(img[lin][col][0] > valor):
                            pontos.append([lin, col])
                            #print("entrou no if: ",img[lin][col][2]) saida no python [[0,0]], saida no java java.awt.Point[x=0,y=0]]
            except:
                print("Erro(BufferedImageToMatrix): A imagem nao deve ser nula")

            return pontos

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

        '''matriz = [[1, 2, 3], [654, 323, 531], [3432, 434, 456]]
        min = 100000000
        index = 0

        for lin in range(0, len(matriz)):
            if (min > matriz[lin][2]):
                min = matriz[lin][2]
                index = lin

        print(index)'''

        '''max([valor for linha in matriz for valor in linha])'''
        '''def Hough(self, img, rmin, rmax):
               self.__allocateAcumulador(self.height, self.width)  # criando acumulaador apartir da altura e largura
               self.px_on = Converters.BufferedImageToPoint(self, img, 0)
               #self.applyMethod(10,10,10)'''


'''    def __allocateAcumulador(self, lmax, cmax): # cria um acumulador
        try:
            #print('alocando...')
            #self.__acumalador = np.empty(shape=[lmax, cmax, (self.rmax - self.rmin)])  # aloca uma matriz [][][],
            for linha in range(0, lmax):
                for coluna in range(0, cmax):
                    self.__acumulador[linha][coluna] = np.empty(shape = [self.rmax - self.rmin]) #(self.rmax - self.rmin)
=======
            self.__acumalador = np.empty(shape=[lmax, cmax, (self.rmax - self.rmin)])  # aloca uma matriz [][][],
            for linha in range(0, lmax-1):
                for coluna in range(0, cmax-1):
                    self.__acumalador[linha][coluna] = np.empty(shape=[self.rmax - self.rmin]) #(self.rmax - self.rmin)
>>>>>>> 4bb310fa49d7d5dfecb01c270793e2c2ea8bce16
            #print('alocado')

            #print('inicializando...')

            for raio in range(0, (self.rmax - self.rmin)):
                for linha in range(0, lmax):
                    for coluna in range(0, cmax):
                        self.__acumulador[linha][coluna][raio] = 0
            #print('inicializado')
        except:
            print("Hough Transform: Erro na inicializa do acumulador.")'''

'''def getCirculo(self, raio, perc, fator):
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
'''

'''def index_Min(self, matriz):
    min = 100000000
    index = 0
    try:
        for lin in range(0, len(matriz)):
            if(min > matriz[lin][3]):
                min = matriz[lin][3]
                index = lin
    except Exception as erro:
        print(f"Matriz sem memoria na funcao Index_min classe Hough Transform, erro {erro.__class__}")

    return index'''

'''import numpy as np
import cv2
from Converters import *
from math import radians,sin,cos
from math import radians, cos, sin
import numpy



class HoughTrans:
    def __init__(self, img, rmin, rmax): # passar parametros
        #print("iniciando")
        self.img = img
        self.rmin = rmin
        self.rmax = rmax
        self.limSupD = 60 #por parametro
        self.limSupE = 120
        self.limInfE = 240
        self.limInfD = 300
        self.width = img.shape[0]
        self.height = img.shape[1]
        #self.px_on = np.empty(shape = [1])
        #self.circulo = np.empty(shape=[1])
        self.__acumulador = np.zeros(shape=[self.height, self.width, (self.rmax - self.rmin)])  # aloca uma matriz [][][]
        self.__allocateAcumulador(self.height, self.width) # criando acumulaador apartir da altura e largura
        self.px_on = Converters.BufferedImageToPoint(self, img, 0)
        #self.__acumalador = np.empty(shape=[img.shape[0], img.shape[1], (self.rmax - self.rmin)])  # aloca uma matriz [][][]

    def applyMethod(self, qtd):
        perc = 1.03
        h_x = 0
        h_y = 0

        for raio in range(0, (self.rmax - self.rmin)):
            #circulo = []
            #circulo = ((self.getCirculo((raio + self.rmin), perc).copy()))  # cria o circulo modelo
           #self.circulo = self.getCirculo(self.rmin + raio)
            self.circulo = self.getCirculo(self.rmin-raio)
            for np in range(0, len(self.px_on)):
                for coord in range(0, len(self.circulo)):
                    h_x = (self.px_on[np][0] + self.circulo[coord][1])
                    h_y = (self.px_on[np][1] + self.circulo[coord][0])
                    #print("erro")
                    if ((h_x >= 0) and (h_x < self.width) and (h_y >= 0) and (h_y < self.height)):
                            self.__acumulador[h_x][h_y][raio] += 1

            cv2.imshow("tela", self.__acumulador)
            cv2.waitKey(0)

        return self.getPeak(self)

    def getCirculo(self, raio):

        circulo = []
        pontos = [0, 0]

        for passo in range(0, 360):
            if ((passo > 0 and passo < self.limSupD) or (passo > self.limInfD and passo < 360) or (passo > self.limSupE and passo < self.limInfE)):
                angulo = radians(passo)
                Xc = round(raio  * cos(angulo))
                Yc = round(raio  * sin(angulo))
                if ((passo == 0) or (Xc != pontos[0]) or (Yc != pontos[1])):
                    pontos[0] = Xc
                    pontos[1] = Yc
                    circulo.append(pontos.copy())
        return circulo

    def getPeak(self, qtd):
        coord_center = np.empty(shape=[qtd, 4])
        linha = 0
        coluna = 0
        cont = 0
        trocou = True
        for raio in range(0, (self.rmax - self.rmin)):
            for lin in range(0, len(self.__acumulador)):
                for col in range(0, len(self.__acumulador[0])):
                    if (cont < len(coord_center)):
                        coord_center[cont][0] = lin
                        coord_center[cont][1] = col
                        coord_center[cont][2] = raio + self.rmin
                        coord_center[cont][3] = self.__acumulador[lin][col][raio]
                        cont += 1
                    else:
                        if (trocou == True):
                            linha, coluna = self.index_Min(coord_center)
                            # index = max([valor for linha in coord_center for valor in linha])
                            trocou = False
                        if (self.__acumulador[lin][col][raio] > coord_center[linha][coluna]):  # verificar
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
        for lin in range(0, matriz.shape[0]):
            for col in range(0, matriz.shape[1]):
                if (min > matriz[lin][col]):
                    min = matriz[lin][col]
                    linha, coluna = lin, col
        return linha, coluna'''