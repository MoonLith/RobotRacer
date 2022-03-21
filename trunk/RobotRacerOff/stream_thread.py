from threading import Thread
import  time
import sys
import os
from subprocess import call
import webbrowser


class InitRobotStream(Thread):

    """cette classe permet d'initialiser le stream coté robot"""

    def __init__(self):

        Thread.__init__(self)

    def run(self):

        """Ci dessousl le code executé lorsque l'on lance le thread"""

        pwd = "/home/pi/Sunfounder_Smart_Video_Car_Kit_for_RaspberryPi/mjpg-streamer/mjpg-streamer/"
        os.chdir(pwd)
        call(["sudo","make", "USE_LIBV4L2=true", "clean", "all"])  # compilation
        call(["sudo", "make", "DESTDIR=/usr", " install"])  # installation
        print("installation du module de streaminng en cours")

        call(["sudo", "sh", "start.sh"])  # connexion
        print("Pret à se connecter")


class InitClientStream(Thread):

    def __init__(self, IP_RPI):

        Thread.__init__(self)
        self.IP_RPI = IP_RPI

    def run(self):

        """Cette fonction permet d'activer le streaming video du robot coté client"""

        webpath = "http://" + self.IP_RPI + ":8080/stream.html"
        print("Connection streaming avec le RASPEBRRY en cours")

        try:
            webbrowser.open(webpath)
        except ValueError as e:
            print("La connexion a echouché\n Erreur : {}".format(e))
        finally:
            print("Fin de la connexion")