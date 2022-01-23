import cv2
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

threshold = 0.8
grayminimum = 120

# converte a imagem para cinza

img = cv.imread("testando.png", 0)
_, img_gray = cv.threshold(img, grayminimum, 255, cv.THRESH_BINARY)
template = cv.imread("postfight.png", 0)
_, template = cv.threshold(template, grayminimum, 255, cv.THRESH_BINARY)

img_gray = cv.cvtColor(img_gray, cv.COLOR_GRAY2BGR)  # 3 channel mask
template = cv.cvtColor(template, cv.COLOR_GRAY2BGR)  # 3 channel mask

cv2.imshow("tela2", img_gray)
cv2.waitKey()
cv2.imshow("tela3", template)
cv2.waitKey()

res_img_gray = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)

loc = np.where(res_img_gray >= threshold)

# w, h = template.shape[::-1]

for pt in zip(*loc[::-1]):
    cv2.rectangle(time_inimigo, pt, (pt[0] + 50, pt[1] + 50), (255, 0, 0), 1)
# break
cv2.imshow("tela1", img)
cv2.waitKey()
cv2.imshow("tela2", img_gray)
cv2.waitKey()
cv2.imshow("tela3", template)
cv2.waitKey()
