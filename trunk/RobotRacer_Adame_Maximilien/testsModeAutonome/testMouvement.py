"""Module de test du module mouvement.py destine a tous les mouvements des
elements du Robot (camera, roues, moteurs).

Lancer ce programme et comparer ce qui s'affiche sur le terminal avec les
mouvements effectifs du Robot."""

# Import du repertoire parent et du module mouvement comprenant les fonctions
# a tester
import sys
sys.path.insert(0,'..')
from mouvement import *
import time
import unittest

class TestRobot :
    """Tests des deplacements du Robot : les moteurs (vitesse et arret), le
    braquage des roues avant, et les servos de la camera (x (rotation) et
    y (hauteur))"""

    def setUp(self) :
        """Initialisation des test en creant un objet de type Robot"""
        self.robot1 = Robot(1800)
        print("Le Robot a les roues et la camera dans son axe.")
        print("Si le Robot n'est pas place sur une grande surface, ARRETEZ \
            TOUT DE SUITE le test en tappant CTRL + C.")
        print()
        time.sleep(5)

    def testMoteurs(self, robot) :
        """Cette methode teste si le Robot peut avancer, s'arreter, et changer
        d'allure entre lent et rapide"""
        print("==================== TESTS MOTEURS ====================")
        time.sleep(3)
        print("Le Robot avance pendant 2 secondes.")
        robot.tourner(230, 1800)
        time.sleep(1)
        robot.arret()
        print()
        print("Le Robot s'arrete et reste immobile.")
        time.sleep(3)
        print()
        print("Le Robot accelere...")
        robot.tourner(230, 1300)
        time.sleep(1)
        robot.tourner(230, 1500)
        time.sleep(0.8)
        robot.tourner(230, 1700)
        time.sleep(0.6)
        robot.tourner(230, 1900)
        time.sleep(0.5)
        robot.tourner(230, 2000)
        time.sleep(0.3)
        robot.tourner(230, 2200)
        time.sleep(0.2)
        print("...et s'arrete.")
        robot.arret()
        print()
        print("=======================================================")
        print()
        print()
        time.sleep(5)

    def testRoues(self, robot) :
        """Cette methode teste si les roues peuvent aller a gauche et a droite a
        l'arret dans un premier temps, puis en avancant par la suite. Puis tourne
        lentement"""
        print("================== TESTS ROUES AVANT ==================")
        time.sleep(3)
        print("Les roues tournent a gauche.")
        robot.tourner(190, 1800)
        robot.arret()
        time.sleep(2)
        print()
        print("Les roues tournent a droite.")
        robot.tourner(270, 1800)
        robot.arret()
        time.sleep(2)
        print()
        print("Le Robot effectue un virage a gauche.")
        robot.tourner(200, 1500)
        time.sleep(2)
        robot.arret()
        print()
        print("Les roues tournent de gauche a droite.")
        braquage = 190
        while braquage < 270 :
            robot.tourner(braquage, 0)
            time.sleep(0.4)
            braquage += 10
        robot.arret()
        print()
        print("=======================================================")
        print()
        print()
        time.sleep(5)

    def testCamera(self, robot) :
        """Cette methode sert a verifier que les methodes de deplacement de la
        camera marchent effectivement, en la faisant tourner de la droite a la
        gauche lentement"""
        print("==================== TESTS  CAMERA ====================")
        time.sleep(3)
        print("La camera tourne de droite a gauche.")
        tournure = 200
        while tournure <= 300 :
            robot.tournerCamera(tournure)
            time.sleep(0.2)
            tournure += 8
        print()
        print("=======================================================")
        time.sleep(3)
        print()
        print()

    def testMain(self) :
        """Methode de la classe TestRobot a appeler pour effectuer tous les tests
        de la classe"""
        self.setUp()
        self.testMoteurs(self.robot1)
        self.testRoues(self.robot1)
        self.testCamera(self.robot1)
        print("Les tests sont termines.")


class TestConstructeur(unittest.TestCase) :
    """Tests du constructeur de l'objet, qui doit lancer les bonnes exceptions"""

    def testArguments(self) :
        # Test vitesse
        self.assertRaises(ValueError, Robot(3000))
        # Test camera
        self.assertRaises(ValueError, Robot(1800, 7))



test1 = TestRobot()
test1.testMain()

time.sleep(1)

unittest.main()

