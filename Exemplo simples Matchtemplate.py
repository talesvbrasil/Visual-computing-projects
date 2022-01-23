import cv2
import numpy as np

# define o limiar aceitavel de correspondencia entre imagem e template
threshold = 0.5

# carrega a imagem fonte
img_rgb = cv2.imread("sourceImages/test.png")
# transforma a imagem fonte em escala de cinza
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

# carrega o template
template = cv2.imread("assets/lam.png")
# transforma o template em escala de cinza
template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
# obtem as dimensões do template para desenhar o retangulo
h, w = template.shape[::-1]

# mostra o template obtido
cv2.imshow("Template obtido", template)
cv2.waitKey()

# varre a imagem fonte para encontrar correspondencias com o template
res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
# salva as correspondencias que tem valor superior ao threshold definido
loc = np.where(res >= threshold)

# desenha retangulos em todas as coordenadas obtidas com valores superiores ao threshold
for pt in zip(*loc[::-1]):
    cv2.rectangle(img_rgb, pt, (pt[0] + h, pt[1] + w), (255, 0, 0), 1)

# mostra a imagem final com as correspondencias destacadas por retangulos
cv2.imshow("Imagem encontrada", img_rgb)
cv2.waitKey()
