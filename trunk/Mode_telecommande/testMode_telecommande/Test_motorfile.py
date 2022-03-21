"""Ce module permet de tester
les differents fonctions consituant le module motorfile.py destine au mouvement motrice du Robot (roues, moteurs)
visible sur l'interface graphique.
"""
import unittest
from motorfile import *
import RPi.GPIO as GPIO
import Adafruit_PCA9685

class TestMotor(unittest.TestCase):

    def setUp(self):
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

        self.pins = [self.MOTOR_A1, self.MOTOR_A2, self.MOTOR_B1, self.MOTOR_B2]

    def test_start(self):
        self.assertEqual(GPIO.setup(self.pins,GPIO.OUT))
        self.assertEqual(self.pwm.set_pwm_freq(30))

    def test_speed(self):
        motor.set_speed(0)
        self.assertEqual(self.pwm.set_pwm(self.m1, 0, 0))
        motor.set_speed(1)
        self.assertEqual(self.pwm.set_pwm(self.m1, 0, 1))

    def test_forward(self):
        motor.forward(GPIO.LOW)
        self.assertEqual(self.MOTOR_A2, GPIO.LOW)
        self.assertEqual(self.MOTOR_B1, GPIO.LOW)
        time.sleep(4)
        motor.forward(GPIO.HIGH)
        self.assertEqual(self.MOTOR_A2, GPIO.HIGH)
        self.assertEqual(self.MOTOR_B1, GPIO.HIGH)
        time.sleep(4)

    def test_backward(self):
        motor.backward(GPIO.LOW)
        self.assertEqual(self.MOTOR_A1, GPIO.LOW)
        self.assertEqual(self.MOTOR_B2, GPIO.LOW)
        time.sleep(4)
        motor.backward(GPIO.HIGH)
        self.assertEqual(self.MOTOR_A1, GPIO.HIGH)
        self.assertEqual(self.MOTOR_B2, GPIO.HIGH)
        time.sleep(4)


if __name__ == '__main__':
    unittest.main()
