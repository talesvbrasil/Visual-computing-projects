import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

# define os parametros nessessários para o dilate (engrossamento da linha do desenho )
kernel = np.ones((3, 3), np.uint8)
# define o parametro de qualidade de match
threshold = 0.5
# define a proporção de redimencionamento da fonte
sourceprop = 1
# define a proporção de redimencionamento do template (3.4 para uma fonte de 1920-1080)
templateprop = 1 / 3.4


# carrega a fonte
img = cv.imread("passarinho.png")
# cria uma copia cinza da imagem fonte original
img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
# obtem as dimensões de largura e altura da imagem fonte original
w, h = img_gray.shape[::-1]
# redmenciona para o parametro de proporção de imagem fonte definido anteriormente
img_gray = cv.resize(img_gray, [int(w * sourceprop), int(h * sourceprop)])
# aplica um efeito de borrão na imagem fonte para facilitar a obtenção dos contornos
img_blur = cv.GaussianBlur(img_gray, (3, 3), cv.BORDER_DEFAULT)
# transforma a imagem fonte em contornos
img_canny = cv.Canny(img_blur, 125, 175)

# mostra a imagem obtida através da imagem fonte
# cv.imshow("Imagem Fonte", img_canny)
# cv.waitKey()

# carrega a imagem para ser usada como template
template = cv.imread("biquinho.png")
# converte a o template para preto e branco
template = cv.cvtColor(template, cv.COLOR_BGR2GRAY)
# coloca um efeito de borrão no template para facilitar o rastreamento de linhas
template = cv.GaussianBlur(template, (5, 5), cv.BORDER_DEFAULT)
# transforma a imagem template em linhas
template = cv.Canny(template, 125, 175)
# dilata as linhas para facilitar a combinação com formas presentes na fonte
template = cv.dilate(template, kernel, iterations=1)
# obtem o tamanho do template para poder redimencionar
w, h = template.shape[::-1]
# redimenciona o template para os parametros definidos no inicio do programa
template = cv.resize(template, [int(w * templateprop), int(h * templateprop)])

# mostra o template final obtido
# cv.imshow("Imagem Template", template)
# cv.waitKey()

# obtem todas as correspondencias entra a imagem fonte e o template
res_template = cv.matchTemplate(img_canny, template, cv.TM_CCOEFF_NORMED)
# filtra as correspondencias em relação ao threshold definido
loc = np.where(res_template >= threshold)
# obtem o tamanho do template para que seja desenhado o retangulo do mesmo tamanho
w, h = template.shape[::-1]

# percorre o vetor de correspondencias filtradas (loc) e desenha retangulos no local de todas as correspondencias
for pt in zip(*loc[::-1]):
    cv.rectangle(img, pt, (pt[0] + w, pt[1] + h), (255, 0, 0), 1)

# mostra a imagem final com as correspondencias destacadas
cv.imshow("img", img)
cv.waitKey()
