"""Module analysant les images :
Son unique fonction prend en entree une frame et renvoie
l'abscisse du centre de la forme permettant la direction du robot"""

###### IMPORT #########
import cv2
import numpy as np
#######################
def color_treatment (image):
    """Analyse une image et trouve le centre de la forme si elle existe.
        Prend en parametre :
        - image : l'image a analyser

        Renvoie : Une image binaire, composé uniquement de noir et de blanc"""

    ####### Les prochaines lignes permettent de travailler l'image pour #######
    #######            la rendre plus facilement analysable             #######

    # On transforme l'image en niveaux de gris
    gris = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # On floute l'image
    flou = cv2.GaussianBlur(gris, (5, 5), 0)

    # On transforme en image binaire
    ret, binaire = cv2.threshold(flou, 100, 255, cv2.THRESH_BINARY_INV)

    # On elimine les bruits restants
    masque = cv2.erode(binaire, None, iterations=2)
    masque = cv2.dilate(masque, None, iterations=2)

    ###########################################################################
    ###########################################################################
    return masque
def find_extrem_pos(masque):
    """Permet de récuperer les coordonnées des points
    extreme correspondant à la forme perçus"""
    contours, hierarchy = cv2.findContours(masque.copy(),1,cv2.CHAIN_APPROX_NONE)
    if len(contours) > 0: #si le contour existe
        cnt = max(contours,key= cv2.contourArea)
        max_left = tuple(cnt[cnt[:, :, 0].argmin()][0])
        max_right = tuple(cnt[cnt[:, :, 0].argmax()][0])
        max_top = tuple(cnt[cnt[:, :, 1].argmin()][0])
        max_bottom = tuple(cnt[cnt[:, :, 1].argmax()][0])

        return max_left,max_right,max_top,max_bottom
    else :
        return 0,0,0,0

    #cv2.circle(masque, (max_left), 30, (220, 255, 0), -1)
    #cv2.circle(masque, (max_right), 30, (220, 220, 0), -1)  # nope
    #cv2.circle(masque, (max_top), 30, (220, 220, 0), -1)
    #cv2.circle(masque, (max_bottom), 30, (220, 220, 0), -1)  # nope
    #while True:
        #cv2.imshow("Photo", masque)
        # cv2.imshow("masque",masque)
        #key = cv2.waitKey(1)
        #if key & 0xFF == ord("q"):  # quitter
           # break
    #print(leftmost)
    #print(rightmost)
    #print(topmost)
    #print(bottommost)
def centroidDetector(masque):
    """Analyse une image et trouve le centre de la forme si elle existe.
    prend en paramètre : - Une image filtréé
        Renvoie :  -Les coordonnées x et y du centre de l'image
                   - False si aucun centre n'est observé"""
    # On cherche les contours dans l'image
    contours, hierarchy = cv2.findContours(masque,1,cv2.CHAIN_APPROX_NONE)




    # Si l'on a plus d'un contour, on observe une forme
    if len(contours) > 0 :

        # On recupere le plus grand contour
        c = max(contours, key = cv2.contourArea)

        # On applique la fonction moments d'openCV pour chercher le centre
        # de la forme observee
        M = cv2.moments(c)

        # On cherche les coordonnées du centre
        centre_x = int(M['m10']/M['m00'])#coordonnée X
        centre_y = int(M['m01']/M['m00'])#coordonnée y
        # On retourne les coordonées de ce centre a la fonction appellante : main
        return centre_x,centre_y


    # Si l'on n'observe aucune forme
    else :
        return False
