""" Ce module contient les différenes manoeuvres de déplacmeent du robot
Ces manoeuvres sont à effectuer en amond de l'algorithme par centre géométrique
Elles viennent répondre aux angles considéré commme brut.

Virage Gauche & Droite sont des manoeuvres de virage permettant au robot
d'abborder d'une meilleur façons les angles brutes

Tourner doite & gauches sont des virages permettant d'éxcuter un virage pendant un temps
défini

Forward et backward sont des maneouvres basique pour faire avancer et reculer le robot

man_gauche et man_droite sont les fonctions permettans de detecter les virages brutes
à droites et à gauches.

"""
#---IMPORT -------------
import RPi.GPIO as GPIO
import Adafruit_PCA9685
import time
#---------------------

#Constante
M1 = 4
M2 = 5

cam_x = 14
cam_y = 15

ROUE = 0
cam_gauche = 300
cam_droite = 235
gauche = 150
droite = 300
#--------

#---Init PWM
pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(30)
#---------
#INIT GPIO sur le RPI
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
LEFT_BACKW = GPIO.setup(11, GPIO.OUT)
LEFT_FORW = GPIO.setup(12, GPIO.OUT)
RIGHT_FORW = GPIO.setup(18, GPIO.OUT)
RIGHT_BACKW = GPIO.setup(16, GPIO.OUT)
#-------------------


def virage_gauche(temps,temps2):
    """Cette fonction permet d'entamer une manoeuvre de virage à droite"""
    #etape 1
    forward(GPIO.HIGH)
    time.sleep(1) #On dépasse volontairement la piste

    GPIO.output(12,0)#coupeer le moteur
    pwm.set_pwm(0,0,gauche)# on tourne les roues a gauche
    pwm.set_pwm(M1,0,4000)#vitesse
    pwm.set_pwm(M2,0, 0)
    
    GPIO.output(18, GPIO.HIGH)#Manoeuvre de dérapage
    GPIO.output(11, GPIO.HIGH)
    time.sleep(temps)

    pwm.set_pwm(0,0,droite)#On remet une vitesse stable
    set_speed(1300)

    backward(GPIO.LOW)#on coupe les moteurs d'arret
    forward(GPIO.HIGH)#Forward
    time.sleep(temps2)


def virage_droite(temps, temps2):
    """Cette fonction permet d'entermaner une manoeuvre de virage à droite"""
    GPIO.output(18, GPIO.HIGH)  # Forward
    GPIO.output(12, GPIO.HIGH)
    time.sleep(1)

    #on coupe l'un des moteurs et on paramètre la vitesse
    GPIO.output(18, 0)
    pwm.set_pwm(0, 0, gauche)
    pwm.set_pwm(M1, 0, 4000)
    pwm.set_pwm(M2, 0, 4000)

    GPIO.output(12, GPIO.HIGH)#dérapage
    GPIO.output(16, GPIO.HIGH)
    time.sleep(temps)

    pwm.set_pwm(0, 0, droite)# on met les roues à droites
    set_speed(1300)

    backward(GPIO.LOW)
    forward(GPIO.HIGH)
    time.sleep(temps2)

def set_speed(speed):
    """Cette fonction paramètre la vitesse,
    elle vient agir uniquement dans ce module afin d'apporter une meilleur
    comprehension"""
    pwm.set_pwm(M1, 0, speed)  # vitesse
    pwm.set_pwm(M2, 0, speed)  # vitesse

def tourner_droite(temps):
    """Cette methode permet au robot de tourner à droite"""
    set_speed(2200)
    pwm.set_pwm(ROUE,0,droite)
    forward(GPIO.HIGH)
    time.sleep(temps)

def tourner_gauche(temps):
    """ cette fonction permet au robot de tourner à gauche pendant un temps impartit"""
    set_speed(2200)
    pwm.set_pwm(ROUE,0,gauche)
    forward(GPIO.HIGH)
    time.sleep(temps)

def forward(set):
    """cette fonction permet de paramétrer les moteurs avant du robot"""
    GPIO.output(18,set)
    GPIO.output(12,set)

def backward(set):
    """Cette fonction permet de paramétrer les moteurs arrière du robot"""
    GPIO.output(16,set)
    GPIO.output(11,set)

def man_droite(coord_right_x,coord_right_y,coord_top_x,coord_top_y,width,height) :
    """

    :param coord_right_x: l'abscisse du point le plus à droite de la forme
    :param coord_right_y: l'ordonnée du point le plus à droite de la forme
    :param coord_top_x: l'abscisse du point le plus à droite de la forme
    :param width: la longeur de frame
    :param height: la hauteeur de la frame

    Cette fonction permet de determiner via ses différentes conditions s'il y a un angle brute présent sur
    la frame;
    Dans la mesure où les conditions sont vérifés, le robot exectureas des suites d'instructions lui
    permettant d'aborder des angles côté droit
    qui lui seraient physiquement impossible par son rayon de braquage limité.

    """
    print("coord max right")
    print(coord_right_x, coord_right_y)
    print("top y", coord_top_y)
    print("top x", coord_top_x)
    if coord_right_x > int(width * 60 / 100) and coord_right_y > int(height* 50/100) and coord_top_y > int(height* 20/100):
        pwm.set_pwm(cam_x, 0, cam_droite)  # vitesse

        tourner_droite(1.4)

        print("VIRAGE DROITE TYPE 1")

    else :
        pass
def man_gauche(coord_left_x,coord_left_y,coord_top_x,coord_top_y,width,height):
    """

    :param coord_left_x: l'abscisse du point le plus à gauche de la forme
    :param coord_left_y: l'ordonnée du point le plus à gauche de la forme
    :param coord_top_x: l'abscisse du point le plus en haut de la forme
    :param coord_top_y: l'ordonnée du point le plus en haut de la forme
    :param width:  la longeur de frame
    :param height: la hauteeur de la frame

    Cette fonction permet de determiner via ses différentes conditions s'il y a un angle brute présent sur
    la frame;
    Dans la mesure où les conditions sont vérifés, le robot exectureas des suites d'instructions lui
    permettant d'aborder des angles côté gauche
    qui lui seraient physiquement impossible par son rayon de braquage limité.
    """
    print("coord max left")
    print(coord_left_x, coord_left_y)
    print("top y",coord_top_y)

    if coord_left_x < int(width * 15 / 100) and coord_left_y > int(height * 50/ 100)  \
            and coord_top_x < int(width * 15 / 100) and coord_top_y > int(height *20/100):
        print("VIRAGE GAUCHE")
        tourner_gauche(1.4)

    else :
        pass
