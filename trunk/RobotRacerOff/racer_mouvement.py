"""Module gerant les deplacements du Robot.

Il est constitue de la classe Robot qui est composee de methodes d'instance
effectuant des actions concretes sur le Robot (tourner les roues, avancer,
s'arreter, tourner la camera). Les instructions qui commandent le robot
se trouvent seulement dans ce module.
"""

########## IMPORTS ##########
import RPi.GPIO as GPIO
import Adafruit_PCA9685
#############################

class Robot :
    """La classe Robot contient les methodes d'instance qui deplacent le
    robot :
    - void:arret() : eteint les moteurs.
    - void:tourner(int:inclinaison, int:vitesse) : tourne les roues selon
    l'entier specifie (inclinaison) et met a jour la vitesse des moteurs
    selon la vitesse specifiee (vitesse).
    - void:tournerCamera(int:camera_x) : place le servo X de la camera a la
    position specifiee (camera_x).
    """

    # Constante M1 : activite du premier moteur,
    # M2 : activite du deuxieme moteur.
    M1 = 4
    M2 = 5

    # Constante pour les roues
    ROUE = 0

    # Constantes pour les servos de la camera
    CAMERA_Y = 15
    CAMERA_X = 14

    def __init__(self, vitesse_choisie=1500, camera_direction=250, camera_hauteur = 90) : 
        """Constructeur d'un objet de la classe Robot avec une vitesse
        donnee, et une position de la camera donnee.

        Prend en parametre :
        - int:vitesse_choisie : la vitesse dans les trajets rectilignes, doit
        etre comprise entre 1500 et 2300. La vitesse par defaut est 1500.
        - int:camera_direction : le placement du servo X de la camera ; doit
        etre compris entre 180 et 320. Le placement par defaut est 250.
        - int:camera_hauteur : le placement du servo Y de la camera, compris
        entre 90 et 200. Le placement par defaut est 90.

        Des exceptions de type ValueError sont lancees si le constructeur du
        robot cree est appele avec des arguments qui ne sont pas dans le bon
        intervalle.
        """

        if vitesse_choisie < 1300 or vitesse_choisie > 2300 :
            raise ValueError("Vitesse incorrecte")
        if camera_direction < 180 or camera_direction > 320 :
            raise ValueError("Positionnement camera impossible")
        if camera_hauteur < 90 or camera_hauteur > 200 :
            raise ValueError("Positionnement camera impossible")

        # 230 correspond a un placement des roues avant dans l'axe du Robot
        self.roues_droites = 230

        # On configure la table GPIO
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        # On initialise les servos permettant le controle des roues et de la
        # camera
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(30)

        # On initialise les ports GPIO controlant les moteurs
        GPIO.setup(12, GPIO.OUT) # moteur de gauche forward
        GPIO.setup(18, GPIO.OUT) # moteur de droite forward
        GPIO.setup(11, GPIO.OUT)
        GPIO.setup(16, GPIO.OUT)

        # On configure l'activite des moteurs, pour la vitesse renseignee
        # lors de l'instanciation
        self.vitesse_choisie = vitesse_choisie
        self.pwm.set_pwm(Robot.M1, 0, self.vitesse_choisie)
        self.pwm.set_pwm(Robot.M2, 0, self.vitesse_choisie)

        # On configure le placement des roues avant au demarrage
        # (dans l'axe du robot)
        self.pwm.set_pwm(Robot.ROUE, 0, self.roues_droites)

        # On configure le placement de la camera comme renseigne lors de
        # l'instanciation
        self.pwm.set_pwm(Robot.CAMERA_X, 0, camera_direction)
        self.pwm.set_pwm(Robot.CAMERA_Y, 0, camera_hauteur)


    def arret(self) :
        """Methode d'instance de la classe Robot qui ne prend aucun parametre
        et arrete les moteurs.
        """
        GPIO.output(12, GPIO.LOW)
        GPIO.output(18, GPIO.LOW)
        GPIO.output(11, GPIO.LOW)
        GPIO.output(16, GPIO.LOW)
        self.pwm.set_pwm(Robot.ROUE, 0, 0)
        self.pwm.set_pwm(Robot.M1, 0, 0)
        self.pwm.set_pwm(Robot.M2, 0, 0)
        self.pwm.set_pwm(Robot.CAMERA_X, 0, 0)
        self.pwm.set_pwm(Robot.CAMERA_Y, 0, 0)



    def tourner(self, inclinaison, vitesse) :
        """Cette methode d'instance de la classe Robot tourne les roues du
        Robot et donne la vitesse.

        Prend en parametre :
        - int:inclinaison : le braquage des roues avant (compris entre 190
        et 270).
        - int:vitesse : la vitesse a adopter (comprise entre 1300 et 2300).
        """

        # On tourne selon le braquage demande (inclinaison)
        self.pwm.set_pwm(Robot.ROUE, 0, inclinaison)

        # On met a jour la vitesse pour les deux moteurs
        self.pwm.set_pwm(Robot.M1, 0, vitesse)
        self.pwm.set_pwm(Robot.M2, 0, vitesse)

        GPIO.output(12, GPIO.HIGH)
        GPIO.output(18, GPIO.HIGH)


    def tournerCamera(self, camera_x):
        """Cette methode tourne la camera dans une certaine position.

        Prend un parametre :
        - int:camera_x : la position que doit prendre la camera.
        """
        
        self.pwm.set_pwm(Robot.CAMERA_X, 0, camera_x)
