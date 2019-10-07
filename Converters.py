import numpy as np
import cv2


class Converters(object):

        def BufferedImageToPoint(self, img, valor):
            pontos = []
            try:
                for lin in range(0, img.shape[0] - 1):#pq de 0 ate o penultimo ??
                    for col in range(0, img.shape[1] - 1):
                        if(img[lin][col][2] > 0):
                            pontos.append([lin, col])
                            #print("entrou no if: ",img[lin][col][2]) saida no python [[0,0]], saida no java java.awt.Point[x=0,y=0]]
            except:
                print("Erro(BufferedImageToMatrix): A imagem nao deve ser nula")

            return pontos