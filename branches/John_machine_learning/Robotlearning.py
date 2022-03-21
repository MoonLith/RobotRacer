
"""Programme permettant de prendre des photos afin de
réaliser une base donnée ainisi que différente fonction
réalisant les 3 étapes coeur du machine learning,
 préprocessing, testing, prediction"""

#Importation LIB
#-------------------------
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import time
#preprocessing
from glob import glob
from keras import preprocessing
#list array preprocessing
from keras.utils import to_categorical
#testing phase
from keras.models import Sequential
from keras.layers.core import Activation,Dropout, Flatten, Dense
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.optimizers import Adam
#---------------------------------


camera = cv.VideoCapture(0)
camera_height = 500
type_name = ["CENTER","LEFT","RIGHT","END","START"]
#FRAME TYPE INITIALISATION
frame_type_center = []
frame_type_left = []
frame_type_right = []
frame_type_end = []
frame_type_start = []

def take_pic_type():
    """Cette fonction permet de prendre des photos
    ainsi que des categorieser"""

    while True :
        _, frame =  camera.read()
        # RESCALING de l'image
        aspect = frame.shape[1]/frame.shape[0]
        res = int (aspect * camera_height)
        frame = cv.resize(frame, (res, camera_height))

        cv.rectangle(frame, (180, 75), (530, 425), (255, 0, 0), 2)

        cv.imshow("Capturing Image", frame)

        #--------------------------
        key = cv.waitKey(1)
        if key & 0xFF == ord("q"):#quitter
            break
        elif key & 0xFF == ord("1"):#touche 1
            frame_type_center.append(frame)
            print("Key 1 pressed saved Type Center")
        elif key & 0xFF == ord("2"):#touche 2
            frame_type_left.append(frame)
            print("Key 2 pressed saved Type Left")
        elif key & 0xFF == ord("3"):#touche 3
            frame_type_right.append(frame)
            print("Key 3 pressed saved Type Right")
        elif key & 0xFF == ord("4"):#touche 4
            frame_type_end.append(frame)
            print("Key 4 pressed saved Type End")
        elif key & 0xFF == ord("5"):#touche 5
            frame_type_start.append(frame)
            print("Key 5 pressed saved Type Start")
        #--------------------------------

    camera.release()
    cv.destroyAllWindows()

take_pic_type()

save_width = 200 #très important
save_height = 200
start = time.time()
#enregistrer les images de début

#def save_test(frametype):
    #for i, frame in enumerate(frametype):
        #roi = frame[75+2:425-2, 180+2:530-2]
        #roi = cv.cvtColor(roi, cv.COLOR_BGR2RGB)
        #roi = cv.resize(roi, (save_width,save_height))
        #cv.imwrite('C:\\Users\\allou\\PycharmProjects\\motorproject\\imgtypefile\\'+str(image_type_start)+'/{}.png'.format(i),
                   #cv.cvtColor(roi, cv.COLOR_BGR2RGB))


def save_file_type():
    """Permet de sauvegarder les images catégorisé
      dans leur dossier respectif
    """
    for i, frame in enumerate(frame_type_start):
        roi = frame[75+2:425-2, 180+2:530-2]#determine quelle partie de la frame est rogné
        roi = cv.cvtColor(roi, cv.COLOR_BGR2RGB)#changement de couleur
        roi = cv.resize(roi, (save_width,save_height))#resize permet un traitement plus rapide
        cv.imwrite('C:\\Users\\allou\\PycharmProjects\\motorproject\\imgtypefile\\image_type_start/{}.png'.format(i),
                   cv.cvtColor(roi, cv.COLOR_BGR2RGB))
    #enregistrer les images d'arret
    for i, frame in enumerate(frame_type_end):
        roi = frame[75+2:425-2, 180+2:530-2]
        roi = cv.cvtColor(roi, cv.COLOR_BGR2RGB)
        roi = cv.resize(roi, (save_width,save_height))
        cv.imwrite('C:\\Users\\allou\\PycharmProjects\\motorproject\\imgtypefile\\image_type_end/{}.png'.format(i),
                   cv.cvtColor(roi, cv.COLOR_BGR2RGB))
    #enregistrer les images de gauche
    for i, frame in enumerate(frame_type_left):
        roi = frame[75+2:425-2, 180+2:530-2]
        roi = cv.cvtColor(roi, cv.COLOR_BGR2RGB)
        roi = cv.resize(roi, (save_width,save_height))
        cv.imwrite('C:\\Users\\allou\\PycharmProjects\\motorproject\\imgtypefile\\image_type_left/{}.png'.format(i),
                   cv.cvtColor(roi, cv.COLOR_BGR2RGB))

    #enregistrer les images de droite
    for i, frame in enumerate(frame_type_right):
        roi = frame[75+2:425-2, 180+2:530-2]
        roi = cv.cvtColor(roi, cv.COLOR_BGR2RGB)
        roi = cv.resize(roi, (save_width,save_height))
        cv.imwrite('C:\\Users\\allou\\PycharmProjects\\motorproject\\imgtypefile\\image_type_right/{}.png'.format(i),
                   cv.cvtColor(roi, cv.COLOR_BGR2RGB))
    #Enregistrer les images de centre
    for i, frame in enumerate(frame_type_center):
        roi = frame[75+2:425-2, 180+2:530-2]
        roi = cv.cvtColor(roi, cv.COLOR_BGR2RGB)
        roi = cv.resize(roi, (save_width,save_height))
        cv.imwrite('C:\\Users\\allou\\PycharmProjects\\motorproject\\imgtypefile\\image_type_center/{}.png'.format(i),
                   cv.cvtColor(roi, cv.COLOR_BGR2RGB))
