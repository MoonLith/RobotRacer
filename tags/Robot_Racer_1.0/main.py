"""Programme principal du Robot Racer"""

###### IMPORT #########
import RPi.GPIO as GPIO
import time
import cv2
import Adafruit_PCA9685
import numpy as np
import arret
#######################

print("====================================================================")
print("-------------------- LANCEMENT DU MODE AUTONOME --------------------")
print("==================================================================== \n")

print("Veuillez rentrer une vitesse : (comprise entre 1300 & 2500)")
vitesse = input()
vitesse = int(vitesse)


camera = cv2.VideoCapture(0) #On ouvre le flux de la camera
ret = camera.set(3,192); # On configure la resolution a 192x108
ret = camera.set(4,108);
GPIO.setmode(GPIO.BOARD) #On configure la table GPIO
GPIO.setwarnings(False)

pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(30)
ROUE=0

m1 = 4
m2 = 5
GPIO.setup(11, GPIO.OUT) #On initialise les ports GPIO controlant les moteurs
GPIO.setup(12, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
pwm.set_pwm(m1, 0, vitesse) #On configure l'activite des moteurs, le troisieme parametre est la vitesse
pwm.set_pwm(m2, 0, vitesse)

while True:
    try:
        _, image = camera.read() #On lit une frame
    	key = cv2.waitKey(1) & 0xFF #On recupere les frappes du clavier

        # Les prochaines lignes permettent de travailler l'image pour la rendre plus facilement analysable

    	gris = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # On transforme en nuance de gris
    	flou = cv2.GaussianBlur(gris,(5,5),0) # On floute
    	ret,binaire = cv2.threshold(flou,100,255,cv2.THRESH_BINARY_INV) #On transforme en image binaire
    	masque = cv2.erode(binaire, None, iterations=2) # On élimine les bruits
    	masque = cv2.dilate(masque, None, iterations=2)


    	something, contours, hierarchy = cv2.findContours(masque.copy(),1,cv2.CHAIN_APPROX_NONE) # On cherche les contours dans l'image


    	if len(contours) > 0: # Si on detecte une forme

    		c = max(contours, key = cv2.contourArea) # On recupere le plus grand contour
    		M = cv2.moments(c) # On applique la fonction moments de openCV pour chercher le centre de la forme


    		centre_x = int(M['m10']/M['m00']) #On cherche l'abscisse du centre

    		print("centre_x = ", centre_x)

    		if centre_x >= 140: # Virage serre a droite
    			GPIO.output(13, GPIO.HIGH) #On actionne les moteurs
    			GPIO.output(12, GPIO.HIGH)
    			print("     >= 140")
    			pwm.set_pwm(ROUE, 0, 270) #On tourne a droite

    		if centre_x < 140 and centre_x > 120 : # Virage a droite
    			GPIO.output(12, GPIO.HIGH)
    			GPIO.output(13, GPIO.HIGH)
    			print("     120< <140")
    			inclinaison = int(40*((140-centre_x)//20) + 230) # On cherche le braquage des roues adapte
    			print("inc = ", inclinaison)
    			pwm.set_pwm(ROUE, 0, inclinaison) # On tourne selon le braquage trouve

    		if centre_x <=120 and centre_x >= 40: # Tout Droit
    			GPIO.output(12, GPIO.HIGH)
    			GPIO.output(13, GPIO.HIGH)
    			print("     Tout droit")
    			pwm.set_pwm(ROUE, 0, 230)

    		if centre_x < 40 and centre_x > 20: # Virage a gauche
    			GPIO.output(12, GPIO.HIGH)
    			GPIO.output(13, GPIO.HIGH)
    			print("     20< <40")
    			inclinaison = int(40*((40-centre_x)//20) + 180)# Meme methode que pour le virage a droite
    			print("inc = ", inclinaison)
    			pwm.set_pwm(ROUE, 0, inclinaison)

    		if centre_x <= 20: # Virage serre a gauche
    			GPIO.output(13, GPIO.HIGH)
    			GPIO.output(12, GPIO.HIGH)
    			print("<20")
    			pwm.set_pwm(ROUE, 0, 190) # Meme methode que pour le virage serre a droite



    	if key == ord("q"): # si on frappe la touche q la boucle s'arrete
                break
    except Exception as e: #On arrete les moteurs en cas d'erreur
        arret.arret()



GPIO.output(11, GPIO.LOW) # On met les sorties de moteurs à 0
GPIO.output(13, GPIO.LOW)
GPIO.output(12, GPIO.LOW)
GPIO.output(15, GPIO.LOW)

GPIO.cleanup() # On nettoie les sorties
