"""Module principale de connexion et d'utilisation de l'utilisateur """

from tkinter import *
import os
from subprocess import Popen, PIPE,call
import install
from paramiko import SSHClient,AutoAddPolicy
import install,installlib

user = SSHClient()

def pagedeconnexion():
    """Page de connexion de l'utilisateur
    L'utilisateur devra y insérer son adresse IP, ainsi que son mot de passe
    nous partons du principe où l'utilisateur est débutant"""
    fenetre = Tk() #on créé la fenetre
    fenetre.geometry("300x200")
    ip_label = Label(fenetre, text="Inserrer votre adresse IP")
    ip_label.pack()#on colle le label dans la fenetre

    ip_string = StringVar()#l'adresse IP sera stocké ici
    ip_input = Entry(fenetre, textvariable= ip_string, width =20)# zone où insèrre l'IP
    ip_input.pack()

    nom_label = Label(fenetre, text="Inserrer votre nom d'utilisateur")
    nom_label.pack()

    nom_string = StringVar()  # l'adresse IP sera stocké ici
    nom_input = Entry(fenetre, textvariable=nom_string, width=20)  # zone où insèrre l'IP
    nom_input.pack()

    mdp_label = Label(fenetre, text="Inserrer votre mot de passe")
    mdp_label.pack()

    mdp_string = StringVar()
    mdp_input = Entry(fenetre, text ="mot de passe", show="*",textvariable=mdp_string, width = 20)
    mdp_input.pack()

    button_quit = Button(fenetre, text= "Connexion", command=fenetre.quit)
    button_quit.pack()


    fenetre.mainloop()
    user_ip = ip_string.get()
    user_nom = nom_string.get()
    user_mdp = mdp_string.get()
    fenetre.destroy()
    return user_ip,user_nom, user_mdp

def sshconnexion(IP,NOM_USER,MDP):
    """
    Cette fonction permet de se connecter par SSH au robot, de cette façon
    l'utilisateur se capable d'utilisaer les différentes fonctionnalités du robot
    racer mis à disposition.
    :param IP: l'adresse IP du RobotRacer
    :param NOM_USER: le nom d'utilisateur correspondant à la RaspberryPi
    :param MDP: le mot de passe utilisateur correspondant à la raspberry PI
    :return: Renvoie un parametre user, permettant par la suite
    de réaliser différente fonction via SSH.
    """
    global user #on recupère le client SS
    user.load_system_host_keys() #Permet de generer les clefs SSH
    user.set_missing_host_key_policy(AutoAddPolicy())
    user.connect(IP,port=2222, username=NOM_USER, password=MDP)#on se connecte par SSH

    stdin, stdout, stderr = user.exec_command('ls robotRacerOff/')# on montre le dossier
    print("***************************************")
    print("*****BIENVENUE SUR LE ROBOT RACER******")
    print("***************************************")
    out = stdout.readlines(1000)
    print('\n'.join(out))#on affiche le resultat du LS
    # cette commande simple nous confirme qu'on est conecté

    return user #on renvoie le client SSH mis à jour

def page_de_config():
    """Cette fonction permmet de gerer la page de configuration
    La page de configuration permet à l'utilisateur d'installer les fichiers et les librairies necessaire
    au fonctionnement du RobotRacer"""
    fenetre_config = Tk()
    fenetre_config.geometry("300x200")

    label_file = Label(fenetre_config, text="installez vos fichier !")
    label_lib = Label(fenetre_config, text="installez les librairies necessaires !")

    button_file = Button(fenetre_config, text="File",
                         command=lambda: onclickconfig('fichier'))

    button_lib = Button(fenetre_config, text="Lib",
                        command=lambda: onclickconfig('lib'))

    button_quitter = Button(fenetre_config, text="Quitter",
                            command=fenetre_config.quit)

    # -----PACKING SUR FENETRE-------
    label_file.pack()
    button_file.pack()
    label_lib.pack()
    button_lib.pack()
    button_quitter.pack()
    fenetre_config.mainloop()
    fenetre_config.destroy()

def onclick(event):
    """Fonction permettant de gerer les evenement cliqué de la page autonome du robot racer """
    global user #on recupère le client SSH

    if event == 'racer': #le bouton cliqué correspond à celui du mode racer
        print("go racer")
        #on execute le module main du racer
        stdin, stdout, stderr = user.exec_command('python3 robotRacerOff/racer/racer_main.py')
        out = stdout.readlines(1024)
        print('\n'.join(out))
    elif event == 'beta':#Ccrrespond à lancer le mode autonome beta
        print("go beta")
        stdin, stdout, stderr = user.exec_command('python3 robotRacerOff/beta/beta_main.py')
        out = stdout.readlines(1024)
        print('\n'.join(out))
        stdin.write("1300")# à checker
        stdin.flush()#
        stdin.write("1300")#
        stdin.flush()#
    elif event == 'stream': #Mode autonome stream
        print("go stream")
        stdin, stdout, stderr = user.exec_command('python3 robotRacerOff/stream/stream_main.py')
        out = stdout.readlines(1024)
        print('\n'.join(out))
    elif event == 'stop':
        stdin, stdout, stderr = user.exec_command("\x03")
        print('arret du robot')

