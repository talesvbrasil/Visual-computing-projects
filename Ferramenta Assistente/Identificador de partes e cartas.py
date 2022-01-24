import cv2
import numpy as np
from matplotlib import pyplot as plt
import os
from assistentLibraryV1 import cardidentifier


#----------------------------------------------------------------
#-----------------------Define a strutura do axie ---------------

class axie_class:    
    # The init method or constructor
    
    def __init__(self, mouth,horn,back,tail):
           
        # Instance Variable
        self.mouth = mouth            
        self.horn = horn
        self.back = back
        self.tail = tail

#----------------------------------------------------------------
#-----------------------Paths------------------------------------

sourceImages = "sourceImages/"
sourceTemplates = "templates/"
sourceRacas = "racas/"
sourceCards = "cards/"
#----------------------------------------------------------------
#----------------------- Constantes -----------------------------

raca_threshold = 0.5
part_threshold = 0.4

tail_threshold = 0.2
horn_threshold = 0.2
mouth_threshold = 0.2
back_threshold = 0.2

method = cv2.TM_CCOEFF_NORMED
method_back = cv2.TM_CCORR_NORMED
#method = cv2.TM_SQDIFF_NORMED


templateprop = 1 / 3.4
kernel = np.ones((3, 3), np.uint8)

#----------------------------------------------------------------
#--------------------- Dimensões e divisões ---------------------

largura_axie = 250
altura_axie = 175



xmouth = int(largura_axie / 2)
ymouth = int(altura_axie)/2
xtail = int(largura_axie * 2 / 4)
ytail = int(altura_axie)
xhorn = int(largura_axie /2)
yhorn = int(altura_axie/2)
xback = int(largura_axie/2)
yback = int(altura_axie/2)

#-----------------------------------------------------------------
#---------------- Inicialização de Variaveis ---------------------

enemy = []
enemy_races = []
cartas_enemys = []

##################################################################
#-----------------------------------------------------------------
#-------------- Carregando Fonte de Vídeo/Imagem -----------------
#-----------------------------------------------------------------
##################################################################

# define local e arquivo fonte
img = cv2.imread(sourceImages + "jogo3.png")
# converte imagem para preto e branco
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# salva o tamanho da imagem
source_w, source_h = img_gray.shape[::-1]
# recorta a imagem correspondente ao time inimigo
time_inimigo = img_gray[:, int((source_w / 2) - 100) :]
aux_timeinimigo = time_inimigo
time_inimigo = cv2.GaussianBlur(time_inimigo, (3, 3), cv2.BORDER_DEFAULT)
time_inimigo = cv2.Canny(time_inimigo, 20, 40)

#################################################################
#----------------------------------------------------------------
#-------------------identificando inimigos-----------------------
#----------------------------------------------------------------
#################################################################

#---- Inicia a varredura para identificar as classes inimigas ---
#--- Carrega os nomes de arquivos de logo de raça em uma lista --
lista_racas = os.listdir(sourceRacas)
#------------- Percorre todos arquivos da lista gerada ----------
for logo_racas in lista_racas:
  #reinicializa o detor de coordenadas duplicadas 
  duplicadosx = []
  duplicadosy = []

  #carrega arquivo do logo de raça correspondente
  raca = cv2.imread(sourceRacas+logo_racas, 0)
  
  raca = cv2.Canny(raca, 30, 40)
  
  #encontra as coordenadas de correspondencia
  res_raca = cv2.matchTemplate(time_inimigo, raca, method)
  #filtra as coordenadas de correspondencia pelo valor de threshold
  (Cordy, Cordx) = np.where(res_raca >= raca_threshold)
  #verifica se existe pelo menos 1 coordenada encontrada
  if(len(Cordy)>0):

    #encontra coordenadas duplicadas
    for cont in range(len(Cordx) - 1):
      aux_1 = Cordx[cont] / Cordx[cont + 1]
      aux_2 = Cordy[cont] / Cordy[cont + 1]
      if ((aux_1 > 0.9) and (aux_1 < 1.1)) and ((aux_2 > 0.9) and (aux_2 < 1.1)):
          duplicadosx.append(cont)
          duplicadosy.append(cont)

    #remove coordenadas duplicadas
    Cordx = np.delete(Cordx, duplicadosx, 0)
    Cordy = np.delete(Cordy, duplicadosy, 0)

    for cont in range(len(Cordx)):
        # salva a coordenada dos inimigos encontrados dentro de uma unica variável
        enemy.append(
            (Cordx[cont],Cordy[cont])
        )
        enemy_races.append(logo_racas)

#################################################################
#----------------------------------------------------------------
#---------------Identificando Cartas dos axies-------------------
#----------------------------------------------------------------
#################################################################


enemycards = []
cont = 1
for inimigo in enemy:
  print("==================\nVERIFICANDO CARTAS DO INIMIGO:"+str(cont)+"\n==================")
  enemycards.append(cardidentifier(sourceTemplates,aux_timeinimigo,inimigo[0],inimigo[1],altura_axie,largura_axie,cont))  
  cont = cont+1
  cv2.waitKey()
cartinhas = []
for cardgroup in enemycards:
  print(cardgroup)
  conjuntodecartas = []
  if len(cardgroup[0]) >1:
    carta1 = cv2.imread(str(sourceCards)+str(cardgroup[0]),0)
  else:
    carta1 = cv2.imread(str(sourceCards)+"interrogacao.png",0)
 
  if len(cardgroup[1]) >1:
    carta2 = cv2.imread(str(sourceCards)+str(cardgroup[1]),0)
  else:
    carta2 = cv2.imread(str(sourceCards)+"interrogacao.png",0)

  if len(cardgroup[2]) >1:
    carta3 = cv2.imread(str(sourceCards)+str(cardgroup[2]),0)
  else:
    carta3 = cv2.imread(str(sourceCards)+"interrogacao.png",0)

  if len(cardgroup[3]) >1:
    carta4 = cv2.imread(str(sourceCards)+str(cardgroup[3]),0)
  else:
    carta4 = cv2.imread(str(sourceCards)+"interrogacao.png",0)

  conjuntodecartas = cv2.hconcat([carta1,carta2,carta3,carta4])
  cartinhas.append(conjuntodecartas)
cont = 1  
for cartas in cartinhas:
  cv2.imshow("cartas do axie"+str(cont)+":",cartas)
  cont = cont+1
cv2.waitKey(0)
cv2.destroyAllWindows()