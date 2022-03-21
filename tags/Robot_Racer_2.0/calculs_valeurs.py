"""Module contenant des fonctions qui, a partir des resultats de l'analyse
d'image, renvoient des valeurs qui servent de parametres aux methodes des
objets de la classe Robot.

On distingue des fonctions dont les resultats servent a savoir comment la
camera doit tourner, et d'autres qui servent a determiner la vitesse et
l'inclinaison de roues avant a adopter pour tous les virages :

- int:centrexCamera(int:centre_x, int:camera_x) : fonction qui donne la "position
absolue" du centre de la forme observee sur la photo, a partir de l'abscisse
de ce centre et le positionnement qu'avait la camera lors de la photo.
Elle est appelee dans le module main.

- int:valPourCamera(int:position_x) : fonction qui, avec la position de centre_x
renvoie la nouvelle orientation de la camera a adopter pour ne pas perdre
le circuit. Elle est appelee dans le module main et son resultat est envoye
en parametre de la methode tournerCamera() de l'objet robot.

- int:typeDeVirage(int:position_x) : fonction qui, pour une "position absolue" de
centre de forme, nous indique s'il faut aller tout droit ou tourner, de
quel cote, et dans quelle mesure. Elle est appelee par valPourMouvement
et permet de ne tester les instructions conditionnelles qu'une fois.

- int:inclinaisonRoues(int:type_virage, int:position_x) : fonction qui, a partir
d'un type de virage renvoye par typeDeVirage(), et la position exacte du
centre de la forme, renvoie une valeur qui correspond a la valeur avec laquelle
sera positionne le servo des roues avant du Robot.

- int:vitesseMoteurs(int:type_virage, int:vitesse) : fonction qui a partir d'un type
de virage (donne par la fonction typeDeVirage()) et de la vitesse que prend
le Robot dans les lignes droites, renvoie la vitesse que doivent prendre les
moteurs a cet instant. L'entier renvoye est donne en parametre a la fontion
qui gere les servos avant dans mouvement.py.

- int,int:valPourMouvement(int:position_x, int:vitesse) : fonction qui donne au module
main les valeurs qu'il enverra a l'objet 'robot' comme le braquage des roues et
la vitesse des moteurs, en appelant differentes fonctions du module. Elle est
appelee avec la position absolue de la forme et la vitesse en ligne droite
du Robot.
"""

# On definie des valeurs significatives dans le domaine de definition de la
# variable position_x
width = 192
borne_droite = int(0.8*width)
borne_droit_max = int(0.55*width)
borne_droit_min = int(0.45*width)
borne_gauche = int(0.2*width)

# Des constantes qui correspondent a des types de virages
A_DROITE_SERRE = 2
A_DROITE = 1
A_GAUCHE = -1
A_GAUCHE_SERRE = -2
EN_FACE = 0


def centrexCamera(centre_x, camera_x) :
    """Cette fonction permet de recalculer centre_x par rapport a la position
    de la camera, c'est-a-dire : remettre centre_x dans l'axe initial du Robot.

    Prend en parametre :
    - int:centre_x : l'abscisse du centre geometrique
    - int:camera_x : la position de la camera lors de la photo dans laquelle on a
    trouve centre_x

    Retourne :
    - int:position_x : la position de centre_x par rapport au Robot.
    >    Plus position_x est grand, plus le ruban adhesif est a droite du Robot.
    >    L'inverse signifie que le ruban adhesif est a gauche du Robot.
    >    Si position_x est proche de 96, cela signifie que le ruban adhesif est
    en face du Robot"""

    position_x = int(centre_x-2.5*(camera_x-250))

    return position_x


def valPourCamera(position_x) :
    """Fonction qui donne la position que doit prendre la camera selon la
    derniere photo qui a ete prise, pour eviter de perdre le circuit.

    Prend un parametre :
    - int:position_x : la position de l'abscisse du centre de la forme en
    prenant en compte le fait que la camera est tournee ou non

    Renvoie une valeur :
    - int:camera_x : la position que doit prendre le servo X de la camera
    """
    if position_x < 76 :
        if position_x > 48 :
            return 255
        elif position_x > -4 :
            return 265
        elif position_x > -40 :
            return 275
        else :
            return 290
    elif position_x > 116 :
        if position_x < 140 :
            return 245
        elif position_x < 188 :
            return 235
        elif position_x < 220 :
            return 225
        else :
            return 210
    else :
        return 250


def typeDeVirage(position_x) :
    """Fonction qui a partir du placement de la forme renvoie le type de
    virage.

    Prend un parametre :
    - int:position_x : entier resultant de la fonction centrexCamera.

    Renvoie une valeur :
    - type_virage : une constante qui correspond a un type de virage :
    >   virage a droite serre : 2,
    >   virage leger a droite : 1,
    >   tout droit : 0,
    >   virage leger a gauche : -1,
    >   virage a gauche serre : -2

    Une exception de type ValueError est levee si position_x n'est pas
    un entier."""

    try :
        position_x = int(position_x)
    except ValueError :
        print("La valeur de centre_x n'est pas exploitable.")

    # Virage a droite
    if (position_x > borne_droit_max) :
        if (position_x >= borne_droite) :
            return A_DROITE_SERRE
        else :
            return A_DROITE

    # Virage a gauche
    elif (position_x < borne_droit_min) :
        if (position_x <= borne_gauche) :
            return A_GAUCHE_SERRE
        else :
            return A_GAUCHE

    # Trajectoire rectiligne
    elif (position_x <= borne_droit_max) and (position_x >= borne_droit_min) :
        return EN_FACE


