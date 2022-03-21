"""
Ce module contient les fonction de base de controle
des roues et servos du Robot de manière commander
exécuté sur la machine du client
"""

from tkinter import *
from socket import *


HOST = input("Confirmez l'adresse IP :")
PORT = 21567
BUFSIZ = 1024
ADDR = (HOST, PORT)

CliSock = socket(AF_INET, SOCK_STREAM)
CliSock.connect(ADDR)

window_menu = Tk() # Création de la fenêtre du Menu
window_menu.title("ROBOT RACER")
label = Label(window_menu, text="Welcome")
label.grid(row = 0, column = 1)

"""
ACTIVATION DU MODE AUTONOME:
Cette fonction permet l'activation
du mode autonome une fois le Bouton appuyer
"""
def autonome():
    print("Lancement autonomie")
    CliSock.send(b'Autonome')  # Demande envoyer a la Raspberry

B_autonome = Button(window_menu, width=10, text='Autonome', command =autonome)
B_autonome.grid(row=1,column=0)

"""
ACTIVATION DU MODE TELECOMMANDE:
Cette fonction permet l'activation
du mode télécommander une fois le Bouton appuyer
"""
def commande():
    print("Lancement commande robot")
    window = Tk() # Création de la fenêtre commande
    window.title("ROBOT RACER")
    label = Label(window, text="Commande:")
    label.grid()

    """
    Les fonctions suivante sont envoyé a RobotSokect
    afin d'exécuter les demandes du client
    """
    # --------Fonction Motrice----------
    def forwardB(event):
        print("Avancer")
        CliSock.send(b'forward') #Demande envoyer a la Raspberry


    def backwardB(event):
        print("Reculer")
        CliSock.send(b'backward')

    def leftB(event):
        print("Gauche")
        CliSock.send(b'left')

    def rightB(event):
        print("Droite")
        CliSock.send(b'right')

    def centreB(event):
        print("centre")
        CliSock.send(b'centre')

    def stopB(event):
        print("STOP")
        CliSock.send(b'stop')

    # --------Fonction Servo Caméra----------
    def camerahighB(event):
        print("Y+")
        CliSock.send(b'camHigh')
    def cameralowB(event):
        print("Y-")
        CliSock.send(b'camLow')

    def cameraleftB(event):
        print("X-")
        CliSock.send(b'camLeft')

    def camerarightB(event):
        print("X+")
        CliSock.send(b'camRight')


    def returnB(event):
        window.destroy()

    # --------Création boutons----------

    #Moteur
    label = Label(window, text="Moteur:")
    label.grid(row=0, column=1)
    B_forward = Button(window, width=10, text='Avancer')
    B_backward = Button(window, width=10, text='Reculer')
    B_left = Button(window, width=10, text='Gauche')
    B_right = Button(window, width=10, text='Droite')
    B_center = Button(window, width=10, text='Centre')
    B_stop = Button(window, width=10, text='STOP')

    #Caméra
    label = Label(window, text="Caméra:")
    label.grid(row=0, column=10)
    B_camHigh = Button(window, width=10, text='Y+')
    B_camLow = Button(window, width=10, text='Y-')
    B_camLeft = Button(window, width=10, text='X-')
    B_camRight = Button(window, width=10, text='X+')

    #Quitter la fenêtre
    B_return=Button(window, text="Retour", width=10)

    # --------Création block et ajustement----------

    #Moteur
    B_forward.grid(row=2,column=1)
    B_backward.grid(row=4,column=1)
    B_left.grid(row=3,column=0)
    B_right.grid(row=3,column=2)
    B_center.grid(row=3,column=1)
    B_stop.grid(row=1,column=2)

    #Caméra
    B_camHigh.grid(row=2,column=10)
    B_camLow.grid(row=4,column=10)
    B_camLeft.grid(row=3,column=9)
    B_camRight.grid(row=3,column=11)

    #Quitter la fenêtre
    B_return.grid(row=1,column=0)

    # --------Appel des fonction à l'aide des boutons----------

    #Moteur
    B_forward.bind('<ButtonPress-1>', forwardB) # Appel de la fonction forwardB une fois le bouton préssé
    B_forward.bind('<ButtonRelease-1>', stopB) # Appel de la fonction stopB une fois le bouton rélaché
    B_backward.bind('<ButtonPress-1>', backwardB)
    B_backward.bind('<ButtonRelease-1>', stopB)
    B_left.bind('<ButtonPress-1>', leftB)
    B_left.bind('<ButtonRelease-1>', stopB)
    B_right.bind('<ButtonPress-1>', rightB)
    B_right.bind('<ButtonRelease-1>', stopB)
    B_center.bind('<ButtonPress-1>', centreB)
    B_center.bind('<ButtonRelease-1>', stopB)
    B_stop.bind('<ButtonPress-1>', stopB)

    #Caméra
    B_camHigh.bind('<ButtonPress-1>', camerahighB)
    B_camLow.bind('<ButtonPress-1>', cameralowB)
    B_camLeft.bind('<ButtonPress-1>', cameraleftB)
    B_camRight.bind('<ButtonPress-1>', camerarightB)

    #Quitter la fenêtre
    B_return.bind('<ButtonPress-1>', returnB)

    # --------Appel des fonction à l'aide du clavier----------
    #Moteur
    window.bind('<KeyPress-Up>', forwardB) # Appel de la fonction forwardB une fois la touche 'Up' appuyé
    window.bind('<KeyRelease-Up>', stopB) # Appel de la fonction stopB une fois la touche 'Up' relaché
    window.bind('<KeyPress-Down>', backwardB)
    window.bind('<KeyRelease-Down>', stopB)
    window.bind('<KeyPress-Left>', leftB)
    window.bind('<KeyRelease-Left>', stopB)
    window.bind('<KeyPress-Right>', rightB)
    window.bind('<KeyRelease-Right>', stopB)
    window.bind('<KeyPress-Shift_L>', centreB)
    window.bind('<KeyRelease-Shift_L>', stopB)
    window.bind('<KeyPress-space>', stopB)

    #Caméra
    window.bind('<KeyPress-z>', camerahighB)
    window.bind('<KeyPress-s>', cameralowB)
    window.bind('<KeyPress-q>', cameraleftB)
    window.bind('<KeyPress-d>', camerarightB)

    #Quitter la fenêtre
    window.bind('<KeyPress-Escape>', returnB)

    window.mainloop() # Exécution de la fenêtre du Mode Commande

B_commande = Button(window_menu, width=10, text='Commande', command= commande)
B_commande.grid(row=1,column=3)



def quit(event):
    KeyboardInterrupt
    window_menu.destroy()
    CliSock.close()



bouton = Button(window_menu, text="Fermer")
bouton.grid(row=2, column=1)
bouton.bind('<ButtonPress-1>', quit)
window_menu.bind('<KeyPress-Escape>', quit)
def mainfonction() :
    window_menu.mainloop()  # Exécution de la fenêtre du Menu principal


if __name__ == '__main__':
    mainfonction()
