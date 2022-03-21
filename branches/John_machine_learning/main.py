"""Module principal du mode autonome du Robot Racer"""

###### IMPORT #########
import cv2
import image
import mouvement
from centroid_onframe import getBGRcolor,dominentColor
#######################

print("====================================================================")
print("-------------------- LANCEMENT DU MODE AUTONOME --------------------")
print("====================================================================\n")

vitesse = 0
color_available = ['rouge','noir','jaune']

while (vitesse < 1300) or (vitesse > 2500) :
    vitesse = input("Veuillez entrer une vitesse : (comprise entre 1300 & 2500)")
    try :
        vitesse = int(vitesse)
    except ValueError :
        print("Erreur lors de la conversion")

print("Pour quitter, taper 'q'")

# L'objet robot va permettre de se deplacer et de s'arreter
robot = mouvement.Robot(vitesse)

# On configure le flux de la camera et la resolution a 192x108
camera = cv2.VideoCapture(0)
ret = camera.set(3,192)
ret = camera.set(4,108)



# En continu
while True:
    try:
        # On lit une frame depuis la caméra
        _, image = camera.read()
        moy_color = getBGRcolor(image)
        dominent_color = dominentColor(moy_color)
        if dominentColor == 'red':
            robot = mouvement.Robot(1200)
            print("La couleur est rouge, vitesse paramétré à 1200")
        elif dominentColor == 'noir':
            robot = mouvement.Robot(1700)
            print("La couleur est rouge, vitesse paramétré à 1700")
        elif dominentColor == 'noir':
            robot = mouvement.Robot(2000)
            print("La couleur est rouge, vitesse paramétré à 2000")

        # On recupere les frappes du clavier pour plus tard
        key = cv2.waitKey(1) & 0xFF

        # On lance l'analyse d'image via le module image et
        # sa fonction centroidDetector qui va nous renvoyer
        # centre_x, l'abscisse du centre de la forme observee
        masque = image.color_treatment(image)
        pos_centre = image.centroidDetector(masque)

        centre_x = pos_centre[0]#coordonnée X
        centre_y = pos_centre[1]#coordonénée Y

        # Si on observe bien un centre de forme
        if centre_x is not False : # Faire if centre_x du coup?
            # On affiche l'abscisse du centre
            print("centre_x = ", centre_x)

            # Et on fait appel a la fonction tourner du module mouvement
            # qui va se deplacer en fonction de l'abscisse du centre
            robot.tourner(centre_x)

        # Si la frappe de clavier recuperee est un "q" on arrete la boucle
        if key == ord("q"):
                break

    # En cas d'erreur l'exception est attrapee
    except Exception as e:
        # Et on arrete les moteurs
        robot.arret()
        print(e)
        break

# Si la boucle est terminee on arrete les moteurs
robot.arret()
