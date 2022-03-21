"""Module analysant les images :
Son unique fonction prend en entree une frame et renvoie
l'abscisse du centre de la forme permettant la direction du robot"""


#---IMPORT----
import cv2
import numpy as np
import time
#------------
def colortreatment (image):
    """Analyse une image et trouve le centre de la forme si elle existe.
        Prend en parametre :
        - image : l'image a analyser

        Renvoie : Une image binaire, composé uniquement de noir et de blanc"""

    # On transforme l'image en niveaux de gris
    gris = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # On floute l'image
    flou = cv2.GaussianBlur(gris, (5, 5), 0)

    # On transforme en image binaire
    ret, binaire = cv2.threshold(flou, 100, 255, cv2.THRESH_BINARY_INV)

    # On elimine les bruits restants
    masque = cv2.erode(binaire, None, iterations=2)
    masque = cv2.dilate(masque, None, iterations=2)

    return masque

def find_extrem_pos(masque):
    """Permet de récuperer les coordonnées des points
    extreme correspondant à la forme perçus
    :param une image filtré
    :return : - les coordonnées des points les plus à l'extrimité d'une forme
             -  des couples 0 s'il ne perçoit rien"""
    something, contours, hierarchy = cv2.findContours(masque.copy(),1,cv2.CHAIN_APPROX_NONE)
    if len(contours) > 0: #si le contour existe
        cnt = max(contours,key= cv2.contourArea)
        max_left = tuple(cnt[cnt[:, :, 0].argmin()][0])#points le plus à gauche
        max_right = tuple(cnt[cnt[:, :, 0].argmax()][0])#points le plus à droite
        max_top = tuple(cnt[cnt[:, :, 1].argmin()][0]) #points le plus en haut
        max_bottom = tuple(cnt[cnt[:, :, 1].argmax()][0])#points le plus au centre

        return max_left,max_right,max_top,max_bottom
    else :
        return (0,0),(0,0),(0,0),(0,0)

def contourcont(masque):
    """Cette fonction permet de compter le nombdre de côté sur forme perçus.
    contourcont a été créé dans le but determiner les futurs angles afin
    d'amorcer des virages brutes.

    :param : Le masque, soit une photo filtré
    :return : le nombre de côté perçu sur la forme du masque"""

    something, contours, hierarchy = cv2.findContours(masque, 1, cv2.CHAIN_APPROX_SIMPLE)#On récuprère la forme
    approx = None #Le nombre de côté perçus#
    for cnt in contours:

        #on parcourt tous les points perçus dans la frame
        #Ici approx permet de récupère nombre de côté,
        #plus approxPoly a un ratio, moins il sera précis sur les formes

        approx = cv2.approxPolyDP(cnt, 0.04* cv2.arcLength(cnt, True), True)
    if len(approx) == 5:#test determinant pour calibrage
        #On considère que le nombre de côté determinant à remarquer un angle
        #est de 5 ou 6 côté remarqué sur la frame
        print("angle posssible de type 1")
    if len(approx) == 6:#test determinant pour calibrage
        print("agne possible de type 2")
    print(len(approx))
    return len(approx)

def centroidDetector(masque):
    """Analyse une image et trouve le centre de la forme si elle existe.
    :param - Une image filtréé
    :return :  -Les coordonnées x et y du centre de l'image
                - 0 si aucun centre n'est observé"""
    # On cherche les contours dans l'image
    something, contours, hierarchy = cv2.findContours(masque,1,cv2.CHAIN_APPROX_NONE)


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
        return centre_x, centre_y


    # Si l'on n'observe aucune forme
    else :
        return 0



def getBGRcolor(photo,width,height):
    """
    Cette fonction permet au robot de récupèrer la couleur
    qu'il perçoit au centre de la caméra;

    elle sert de base pour établir la vitesse que le robot
    adaptera durant son parcours.

    :param photo: la photo récupéré par la caméra
    :param width: la longeur de la taille de la photo
    :param height: la hauteur de la taille la photo
    :return: une moyenne de valeur correspondant aux couleurs de type BGR
    récupéré au centre de l'image
    """
    max = 10
    value_x,value_y,value_z = 0,0,0
    print (photo[int(width//2),int(height//2),])
    for i in range(0,max):
        for j in range (0,max):
            value = photo[int(width//2+i),int(height//2+j),]
            value_x = value_x + value[0]#Valeur de Bleu  |B
            value_y = value_y+ value[1]#Valeur de Vert   |G
            value_z = value_z+ value[2]#valeur de Rouge  |R
    #On cacule la moyenne des valeures perçus
    value_x = (value_x // (max*max))
    value_y = (value_y // (max*max))
    value_z = (value_z // (max*max))
    #On le concatene en tableau BGR
    med = [value_x, value_y, value_z]
    return med



def dominentColor(tabcolor):
    """ Cette fonction permet de renvoyer une couleur perçus suite
    à une analyse par étallonage du tableau BGR

     :param: un paramètre un tableau de couleur de type B G R
    :return : sa couleur la plus dominante"""
    blue = 'blue'
    green = 'green'
    red = 'red'
    noir = 'noir'
    jaune = 'jaune'
    blanc = 'blanc'
    #tab[0] correspond à la marge B(lue)
    #tab[1] correspond à la marge G(reen)
    #tab[2] correspond à la marge R(ed)
    if tabcolor[0] > 130 and tabcolor[1] > 130 and tabcolor[2] > 130:
        return blanc

    if tabcolor[0] < 50 and tabcolor[1] < 50 and tabcolor[2] < 50:
        return noir
    if tabcolor[0] < 50 and tabcolor[1] > 120 and tabcolor[2] > 120:
        return jaune
    elif max(tabcolor[0],tabcolor[1],tabcolor[2]) == tabcolor[0]:
        return blue
    elif max(tabcolor[0],tabcolor[1],tabcolor[2]) == tabcolor[1]:
        return green
    elif max(tabcolor[0],tabcolor[1],tabcolor[2]) == tabcolor[2] and tabcolor[2] > 135:
        return red

def chrono_time():
    """Retourne le temps passé à chaque appelle"""
    return time.time()
