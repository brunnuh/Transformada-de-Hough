from HoughTrans import *
import cv2

img = cv2.imread("C:/Users/Brunno Santos/Downloads/HOUGH/circulo.png")
'''print(img.shape[2])'''

hough = HoughTransform(img, 95, 100, 60, 120, 240, 300)
#hough = HoughTransform(img, 10, 11)

#cv2.imshow("imagem", img)
'''for i in range(hough.rmax-hough.rmin):
    cv2.imshow("Acumulador", hough.accumulator[:,:,i])'''
ponto = hough.applyMethod(1)
cv2.circle(img, (246, 150), 99, (255, 0, 0))
cv2.imshow("tela", img)
cv2.waitKey(0)



'''acumulador = ob.applyMethod(1)'''


'''print([valor for linha in (ob.applyMethod(4)) for valor in linha])
img = cv2.imread('2.png')'''

'''cv2.imshow('imagem', img)
cv2.waitKey(0)
cv2.destroyAllWindows()'''
'''test = HoughTrans(img, 0, 10)
i = test.a
print(i)
maior = i[0][0]
maiorl = 0
maiorc = 0'''
'''for l in range(0, len(i[:][:])):
    for c in range(0, len(i[:][:])):
        if(maior < i[l][c]):
            maior = i[l][c]
            maiorl = l
            maiorc = c
print(maior, maiorl, maiorc)
print(i)'''


