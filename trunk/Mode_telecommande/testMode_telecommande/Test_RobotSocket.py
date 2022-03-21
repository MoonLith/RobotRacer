"""Ce module permet de tester
une connexion quelconques via le robot
"""
import unittest
from RobotSocket import *


class TestRobot(unittest.TestCase):
    """Initialisation des tests"""
    def setUp(self):
        HOST = ''
        PORT = 21567
        ADDR = (HOST, PORT)

        SerSock = socket(AF_INET, SOCK_STREAM)
        print("Socket crée en attente de réponse..")
        SerSock.bind(ADDR)
        SerSock.listen(5)

    """VERIFIE LA FONCTION NON NUL"""
    def test_verifyconnexion(self):
        self.assertIsNotNone(verifyconnexion())


if __name__ == '__main__':
    unittest.main()