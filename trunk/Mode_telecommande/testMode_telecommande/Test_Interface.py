"""Ce module permet de tester
les differents fonctions consituant
le module Interface.py
"""
import unittest
from Interface import *

class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.app = window_menu

    def test_autonome(self):
        self.assertEqual(window_menu.children.get(B_autonome),autonome())

    def test_commande(self):
        self.assertEqual(self.app.children.get(B_commande), commande())

    def test_mainfonction(self):
        self.app.destroy()



if __name__ == '__main__':
    unittest.main()
