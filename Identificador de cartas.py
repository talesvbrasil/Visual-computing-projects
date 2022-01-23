import cv2
import numpy as np
from matplotlib import pyplot as plt
import os


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
sourceMouth = "templates/mouth_edge/"
sourceHorn = "templates/horn_edge/"
sourceBack = "templates/back_edge/"
sourceTail = "templates/tail_edge/"

#----------------------------------------------------------------
#----------------------- Constantes -----------------------------

raca_threshold = 0.6
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
img = cv2.imread(sourceImages + "jogo1.png")
# converte imagem para preto e branco
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# salva o tamanho da imagem
source_w, source_h = img_gray.shape[::-1]
# recorta a imagem correspondente ao time inimigo
time_inimigo = img_gray[:, int((source_w / 2) - 100) :]
aux_timeinimigo = time_inimigo
time_inimigo = cv2.GaussianBlur(time_inimigo, (3, 3), cv2.BORDER_DEFAULT)
time_inimigo = cv2.Canny(time_inimigo, 125, 175)

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

    # Desenha um retangulo na volta do axie encontrado e em seguida apresenta-o na tela
    for cont in range(len(Cordx)):
        # desenha um retangulo no local onde se encontram as correspondencias
        #cv2.rectangle(
        #    time_inimigo,
        #    (Cordx[cont], Cordy[cont]),
        #    (Cordx[cont] + largura_axie, Cordy[cont] + altura_axie),
        #    (255, 0, 0),
        #    1,
        #)
        # cria uma nova imagem para o axie encontrado e adiciona no array de imagens "enemy"
        enemy.append(
            (Cordx[cont],Cordy[cont])
        )
        enemy_races.append(logo_racas)

#cv2.imshow("time inimigo",time_inimigo)

