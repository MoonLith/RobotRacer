""" Ce module permet de tester de tester les fonctions de traitement
et d'analyse d'images du Robot, contenues dans le module image.py.
"""

import sys
sys.path.insert(0,'..')
import image
import unittest
import cv2


class TestCentroidDetector(unittest.TestCase) :
    """Classe de test du traitement et d'analyse d'image du mode autonome du
    Robot contenant deux methodes, appelees une fois que les images situees
    dans le repertoire 'images' sont recuperees par la methode setUp().

    On distingue deux tests :
    - testExistenceDeCircuit() : teste si la photo contient du ruban adhesif
    que le Robot va suivre.
    - testAbscisseDeForme() : teste l'abscisse du centre de forme trouve.
    """

    def setUp(self) :
        """Initialisation des tests avec des images contenues dans le repertoire
        'images' et prises a l'avance.
        """

        ################## Imports des images sans circuit #####################
        self.image_sans_ruban01 = cv2.imread("images/frame01.jpg")
        self.image_sans_ruban02 = cv2.imread("images/frame02.jpg")
        self.image_sans_ruban03 = cv2.imread("images/frame03.jpg")
        ########################################################################


        ################## Imports des images avec circuit #####################
        self.image_avec_ruban11 = cv2.imread("images/frame11.jpg")
        self.image_avec_ruban12 = cv2.imread("images/frame12.jpg")
        self.image_avec_ruban13 = cv2.imread("images/frame13.jpg")
        self.image_avec_ruban14 = cv2.imread("images/frame14.jpg")
        self.image_avec_ruban14 = cv2.imread("images/frame14.jpg")
        self.image_avec_ruban15 = cv2.imread("images/frame15.jpg")
        self.image_avec_ruban16 = cv2.imread("images/frame16.jpg")
        self.image_avec_ruban17 = cv2.imread("images/frame17.jpg")
        self.image_avec_ruban18 = cv2.imread("images/frame18.jpg")
        self.image_avec_ruban19 = cv2.imread("images/frame19.jpg")
        ########################################################################


    def testExistenceDeCircuit(self) :
        """Dans cette methode, on teste pour differentes images si le programme
        renverra l'existence d'un chemin a suivre pour le Robot.
        """

        #################### Test des images sans circuit ######################
        self.assertFalse(image.centroidDetector(self.image_sans_ruban01))
        self.assertFalse(image.centroidDetector(self.image_sans_ruban02))
        self.assertFalse(image.centroidDetector(self.image_sans_ruban03))
        ########################################################################

        ################### Test des images avec circuit #######################
        self.assertIsNot(image.centroidDetector(self.image_avec_ruban11), False)
        self.assertIsNot(image.centroidDetector(self.image_avec_ruban12), False)
        self.assertIsNot(image.centroidDetector(self.image_avec_ruban13), False)
        self.assertIsNot(image.centroidDetector(self.image_avec_ruban14), False)
        self.assertIsNot(image.centroidDetector(self.image_avec_ruban15), False)
        self.assertIsNot(image.centroidDetector(self.image_avec_ruban16), False)
        self.assertIsNot(image.centroidDetector(self.image_avec_ruban17), False)
        self.assertIsNot(image.centroidDetector(self.image_avec_ruban18), False)
        self.assertIsNot(image.centroidDetector(self.image_avec_ruban19), False)
        ########################################################################


    def testAbscisseDeForme(self) :
        """Dans cette methode, on teste la valeur renvoyee par l'analyse d'image,
        qui est l'abscisse du centre de la forme principale observee sur l'image.

        On choisit de tester la valeur retournee par centroidDetector avec une
        marge de 15px. Le but est de tester la direction donnee par centroidDetector
        et non l'egalite exacte a un pixel pres.
        """

        #############=== Trajectoire rectiligne ===#############
        self.assertAlmostEqual(image.centroidDetector(self.image_avec_ruban11),96, delta=15)
        self.assertAlmostEqual(image.centroidDetector(self.image_avec_ruban12),96, delta=15)

        #############=== Virage a droite ===#############
        self.assertAlmostEqual(image.centroidDetector(self.image_avec_ruban13),105, delta=15)
        self.assertAlmostEqual(image.centroidDetector(self.image_avec_ruban16),105, delta=15)
        self.assertAlmostEqual(image.centroidDetector(self.image_avec_ruban17),115, delta=15)
        self.assertAlmostEqual(image.centroidDetector(self.image_avec_ruban18),135, delta=15)
        self.assertAlmostEqual(image.centroidDetector(self.image_avec_ruban19),105, delta=15)

        #############=== Virage a gauche ===#############
        self.assertAlmostEqual(image.centroidDetector(self.image_avec_ruban14),70, delta=15)
        self.assertAlmostEqual(image.centroidDetector(self.image_avec_ruban15),90, delta=15)


unittest.main()
