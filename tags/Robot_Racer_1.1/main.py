"""Module principal du mode autonome du Robot Racer.
A executer."""

###### IMPORT #########
import cv2
import image
import mouvement
#######################

print("====================================================================")
print("-------------------- LANCEMENT DU MODE AUTONOME --------------------")
print("====================================================================\n")

vitesse = 0
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
ret = camera.set(3,192);
ret = camera.set(4,108);


# En continu
while True:
    try:
        # On lit une frame depuis la caméra
        _, frame = camera.read()

        # On recupere les frappes du clavier pour plus tard
        key = cv2.waitKey(1) & 0xFF

        # On lance l'analyse d'image via le module image et
        # sa fonction centroidDetector qui va nous renvoyer
        # centre_x, l'abscisse du centre de la forme observee
        centre_x = image.centroidDetector(frame)

        # Si on observe bien un centre de forme
        if centre_x is not False :
            # On affiche l'abscisse du centre
            print("centre_x = ", centre_x)

            # Et on fait appel a la fonction tourner du module mouvement
            # qui va se deplacer en fonction de l'abscisse du centre
            robot.tourner(centre_x)

        # Si la frappe de clavier recuperee est un "q" on arrete la boucle
        elif centre_x is False :
            print("ARRET")
            robot.arret()
            
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