#################################################################
#----------------------------------------------------------------
#---------------Identificando Cartas dos axies-------------------
#----------------------------------------------------------------
#################################################################
contenemy = 0
for inimigo,raca_axie in zip(enemy,enemy_races):
  cartas = axie_class(1,2,3,4)
  contenemy = contenemy+1
  #################################################################
  #----------------------------------------------------------------
  #---------------Identificando Parte a boca ----------------------
  #----------------------------------------------------------------
  #################################################################

  lista_mouth = os.listdir(sourceMouth)
  mouthArea = aux_timeinimigo[int(inimigo[1]+ymouth):int(inimigo[1]+(altura_axie)),int(inimigo[0]):int(inimigo[0]+xmouth)]
  h, w = mouthArea.shape[::-1]
  mouthArea = cv2.resize(mouthArea, (int(h / templateprop), int(w / templateprop)))
  mouthArea = cv2.GaussianBlur(mouthArea, (3, 3), cv2.BORDER_DEFAULT)
  mouthArea = cv2.Canny(mouthArea, 20, 40)
 
  for mouth in lista_mouth:
    mouthTemplate = cv2.imread(sourceMouth+mouth, 0)
    res_mouth = cv2.matchTemplate(mouthArea, mouthTemplate, method)
    (Cordy, Cordx) = np.where(res_mouth >= part_threshold)
    duplicadosx = []
    duplicadosy = []
    if(len(Cordx)>0):
      #print(raca_axie,mouth,h,w)
      #cv2.imshow(mouth,mouthTemplate)
      #cv2.imshow("Inimigo "+str(contenemy)+" mouth:",mouthArea)
      cartas.mouth = mouth
      break    
  
  #################################################################
  #----------------------------------------------------------------
  #--------------- Identificando Chifre ---------------------------
  #----------------------------------------------------------------
  #################################################################

  lista_horn = os.listdir(sourceHorn)
  hornArea = aux_timeinimigo[int(inimigo[1]):int(inimigo[1]+yhorn),int(inimigo[0]):int(inimigo[0]+xhorn)]
  h, w = hornArea.shape[::-1]
  hornArea = cv2.resize(hornArea, (int(h / templateprop), int(w / templateprop)))
  hornArea = cv2.GaussianBlur(hornArea, (3, 3), cv2.BORDER_DEFAULT)
  hornArea = cv2.Canny(hornArea, 20, 40)

  for horn in lista_horn:
    #print(sourceTail+horn)
    hornTemplate = cv2.imread(sourceHorn+horn,0)
    #cv2.imshow(horn,hornTemplate)

    h, w = hornTemplate.shape[::-1]
    hornTemplate = hornTemplate[int(h/4):,:w]
    res_horn = cv2.matchTemplate(hornArea, hornTemplate, method)
    (Cordy, Cordx) = np.where(res_horn >= horn_threshold)

    if(len(Cordx)>0):
      #print(raca_axie,horn,h,w)
      #cv2.imshow(horn,hornTemplate)
      #cv2.imshow("Inimigo "+str(contenemy)+" horn:",hornArea)
      cartas.horn = horn
      break    

  #################################################################
  #----------------------------------------------------------------
  #--------------- Identificando Back ---------------------------
  #----------------------------------------------------------------
  #################################################################
  Cordx=[]
  Cordy=[]
  lista_back = os.listdir(sourceBack)
  backArea = aux_timeinimigo[int(inimigo[1]):int(inimigo[1]+yback),int(inimigo[0])+xback:int(inimigo[0])+largura_axie]
  h, w = backArea.shape[::-1]
  backArea = cv2.resize(backArea, (int(h / templateprop), int(w / templateprop)))
  backArea = cv2.GaussianBlur(backArea, (3, 3), cv2.BORDER_DEFAULT)
  backArea = cv2.Canny(backArea, 20, 40)

  for back in lista_back:

    backTemplate = cv2.imread(sourceBack+back,0)
    h, w = backTemplate.shape[::-1]
    #BLACK = (0, 0, 0)
    #pts = [(0,0),(int(0),int(w)), (int(h),int(w)), (int(h), int(w*0.9)),(int(h*0.1), 0)]
    #cv2.polylines(backTemplate, np.array([pts]), True, BLACK, 5)
    #cv2.fillPoly(backTemplate, np.array([pts]), BLACK)
    #cv2.imshow(back, backTemplate)

    #backTemplate = backTemplate[:int(h/2),:w]
    res_back = cv2.matchTemplate(backArea, backTemplate, method_back)
    (Cordy, Cordx) = np.where(res_back >= back_threshold)
    
    #cv2.imshow("Inimigo "+str(contenemy)+" back:",backArea)
    if(len(Cordx)>0):
      #print(raca_axie,back,h,w)
      #cv2.imshow(back,backTemplate)
      #cv2.imshow("Inimigo "+str(contenemy)+" back:",backArea)
      cartas.back = back
      break  

  #################################################################
  #----------------------------------------------------------------
  #--------------- Identificando Rabo ---------------------------
  #----------------------------------------------------------------
  #################################################################

  lista_tail = os.listdir(sourceTail)
  tailArea = aux_timeinimigo[int(inimigo[1]+altura_axie/3):int(inimigo[1]+ytail),int(inimigo[0]+xtail):int(inimigo[0]+largura_axie)]
  h, w = tailArea.shape[::-1]
  tailArea = cv2.resize(tailArea, (int(h / templateprop), int(w / templateprop)))
  tailArea = cv2.GaussianBlur(tailArea, (3, 3), cv2.BORDER_DEFAULT)
  tailArea = cv2.Canny(tailArea, 20, 40)
  
  for tail in lista_tail:

    tailTemplate = cv2.imread(sourceTail+tail, 0)
    h, w = tailTemplate.shape[::-1]
    tailTemplate = tailTemplate[:,int(w/2):]
    res_tail = cv2.matchTemplate(tailArea, tailTemplate, method)
    (Cordy, Cordx) = np.where(res_tail >= tail_threshold)

    if(len(Cordx)>0):
      #print(raca_axie,tail,h,w)
      #cv2.imshow(tail,tailTemplate)
      #cv2.imshow("Inimigo "+str(contenemy)+" tail:",tailArea)
      cartas.tail = tail
      break    

  cartas_enemys.append(cartas)
cv2.waitKey()
cv2.destroyAllWindows()
for cartas in cartas_enemys:
  print(cartas.mouth,cartas.horn,cartas.back,cartas.tail)

  
