import numpy as np
import cv2
import math

class HoughTransform:

    def __init__(self, img, rmin, rmax, limSupD=None, limSupE=None, limInfE=None, limInfD=None):
        self.img = img
        self.rmin = rmin
        self.rmax = rmax
        self.limSupD = limSupD
        self.limSupE = limSupE
        self.limInfE = limInfE
        self.limInfD = limInfD
        self.width = img.shape[0]
        self.height = img.shape[1]
        self.accumulator=np.zeros((self.width,self.height,(self.rmax-self.rmin)))
        self.pxs_on = self.BufferedImageToPoint(self.img, 0)
        #self.applyMethod(80)

    def BufferedImageToPoint(self, img, valor):
        pontos = []
        for  lin in range(0, img.shape[0]):
            for col in range(0, img.shape[1]):
                if(img[lin][col][0] > valor):
                    pontos.append([lin, col])

        return pontos

    def getCirculo(self, raio):
        xc=0
        yc=0
        xant=0
        yant=0
        circulo = []

        if (self.limSupD==None or self.limSupE==None or self.limInfE==None or self.limInfD==None):
            for passo in range (0,360):
                angulo=passo
                angulo=math.radians(angulo)

                xc=round(raio*math.cos(angulo))
                yc=round(raio*math.sin(angulo))

                if (passo ==0 or xc!=xant or yc!=yant):
                    xant=xc
                    yant=yc
                    circulo.append([xc, yc])
        else:
            for passo in range (0,360):
                if ((passo > 0 and passo < self.limSupD) or (passo > self.limInfD and passo < 360) or (passo > self.limSupE and passo < self.limInfE)):
                    angulo=passo
                    angulo=math.radians(angulo)

                    xc=round(raio*math.cos(angulo))
                    yc=round(raio*math.sin(angulo))

                    if (passo ==0 or xc!=xant or yc!=yant):
                        xant=xc
                        yant=yc
                        circulo.append([xc, yc])
        return circulo



    def applyMethod(self, qtd):
        #implementar restricoes
        h_x=0
        h_y=0

        for delta_raio in range(0, (self.rmax-self.rmin)):
            self.circulo = self.getCirculo(self.rmin + delta_raio)

            for pixel in range(0, len(self.pxs_on)):
                for coord in range (0, len(self.circulo)):
                    h_x=int(self.pxs_on[pixel][0]+self.circulo[coord][1])
                    h_y=int(self.pxs_on[pixel][1]+self.circulo[coord][0])
                    #print(h_x, h_y, delta_raio)
                    if ((h_x >= 0 and h_x < self.width) and (h_y >= 0 and h_y < self.height)):
                        self.accumulator[h_x][h_y][delta_raio] += 1
        self.accumulator=self.accumulator/255

        return self.getPeak(qtd)

    def getPeak(self, qtd):
        coord_center = np.zeros((qtd, 4))
        cont = 0
        index = 0
        trocou = True
        for raio in range(0, (self.rmax - self.rmin)):
            for lin in range(0, len(self.accumulator)):
                for col in range(0, len(self.accumulator[0])):
                    if (cont < len(coord_center)):
                        coord_center[cont][0] = lin
                        coord_center[cont][1] = col
                        coord_center[cont][2] = raio + self.rmin
                        coord_center[cont][3] = self.accumulator[lin][col][raio]
                        cont += 1
                    else:
                        if (trocou == True):
                            index = np.argmin(coord_center[:,3])
                            trocou = False
                        if (self.accumulator[lin][col][raio] > coord_center[index][3]):  # verificar
                            coord_center[index][0] = lin
                            coord_center[index][1] = col
                            coord_center[index][2] = raio + self.rmin
                            coord_center[index][3] = self.accumulator[lin][col][raio]
                            trocou = True

        return coord_center



        #Index_Min?

    #localizaLimbo?
    #ordenaHough?

