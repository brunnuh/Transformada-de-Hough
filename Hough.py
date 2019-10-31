import numpy as np
import math
import cv2


class HoughTransform:
    def __init__(self, img, rmin, rmax, minDist, qtd, limSupD=None, limSupE=None, limInfE=None, limInfD=None):
        self.img = img
        self.rmin = rmin
        self.rmax = rmax
        self.minDist = minDist
        self.qtd = qtd
        self.limSupD = limSupD
        self.limSupE = limSupE
        self.limInfE = limInfE
        self.limInfD = limInfD
        self.pelUma = True
        self.width = img.shape[0]
        self.height = img.shape[1]
        self.accumulator=np.zeros((self.width, self.height, (self.rmax-self.rmin)))
        self.pxs_on = self.BufferedImageToPoint(self.img, 0) #verificar se faz sentido usar 0, ou se e melhor outro numero
        self.applyMethod(self.qtd)

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
        values = list()
        dtype = [('lin', int), ('col', int), ('raio', int), ('acc', float)]

        for delta_raio in range(0, (self.rmax-self.rmin)):
            self.circulo = self.getCirculo(self.rmin + delta_raio)
            for pixel in range(0, len(self.pxs_on)):
                for coord in range (0, len(self.circulo)):
                    h_x=int(self.pxs_on[pixel][0]+self.circulo[coord][1])
                    h_y=int(self.pxs_on[pixel][1]+self.circulo[coord][0])
                    if ((h_x >= 0 and h_x < self.width) and (h_y >= 0 and h_y < self.height)):
                        self.accumulator[h_x][h_y][delta_raio] += 1

        self.accumulator=self.accumulator/255

        for r in range(0, (self.rmax-self.rmin)):
            for x in range(0, self.width):
                for y in range(0, self.height):
                    try:
                        values.append((x,y,r,self.accumulator[x][y][r]))
                    except:
                        print("erro")
        coord = np.array(values, dtype=dtype)
        coord=np.sort(coord, order='acc')
        print(coord[len(coord)-10:])
        cv2.circle(self.img, (self.width,self.height), 0, (0, 255, 0), 1)
        cv2.imshow("imagem", self.img)
        cv2.waitKey(0)
        #self.getPeak(coord)
        #return coord



    def getPeak(self, qtd):
        self.coord_center=np.zeros([qtd, 4])
        self.maior_coord = np.zeros([4])
        index=0
        cont=0

        trocou=True

        #for coluna in linha for valor in coluna
        #maiorcol = max(coluna for linha in self.accumulator )#for coluna in linha for valor in coluna
        #print(maiorlin)

        for delta_raio in range (0, (self.rmax-self.rmin)):
            for lin in range (0, len(self.accumulator)):
                for col in range (0, len(self.accumulator[0])):
                    if (cont<len(self.coord_center)):
                        self.coord_center[cont][0]=lin
                        self.coord_center[cont][1]=col
                        self.coord_center[cont][2]=self.rmin+delta_raio
                        self.coord_center[cont][3]=self.accumulator[lin][col][delta_raio]
                        cont+=1
                    else:
                        if(trocou):
                            index = np.argmin(self.coord_center[:,3])
                            trocou = False

                        if ((self.accumulator[lin][col][delta_raio] > self.coord_center[index][3]) and self.verDista(lin, col, qtd)):
                            self.coord_center[index][0]=lin
                            self.coord_center[index][1]=col
                            self.coord_center[index][2]=self.rmin+delta_raio
                            self.coord_center[index][3]=self.accumulator[lin][col][delta_raio]
                            trocou = True
                            '''if((self.accumulator[lin][col][delta_raio] > self.maior_coord[3])):
                                self.maior_coord[0] = lin
                                self.maior_coord[1] = col'''

        #cv2.circle(self.img, (int(self.maior_coord[1]), int(self.maior_coord[0])), 80, (0, 255, 0)
        return self.coord_center




    def verDista(self, lin, col, qtd):
        #dist=0
        #print(self.coord_center)
        if(self.pelUma == False):
            #print("if")
            for i in range(0, qtd):
                try:#(self.coord_center[i][0] - self.minDist >= lin and self.coord_center[i][1] - self.minDist >= col) or
                    if((self.coord_center[i][0] + self.minDist < lin and self.coord_center[i][1] + self.minDist < col) or (self.coord_center[i][0] - self.minDist > lin and self.coord_center[i][1] - self.minDist > col)):
                        #print(self.coord_center[i][0])
                        return True
                    else:
                        return False
                except:
                    print("erro na comparacao")
        else:
            #print("else")
            self.pelUma = False
            return True
