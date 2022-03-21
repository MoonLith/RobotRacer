import os
import subprocess
from subprocess import call
from pathlib import Path

def lib_to_install():
    """Cette fonction à lancer le robot, permet de réaliser les différentes
    commandes à la place de l'utilisateur afin d'installer toutes les librairies necessaire
    pour l'utilisation du robot, allant des libraries des moteurs, à celle du traiteement d'image

    Dans la mesure où certaines libraries seront déjà installer le programma passera automatiquement
    au suivant"""

    home = str(Path.home())
    try :
    #-- Update
        call(['sudo', 'apt-get','-y', 'update',])

        #--Installation port I2C
        os.chdir(home)
        call(['sudo', 'apt-get','-y', 'install', 'i2c-tools'])
        call(['sudo','adduser','pi','i2c'])

        #---Installation SM BUS
        call(['sudo', 'apt-get','-y' 'install', 'python-smbus'])

       #--Installtion PIP
        call(['sudo', 'apt-get', '-y', 'install', 'python3-pip'])
        #installation ADAFRUIT & GPIO
        call(['sudo','pip3','install','rpi.gpio'])
        call(['sudo','apt-get','-y','install','git','build-essential','python3-dev'])
        call(['git', 'clone', 'https://github.com/adafruit/Adafruit_Python_PCA9685'])
        os.chdir('Adafruit_Python_PCA9685/')
        call(['sudo','python3','setup.py','install'])

        #--------------OPEN CV
        os.chdir(home)
        call(['sudo', 'apt-get','-y', 'install', 'build-essential', 'cmake', 'git', 'pkg-config'])
        call(['sudo', 'apt-get','-y', 'install', 'libjpeg-dev', 'libtiff5-dev', 'libjasper-dev', 'libpng12-dev'])
        call(['sudo', 'apt-get','-y' 'install', 'libavcodec-dev', 'libavformat-dev', 'libswscale-dev', 'libv4l-dev'])
        call(['sudo', 'apt-get','-y' 'install' ,'libgtk2.0-dev', 'libcanberra-gtk-module'])
        call(['sudo', 'apt-get','-y', 'install', 'libatlas-base-dev', 'gfortran'])
        call(['sudo','pip3', 'install', 'numpy'])

        call(['wget','-O','opencv.zip','https://github.com/opencv/opencv/archive/3.3.0.zip'])
        call(['unzip','opencv.zip'])
        os.chdir('~/opencv-3.3.0')
        call(['mkdir', 'build'])
        os.chdir('build')

        call(['cmake', '-D', 'CMAKE_BUILD_TYPE=RELEASE',
            '-D', 'CMAKE_INSTALL_PREFIX=/usr/local',
            '-D', 'INSTALL_C_EXAMPLES=OFF',
            '-D', 'INSTALL_PYTHON_EXAMPLES=ON',
            '-D', 'OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-3.3.0/modules',
            '-D', 'BUILD_EXAMPLES=ON', '..'])

        call(['make','-j4'])
        call(['make','clean'])
        call(['make'])
        call(['make','install'])
        call(['ldconfig'])

    except OSError as error:
        print('Erreur lors du lancement de la commande : {}'.format(error))

if __name__ == '__main__':
    print("installation de toutes librairies..")
    lib_to_install()
    print("Fin de l'installation")