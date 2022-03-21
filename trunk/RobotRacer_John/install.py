"""Module d'installation des fichiers pour l'utilisation du mode autonome Beta
    Ce module utilise la librairie Paramiko, seule librarie utilisable sur machine
    WINDOWS afin de se connecter via SSH sans clé ou invité de commande au Raspberry PI"""

from paramiko import SSHClient, AutoAddPolicy
from subprocess import  call
import os

#IP = "192.168.43.214"
#MDP= "apqmwnapqmwn"

def installfile(IP,NOM_USER,MDP):
    """Seule fonction du module, elle utilise l'adresse IP de l'utilisateur
    ainsi que son mot de passe pour se connecter via SSH
    elle verifiera via un ficheir un externe : checker.txt
    pour s'arrurer que l'utilisateur ne réinstalle pas à chaque utilisation
    les fichiers d'utilisation du mode autonome
    """
    user = SSHClient()#on créé le client SSH
    user.load_system_host_keys()
    user.set_missing_host_key_policy(AutoAddPolicy())
    dirlist = ['racer','beta','stream','tele']

    filelistconfig = ['installlib.py','readme.md']
    filelistbeta = ['beta_image.py','beta_main.py','beta_RobotBeta.py','beta_RobotMoveSet.py']
    filelistracer = ['racer_calculs_valeurs.py','beta_image.py','beta_main.py','racer_mouvement.py','racer_arret.py']
    fileliststream =  ["stream_image.py","stream_main.py","beta_RobotBeta.py","stream_RobotMoveSet.py",'stream_thread.py']
    filelisttele = ['tele_motorfile.py','tele_interface.py','tele_axecamera.py','tele_robotsocket.py']


    file = open("checker.txt",  "r+")
    try :
        if file.mode == 'r+':#on s'assure que le fichier soit en mode lecture et ecriture

            content = file.readline()#seul a première ligne nous intéresse
            print(content)


            if not content.strip(): #si il n'y a pas de contenu

                print("ok")
                user.connect(IP,port=2222 ,username=NOM_USER, password=MDP)  # MODIFIER LE PORT
                trsfile = user.open_sftp()#outil pour transferer les fichiers
                user.exec_command('mkdir robotRacerOff') #on creer un dossier

                for dir in dirlist:#on creer chaque dossier correspondant
                    user.exec_command('mkdir robotRacerOff/'+dir)

                for elem in filelistconfig:
                    try:
                        trsfile.put(elem, 'robotRacerOff/%s' % (elem)) #on insère chaque fichier dans le dossier
                    except  FileNotFoundError as FileError:
                        print("Erreur de fichier :{}".format(FileError))


                for elem in filelistbeta:#FILE BETA

                    try:
                        trsfile.put(elem, 'robotRacerOff/beta/%s' % (elem)) #on insère chaque fichier dans le dossier
                    except  FileNotFoundError as FileError:
                        print("Erreur de fichier :{}".format(FileError))


                for elem in fileliststream:
                    try:
                        trsfile.put(elem, 'robotRacerOff/stream/' + elem)  # on insère chaque fichier dans le dossier
                    except  FileNotFoundError as FileError:
                        print("Erreur de fichier :{}".format(FileError))

                for elem in filelistracer:
                    try:
                        trsfile.put(elem, 'robotRacerOff/racer/' + elem)  # on insère chaque fichier dans le dossier
                    except  FileNotFoundError as FileError:
                        print("Erreur de fichier :{}".format(FileError))


                for elem in filelisttele:
                    try:
                        trsfile.put(elem, 'robotRacerOff/tele/' + elem)  # on insère chaque fichier dans le dossier
                    except  FileNotFoundError as FileError:
                        print("Erreur de fichier :{}".format(FileError))



                file.write("vos fichier sont installes")
                stdin, stdout, stderr = user.exec_command('ls robotRacerOff/') #on creer un dossier
                out = stdout.readlines()
                print('\n'.join(out)) #on affiche ligne par ligne


            else :

                print("vos fichiers sont dejà installé")
                user.connect(IP,port= 2222, username=NOM_USER, password=MDP)  # MODIFER LE PORT
                stdin, stdout, stderr = user.exec_command('ls robotRacerOff/') #on creer un dossier
                out = stdout.readlines()
                print('\n'.join(out))

    except FileNotFoundError as FileError:
        print("Nous n'avons pas trouvé votre fichier : {}".format(FileError))
    finally:
        file.close()
#installfile(IP, MDP)
