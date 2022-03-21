"""Module gerant les deplacements du Robot apres l'analyse d'image"""

###### IMPORT #########
import RPi.GPIO as GPIO
import Adafruit_PCA9685
#######################

class Robot :
    """La classe Robot contient les methodes d'instance qui deplacent le
    robot :
    - arret() : eteint les moteurs.
    - tourner(int) : effectue des calculs et tourne les roues selon l'entier
    specifie."""

    # Constante M1 : activite du premier moteur,
    # M2 : activite du deuxieme moteur.
    M1 = 4
    M2 = 5

    # Constante pour les roues
    ROUE = 0


    def __init__(self, vitesse=1500) :
        """Constructeur d'un objet de la classe Robot avec une vitesse
        donnee.

        Prend un parametre :
        - vitesse : la vitesse, doit etre comprise entre 1500 et 2300.
        La vitesse par defaut est 1500."""

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
        self.vitesse = vitesse
        self.pwm.set_pwm(Robot.M1, 0, self.vitesse)
        self.pwm.set_pwm(Robot.M2, 0, self.vitesse)

        # On definie les bornes des valeurs a envoyer a set_pwm pour tourner
        # les roues
        self.roues_a_droite_max = 270
        self.roues_a_gauche_max = 190
        self.roues_droites = int((self.roues_a_droite_max+self.roues_a_gauche_max)/2)

        # On definie des valeurs significatives qui sont les bornes du domaine
        # que prennent les valeurs de centre_x
        self.borne_droite = 140
        self.borne_droit_max = 120
        self.borne_droit_min = 40
        self.borne_gauche = 20

        # On configure le placement des roues avant au demarrage
        # (dans l'axe du robot)
        self.pwm.set_pwm(Robot.ROUE, 0, self.roues_droites)




    def arret(self) :
        """Methode d'instance de la classe Robot qui ne prend aucun parametre
        et arrete les moteurs"""
        GPIO.output(11, GPIO.LOW)
        GPIO.output(13, GPIO.LOW)
        GPIO.output(12, GPIO.LOW)
        GPIO.output(15, GPIO.LOW)




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
                # Virage serre a droite

                GPIO.output(12, GPIO.HIGH)
                GPIO.output(13, GPIO.HIGH)
                #print(">= ", self.borne_droite)
                self.pwm.set_pwm(Robot.ROUE, 0, self.roues_a_droite_max)
            else :
                # Virage leger a droite

                GPIO.output(12, GPIO.HIGH)
                GPIO.output(13, GPIO.HIGH)
                #print(self.borne_droit_min, "< <", self.borne_droit_max)

                # Taille de l'intervalle dans lequel les roues doivent tourner
                # a droite proportionnellement a centre_x
                taille_interv_roues = self.roues_a_droite_max-self.roues_droites
                # Taille de l'intervalle des valeurs de centre_x, pour lequel
                # on doit tourner a droite proportionnellement
                taille_interv_centre_x = self.borne_droite - self.borne_droit_max
                # Braquage des roues adapte
                inclinaison = int((taille_interv_roues)*(((self.borne_droite)-centre_x)/(taille_interv_centre_x))+self.roues_droites)
                print("inc = ", inclinaison, "inter_roues = ", taille_interv_roues)

                # On tourne selon le braquage trouve
                self.pwm.set_pwm(Robot.ROUE, 0, inclinaison)

        # Virage a gauche
        elif (centre_x < self.borne_droit_min) :
            if (centre_x <= self.borne_gauche) :
                # Virage serre a gauche

                GPIO.output(12, GPIO.HIGH)
                GPIO.output(13, GPIO.HIGH)
                #print("<", self.borne_gauche)
                self.pwm.set_pwm(Robot.ROUE, 0, self.roues_a_gauche_max)
            else :
                # Virage leger a gauche
                GPIO.output(12, GPIO.HIGH)
                GPIO.output(13, GPIO.HIGH)
                #print(self.borne_gauche, "< <", self.borne_droit_min)

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

        # Roues dans l'axe (aller tout droit)
        elif (centre_x <= self.borne_droit_max) and (centre_x >= self.borne_droit_min) :
            GPIO.output(12, GPIO.HIGH)
            GPIO.output(13, GPIO.HIGH)
            #print("Tout droit")
            self.pwm.set_pwm(Robot.ROUE, 0, self.roues_droites)
