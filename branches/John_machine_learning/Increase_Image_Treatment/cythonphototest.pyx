import cv2
import matplotlib as pl
import numpy as np
import matplotlib
import cython
import time

xsum1, xsum2, ysum1, ysum2, acc = 0,0,0,0,0
path ="C:/Users/allou/Desktop/L3Q1/L3Q1projetwc/trunk/Ressources/images/Frame4.jpg"
norm_photo = cv2.imread(path,cv2.IMREAD_ANYCOLOR)
photo = cv2.resize(norm_photo,(200,200),interpolation=cv2.INTER_AREA)

height = np.size(photo, 0)
width = np.size(photo, 1)
x_med_screen = width //2
y_med_screen = height
@cython.cfunc
@cython.boundscheck(False)
cpdef mainfonction(xsum1, xsum2, ysum1, ysum2, acc,height,width,photo):

    start = time.time()
    gray = cv2.cvtColor(photo, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 75, 100)


    # or
    #width = camera.get(3)  # float
    #height = camera.get(4)  # float

    lines = cv2.HoughLines(edges, 1, np.pi/180, 50)


    for x in range(0, 3):  # Parcours des 4 premieres lignes detectees dans l'image, c'est un echantillon assez representatif
        for rho, theta in lines[x]:  # Les instructions suivantes permettent le calcul de deux points de la ligne etudie
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000 * (-b))  # x1, x2, y1, y2 sont les coordonnees des points de la ligne actuellement etudiee
            y1 = int(y0 + 1000 * (a))
            x2  = int(x0 - 1000 *(-b))#1000 représente la longeur
            y2 = int(y0 - 1000 * (a))
            cv2.line(photo, (x1, y1), (x2, y2), (255, 255, 255), 2)  # On trace la ligne etudiee sur l'image de depart
            xsum1 += x1
            xsum2 += x2
            ysum1 += y1
            ysum2 += y2
            acc += 1
    xsum1 = xsum1 / acc  # Calculs des coordonnees des points de la droite jaune directrice et mediane
    xsum2 = xsum2 / acc
    ysum1 = ysum1 / acc
    ysum2 = ysum2 / acc
    a = (ysum2 - ysum1) / (xsum2 - xsum1)  # a est le coefficient directeur de la droite mediane
    mediane = cv2.line(photo, (int(xsum1), int(ysum1)), (int(xsum2), int(ysum2)), (0, 255, 255), 2)  # On trace la ligne mediane
    milieu = cv2.line(photo,((width//2),0),(width//2,height),(0,0,0),3)

    position = intersection(xsum1,xsum2,ysum1,ysum2
                            )
    point_intersection = cv2.circle(photo,(int(position[0]), int(position[1])),10,(0,255,0),-1)
    if int(position[1]) < 3*height//4 and point_intersection.any():
        cv2.line(photo,(0,int(position[1])),(width,int(position[1])),(0,255,0),3)
        print("ACTION A REALISER")


    end = time.time()
    print(end-start)
    cv2.imshow("Photo",photo)
    cv2.imshow("Edges", edges )
    cv2.waitKey(0)
    cv2.destroyAllWindows()
@cython.cfunc
cdef intersection(xsum1,xsum2,ysum1,ysum2):
    eq = ((x_med_screen- x_med_screen) * (int(xsum1) - 0) - (y_med_screen - 0) * (int(xsum1) - width // 2)) / (
            (y_med_screen - 0) * (int(xsum2) - int(xsum1)) - (x_med_screen - x_med_screen) * (int(ysum2) - int(ysum1)))
    """(X4 - X3)*(Y1*Y3) (Y4-Y3) * (X1-X3) / (Y4-Y3)*(X2-X1) - (X4-X3)*(Y2-Y1)"""
    pos_x = int(xsum1) + eq * (int(xsum2) - int(xsum1))
    pos_y = int(ysum1) + eq * (int(ysum2) - int(ysum1))
    return pos_x,pos_y