save_file_type()

#load image :
width = 200
height = 200
image_type_center = []
image_type_left = []
image_type_right = []
image_type_end = []
image_type_start = []


def load_file_type():
    """Permet de charger les images
       pour la phase de preprocessing """
    for image_path in glob("C:/Users/allou/PycharmProjects/motorproject/imgtypefile/image_type_center/*.*"):
        image = preprocessing.image.load_img(image_path,
                                             target_size=(width, height))
        x = preprocessing.image.img_to_array(image)#preprocessing del'image en tab de couleur 0,255
        image_type_center.append(x)#ajoute l'image dans la liste
    print(image_type_center)


    for image_path in glob("C:/Users/allou/PycharmProjects/motorproject/imgtypefile/image_type_left/*.*"):
        image = preprocessing.image.load_img(image_path,
                                             target_size=(width, height))
        x = preprocessing.image.img_to_array(image)
        image_type_left.append(x)


    for image_path in glob("C:/Users/allou/PycharmProjects/motorproject/imgtypefile/image_type_right/*.*"):
        image = preprocessing.image.load_img(image_path,
                                             target_size=(width, height))
        x = preprocessing.image.img_to_array(image)
        image_type_right.append(x)


    for image_path in glob("C:/Users/allou/PycharmProjects/motorproject/imgtypefile/image_type_end/*.*"):
        image = preprocessing.image.load_img(image_path,
                                             target_size=(width, height))
        x = preprocessing.image.img_to_array(image)
        image_type_end.append(x)


    for image_path in glob("C:/Users/allou/PycharmProjects/motorproject/imgtypefile/image_type_start/*.*"):
        image = preprocessing.image.load_img(image_path,
                                             target_size=(width, height))
        x = preprocessing.image.img_to_array(image)
        image_type_start.append(x)
load_file_type()

#plt.figure(figsize= (12,8))
#Show image by type, ici type = 0
#for i, x in enumerate (frame_type_center[:3]):
        #plt.subplot(1,3, i+1)
        #image = preprocessing.image.array_to_img(x)
        #plt.imshow(image)
        #plt.axis('off')
        #plt.title('{} image'.format(type_name[0]))
end = time.time()
print(end-start)
plt.show()

#prepare image as tensor pour le mode de machine learning
X_type_image_center = np.array(image_type_center)
X_type_image_left = np.array(image_type_left)
X_type_image_right = np.array(image_type_right)
X_type_image_end = np.array(image_type_end)
X_type_image_start = np.array(image_type_start)


print(X_type_image_center.shape)
print(X_type_image_left.shape)
print(X_type_image_right.shape)
print(X_type_image_end.shape)
print(X_type_image_start.shape)



#concatene les images dans une liste
X = np.concatenate((X_type_image_center, X_type_image_left),axis=0)
if len(X_type_image_right):
    X = np.concatenate((X, X_type_image_right), axis=0)
if len(X_type_image_end):
    X = np.concatenate((X, X_type_image_end), axis=0)
if len(X_type_image_start):
    X = np.concatenate((X, X_type_image_start), axis=0)

X = X //255


Y_type_image_center = [0 for item in enumerate(X_type_image_center)]
Y_type_image_left =[1 for item in enumerate(X_type_image_left)]
Y_type_image_right = [2 for item in enumerate(X_type_image_right)]
Y_type_image_end = [3 for item in enumerate(X_type_image_end)]
Y_type_image_start = [4 for item in enumerate(X_type_image_start)]


Y = np.concatenate((Y_type_image_center, Y_type_image_left), axis=0)

if len(Y_type_image_right):
    Y = np.concatenate((Y, Y_type_image_right), axis=0)

if len(Y_type_image_end):
    Y = np.concatenate((Y, Y_type_image_end), axis=0)

