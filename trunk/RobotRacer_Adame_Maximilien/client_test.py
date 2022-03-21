"""Ce module permet a l'utilisateur de copier les modules de test et les images
depuis sa machine personnelle"""

###===== IMPORT =====####

import paramiko
from scp import SCPClient
import getpass

########################


def createSSHClient(server, user, password):
    """Cette fonction permet de se connecter en SSH.

    Prend en parametres :
    - server : l'adresse du serveur
    - user : le nom d'utilisateur
    - password : le mot de passe

    Retourne :
    - client : le client SSH
    """

    client = paramiko.SSHClient() #Création du client SSH
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server,username=user,password=password)
    return client

###############################################################################

print("=========================================================")
print("  Bienvenue dans l'application du mode test Robot Racer")
print("=========================================================")

try :
    #On demande l'adresse IP a l'utilisateur
    server = input("Adresse IP ?")

    #On demande le nom d'utilisateur utilise pour la connection
    user = input("User ?")

    #On demande le mot de passe
    password = getpass.getpass("Password ?")

    #On apelle la fonction createSSHClient qui permet de se connecter au Raspberry
    #via SSH
    print("Creation du client SSH...")
    ssh = createSSHClient(server, user, password)

    #On utilise le client SSH pour transporter des donnees avec SCP
    scp = SCPClient(ssh.get_transport())

    #On envoie les fichiers necessaires pour le test au Raspberry Pi
    print("Copie des fichiers vers le RaspberryPi...")
    stdin, stdout, stderr = ssh.exec_command('mkdir appRobotRacer/testRobotRacer')
    scp.put('testsModeAutonome/testCalculsValeurs.py', 'appRobotRacer/testRobotRacer/testCalculsValeurs.py')
    scp.put('testsModeAutonome/testImage.py', 'appRobotRacer/testRobotRacer/testImage.py')
    scp.put('testsModeAutonome/testMouvement.py', 'appRobotRacer/testRobotRacer/testMouvement.py')
    stdin, stdout, stderr = ssh.exec_command('mkdir appRobotRacer/testRobotRacer/images')
    scp.put('testsModeAutonome/images/frame01.jpg', 'appRobotRacer/testRobotRacer/images/frame01.jpg')
    scp.put('testsModeAutonome/images/frame02.jpg', 'appRobotRacer/testRobotRacer/images/frame02.jpg')
    scp.put('testsModeAutonome/images/frame03.jpg', 'appRobotRacer/testRobotRacer/images/frame03.jpg')
    scp.put('testsModeAutonome/images/frame11.jpg', 'appRobotRacer/testRobotRacer/images/frame11.jpg')
    scp.put('testsModeAutonome/images/frame12.jpg', 'appRobotRacer/testRobotRacer/images/frame12.jpg')
    scp.put('testsModeAutonome/images/frame13.jpg', 'appRobotRacer/testRobotRacer/images/frame13.jpg')
    scp.put('testsModeAutonome/images/frame14.jpg', 'appRobotRacer/testRobotRacer/images/frame14.jpg')
    scp.put('testsModeAutonome/images/frame15.jpg', 'appRobotRacer/testRobotRacer/images/frame15.jpg')
    scp.put('testsModeAutonome/images/frame16.jpg', 'appRobotRacer/testRobotRacer/images/frame16.jpg')
    scp.put('testsModeAutonome/images/frame17.jpg', 'appRobotRacer/testRobotRacer/images/frame17.jpg')
    scp.put('testsModeAutonome/images/frame18.jpg', 'appRobotRacer/testRobotRacer/images/frame18.jpg')
    scp.put('testsModeAutonome/images/frame19.jpg', 'appRobotRacer/testRobotRacer/images/frame19.jpg')


    print("Copie finie !")
    print("Lancez maintenant les fichiers python de test depuis un client SSH")
    print("")
    print("=========================================================")
    print("  A bientot dans l'application du mode test Robot Racer")
    print("=========================================================")

except KeyboardInterrupt:
    #Si on est ici c'est que le programme doit s'arrêter
    #On envoie l'interruption clavier au Raspberry Pi
    stdin, stdout, stderr = ssh.exec_command("\x03")
    #On ferme le client SSH
    ssh.close()
    print("")
    print("=========================================================")
    print("  A bientot dans l'application du mode test Robot Racer")
    print("=========================================================")
