import os
import cv2
import numpy as np


def cardidentifier(directory,enemyteam,coordx,coordy,altura_axie,largura_axie,cont):
  card = []
  method = cv2.TM_CCORR_NORMED
  #enemyteam = cv2.imread("sourceImages/" + "jogo1.png",0)
  #source_w, source_h = enemyteam.shape[::-1]  
  #enemyteam = enemyteam[:, int((source_w / 2) - 100) :]
  part_threshold = 0.7
  for newdirectory in os.listdir(directory):
    subdirectory = str("templates/"+newdirectory+"/")
    templates_list = os.listdir(subdirectory)
    # Verifica qual parte vai ser pesquisada
    if(subdirectory == "templates/mouth/"):
      searchArea = enemyteam[int(coordy+altura_axie/2):int(coordy+(altura_axie)),int(coordx):int(coordx+largura_axie/2)]
    if(subdirectory == "templates/horn/"):
      searchArea = enemyteam[int(coordy):int(coordy+70),int(coordx+50):int(coordx+largura_axie/2)]
    if(subdirectory == "templates/back/"):
      searchArea = enemyteam[int(coordy):int(coordy+altura_axie/2),int(coordx+largura_axie/2):int(coordx+largura_axie-75)]
    if(subdirectory == "templates/tail/"):
      searchArea = enemyteam[int(coordy+80):int(coordy+altura_axie),int(coordx+175):int(coordx+largura_axie)]
    # Percorre os templates disponiveis do directorio acessado

    #cv2.imshow(newdirectory + str(cont),searchArea)
    x = 0
    y = 0
    matchedpart = []
    matchnumber = 0
    for part in templates_list:
      partTemplate = cv2.imread(subdirectory+part, 0)
      #partTemplate = cv2.GaussianBlur(partTemplate, (3, 3), cv2.BORDER_DEFAULT)
      #partTemplate = cv2.Canny(partTemplate, 20, 40)
      correspondencias = part_identifier(searchArea,partTemplate,part,x,y)
      x = x + 150
      if (x>=1000):
        x = 0
        y = y+125
      if correspondencias > matchnumber:
        matchedpart = part
        matchnumber = correspondencias
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    card.append(matchedpart)
  return(card)

def part_identifier(searchArea,partTemplate,part,x,y):
  sift = cv2.SIFT_create()
  kp1, des1 = sift.detectAndCompute(partTemplate,None)
  kp2, des2 = sift.detectAndCompute(searchArea,None)
  bf = cv2.BFMatcher()
  matches = bf.knnMatch(des1,des2,k=2)
  good = []
  for m,n in matches:
    if m.distance < 0.6*n.distance: 
      good.append([m])
    
    #print(kp2[g.trainIdx].pt)
  
  img3 = cv2.drawMatchesKnn(partTemplate,kp1,searchArea,kp2,good,None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
  cv2.imshow(part,img3)
  cv2.moveWindow(part, x,y)
  return len(good)
  