if len(Y_type_image_start):
    Y = np.concatenate((Y, Y_type_image_start), axis=0)

Y = to_categorical(Y, num_classes = len(type_name))

print(Y.shape)
print(Y)

#phase de test
conv_1 = 16
conv_1_drop = 0.2
conv_2 = 32
conv_2_drop = 0.2
dense_1_n = 1024
dense_1_drop = 0.2
dense_2_n = 512
dense_2_drop = 0.2

lr = 0.001

epochs = 30
batch_size = 32
color_channel = 3

def build_model(conv_1_drop = conv_1_drop, conv_2_drop = conv_2_drop,
                dense_1_n = dense_1_n, dense_1_drop = dense_1_drop,
                dense_2_n = dense_2_n, dense_2_drop = dense_2_drop,
                lr = lr):
    """Cette fonction permet de réaliser la phase de test,
    retournant donc un model ayant une marge de précision et d'erreur"""
    model = Sequential()
    model.add(Convolution2D(conv_1,(3,3),
                            input_shape = (width,height,color_channel),
                            activation = 'relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))
    model.add(Dropout(conv_1_drop))

    model.add(Convolution2D(conv_2,(3,3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))
    model.add(Dropout(conv_2_drop))

    model.add(Flatten())

    model.add(Dense(dense_1_n, activation='relu'))
    model.add(Dropout(dense_1_drop))

    model.add(Dense(dense_2_n, activation='relu'))
    model.add(Dropout(dense_2_drop))

    model.add(Dense(len(type_name), activation='softmax'))

    model.compile(loss='categorical_crossentropy',
                  optimizer=Adam(lr=lr),
                  metrics=['accuracy'])
    return model


np.random.seed(1)

model = build_model()
model.summary()
epochs = 20
model.fit(X, Y, epochs = epochs)

#type_center = preprocessing.image.load_img("C:/Users/allou/PycharmProjects/motorproject/imgtypefile/image_type_center/0.png"
                                           #,target_size=(width,height))

#type_center_X = np.expand_dims(type_center, axis=0)
#type_center_pred = model.predict(type_center_X)
# print(type_name[np.argmax(type_center_pred)])
#plt.imshow(type_center)
#plt.show()


def mainfonction():
    """fonction principale du programme et etape de prédiction en temps réel"""
    camera = cv.VideoCapture(0)

    while True :
        _, frame = camera.read()
        frame = cv.flip(frame, 1)
        aspect = frame.shape[1] / frame.shape[0]
        res = int(aspect * camera_height)
        frame = cv.resize(frame, (res, camera_height))
        cv.rectangle(frame, (180, 75), (530, 425),(255,100,0),2)

        #paramétrage de l'image----
        roi = frame[75+2:425-2, 180+2:530-2]
        roi = cv.cvtColor(roi, cv.COLOR_BGR2RGB)
        roi = cv.resize(roi, (width, height))
        #--------------------

        #prediction--
        roi_X = np.expand_dims(roi, axis=0)
        predictions = model.predict(roi_X)
        type_center_pred, type_left_pred, type_right_pred, type_end_pred,type_start_pred = predictions[0]
        #----------


        #text mis à jour en temps réel sur la correspondance de la frame
        #par rapport à la base de donnée
        #-------------------------------------
        type_center_text = '{}: {}%'.format(type_name[0], int (type_center_pred*100))
        cv.putText(frame,type_center_text,(70,180), cv.FONT_HERSHEY_SIMPLEX, 0.6,
                   (240,240,240),2)

        type_left_text = '{}: {}%'.format(type_name[1], int(type_left_pred * 100))
        cv.putText(frame, type_left_text, (70, 200), cv.FONT_HERSHEY_SIMPLEX, 0.6,
                   (240, 240, 240), 2)

        type_right_text = '{}: {}%'.format(type_name[2], int(type_right_pred * 100))
        cv.putText(frame, type_right_text, (70, 220), cv.FONT_HERSHEY_SIMPLEX, 0.6,
                   (240, 240, 240), 2)

        type_end_text = '{}: {}%'.format(type_name[3], int(type_end_pred * 100))
        cv.putText(frame, type_end_text, (70, 240), cv.FONT_HERSHEY_SIMPLEX, 0.6,
                   (240, 240, 240), 2)

        type_start_text = '{}: {}%'.format(type_name[4], int(type_start_pred * 100))
        cv.putText(frame, type_start_text, (70, 260), cv.FONT_HERSHEY_SIMPLEX, 0.6,
                   (240, 240, 240), 2)
        #---------------------------------------

        cv.imshow("Test Machine Learning", frame)

        key = cv.waitKey(1)

        if key & 0xFF == ord('q'):
            break
    camera.release()
    cv.destroyAllWindows()

if __name__ == '__main__':
    mainfonction()