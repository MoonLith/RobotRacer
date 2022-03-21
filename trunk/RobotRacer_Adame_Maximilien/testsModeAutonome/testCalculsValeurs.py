""" Ce module permet de tester de tester les differents fonctions consituant
le module calculs_valeurs, notamment la fonction qui trouve la position de la
en tenant compte du placement de la camera, celle qui donne le placement a
prendre pour la camera, et celle qui donne les valeurs de braquage et vitesse
du Robot.
"""

# Import du reperoire parent, du module calculs_valeurs comprenant les
# fonctions a tester et de unittest
import sys
sys.path.insert(0,'..')
import calculs_valeurs
import unittest


class TestPositionX(unittest.TestCase) :
    """Tests de la premiere fonctionnalite attribuee au module calculs_valeurs,
    la position de l'abscisse du centre de la forme observee par la camera dans
    l'environnement du Robot"""
       
    def testDeLaPosition(self) :
        """Cette methode teste si les positions des centres de formes ont les
        bonnes valeurs pour certaines positions de camera precises comme la
        camera droite"""

        # La camera en face (250) n'a aucun incident sur la valeur de position_x
        self.assertEqual(calculs_valeurs.centrexCamera(96, 250), 96)
        self.assertEqual(calculs_valeurs.centrexCamera(120, 250), 120)

        # Le deplacement de la camera a un incident sur position_x
        self.assertNotEqual(calculs_valeurs.centrexCamera(96, 251), 96)

        # On teste si lorsque la camera est tournee, un centre sur la photo
        # plus a gauche, renvoie bien une position plus a gauche
        self.assertLessEqual(calculs_valeurs.centrexCamera(40, 240), calculs_valeurs.centrexCamera(80, 240))
        self.assertLessEqual(calculs_valeurs.centrexCamera(40, 270), calculs_valeurs.centrexCamera(100, 270))


    def testRelations(self) :
        """Cette methode verifie si les positions des formes par rapport au
        Robot sont coherentes entre elles lorsque la camera n'a pas la meme
        position"""

        # On teste si pour deux positions trouvees au centre de la photo
        # (seulement pour la premiere instruction),
        # l'une prise la camera tournee vers la gauche, et l'autre prise la
        # camera tournee vers la droite, le retour de la premiere doit etre
        # inferieur au retour de la seconde
        self.assertLessEqual(calculs_valeurs.centrexCamera(96, 255), calculs_valeurs.centrexCamera(96, 233))
        self.assertLessEqual(calculs_valeurs.centrexCamera(47, 255), calculs_valeurs.centrexCamera(47, 233))
        self.assertLessEqual(calculs_valeurs.centrexCamera(169, 255), calculs_valeurs.centrexCamera(169, 243))

        # Deux cameras tournees a gauche mais sur le premier la forme est
        # plus a gauche de la photos
        self.assertLess(calculs_valeurs.centrexCamera(30, 270), calculs_valeurs.centrexCamera(50, 255))
        
        # On teste si la camera tourne beaucoup si ca ne fausse les resultats
        self.assertLessEqual(calculs_valeurs.centrexCamera(50, 290), calculs_valeurs.centrexCamera(30, 270))





class TestValPourCamera(unittest.TestCase) :
    """Tests des valeurs necessaires au positionnement de la camera par rapport
    a la position du centre de la forme observee"""

    def testValPourCamera(self) :
        """Cette methode verifie si les valeurs de placement de camera
        correspondent bien a la position du centre de la forme observee
        Rappel :
        >   Camera tourne a droite : <250
        >   Camera en face : 250
        >   Camera tourne a gauche : >250"""

        # Est ce que position_x en face (96) renvoie camera en face
        self.assertEqual(calculs_valeurs.valPourCamera(96), 250)

        # Plusieurs tests si plus position_x est grand, plus la position de la
        # camera adaptee retournee est petite (vers la droite)
        self.assertGreaterEqual(calculs_valeurs.valPourCamera(120), calculs_valeurs.valPourCamera(121))
        self.assertGreaterEqual(calculs_valeurs.valPourCamera(-12), calculs_valeurs.valPourCamera(0))
        self.assertGreaterEqual(calculs_valeurs.valPourCamera(-1), calculs_valeurs.valPourCamera(130))
        self.assertGreaterEqual(calculs_valeurs.valPourCamera(50), calculs_valeurs.valPourCamera(51))
        self.assertGreaterEqual(calculs_valeurs.valPourCamera(80), calculs_valeurs.valPourCamera(200))