def onclickchoix(event):
    """Cette fonction correspond au evenement réalisé lorsque l'on clique
    sur un bouton de la page de choix proposé"""
    global user
    global IP
    global NOM_USER
    global MDP
    print(IP,NOM_USER,MDP)
    if event == 'racer':  # RobotRacer1
        print("go racer")
        user = sshconnexion(IP, NOM_USER, MDP)
        stdin, stdout, stderr = user.exec_command('ls robotRacerOff/racer/')
        out = stdout.readlines()
        print('\n'.join(out))
        pageautonome('racer')

    elif event == 'beta':  # RobotRacerBeta
        print("go beta")
        user = sshconnexion(IP, NOM_USER, MDP)
        stdin, stdout, stderr = user.exec_command('ls robotRacerOff/beta/')
        out = stdout.readlines()
        print('\n'.join(out))
        pageautonome('beta')

    elif event == 'stream':  # RobotRacerStream
        print('go stream')
        user = sshconnexion(IP, NOM_USER, MDP)
        stdin, stdout, stderr = user.exec_command('ls robotRacerOff/stream/')
        out = stdout.readlines()
        print('\n'.join(out))
        pageautonome('stream')

    elif event == 'tele':  # RobotRacerTele
        sshconnexion(IP, NOM_USER, MDP)
        stdin, stdout, stderr = user.exec_command('python3 robotRacerOff/stream/tele_robotsocket.py')
        os.system('python3 tele_interface.py')


def page_choix():
    """Fonction permettant à l'utilisateur de choisir ce qu'il veut faire"""
    fenetre_choix = Tk()
    fenetre_choix.geometry("300x200")

    label_choix = Label(fenetre_choix, text="Que voulez vous lancer ?")
    #En ayant cliqué on affiche la page autonome et on se connecte par SSH

    #////////////////  Bouton correspondant aux choix disponible /////////////////
    button_robot_racer = Button(fenetre_choix, text = 'RobotRacer',
                                command= lambda :onclickchoix('racer') and fenetre_choix.quit)

    button_robot_racer_beta = Button(fenetre_choix, text = 'RobotRacerBeta',
                                     command= lambda :[onclickchoix('beta'), fenetre_choix.quit])

    button_robot_racer_stream = Button(fenetre_choix, text = 'RobotRacerStream',
                                       command= lambda :[onclickchoix('stream'), fenetre_choix.quit])

    button_robot_racer_tele = Button(fenetre_choix, text = 'RobotRacer telecommande',
                                     command= lambda :[onclickchoix('tele'), fenetre_choix.quit])

    button_quit = Button(fenetre_choix, text= "Quitter", command=fenetre_choix.quit)
    #//////////////// ----------------------------------------/////////////////////////

    #On appllique les boutons--
    label_choix.pack()
    button_robot_racer.pack()
    button_robot_racer_beta.pack()
    button_robot_racer_stream.pack()
    button_robot_racer_tele.pack()
    button_quit.pack()
    #--------------------------

    fenetre_choix.mainloop()
    fenetre_choix.destroy()

def pageautonome(choix):
    """Page du mode autonome du Robot Racer,
    prend en variable le choix afin de choisir, quel bouton
    effectura une action"""

  #---CREATION DES DIFFERENTS OUTILS UTILISATEURS--
    fenetre_autonome = Tk()
    fenetre_autonome.geometry("300x200")

    label_autonome = Label(fenetre_autonome, text ="Lancer le mode autonome !")
    label_arreter = Label(fenetre_autonome,text="Arreter le mode autonome")

    button_autonome_racer = Button(fenetre_autonome, text ="GO",command=lambda :onclick('racer'))
    button_autonome_beta = Button(fenetre_autonome, text ="GO",command=lambda :onclick('beta'))
    button_autonome_stream = Button(fenetre_autonome, text ="GO",command=lambda :onclick('stream'))

    button_arreter = Button(fenetre_autonome, text = "STOP",command=lambda: onclick('stop'))
    button_quitter = Button(fenetre_autonome, text= "Quitter", command=fenetre_autonome.quit)

#-----On affiche le bouton correspondant en fonction du choix ---
    label_autonome.pack()
    if choix == 'racer' :
        button_autonome_racer.pack()
    elif choix == 'beta':
        button_autonome_beta.pack()
    elif choix == 'stream':
        button_autonome_stream.pack()
#-------------------------------------------
    label_arreter.pack()
    button_arreter.pack()
    button_quitter.pack()
#----------------------------
    fenetre_autonome.mainloop()
    fenetre_autonome.destroy()

def onclickconfig(event):
    """ Cette fonction permet de gerer les evenement par rapport
    à la page de configuration ou du Menu principale
    :param event: l'eveneement cliqué correspondant au bouton
    de la librairie ou des fichiers à installer.
    """
    global IP,NOM_USER,MDP
    global user
#********************************************
    if event == 'gorobot':
        page_choix()

    elif event == 'goconfig':
        page_de_config()
#********************************************

    elif event == 'fichier':

        install.installfile(IP,NOM_USER,MDP)
    elif event == 'lib':

        print('Vous allez isntaller toutes les librairies')
        user = sshconnexion(IP,NOM_USER,MDP)
        stdin, stdout, stderr = user.exec_command('python3 installlib.py')

def menu_2():
    """Menu pour aller sur le robot ou dans le panneau de configuration"""

    fenetre_menu2= Tk()
    fenetre_menu2.geometry("300x200")

    robot_label = Label(fenetre_menu2, text="Connectez vous au robot")
    robot_label.pack(fill=BOTH)

    button_robot = Button(fenetre_menu2, text="Robot", command=lambda: onclickconfig('gorobot'))
    button_robot.pack()

    configuration_label = Label(fenetre_menu2, text="Paneau de configuration")
    configuration_label.pack()

    button_configuration = Button(fenetre_menu2, text="Configuration", command=lambda :onclickconfig('goconfig'))
    button_configuration.pack()

    fenetre_menu2.mainloop()
    fenetre_menu2.destroy()


if __name__ == '__main__':
    IP, NOM_USER, MDP = pagedeconnexion()
    menu_2()










