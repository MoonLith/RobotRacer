import unittest
from RobotMoveSet import *
import RPi.GPIO as GPIO
import Adafruit_PCA9685

import RobotMoveSet
class MyvirageTest(unittest.TestCase):
    def setUp(self):
        """Fonction d'initialisation"""
        M1 = 4
        M2 = 5
        ROUE = 0
        gauche = 150
        droite = 260
        pwm = Adafruit_PCA9685.PCA9685()
        pwm.set_pwm_freq(30)
       #-------- PORT INIT---------
        GPIO.setup(11, GPIO.OUT)
        GPIO.setup(12, GPIO.OUT)
        GPIO.setup(18, GPIO.OUT)
        GPIO.setup(16, GPIO.OUT)
    def check_forward(self):
        """Ce test permet de verfier que les ports
        GPIO 12 et 18, ports allants dans le sens anti horraire
         repondes correcetements aux instructions"""
        forward(0)
        self.assertEqual(GPIO.input(12), 0)
        self.assertEqual(GPIO.input(18), 0)
        time.sleep(2)
        forward(1)
        self.assertEqual(GPIO.input(12), 1)
        self.assertEqual(GPIO.input(18), 1)
        time.sleep(2)
    def check_backward(self):
        """Ce test permet de verfier que les ports
            GPIO 11 et 16, ports allants dans le sens horraire
             repondes correcetements aux instructions"""
        backward(0)
        self.assertEqual(GPIO.input(11), 0)
        self.assertEqual(GPIO.input(16), 0)
        time.sleep(2)
        backward(1)
        self.assertEqual(GPIO.input(11), 1)
        self.assertEqual(GPIO.input(16), 1)
        time.sleep(2)
    def test_viragegauche(self):
        """Dans ce test, on utilise le temps comme gage de sureté,
        en effet l'execution complète de la manoouvre virage gauche prends plus d'une demi
        """
        start = time.time()
        virage_gauche()
        end = time.time()
        self.assertGreater(end-start,0.5)
    def test_viragedroite(self):
        """Dans ce test, on utilise le temps comme gage de sureté,
        en effet l'execution complète de la manoouvre virage gauche prends plus d'une demi
        """
        start = time.time()
        virage_droite()
        end = time.time()
        self.assertGreater(end - start, 0.5)

    def mainfonction(self):

        self.test_viragedroite()
        self.test_viragegauche()
        virage_droite()
        tourner_gauche(3)
        tourner_droite(3)

MyvirageTest.mainfonction()