def inclinaisonRoues(type_virage, position_x) :
    """Fonction qui a partir d'un type de virage donne par typeDeVirage
    et la position exacte de la forme analysee dans l'image, renvoie le
    braquage des roues avant a adopter.

    Prend deux parametres :
    - int:type_virage : un entier entre -2 et 2 correspondant a un type de
    virage
    - int:position_x : entier resultant de centrexCamera()

    Renvoie un entier :
    - int:inclinaison : le braquage associe au type de virage"""

    # On definie les bornes des valeurs a envoyer a set_pwm pour tourner
    # les roues dans la fonction tourner() de la classe Robot (module mouvement)
    roues_a_droite_max = 270
    roues_a_gauche_max = 190
    roues_droites = int((roues_a_droite_max+roues_a_gauche_max)/2)

    try :
        if type_virage == A_DROITE_SERRE:
            return roues_a_droite_max

        elif type_virage == A_DROITE :
            # Taille de l'intervalle dans lequel les roues doivent tourner
            # a droite proportionnellement a position_x
            taille_interv_roues = roues_a_droite_max - roues_droites
            # Taille de l'intervalle des valeurs de position_x, pour lequel
            # on doit tourner a droite proportionnellement
            taille_interv_centre_x = borne_droite - borne_droit_max
            # Braquage des roues adapte
            inclinaison = int((taille_interv_roues)*(((borne_droite)-position_x)/(taille_interv_centre_x))+roues_droites)
            return inclinaison

        elif type_virage == A_GAUCHE_SERRE :
            return roues_a_gauche_max

        elif type_virage == A_GAUCHE:
            # Taille de l'intervalle dans lequel les roues doivent
            # tourner a gauche proportionnellement a position_x
            taille_interv_roues = roues_droites - roues_a_gauche_max
            # Taille de l'intervalle des valeurs de position_x, pour lequel
            # on doit tourner a droite proportionnellement
            taille_interv_centre_x = borne_droit_min - borne_gauche
            # Braquage des roues adapte
            inclinaison = int((taille_interv_roues)*(((borne_droit_min)-position_x)/(taille_interv_centre_x))+roues_a_gauche_max)
            return inclinaison

        elif type_virage == EN_FACE :
            return roues_droites

        else :
            raise ValueError("Type de virage inconnu")

    except ValueError as e :
        print(e)



def vitesseMoteurs(type_virage, vitesse) :
    """Fonction qui a partir du type de virage, renvoie la vitesse a
    adopter par les moteurs.

    Prend en parametres :
    - int:type_virage : un entier entre -2 et 2 correspondant a un type de
    virage
    - int:vitesse : la vitesse du robot pour les trajectoires rectilignes

    Renvoie une valeur :
    - vitesse_ideale : un entier correspondant a la valeur que prendront
    les fonctions qui configurent la vitesse des moteurs
    """

    vitesse_min = 1300
    vitesse_max = 2500

    if type_virage == A_DROITE_SERRE or type_virage == A_GAUCHE_SERRE:
        vitesse_ideale = int(vitesse*(0.80))

    elif type_virage == A_DROITE or type_virage == A_GAUCHE :
        vitesse_ideale = int(vitesse*(0.90))

    # Roues dans l'axe (aller tout droit)
    elif type_virage == EN_FACE :
        vitesse_ideale = vitesse


    # Attention, les valeurs de vitesse ne peuvent pas etre plus grandes ou
    # plus petites que certaines valeurs
    if vitesse_ideale < vitesse_min :
        vitesse_ideale = vitesse_min
    if vitesse_ideale > vitesse_max :
        vitesse_ideale = vitesse_max

    return vitesse_ideale



def valPourMouvements(position_x, vitesse) :
    """Se sert des fonctions du module pour, quand elle est appelee par main
    avec position_x et la vitesse en argument, renvoyer un tuple contenant
    les valeurs utilisees par la methode robot.tourner() de mouvement.py.

    Prend en parametre :
    - int:position_x : represente la position du circuit par rapport au robot
    - int:vitesse : la vitesse choisie pour une trajectoire rectiligne par
    l'utilisateur dans main.py

    Renvoie deux valeurs :
    - int:inclinaison : le braquage optimal des roues avant
    - int:vitesse : la vitesse optimale des moteurs a cet instant"""

    type_virage = typeDeVirage(position_x)

    inclinaison = inclinaisonRoues(type_virage, position_x)

    vitesse = vitesseMoteurs(type_virage, vitesse)

    return inclinaison, vitesse
