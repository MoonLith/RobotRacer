"""Module gerant les deplacements du Robot apres l'analyse d'image.

Il est constitue de la classe Robot qui est composee de methodes d'instance
effectuant des actions concretes sur le Robot (tourner les roues, avancer,
s'arreter, tourner la camera). Les instructions qui commandent le robot
se trouvent seulement dans ce module."""

###### IMPORT #########
import RPi.GPIO as GPIO
import Adafruit_PCA9685
#######################

class Robot :
    """La classe Robot contient les methodes d'instance qui deplacent le
    robot :
    - void:arret() : eteint les moteurs
    - void:tourner(int:inclinaison, int:vitesse) : tourne les roues selon
    l'entier specifie (inclinaison) et met a jour la vitesse des moteurs
    selon la vitesse specifiee (vitesse)
    - void:tournerCamera(int:camera_x) : place le servo X de la camera a la
    position specifiee (camera_x)"""

    # Constante M1 : activite du premier moteur (gauche?),
    # M2 : activite du deuxieme moteur (droite?).
    M1 = 4
    M2 = 5

    # Constante pour les roues
    ROUE = 0

    # Constantes pour les servos de la camera
    CAMERA_Y = 15
    CAMERA_X = 14

    def __init__(self, vitesse_choisie=1500, camera_direction=250) : #camera_hauteur
        """Constructeur d'un objet de la classe Robot avec une vitesse
        donnee, et une position de la camera donnee.

        Prend en parametre :
        - int:vitesse_choisie : la vitesse, doit etre comprise entre 1500 et
        2300. La vitesse par defaut est 1500.
        - int:camera_direction : le placement du servo X de la camera ; doit etre
        compris entre 180 et 320. Le placement par defaut est 250."""

        self.roues_droites=230
        # On configure la table GPIO
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        # On initialise les servos permettant le controle des roues
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(30)


        # On initialise les ports GPIO controlant les moteurs
        GPIO.setup(11, GPIO.OUT)
        GPIO.setup(12, GPIO.OUT) # moteur de gauche
        GPIO.setup(13, GPIO.OUT) # moteur de droite
        GPIO.setup(15, GPIO.OUT)

        # On configure l'activite des moteurs, pour la vitesse renseignee
        # lors de l'instanciation
        self.vitesse_choisie = vitesse_choisie
        self.pwm.set_pwm(Robot.M1, 0, self.vitesse_choisie)
        self.pwm.set_pwm(Robot.M2, 0, self.vitesse_choisie)

        # On configure le placement des roues avant au demarrage
        # (dans l'axe du robot)
        self.pwm.set_pwm(Robot.ROUE, 0, self.roues_droites)

        # On configure le placement de la camera dans l'axe, vers le bas
        self.pwm.set_pwm(Robot.CAMERA_X, 0, camera_direction)
        #self.pwm.set_pwm(Robot.CAMERA_Y, 0, camera_hauteur)


    def arret(self) :
        """Methode d'instance de la classe Robot qui ne prend aucun parametre
        et arrete les moteurs"""
        GPIO.output(11, GPIO.LOW)
        GPIO.output(13, GPIO.LOW)
        GPIO.output(12, GPIO.LOW)
        GPIO.output(15, GPIO.LOW)
        #self.set_pwm(Robot.ROUE, 0, 0)
        #self.set_pwm(Robot.M1, 0, 0)
        #self.set_pwm(Robot.M2, 0, 0)
        #self.set_pwm(Robot.CAMERA_X, 0, 0)
        #self.set_pwm(Robot.CAMERA_Y, 0, 0)



    def tourner(self, inclinaison, vitesse) :
        """Cette methode tourne les roues du Robot et change sa vitesse.

        Prend en parametre :
        - int:inclinaison : le braquage des roues avant (compris entre 190
        et 270)
        - int:vitesse : la vitesse a adopter (comprise entre 1300 et 2500)
        """

        # On tourne selon le braquage trouve (inclinaison)
        self.pwm.set_pwm(Robot.ROUE, 0, inclinaison)

        # On met a jour la vitesse pour les deux moteurs
        self.pwm.set_pwm(Robot.M1, 0, vitesse)
        self.pwm.set_pwm(Robot.M2, 0, vitesse)

        GPIO.output(12, GPIO.HIGH)
        GPIO.output(13, GPIO.HIGH)


    def tournerCamera(self, camera_x):
        """Cette methode tourne la camera a une certaine position.

        Prend un parametre :
        - int:camera_x : la position que doit prendre la camera
        """
        
        self.pwm.set_pwm(Robot.CAMERA_X, 0, camera_x)
