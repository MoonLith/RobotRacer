"""
Ce module contient les réponses demandées
par la machine du client
"""
from socket import *
from main import *
from motorfile import *
from axecamera import *



HOST = ''       # Varriable HOST null permettant à la fonction bind() de lié une adresse valide
PORT = 21567
BUFSIZ = 1024
ADDR = (HOST, PORT)

SerSock = socket(AF_INET, SOCK_STREAM)      # Creation de socket
SerSock.bind(ADDR)      # Liaison de l'adresse IP et le port au serveur
SerSock.listen(5)       # Le paramètre listen() definie le nombre de connexion permisse


motor1 = motor()
axecamera1 = axecamera()
x = 1
y = 10
z = 20

"""VERIFICATION DE LA CONNEXION DES 2 MODULE:
Cette fonction permettra à l'interface une fois lancé
d'accepter la connexion de celui-ci"""
def verifyconnexion():
    CliSock, addr = SerSock.accept()  # Acceptation de la connexion
    print("Connexion reussite, IP connecté : ", addr)
    if CliSock is not None:
        return CliSock
    else :
        print("Connexion échoué")
        return False


while True:
    CliSock = verifyconnexion()

    while True:
        reponse = CliSock.recv(BUFSIZ)
        # Reception des demande du client
        # Analyse les commande reçu et controle le robot en conséquence
        if not reponse:
            break
        # --------Appel des fonctions Autonome----------
        if reponse == b'Autonome':
            autonomie()
            if robot.arret():
                break
        # --------Appel des fonctions motrices----------
        elif reponse == b'forward':
            motor1.start()
            motor1.set_speed(60)
            motor1.forward(x)

        elif reponse == b'backward':
            motor1.start()
            motor1.set_speed(60)
            motor1.backward(x)

        elif reponse == b'left':
            motor1.left()

        elif reponse == b'right':
            motor1.right()

        elif reponse == b'centre':
            motor1.centre()

        elif reponse == b'stop':
            motor1.stop()

        # --------Appel des fonctions Servo Caméra----------
        elif reponse == b'camHigh':
            axecamera1.high(z)

        elif reponse == b'camLow':
            axecamera1.low(y)

        elif reponse == b'camLeft':
            axecamera1.left(z)

        elif reponse == b'camRight':
            axecamera1.right(y)

        #--------Si aucune des commandes précédente est appelé----------
        else:
            print('Command Error!')
            CliSock.close()
            SerSock.close()

    SerSock.close()
