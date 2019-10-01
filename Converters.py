import numpy as np
import cv2


class Converters(object):

        def BufferedImageToPoint(self, img, valor):

            pontos = []

            try:
                for  lin in range(0, img.shape[0]):
                    for col in range(0, img.shape[1]):
                        if(img[lin][col][2] > 0):
                            pontos.append([lin, col])
            except:
                print("Erro(BufferedImageToMatrix): A imagem n�o deve ser nula")

            print(pontos)