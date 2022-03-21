"""Ce module permet d'applique les fondements de centroid detector
    sur une image défini
    Permet également de determiner sa vitesse de traitement d'image"""
#---IMPORT---#
import cv2
import image
import time
import numpy as np
#------------#

path = "C:/Users/allou/Desktop/L3Q1/L3Q1projetwc/trunk/Ressources/images/Frame3.jpg"
path2 = "C:/Users/allou/Desktop/L3Q1/L3Q1projetwc/trunk/Ressources/images/Frame6.jpg"
path_left = "C:/Users/allou/PycharmProjects/motorproject/imgtypefile/image_type_left/30.png"
path_right = "C:/Users/allou/PycharmProjects/motorproject/imgtypefile/image_type_right/24.png"
path3 = "C:/Users/allou/Desktop/L3Q1/L3Q1projetwc/branches/John_machine_learning/image_type_file/image_type_left/1.png"

photo = cv2.imread(path3,cv2.IMREAD_ANYCOLOR)
height = np.size(photo, 0)
width = np.size(photo, 1)
def chrono_time():
    """Retourne le temps passé à chaque appelle"""
    return time.time()
def traitement_image(photo):
    """Prend en paramètre une image et renvoie
    les coordonnées du centre de l'image si elle existe"""
    masque = image.color_treatment(photo)
    pos_centre = image.centroidDetector(masque)
    return pos_centre
def calcul_pos(photo):
    masque = image.color_treatment(photo)
    extrem_pos = image.extrem_pos(masque)
    return  extrem_pos


start = chrono_time()
masque = image.color_treatment(photo) #JUSTE EN TEST
pos_centre = traitement_image(photo)
extrem_pos = image.find_extrem_pos(masque)

def contourcont(masque,photo):
    contours, hierarchy = cv2.findContours(masque, 1, cv2.CHAIN_APPROX_SIMPLE)
    approx = None
    for cnt in contours:
        # plus 0.01 est > moins il comptera de point
        approx = cv2.approxPolyDP(cnt, 0.03 * cv2.arcLength(cnt, True), True)
        cv2.drawContours(photo,[approx],0,(0),5)
    if len(approx) == 4:
        print("carré")
    if len(approx) == 5:
        print("angle interne")
    if len(approx) == 6:
        print("angle angle externe")
    print(len(approx))
contourcont(masque,photo)

max_left = extrem_pos[0]
max_right = extrem_pos[1]
max_top = extrem_pos[2]
max_bottom = extrem_pos[3]

cv2.circle(photo,max_left,7,(220,225,0),-1)
cv2.circle(photo,max_right,7,(220,225,0),-1)
cv2.circle(photo,max_top,7,(220,225,0),-1)
cv2.circle(photo,max_bottom,7,(220,225,0),-1)

print("Les positions maximales sont  :")
print(max_left,max_right,max_top,max_bottom)

if pos_centre is not False:
    # On affiche l'abscisse du centre
    print("centre_x = ", pos_centre[0])
    cv2.circle(photo,(pos_centre),10,(220,0,0),-1)
end = chrono_time()
print("La vitesse du traitement de l'image correspond à :{}".format(end-start))

#-------------------------
#x,y,z =0,0,0
imagecolor = photo[width//2,height//2,]
def getBGRcolor(photo):
    """Prend en paramètre une photo :
    Permet d'avoir la couleur la plus presente au centre
    de l'image"""
    value = photo[width//2,height//2]
    max = 10
    value_x,value_y,value_z = 0,0,0
    med = []
    for i in range(0,max):
        for j in range (0,max):
            value = photo[width//2+i,height//2+j]
            value_x += value[0]
            value_y += value[1]
            value_z += value[2]
    value_x = (value_x // (max*max))
    value_y = (value_y // (max*max))
    value_z = (value_z // (max*max))
    med = [value_x, value_y, value_z]
    return med


print("la taille de l'image est {}".format(photo.shape))
print("la valeur BGR du pixel au centre de l'image est {}".format(imagecolor))
print("La couleur la plus presente dans l'image est :{}".format(getBGRcolor(photo)))
#---------------------------
med_color = getBGRcolor(photo)
def dominentColor(tabcolor):
    """prend un paramètre un tableau de couleur
        et renvoie sa couleur la plus dominante"""
    blue = 'blue'
    green = 'green'
    red = 'red'; noir = 'noir'; jaune = 'jaune';
    #tab[0] correspond à

    if tabcolor[0] < 50 and tabcolor[1] < 50 and tabcolor[2] < 50:
        return noir
    if tabcolor[0] < 50 and tabcolor[1] > 120 and tabcolor[2] > 120:
        return jaune
    elif max(tabcolor[0],tabcolor[1],tabcolor[2]) == tabcolor[0]:
        return blue
    elif max(tabcolor[0],tabcolor[1],tabcolor[2]) == tabcolor[1]:
        return green
    elif max(tabcolor[0],tabcolor[1],tabcolor[2]) == tabcolor[2]:
        return red

maxvalue = dominentColor(med_color)
print("la couleur la plus présente est {}".format(maxvalue))
#------------------------------------------


color_available = ['rouge','noir','jaune']
def getcolorUser():
    """Permet à l'utilisateur d'inserer une couleur parmis celle disponible"""
    color = input("Veuillez inserrer une couleur parmis {} :".format(color_available))
    try :
        color = color.lower()
        return color
    except ValueError:
        print("Erreur lors de l'insertion")
#----------------------------------------
def mainfonction():
    """Fonction principale du programme"""
    while True :
        cv2.imshow("Photo",photo)
        cv2.imshow("Masque",masque)
      #cv2.imshow("masque",masque)
        key = cv2.waitKey(1)
        if key & 0xFF == ord("q"):  # quitter
            break
if __name__ == '__main__':
    """Main de la fonction"""

    #couleur_choisie = getcolorUser()
    #print(couleur_choisie)
    mainfonction()
    cv2.destroyAllWindows()
