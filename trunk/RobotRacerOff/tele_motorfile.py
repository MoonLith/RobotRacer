"""Ce module contient les fonctions de base de controle des moteurs, roues et servos du Robot"""

import time
import RPi.GPIO as GPIO
import Adafruit_PCA9685


class motor:

    def __init__(self):
        """ON INITIALISE LES VARIABLES POUR LES PORTS GPIO ET PCA9685"""

        # MOTEUR GAUCHE
        self.MOTOR_A1 = 11  # premiere sortie pour reculer
        self.MOTOR_A2 = 12  # deuxieme sortie pour avancer
        # MOTEUR DROITE
        self.MOTOR_B1 = 18  # premiere sortie pour avancer
        self.MOTOR_B2 = 16  # deuxieme sortie pour reculer
        
        # ROUES DIRECTIONNELLES
        self.ROUE = 0  # sortie des roues directionnelles

        # PORT PCA9685
        self.m1 = 4  # activité du premier moteur
        self.m2 = 5  # activité du deuxième moteur

        # Pulse avec modulation
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(30)

        self.MIN = 190  # 150 est la valeur minimal
        self.MAX = 270  # 600 est la valeur maximal
        self.MED = int((self.MIN + self.MAX)/2)

        # --PINS AU PORT GPIO
        self.pins = [self.MOTOR_A1, self.MOTOR_A2, self.MOTOR_B1, self.MOTOR_B2]

        # type de lecture sur le port
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)



    def set_speed(self, speed):
        """PARAMETRER LA VITESSE DU ROBOT :
        Cette fonction prend en en paramatre un entier
        compris entre 0 et 4096"""
        speed *= 40
        print("vitesse actuelle : ", speed)
        self.pwm.set_pwm(self.m1, 0, speed)
        self.pwm.set_pwm(self.m2, 0, speed)



    def forward(self, x):
        """FAIRE AVANCER LE ROBOT :
        Cette fonction prend en parametre
        un entier indiquant le temps pendant lequel le Robot avance en secondes"""

        GPIO.output(self.MOTOR_A1, GPIO.LOW)  # on coupe le GPIO permettant de reculer
        GPIO.output(self.MOTOR_A2, GPIO.HIGH)  # on active celui qui permet d'avancer

        GPIO.output(self.MOTOR_B1, GPIO.HIGH)  # on active celui qui permet d'avancer
        GPIO.output(self.MOTOR_B2, GPIO.LOW)  # on coupe le GPIO permettant de reculer
        time.sleep(x)
        print("sens direct")


    def backward(self, x):
        """FAIRE RECULER LE ROBOT :
        Cette fonction prend un parametre
        un entier indiquant le temps pendant lequel le Robot recule"""
        GPIO.output(self.MOTOR_A1, GPIO.HIGH)
        GPIO.output(self.MOTOR_A2, GPIO.LOW)

        GPIO.output(self.MOTOR_B1, GPIO.LOW)
        GPIO.output(self.MOTOR_B2, GPIO.HIGH)
        time.sleep(x)
        print("sens inverse")


    def stop(self):
        """ARRET MOTEUR :
        Cette fonction couper tous les moteurs ainsi que leurs ports
        ce qui permet au robot de s'arrêter"""
        for pin in self.pins:
            GPIO.setup(pin, False)
        self.pwm.set_all_pwm(0, 0)


    def start(self):
        """ACTIVER LE ROBOT :
        Cette fonction permet d'enclencher tous les ports du GPIO,
        ce qui permet au servo et aux moteurs de recevoir des intructions"""
        for pin in self.pins:
            GPIO.setup(pin, GPIO.OUT)
        self.pwm.set_pwm_freq(30)


    def left(self):
        """Tourner les roues à gauche
        cette fonction permet de tourner les
        roues a gauche grace a la variable MIN"""
        self.pwm.set_pwm(self.ROUE, 0, self.MIN)  # MIN < MED
        time.sleep(1)


    def right(self):
        """Tourner les roues à droite
        cette fonction permet de tourner les
        roues à droite grace la variable MAX"""
        self.pwm.set_pwm(self.ROUE, 0, self.MAX)  # MAX > MED
        time.sleep(1)

    def centre(self):
        """Replacer les roues au centre
        cette fonction permet de replacer les
        roues au centre grace la variable MED"""
        self.pwm.set_pwm(self.ROUE, 0, self.MED)
        time.sleep(1)
