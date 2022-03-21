"""Module analysant les images :
Son unique fonction prend en entree une frame et renvoie
l'abscisse du centre de la forme permettant la direction du robot.
Cette fonction est appelée par le module main.py pour chaque frame observee"""

###### IMPORT #########
import cv2
import numpy as np
#######################

def centroidDetector(image):
    """Analyse une image et trouve le centre de la forme si elle existe.
    Prend en parametre :
    - image : l'image a analyser

    Renvoie une valeur de retour :
    - centre_x : l'abscisse du centre de la forme si elle existe, Faux sinon"""


    ####### Les prochaines lignes permettent de travailler l'image pour #######
    #######            la rendre plus facilement analysable             #######

    # On transforme l'image en niveaux de gris
    gris = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # On floute l'image
    flou = cv2.GaussianBlur(gris,(5,5),0)

    # On transforme en image binaire
    ret,binaire = cv2.threshold(flou,100,255,cv2.THRESH_BINARY_INV)

    # On elimine les bruits restants
    masque = cv2.erode(binaire, None, iterations=2)
    masque = cv2.dilate(masque, None, iterations=2)

    ###########################################################################
    ###########################################################################


    # On cherche les contours dans l'image
    something, contours, hierarchy = cv2.findContours(masque.copy(),1,cv2.CHAIN_APPROX_NONE)

    # Si l'on a plus d'un contour, on observe une forme
    if len(contours) > 0 :

        # On recupere le plus grand contour
        c = max(contours, key = cv2.contourArea)

        # On applique la fonction moments d'openCV pour chercher le centre
        # de la forme observee
        M = cv2.moments(c)

        # On cherche l'abscisse de ce centre
        centre_x = int(M['m10']/M['m00'])

        # On retourne l'abscisse de ce centre a la fonction appellante : main
        return centre_x


    # Si l'on n'observe aucune forme
    else :
        return False
