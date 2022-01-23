import cv2
import numpy as np
import os


threshold = 0.7
templateDirectory = os.fsencode("templates")

nameDirectory = os.fsencode("nomes")

arquivoparte = os.listdir(templateDirectory)
arquivonome = os.listdir(nameDirectory)
cont = 0 
for file in arquivoparte:
  filename = os.fsdecode(file)
  if filename.endswith(".png"):


    img_rgb = cv2.imread("templates/" + filename)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    img_canny = cv2.Canny(img_gray, 125, 175)
    h2,w2 = img_canny.shape[::-1]
    print ("dimensoes 2:"+str(h2)+":"+str(w2))
    for segundoarquivo in arquivonome:
      
      templateFilename = os.fsdecode(segundoarquivo)
      template = cv2.imread("nomes/" + templateFilename, 0)
      h,w = template.shape[::-1]
      template = cv2.Canny(template, 125, 175)

      if h>h2 and w>w2 :
        res = cv2.matchTemplate(template, img_canny, cv2.TM_CCOEFF_NORMED)
        cordx,cordy = np.where(res >= threshold)

        if len(cordx) > 0:        
          print ("dimensoes 1:"+str(h)+":"+str(w))
          
          cv2.imshow(templateFilename, template)
          cv2.imshow(filename, img_canny)
          cv2.waitKey()
          print(str(cont) + "Parte encontrada: " + (templateFilename) +"corresponde a:" +(filename))
          cont = cont+ 1