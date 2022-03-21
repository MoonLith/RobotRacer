"""
Ce module contient les fonction de base de controle
des roues et servos du Robot de manière commander
via la Raspberry
"""
from tkinter import *
from motorfile import *
import time

motor1 = motor()
x = 1

window = Tk() #Création de la fenêtre
window.title("ROBOT RACER")

label = Label(window, text="Commande:")
label.pack()

def forwardB(x):
    """FAIRE AVANCER LE ROBOT:
    Cette focntion prend en paramètre
    un entier indiquant le temps pendant lequel le Robot avance
    à l'aide de la fonction motorfile"""
    print("Avancer")
    motor1.start()      # appel de la fonction start de la class motor
    motor1.set_speed(1200) # appel de la fonction set_speed de la class motor
    motor1.forward(x) # appel de la fonction forward de la class motor


def backwardB(x):
    """FAIRE RECULER LE ROBOT :
    Cette fonction prend un parametre
    un entier indiquant le temps pendant lequel le Robot recule
    à l'aide de la fonction motorfile"""
    print("Reculer")
    motor1.start()
    motor1.set_speed(1200)
    motor1.backward(x)

def leftB(x):
    """Tourner les roues à gauche
    cette fonction permet de tourner les
    roues a gauche grace a la variable MIN
    à l'aide de la fonction motorfile"""
    print("Gauche")
    motor1.left()

def rightB(x):
    """Tourner les roues à droite
    cette fonction permet de tourner les
    roues à droite grace la variable MAX
    à l'aide de la fonction motorfile"""
    print("Droite")
    motor1.right()

def stopB(x):
    """ARRET MOTEUR :
    Cette fonction coupe tous les moteurs ainsi que leurs ports
    ce qui permet au robot de s'arrêter
    à l'aide de la fonction motorfile"""
    print("STOP")
    motor1.stop()

def quitB():
    """ARRET DU PROGRAMME:
    Cette fonction ferme la fenêtre executé au début du programme"""
    window.quit() # méthode permettant de quitter la fenetre


B_forward = Button(window, width=10, text='Avancer') # Création du bouton
B_forward.pack() # Création du block
B_forward.bind('<ButtonPress-1>', forwardB) # Appel de la fonction forwardB une fois le bouton préssé
B_forward.bind('<ButtonRelease-1>', stopB) # Appel de la fonction stopB une fois le bouton rélaché
window.bind('<KeyPress-z>', forwardB) # Appel de la fonction forwardB une fois la touche 'Z' appuyé
window.bind('<KeyRelease-z>', stopB) # Appel de la fonction stopB une fois la touche 'Z' relaché



B_backward = Button(window, width=10, text='Reculer')
B_backward.pack(side=BOTTOM, padx=30, pady=30) # Création du block et placement de celui-ci
B_backward.bind('<ButtonPress-1>', backwardB)
B_backward.bind('<ButtonRelease-1>', stopB)
window.bind('<KeyPress-s>', backwardB)
window.bind('<KeyRelease-s>', stopB)

B_left = Button(window, width=10, text='Gauche')
B_left.pack(side=LEFT, padx=30, pady=30)
B_left.bind('<ButtonPress-1>', leftB)
B_left.bind('<ButtonRelease-1>', stopB)
window.bind('<KeyPress-q>', leftB)
window.bind('<KeyRelease-q>', stopB)

B_right = Button(window, width=10, text='Droite')
B_right.pack(side=RIGHT, padx=30, pady=30)
B_right.bind('<ButtonPress-1>', rightB)
B_right.bind('<ButtonRelease-1>', stopB)
window.bind('<KeyPress-d>', rightB)
window.bind('<KeyRelease-d>', stopB)

B_stop = Button(window, width=10, text='STOP')
B_stop.pack(side=RIGHT, padx=30, pady=30)
B_stop.bind('<ButtonPress-1>', stopB)
window.bind('<KeyPress-w>', stopB)

B_quit=Button(window, text="Fermer", width=10)
B_quit.pack(side=BOTTOM, padx=30, pady=30)
B_quit.bind('<ButtonPress-1>', quitB)
window.bind('<KeyPress-x>', quitB)


window.mainloop() # Exécution de la fenêtre