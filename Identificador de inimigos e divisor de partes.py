import cv2
import numpy as np
from matplotlib import pyplot as plt

# definição de constantes
# precisão da comparação

threshold = 0.8
method = cv2.TM_CCOEFF_NORMED

largura_axie = 220
altura_axie = 150

duplicadosx = []
duplicadosy = []

shorn = (int(0), int(0))
smouth = (int(0), int((altura_axie / 2)))
sback = (int(largura_axie / 2), int(0))
stail = (int(largura_axie * 9 / 11), int(0))

ehorn = (int((largura_axie / 2)), int((altura_axie / 2)))
emouth = (int((largura_axie / 2)), int(altura_axie))
eback = (int((largura_axie * 9 / 11)), int(altura_axie))
etail = (int(largura_axie), int(altura_axie))

# ----------------------------------------------------------------
enemy = np.zeros([155, 220, 3], dtype=np.uint8)

# input de vídeo
img = cv2.imread("assets/joguinhotest.png")
# converte imagem para preto e branco
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# salva o tamanho da imagem
w, h = img_gray.shape[::-1]
# recorta a imagem correspondente ao time inimigo
time_inimigo = img_gray[:, int((w / 2) - 100) :]

enemy = []
# identificando inimigos
# ------------  verifica as plantas existentes
# carrega o template de planta
planta = cv2.imread("assets/planta.png", 0)
# verifica todas as correspondencias na imagem para o template e armazena as informações na variavel resposta
res_planta = cv2.matchTemplate(time_inimigo, planta, method)
# salva as coordenadas das correspondencias acima do filtro threshold em vetores de coordenada x e y
(Cordy, Cordx) = np.where(res_planta >= threshold)
# remove cooredenadas de correspondencias duplicadas

for cont in range(len(Cordx) - 1):
    aux_1 = Cordx[cont] / Cordx[cont + 1]
    aux_2 = Cordy[cont] / Cordy[cont + 1]
    if ((aux_1 > 0.9) and (aux_1 < 1.1)) and ((aux_2 > 0.9) and (aux_2 < 1.1)):
        duplicadosx.append(cont)
        duplicadosy.append(cont)

Cordx = np.delete(Cordx, duplicadosx, 0)
Cordy = np.delete(Cordy, duplicadosy, 0)

# Desenha um retangulo na volta do axie encontrado e em seguida apresenta-o na tela
for cont in range(len(Cordx)):
    # desenha um retangulo no local onde se encontram as correspondencias
    cv2.rectangle(
        time_inimigo,
        (Cordx[cont], Cordy[cont]),
        (Cordx[cont] + largura_axie, Cordy[cont] + altura_axie),
        (255, 0, 0),
        1,
    )
    # cria uma nova imagem para o axie encontrado e adiciona no array de imagens "enemy"
    enemy.append(
        time_inimigo[
            Cordy[cont] : Cordy[cont] + altura_axie,
            Cordx[cont] : Cordx[cont] + largura_axie,
        ]
    )
# --------------------------------------------------------------------------------------------------------------
dusk = cv2.imread("assets/dusk.png", 0)
# verifica todas as correspondencias na imagem para o template e armazena as informações na variavel resposta
res_dusk = cv2.matchTemplate(time_inimigo, dusk, method)
# salva as coordenadas das correspondencias acima do filtro threshold em vetores de coordenada x e y
(Cordy, Cordx) = np.where(res_dusk >= threshold)
# remove cooredenadas de correspondencias duplicadas
duplicadosx = []
duplicadosy = []
for cont in range(len(Cordx) - 1):
    aux_1 = Cordx[cont] / Cordx[cont + 1]
    aux_2 = Cordy[cont] / Cordy[cont + 1]
    if ((aux_1 > 0.9) and (aux_1 < 1.1)) and ((aux_2 > 0.9) and (aux_2 < 1.1)):
        duplicadosx.append(cont)
        duplicadosy.append(cont)

Cordx = np.delete(Cordx, duplicadosx, 0)
Cordy = np.delete(Cordy, duplicadosy, 0)

# Desenha um retangulo na volta do axie encontrado e em seguida apresenta-o na tela
for cont in range(len(Cordx)):
    # desenha um retangulo no local onde se encontram as correspondencias
    cv2.rectangle(
        time_inimigo,
        (Cordx[cont], Cordy[cont]),
        (Cordx[cont] + largura_axie, Cordy[cont] + altura_axie),
        (255, 0, 0),
        1,
    )
    # cria uma nova imagem para o axie encontrado e adiciona no array de imagens "enemy"
    enemy.append(
        time_inimigo[
            Cordy[cont] : Cordy[cont] + altura_axie,
            Cordx[cont] : Cordx[cont] + largura_axie,
        ]
    )

cv2.imshow("colorida", img)
cv2.waitKey(0)
cv2.imshow("preta e branca", img_gray)
cv2.waitKey(0)
cv2.imshow("time inimigo", time_inimigo)
cv2.waitKey(0)
# apresenta todos inimigos encontrados na tela
for i in range(len(enemy)):
    cv2.imshow("time inimigo", enemy[i])
    cv2.moveWindow("time inimigo", 200, 200)
    cv2.waitKey(0)

    # destaca o chifre
    cv2.rectangle(
        enemy[i],
        shorn,
        ehorn,
        (255, 0, 0),
        1,
    )
    # destaca a boca
    cv2.rectangle(
        enemy[i],
        smouth,
        emouth,
        (255, 0, 0),
        1,
    )
    # destaca as costas
    cv2.rectangle(
        enemy[i],
        sback,
        eback,
        (255, 0, 0),
        1,
    )
    # destaca o rabo
    cv2.rectangle(
        enemy[i],
        stail,
        etail,
        (255, 0, 0),
        1,
    )

    cv2.imshow("time inimigo", enemy[i])
    cv2.waitKey(0)