class TestValPourMouvement(unittest.TestCase) :
    """Tests des valeurs necessaires au deplacement du Robot, comme le braquage
    des roues avant et la vitesse"""

    def setUp(self) :
        self.viragelegergauchemax = range(190,230)
        self.viragelegerdroitemin = range(230,261)
        self.vitesse1 = 2000
        self.vitesse2 = 1300

    def testTypeDeVirage(self) :
        """Cette methode verifie si pour certaines valeurs arbitraires de
        position_x, le type de virage associe est coherent (negatif s'il faut
        tourner a gauche, positif s'il faut tourner a droite, 0 s'il faut aller
        tout droit
        Rappel type de virage :
        >   -2 : virage serre a gauche
        >   -1 : virage leger a gauche
        >   0 : pas de virage (aller tout droit)
        >   1 : virage leger a droite
        >   2 : virage serre a droite
        """

        # Tests pour des valeurs de position_x arbitraires, le virage renvoye
        # est bon
        self.assertEqual(calculs_valeurs.typeDeVirage(-10), -2)
        self.assertEqual(calculs_valeurs.typeDeVirage(0), -2)
        self.assertEqual(calculs_valeurs.typeDeVirage(12), -2)
        self.assertEqual(calculs_valeurs.typeDeVirage(50), -1)
        self.assertEqual(calculs_valeurs.typeDeVirage(62), -1)
        self.assertEqual(calculs_valeurs.typeDeVirage(90), 0)
        self.assertEqual(calculs_valeurs.typeDeVirage(96), 0)
        self.assertEqual(calculs_valeurs.typeDeVirage(100), 0)
        self.assertEqual(calculs_valeurs.typeDeVirage(120), 1)
        self.assertEqual(calculs_valeurs.typeDeVirage(127), 1)
        self.assertEqual(calculs_valeurs.typeDeVirage(180), 2)
        self.assertEqual(calculs_valeurs.typeDeVirage(192), 2)
        self.assertEqual(calculs_valeurs.typeDeVirage(230), 2)


    def testInclinaisonRoues(self) :
        """Cette methode verifie si le braquage des roues qui sera demande au
        robot respecte bien certaines conditions (inferieur a une position_x plus
        grande, pour chaque type de virage possible, et a l'interieur des virages
        legers)"""

        # Tests des virages serres ou de la direction rectiligne
        self.assertEqual(calculs_valeurs.inclinaisonRoues(-2, -200), 190)
        self.assertEqual(calculs_valeurs.inclinaisonRoues(0, 96), 230)
        self.assertEqual(calculs_valeurs.inclinaisonRoues(2, 200), 270)

        # Tests des virages legers
        self.assertIn(calculs_valeurs.inclinaisonRoues(-1, 40), self.viragelegergauchemax)
        self.assertIn(calculs_valeurs.inclinaisonRoues(1, 120), self.viragelegerdroitemin)


    def testVitesseMoteurs(self) :
        """Cette methode verifie si la vitesse est vaut bien une certaine valeur,
        et s'il y a bien un ralentissement dans un virage"""

        # Test ralentissement si virage
        self.assertLess(calculs_valeurs.vitesseMoteurs(-2, self.vitesse1), self.vitesse1)
        self.assertLess(calculs_valeurs.vitesseMoteurs(1, self.vitesse1), self.vitesse1)


        # Test vitesse jamais inferieure a 1300
        self.assertGreaterEqual(calculs_valeurs.vitesseMoteurs(2, self.vitesse2), 1300)


unittest.main()







