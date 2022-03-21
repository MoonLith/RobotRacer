"""Module principal du mode autonome du Robot Racer ; necessite les modules
beta_image.py, racer_calculs_valeurs.py et racer_mouvement.py.

Il appelle son unique fonction autonomie() qui lance le mode autonome.

A executer avec Python 3.
"""

########## IMPORTS ##########
import cv2
import image
import calculs_valeurs
import mouvement
#############################

def autonomie() :
    """Cette fonction correspond au mode autonome du Robot Racer."""

    try:
        print("====================================================================")
        print("-------------------- LANCEMENT DU MODE AUTONOME --------------------")
        print("====================================================================\n")

        # L'utilisateur choisit la vitesse du Robot dans les lignes droites
        vitesse = 1600


        # camera_x est la variable d'etat de l'orientation de la camera
        # Pour 250, la camera est alignee a l'axe du Robot
        # Et plus tard on appelle le constructeur de l'objet Robot pour qu'il
        # configure effectivement le placement de sa camera comme ceci
        camera_x = 250
        camera_y = 90

        # L'objet robot va permettre de deplacer et d'arreter le Robot
        robot = mouvement.Robot(vitesse, camera_x, camera_y)

        # On configure le flux de la camera et la resolution a 192x108
        camera = cv2.VideoCapture(0)
        ret = camera.set(3,192);
        ret = camera.set(4,108);

        # En continu
        while True:
            try:
                # On lit une frame depuis la camera
                _, frame = camera.read()

                # La fonction centroidDetector renvoie l'abscisse du centre de
                # la forme observee par la camera
                # La forme observee correspond au ruban adhesif
                centre_x = image.centroidDetector(frame)

                # Si on observe bien un centre de forme
                if centre_x is not False :
                    # On calcule la position de centre_x en fonction de
                    # l'angle de vue de la photo
                    position_x = calculs_valeurs.centrexCamera(centre_x, camera_x)

                    # Grace a la fonction valPourCamera, on trouve, en fonction
                    # de la position de centre_x et l'ancienne orientation de la camera,
                    # la nouvelle orientation de la camera a adopter pour ne pas perdre
                    # le circuit
                    camera_x = calculs_valeurs.valPourCamera(position_x)
                    robot.tournerCamera(camera_x)

                    inclinaison_roues_avant, vitesse = calculs_valeurs.valPourMouvements(position_x, vitesse)
                    robot.tourner(inclinaison_roues_avant, vitesse)

                elif centre_x is False :
                    print("ARRET")
                    robot.arret()

            # En cas d'erreur l'exception est attrapee
            except Exception as e:
                # Et on arrete les moteurs
                robot.arret()
                print(e)
                break

    except KeyboardInterrupt :
        robot.arret()
        print("")
        print("====================================================================")
        print("----------------------- FIN DU MODE AUTONOME -----------------------")
        print("====================================================================\n")



def mainautonomie():
    autonomie()

if __name__ == '__main__':
    autonomie()
