# Robot Racer Application by Ben Hammouda Adame & Rouge Maximilien

## Introduction

>  Ce readme est destine aux developpeurs qui veulent comprendre l'architecture de notre application. Cette application est divisee en deux parties : une de test et une qui execute le mode autonome lors duquel le Robot va suivre le circuit grace a sa camera.

## Architecture du code

>  == Mode Autonome ==  :
Le Mode autonome est compose de 6 modules que nous allons presenter ci-dessous : 
- main.py :  Module principal du mode autonome. Il appelle a la suite les 3 modules et leur fournit les retours de chacun.
- image.py :   Module de traitement et d'analyse d'image du mode autonome. Il est le premier appele par le module main, il traite l'image, l'analyse et retourne a main une valeur exploite par la suite
- calculs_valeurs.py :  Module de calculs. Il est appelle a la suite d'image et permet de calculer la trajectoire a adopter pour les roues et pour la camera.
- mouvement.py : Module de mouvement du Robot. Permet de deplacer le Robot, toutes les methodes de ce module ont un effet observable sur le Robot physiquement.
- arret.py :  Module qui permet d'arreter le Robot.
- client_app.py :  Module execute par le client sur sa machine personnelle. Gere la copie des fichiers sur le Raspberry Pi et la connexion en SSH. Appelle main ensuite.

> Mode Test :
Le Mode test est compose de 3 modules que nous allons presenter ci-dessous :
- testCalculsValeurs.py : Module qui permet de tester les methodes de calculs_valeurs.py
- testImage.py : Module qui permet de tester les methodes de image.py
- testMouvement.py : Module qui permet de tester les methodes de mouvement.py
- client_test.py : Module qui permet de copier sur le Raspberry Pi tous les fichiers necessaires pour le mode de test

## Installation

> Pour executer notre application vous avez besoin de  :
- Python Version 3
- Paramiko
- SCP
- OpenCV2

/!\ Veuillez vous referer au Manuel d'installation pour plus d'informations sur l'installation de ces bibliotheques. /!\
