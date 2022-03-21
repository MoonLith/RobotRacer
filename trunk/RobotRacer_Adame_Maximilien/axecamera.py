"""Ce module contient les fonctions de base de controle du servo de la caméra"""
import time
import RPi.GPIO as GPIO
import Adafruit_PCA9685

class axecamera:
    def __init__(self):
        """ON INITIALISE LES VARIABLE POUR LES PORT PCA9685"""
        #Channel correspondant aux axes de rotations de la camera
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(30)

        #Channel correspondant aux axes de rotations de la camera
        self.AXE_Y = 15
        self.val_y1 = 90

        self.AXE_X = 14
        self.val_x1 = 250

        #--- Deplacement des axes modulables--#

    def high(self,val):
        """TOURNER LA CAMERA VERS LE HAUT :
            Cette fonction permet de tourner la caméra vers le haut
            à l'aide de la variable y étant l'ordonnée"""
        try :
            self.val_y1 = self.val_y1 + val
            self.pwm.set_pwm(self.AXE_Y, 0, self.val_y1)
            time.sleep(1)
        except:
            raise ValueError ("Erreur valeur")

    def low(self, val):
        """TOURNER LA CAMERA VERS LE BAS :
                Cette fonction permet de tourner la caméra vers le bas
                à l'aide de la variable y étant l'ordonnée"""
        try :
            self.val_y1 = self.val_y1 - val
            self.pwm.set_pwm(self.AXE_Y, 0, self.val_y1)
            time.sleep(1)

        except:
            raise ValueError("Erreur valeur")

    def left(self, val):
        """TOURNER LA CAMERA VERS LA GAUCHE :
                Cette fonction permet de tourner la caméra vers la gauche
                à l'aide de la variable x étant l'abscisse"""
        try :
            self.val_x1 = self.val_x1 + val
            self.pwm.set_pwm(self.AXE_X, 0, self.val_x1)
            time.sleep(1)
        except :

            raise ValueError("Erreur valeur")


    def right(self,val):
        """TOURNER LA CAMERA VERS LA DROITE :
                Cette fonction permet de tourner la caméra vers la droite
                à l'aide de la variable x étant l'abscisse"""
        try:
            self.val_x1 = self.val_x1 - val
            self.pwm.set_pwm(self.AXE_X, 0, self.val_x1)
            time.sleep(1)
        except:
            raise ValueError("Erreur valeur")