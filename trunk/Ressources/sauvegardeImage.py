import cv2 
import sys

"""Prendre une photo en tapant sur la touche 's'.
On appelle ce programme en ligne de commande avec en argument de nom que l'on
veut donner à la photo, sans l'extension qui s'ajoutera automatiquement."""

camera = cv2.VideoCapture(0)

while True :

    #On recupere les frames de la camera
    _, frame = camera.read()
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    if key == ord('s') :
        break

cv2.imwrite(sys.argv[1]+".jpg", frame)
camera.release()
cv2.destroyAllWindows()