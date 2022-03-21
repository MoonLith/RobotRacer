"""Ce module permet a l'utilisateur de lancer le mode autonome sans se soucier
de la connexion SSH et des fichiers serveur et client"""

###===== IMPORT =====####

import sys, os
import paramiko
from scp import SCPClient
import time
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
print("       Bienvenue dans l'application Robot Racer")
print("=========================================================")

try :
    #On demande l'adresse IP a l'utilisateur
    server = input("Adresse IP ?")

    #On demande le nom d'utilisateur utilise pour la connection
    user = input("Nom d'utilisateur (pi par defaut) ?")

    #On demande le mot de passe
    password = getpass.getpass(prompt='Mot de passe ?')

    #On apelle la fonction createSSHClient qui permet de se connecter au Raspberry
    #via SSH
    print("Creation du client SSH...")
    ssh = createSSHClient(server, user, password)

    #On utilise le client SSH pour transporter des donnees avec SCP
    scp = SCPClient(ssh.get_transport())

    #On envoie les fichiers necessaires pour l'application au Raspberry Pi
    print("Copie des fichiers vers le RaspberryPi...")

    #Creation du dossier appRobotRacer
    stdin, stdout, stderr = ssh.exec_command('mkdir appRobotRacer')

    #Envoie des modules de l'application
    scp.put('image.py', 'appRobotRacer/image.py') # Module d'analyse d'image
    scp.put('mouvement.py', 'appRobotRacer/mouvement.py') # Module de controle
    # du Robot
    scp.put('calculs_valeurs.py', 'appRobotRacer/calculs_valeurs.py') # Module de calcul
    # de valeurs
    scp.put('axecamera.py', 'appRobotRacer/axecamera.py')  # Module controle de la caméra mode télécommandé
    scp.put('motorfile.py', 'appRobotRacer/motorfile.py')  # Module controle des roues et moteurs mode télécommandé
    scp.put('RobotSocket.py', 'appRobotRacer/RobotSocket.py') # Module controle de l'interface
    scp.put('main.py', 'appRobotRacer/main.py') # Module principal
    scp.put('arret.py', 'appRobotRacer/arret.py') # Module d'arret du Robot

    print("")
    print("Lancement Interface...")

    #On lance le module main de l'interface
    stdin, stdout, stderr = ssh.exec_command('python3 appRobotRacer/RobotSocket.py')
    os.system('python3 interface.py')

except KeyboardInterrupt:
    #Si on est ici c'est que le programme doit s'arrêter
    #On envoie l'interruption clavier au Raspberry Pi
    stdin, stdout, stderr = ssh.exec_command("\x03")
    stdin, stdout, stderr = ssh.exec_command('python3 appRobotRacer/arret.py')
    #On ferme le client SSH
    ssh.close()
    print("")
    print("=========================================================")
    print("        A bientot dans l'application Robot Racer")
    print("=========================================================")
