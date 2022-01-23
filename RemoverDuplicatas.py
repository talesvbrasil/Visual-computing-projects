import cv2
import numpy as np
import os

threshold = 0.7  # set threshold
templateDirectory = os.fsencode("templates")

arquivobase = os.listdir(templateDirectory)

for file in arquivobase:

  filename = os.fsdecode(file)

  if filename.endswith(".png"):

    print(filename)
    img_rgb = cv2.imread("templates/" + filename)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    img_canny = cv2.Canny(img_gray, 125, 175)
    h,w = img_gray.shape[::-1]

    for segundoarquivo in arquivobase:

      templateFilename = os.fsdecode(segundoarquivo)

      if templateFilename != filename:
        template = cv2.imread("templates/" + templateFilename, 0)
        template = cv2.Canny(template, 125, 175)
        h2,w2 = template.shape[::-1]

        if(h == h2 ) and (w == w2):
          res = cv2.matchTemplate(img_canny, template, cv2.TM_CCOEFF_NORMED)
          cordx,cordy = np.where(res >= threshold)

          if len(cordx) > 0:
            print("detected positive " + (templateFilename))
            os.remove("templates/" + templateFilename)
            arquivobase.remove(segundoarquivo)
