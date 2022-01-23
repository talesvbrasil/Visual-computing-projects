import cv2
import numpy as np
import os

threshold = 0.8  # set threshold
resultsDirectory = "results/"
sourceDirectory = "sourceImages/"
templateDirectory = "templates/"
detectedCount = 0
recize = 1 / 3.5

for file in os.listdir(sourceDirectory):
    if file.endswith(".jpg") or file.endswith(".png"):
        print(file)
        img_rgb = cv2.imread(sourceDirectory + file)
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(resultsDirectory + "graysource_" + file, img_gray)
        for templateFile in os.listdir(templateDirectory):
            
            if templateFile.endswith(".jpg") or templateFile.endswith(".png"):
                template = cv2.imread("templateDirectory" + templatefile, 0)
                w, h = template.shape[::-1]
                w = int(w * recize)
                h = int(h * recize)
                template = cv2.resize(template, (int(w), int(h)))
                cv2.imwrite(
                    resultsDirectory + "template_" + templatefile,
                    template,
                )
                cv2.imshow(templateFile, template)
                cv2.waitKey()

                res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
                loc = np.where(res >= threshold)

                if len(loc[0]):
                    detectedCount = detectedCount + 1
                    for pt in zip(*loc[::-1]):
                        cv2.rectangle(
                            img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2
                        )
                    cv2.imwrite(resultsDirectory + "res_" + templateFile, img_rgb)
                    print("res_" + file + " saved")
                    # break

        print("detected positive " + str(detectedCount))
        continue
    else:
        continue
