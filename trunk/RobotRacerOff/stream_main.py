"""Module principal du mode autonome du Robot Racer"""

###### IMPORT #########
import cv2
import image
from beta_RobotBeta import Robot
from beta_RobotMoveSet import *
import urllib
import urllib.request
import numpy as np
from stream_thread import InitRobotStream
#######################

print("====================================================================")
print("-------------------- MODE AUTONOME BETA --------------------")
print("====================================================================\n")

vitesse_noir = 1350
vitesse_rouge = 1500
robotstream = InitRobotStream()
robotstream.start()
try :
    vitesse_noir = int(vitesse_noir)
    vitesse_rouge = int(vitesse_rouge)

except ValueError as error:
    print("Erreur lors de la conversion error type : {}".format(error))

print("Pour quitter, taper CTRL + C")
#-------MAIN INIT--------------
# L'objet robot va permettre de se deplacer et de s'arreter
robot = Robot(vitesse_noir)

# On configure le flux de la camera et la resolution a 192x108
camera = cv2.VideoCapture(0)
ret = camera.set(3,192)
ret = camera.set(4,108)
width = camera.get(3)
height = camera.get(4)

#----------------

#GESTION DES ETAPES POUR LA BOUCLE INFINI----------


def speed_on_tape(dominent_color):
    """Cette fonction représente l'étape
    où le robot va adapter sa vitesse
    en fonction de la couleur qu'il aura repérré sur le parcours"""
    red = 'red'
    noir = 'noir'
    jaune = 'jaune'
    blanc = 'blanc'
    if dominent_color == red:
        robot.set_speed(vitesse_rouge)
        print("La couleur est rouge, vitesse paramétré à 2300")
    elif dominent_color == noir:
        robot.set_speed(vitesse_noir)
        print("La couleur est noir, vitesse paramétré à 1300")
    elif dominent_color == jaune:
        robot.set_speed(2000)
        print("La couleur est jaune, vitesse paramétré à 2000")
    elif dominent_color == blanc:
        print("La couleur est blanche")

    # En continu

def point_step(nb_contour):
    """Cette fonction représente l'étape où le robot
    se sert des points déterminant qu'il aurait repérré
    sur le parcours pour réaliser ses différentes manoeuvres"""

    max_left, max_right, max_top, max_bottom = image.find_extrem_pos(masque)
    print("ok2")
    if nb_contour == 6 or nb_contour == 7 or nb_contour == 8   :  # Correspondance angle brute

        coord_left_x, coord_left_y = max_left
        coord_right_x, coord_right_y, = max_right
        coord_top_x, coord_top_y = max_top
        coord_bottom_x, coord_bottom_y, = max_bottom
        ("ok3")

        man_droite(int(coord_right_x), int(coord_right_y),
                   int(coord_top_x),int(coord_top_y), width, height)  # appelle de fonction

        man_gauche(int(coord_left_x), int(coord_left_y),
                   int(coord_top_x), int(coord_top_y), width, height)
        print("max left",max_left)
        print("max top",max_top)
#-----------------------------------------------


stream = urllib.request.urlopen('http://localhost:8080/frame.mjpg')
bytes = ''
while True:
     
    try:

        bytes += stream.read(1024)
        a = bytes.find('\xff\xd8')
        b = bytes.find('\xff\xd9')
        if a != -1 and b != -1:
            jpg = bytes[a:b + 2]
            bytes = bytes[b + 2:]
            frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

        # On lit une frame depuis la caméra
        _, frame = camera.read()

#-------ETAPE SPEED ON TAPE----------------#

        moy_color = image.getBGRcolor(frame,width,height)#on fait la moyenne des couleurs
        dominent_color = image.dominentColor(moy_color)#on recupère  la couleur dominante

        speed_on_tape(dominent_color) # paramétrage de la vitesse sur le parcours

        masque = image.colortreatment(frame) #on traite l'image pour obtenir l'image filtré
        print("ok")
#-----------------------------------------#


#--------ETAPE EXTREM POS----------------#
        try:
            nb_contour = image.contourcont(masque)
            point_step(nb_contour)
        except ValueError as error :
            print("Erreur à l'étape extram pos \n Erreur : [} ".format(error))
        finally:
            pass
#-----------------------------------------#


#-----------ETAPE CENTROID DETECTOR ROBOT BETA----------------
        pos_centre = image.centroidDetector(masque)
        centre_x = pos_centre[0]#coordonnée X
        centre_y = pos_centre[1]#coordonénée Y
        print("etape centroid")

        # Si on observe bien un centre de forme
        if centre_x is not False :
            print("centre_x = {}".format(centre_x))
            robot.tourner(centre_x)
        else :
            print ("Pas de centre de forme")
#------------------------------------------#

#------GESTION D EXCEPTION--------------------
    except KeyboardInterrupt:
        # Et on arrete les moteurs
        robot.turnoff()
        print("arret sur commande")
        break
    except :
        robot.turnoff()
        print("Erreur rencontré")

#---------------------------------------------

robot.turnoff()
robotstream.join()