from HoughTrans import *
import cv2

img = cv2.imread('2.png')

'''cv2.imshow('imagem', img)
cv2.waitKey(0)
cv2.destroyAllWindows()'''
#‭50.325‬
test = HoughTrans(img, 2, 6)
# 275 x 183
#138 x 91
#194
i = test.applyMethod(194,2,3)
print(i)
maior = i[0][0]
maiorl = 0
maiorc = 0
'''for l in range(0, len(i[:][:])):
    for c in range(0, len(i[:][:])):
        if(maior < i[l][c]):
            maior = i[l][c]
            maiorl = l
            maiorc = c
print(maior, maiorl, maiorc)
print(i)'''






