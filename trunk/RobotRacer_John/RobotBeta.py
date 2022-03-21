
"""Ce module contient la class robot ainsi que 3 de ses fonctions primaires,
Turnoff : fonction permettant d'arrêter toute les activités motrices du robot,
set_speed: fcnction permettant de modifier la vitesse de déplacement du robot
Tourner : Fonction permettant au robot de se déplacer au en fonction de la position
du centre géométrique au préalablement analysé."""

###### IMPORT #########
import RPi.GPIO as GPIO
import Adafruit_PCA9685
from RobotMoveSet import *
import time
#######################

class Robot :
    """La classe Robot contient les methodes d'instance qui deplacent le
    robot :
    - arret() : eteint les moteurs.
    - tourner(int) : effectue des calculs et tourne les roues selon l'entier
    specifie."""

    # M1 : activite du premier moteur,
    # M2 : activite du deuxieme moteur.
    M1 = 4
    M2 = 5

    # Constante pour les roues
    ROUE = 0
    # Constante pour les caméras
    cam_x = 14
    cam_y = 15

    def __init__(self, vitesse=1500) :
        """Constructeur d'un objet de la classe Robot avec une vitesse
        donnee.

        Prend un parametre :
        - vitesse : la vitesse, doit etre comprise entre 1500 et 2300.
        La vitesse par defaut est 1500."""

        # On configure la table GPIO
        self.mode = GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)#On coupe les futurs erreurs

        # On initialise les servos permettant le controle des roues
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(30)


        #	 On initialise les ports GPIO controlant les moteurs
        self.left_backw = GPIO.setup(11, GPIO.OUT)# gauche arrière
        self.left_forw = GPIO.setup(12, GPIO.OUT) # moteur de gauche avant

        self.right_forw = GPIO.setup(18, GPIO.OUT) # moteur de droite avant
        self.right_backw = GPIO.setup(16, GPIO.OUT)#droite arrière
        #-------------------------------

        # On configure l'activite des moteurs, pour la vitesse renseignee
        # lors de l'instanciation
        self.vitesse = vitesse
        self.pwm.set_pwm(Robot.M1, 0, self.vitesse)
        self.pwm.set_pwm(Robot.M2, 0, self.vitesse)
        #-----------------

        #Paramètrage de la position de la caméra
        self.pwm.set_pwm(Robot.cam_x, 0, 260)
        self.pwm.set_pwm(Robot.cam_y, 0, 20)

        self.cam_gauche = 300
        self.cam_gauche_leger = 280
        self.cam_droite = 210
        self.cam_droite_leger = 240
        self.cam_centre = 260
        #-----------------------------------

        # On definie les bornes des valeurs a envoyer a set_pwm pour tourner
        # les roues
        self.roues_a_droite_max = 300
        self.roues_a_gauche_max = 180
        self.roues_droites = int((self.roues_a_droite_max+self.roues_a_gauche_max)/2)
        #---------------------------------

        # On definie des valeurs significatives qui sont les bornes du domaine
        # que prennent les valeurs de centre_x
        self.borne_droite = 140
        self.borne_droit_max = 120

        self.borne_droit_min = 40
        self.borne_gauche = 20
        #-----------------------------------


        # On configure le placement des roues avant au demarrage
        # (dans l'axe du robot)
        self.pwm.set_pwm(Robot.ROUE, 0, self.roues_droites)


    def turnoff(self):
        """Cette fonction permet de couper toutes les activtés motrices du robot
        Elle interviatn en cas d'ârret ou d'érreur lords du mode autonome"""
        GPIO.output(11, 0)
        GPIO.output(18, 0)
        GPIO.output(12, 0)
        GPIO.output(16, 0)

        self.pwm.set_pwm(Robot.M1, 0, 0)
        self.pwm.set_pwm(Robot.M2, 0, 0)

        self.pwm.set_pwm(Robot.ROUE, 0, 0)
        self.pwm.set_pwm(Robot.cam_x,0,0)
        self.pwm.set_pwm(Robot.cam_y,0,0)

        GPIO.cleanup()

    def set_speed(self,speed):
        """Cette methode permet de modfier la vitesse robot
        :parameter : speed, la vitesse choisie"""
        self.pwm.set_pwm(Robot.M1, 0, speed)
        self.pwm.set_pwm(Robot.M2, 0, speed)

    def tourner(self, centre_x) :
        """Cette methode tourne les roues du Robot.
        Elle est appelee avec un parametre :
        - centre_x : la valeur de l'abscisse du centre de la forme percue sur l'image
        
        Une exception de type ValueError est levee si la valeur de centre_x
        n'est pas dans l'intervalle des valeurs des abscisses du repere de la camera"""

        try :
            centre_x = int(centre_x)
            if ((centre_x < 0) and (centre_x > 200)) :
                raise ValueError("L'echelle du repere a-t-elle changee ?")
        except ValueError :
            print("La valeur de centre_x n'est pas exploitable.")
            # Roues avant remises dans l'axe du Robot
            self.pwm.set_pwm(Robot.ROUE, 0, self.roues_droites)
            # Arret des moteurs
            self.arret()

        # Virage a droite
        if (centre_x > self.borne_droit_max) :
            if (centre_x >= self.borne_droite) :
                print("virage serre droite")
                # Virage serre a droite
                forward(GPIO.HIGH)
                self.pwm.set_pwm(Robot.ROUE, 0, self.roues_a_droite_max)

            else :
                self.pwm.set_pwm(Robot.cam_x,0,self.cam_droite_leger)

                # Virage leger a droite
                print("virage leger droite")
                forward(GPIO.HIGH)

                # Taille de l'intervalle dans lequel les roues doivent tourner
                # a droite proportionnellement a centre_x
                taille_interv_roues = self.roues_a_droite_max-self.roues_droites

                # Taille de l'intervalle des valeurs de centre_x, pour lequel
                # on doit tourner a droite proportionnellement
                taille_interv_centre_x = self.borne_droite - self.borne_droit_max

                # Braquage des roues adapte
                inclinaison = int((taille_interv_roues)*(((self.borne_droite)-centre_x)/(taille_interv_centre_x))+self.roues_droites)


                # On tourne selon le braquage trouve
                self.pwm.set_pwm(Robot.ROUE, 0, inclinaison)

        # Virage a gauche
        elif (centre_x < self.borne_droit_min) :
            if (centre_x <= self.borne_gauche) :
                # Virage serre a gauche
                print("virage serré a gauche")
                forward(GPIO.HIGH)
                self.pwm.set_pwm(Robot.ROUE, 0, self.roues_a_gauche_max)
            else :
                self.pwm.set_pwm(Robot.cam_x,0,self.cam_gauche_leger)

                # Virage leger a gauche
                print("virage leger gauche")
                forward(GPIO.HIGH)
                # Taille de l'intervalle dans lequel les roues doivent
                # tourner a gauche proportionnellement a centre_x
                taille_interv_roues = self.roues_droites-self.roues_a_gauche_max
                # Taille de l'intervalle des valeurs de centre_x, pour lequel
                # on doit tourner a droite proportionnellement
                taille_interv_centre_x = self.borne_droit_min - self.borne_gauche
                # Braquage des roues adapte
                inclinaison = int((taille_interv_roues)*(((self.borne_droit_min)-centre_x)/(taille_interv_centre_x))+self.roues_a_gauche_max)

                print("inc = ", inclinaison, "inter_roues = ", taille_interv_roues)

                # On tourne selon le braquage trouve
                self.pwm.set_pwm(Robot.ROUE, 0, inclinaison)

        # Les roues sont dans la borne du milieux,on va donc tout droit
        elif (centre_x <= self.borne_droit_max) and (centre_x >= self.borne_droit_min) :
            self.pwm.set_pwm(Robot.cam_x, 0, self.cam_centre)
            forward(GPIO.HIGH)
            self.pwm.set_pwm(Robot.ROUE, 0, self.roues_droites)
          
