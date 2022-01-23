import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

threshold = 0.8
grayminimum = 120

# converte a imagem para cinza

img = cv.imread("testando.png", 0)
canny = cv.Canny(img, 125, 175)
cv.imshow("canny", canny)
cv.waitKey()
blur = cv.GaussianBlur(img, (3, 3), cv.BORDER_DEFAULT)
canny = cv.Canny(blur, 125, 175)
cv.imshow("canny", canny)
cv.waitKey()
template = cv.imread("postfight.png", 0)
template = cv.GaussianBlur(template, (3, 3), cv.BORDER_DEFAULT)
template = cv.Canny(template, 125, 175)
cv.imshow("template", template)
cv.waitKey()
