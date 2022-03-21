"""Module analysant les images.

Il contient les fonctions :
- image:imageTreatement(image) : fonction qui, a partir d'une image, renvoie une
image plus facilement analysable. imageTreatement est appelee uniquement par
centroidDetector.

- int:centroidDetector(image) : fonction qui prend en entree une image et renvoie
l'abscisse du centre de la forme permettant la direction a prendre pour le robot.
Cette fonction est appelee par le module main.py pour chaque frame observee,
et elle appelle imageTreatement dans un premier temps.
"""

########## IMPORTS ##########
import cv2
#############################

def imageTreatment(image) :
    """Fonction appelee par centroidDetector qui transforme une image
    en une image dans laquelle il sera possible de trouver des formes
    significatives. Plusieurs fonctions d'OpenCV sont executees a la suite.

    Prend un parametre :
    - image : une image.

    Renvoie une image :
    - masque : image 'image' mais binaire, a laquelle on a elimine les bruits.
    """

    # On transforme l'image en image en niveaux de gris
    gris = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # On floute l'image
    flou = cv2.GaussianBlur(gris,(5,5),0)

    # On la transforme en image binaire
    ret,binaire = cv2.threshold(flou,100,255,cv2.THRESH_BINARY_INV)

    # On elimine les bruits restants, grace a l'erosion puis la dilatation
    masque = cv2.erode(binaire, None, iterations=2)
    masque = cv2.dilate(masque, None, iterations=2)

    return masque


def centroidDetector(image):
    """Analyse une image et trouve le centre de la forme principale s'il y en a
    une.

    Prend un parametre :
    - image : l'image a analyser.

    Renvoie une valeur de retour :
    - centre_x : l'abscisse du centre de la forme si elle existe, Faux sinon.
    """

    masque = imageTreatment(image)

    # On cherche les contours dans l'image
    something, contours, hierarchy = cv2.findContours(masque.copy(),1,cv2.CHAIN_APPROX_NONE)

    # Si l'on a plus d'un contour, on observe au moins une forme
    if len(contours) > 0 :

        # On recupere le plus grand contour
        c = max(contours, key = cv2.contourArea)

        # On applique la fonction moments d'openCV qui nous permettra de trouver
        # le centre de la forme observee
        M = cv2.moments(c)

        # On cherche l'abscisse du centre de cette forme en faisant :
        # son moment d'ordre 10 divise par son moment d'ordre 0
        centre_x = int(M['m10']/M['m00'])

        # On retourne l'abscisse de ce centre a la fonction appellante : main
        return centre_x

    # Sinon, on n'observe aucune forme
    else :
        return False
