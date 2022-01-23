import cv2
import numpy as np
from matplotlib import pyplot as plt

# definição de constantes
# precisão da comparação
threshold = 0.8
# definição do metodo de comparação
method = cv2.TM_CCOEFF_NORMED

# define a largura do axie
largura_axie = 220
altura_axie = 155
# ----------------------------------------------------------------

# input de vídeo
img = cv2.imread("assets/joguinhotest.png")
# converte imagem para preto e branco
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# salva o tamanho da imagem
w, h = img_gray.shape[::-1]
# recorta a imagem correspondente ao time inimigo
time_inimigo = img_gray[:, int(w / 2) - 100 :]

# identificando inimigos
# verifica as plantas existentes
# carrega o template de simbolo de planta
planta = cv2.imread("assets/planta.png", 0)
# encontra as correspondencias do template na imagem fonte
res_planta = cv2.matchTemplate(time_inimigo, planta, method)
# salva as coordenadas das correscondencias com valor superior ao threshold definido
(Cordy, Cordx) = np.where(res_planta >= threshold)

# cria as variaveis auxiliares para a remoção de matchs duplicados
duplicadosx = []
duplicadosy = []

# percorre as cooredenadas das correspondencias para encontrar valores muito próximos e salvalos
for cont in range(len(Cordx) - 1):
    aux_1 = Cordx[cont] / Cordx[cont + 1]
    aux_2 = Cordy[cont] / Cordy[cont + 1]
    if ((aux_1 > 0.9) and (aux_1 < 1.1)) and ((aux_2 > 0.9) and (aux_2 < 1.1)):
        duplicadosx.append(cont)
        duplicadosy.append(cont)

# descartas os valores de correspondencias com valores muito próximos e deixa apenas 1 para evitar duplicatas
Cordx = np.delete(Cordx, duplicadosx, 0)
Cordy = np.delete(Cordy, duplicadosy, 0)
# agrupa as coordenadas resultantes na variavel de localicação
loc = (Cordy, Cordx)

# inicializa a variavel que irá armazenar os axies inimigos
enemy = []

# percorre as correspondencias encontradas, desenha retangulos e salva os axies encontrados em imagens diferentes
for pt in zip(*loc[::-1]):
    # desenha retangulos
    cv2.rectangle(
        time_inimigo, pt, (pt[0] + largura_axie, pt[1] + altura_axie), (255, 0, 0), 1
    )
    # armazena axies na variavel enemy
    enemy.append(
        time_inimigo[pt[1] : pt[1] + altura_axie, pt[0] : pt[0] + largura_axie]
    )

# mostra o time inimigo com os do tipo pesquisado destacados
cv2.imshow("Time inimigo", time_inimigo)
# mostra os inimigos do tipo pesquisado encontrados
cont = 1
for i in enemy:
    cv2.imshow("enemy:" + str(cont), i)
    cont = cont + 1


cv2.waitKey(0)
cv2.destroyAllWindows()
