import unittest
import image
import cv2
import random
from  random import randint
class imagetest (unittest.TestCase):

    def setUp(self):
        path = "C:/Users/allou/Desktop/L3Q1/L3Q1projetwc/branches/John_machine_learning/image_type_file/image_type_left_v2/0.png"
        self.listred= [[20,50,51],[188,2,200],[0,230,233]]
        self.listnoir = [[30,30,30], [40,21,25],[1,1,1],[225,15,30]]
        self.red = 'red'
        self.noir = 'noir'
        self.blanc = 'blanc'
        self.image1 = cv2.imread(path)#"Frame correspondant à un fragrment du parcours"


        #image_no_form = image.color_treatment("Frame correspondant à un fragrment du parcours vide")
    def test_colorexisst(self):
        """Cette fonction permet de tester pour les différentes images
        si la camera perçoit bel et bien unn tableau de couleur"""
        self.assertIsNotNone(image.getBGRcolor(self.image1,
                                           self.image1.shape[1],self.image1.shape[0]))
        #...For all image in directory
    def test_dominientcolor(self):
        """Cette fonction permet de tester pour les différents tableaux de couleur
        si elle renvoit bel et bien le résultat demandé,
        si elle renvoit donc du rouge ou du noir"""
        element_red = [randint(0,150),randint(0,150),randint(151,255)]
        element_noir = [randint(0,40),randint(0,40),randint(0,40)]
        element_blanc = [randint(150,255),randint(150,255),randint(150,255)]

        self.assertEqual(image.dominentColor(element_red),self.red)
        self.assertEqual(image.dominentColor(element_noir),self.noir)
        self.assertEqual(image.dominentColor(element_blanc),self.blanc)
    def test_masque(self):
        """Cette fonction vient tester les capacités du triatement de couleur
        de color_treatment"""
        self.assertIsNotNone(image.color_treatment(self.image1))
    def test_extremPos(self):
        """Cette fonction vient tester find_extre_pos, on souhaite obtenir une valeur supérrieur
        ou égale à 0"""
        val =  (0,0),(0,0),(0,0),(0,0)
        self.assertGreaterEqual(image.find_extrem_pos(image.color_treatment(self.image1)),val)
    def test_contourcont(self):
        """Cette fonction vient verfier les capacités de la fonction contourcont
        on souhaite obtenir une valeur supérrieur à 0
        lorsque que la fonction traite une forme perçus
        """
        self.assertGreater(image.contourcont(image.color_treatment(self.image1)),0)


