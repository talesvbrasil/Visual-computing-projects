import cv2
import os 

resultsDirectory = "results/"
sourceDirectory = "sourceImages/"
templateDirectory = "templates/"

cont2 = 0 
for directory in os.listdir(sourceDirectory):

    foldername = directory    
    caminhodaimagem = (sourceDirectory + str(foldername))

    img = cv2.imread(str(caminhodaimagem))
    caminhoatlas = ("sourceImages/" + str(foldername) + "/axie/axie.atlas")
    
    if(not(os.path.isfile(caminhoatlas))):
        continue
    arquivoatlas = open(caminhoatlas, "r")
    texto = arquivoatlas.readlines()
    cont = 0

    for palavra in texto :
        if (palavra == "horn\n") or (palavra == "mouth\n") or (palavra == "back\n") or (palavra == "tail\n") :
            resto, coordenadas = texto[cont+2].split(':')
            x, y = coordenadas.split(',')
            x = int(x)+2
            y = int(y)+2
            resto, tamanho = texto[cont+3].split(':')

            if texto[cont+1] == '  rotate: false\n' :
                w,h = tamanho.split(',')
            else :
                h,w = tamanho.split(',')

            w = int(w)-2
            h = int(h)-2
            parte = img[int(y):int(y+h),int(x):int(x+w)]
            nomeparte, _ = palavra.split("\n")
            #cv2.imshow(palavra +"_" +str(foldername),parte)
            if texto[cont+1] == '  rotate: true\n' :
                parte = cv2.rotate(parte, cv2.ROTATE_90_CLOCKWISE)
            cv2.imwrite(templateDirectory + str(nomeparte) +"_" +str(foldername)+".png",parte)
            print("Salvando imagem "+ str(cont2) + ": "+ templateDirectory + str(nomeparte) +"_" +str(foldername)+'.png')
            cont2 = cont2+1
        cont = cont+1
        


