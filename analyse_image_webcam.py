# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 12:23:36 2020

@author: Rayane Jay Bencharef
"""
# import des dépendances
from imutils import face_utils
import numpy as np
import dlib
import cv2 as cv

face_cascade = cv.CascadeClassifier(
    cv.data.haarcascades + 'haarcascade_frontalface_alt.xml')


face_encoder = dlib.face_recognition_model_v1(
    'dlib_face_recognition_resnet_model_v1.dat')
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
detector = dlib.get_frontal_face_detector()
pose_predictor_68_point = dlib.shape_predictor(
    "shape_predictor_68_face_landmarks.dat")


# fonction qui prend en paramètre une image,
# detetecte les visages sur l'images, repère les landmarks, calcule un ou des vecteur(s) qui décrit/décrivent le ou les visages détectés
# retourne une liste de visages encodés, une liste de visage (image) et une liste de landmarks
def analyzeFace(image):
    face_encoding_list = []
    landmarks_list = []

    faces = detector(image, 1)

    for face in faces:

        grey = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        landmarks = predictor(grey, face)
        landmarks_list.append(face_utils.shape_to_np(landmarks))
        # calcule un vecteur de 128 de dimension qui décrit le visage
        face_encoding_list.append(
            np.array(face_encoder.compute_face_descriptor(image.astype(np.uint8), landmarks)))

    return (face_encoding_list, faces, landmarks_list)


# fonction qui prend en paramètre une liste de visages encodés, une liste de visage (image) et une liste de landmarks
# et qui les compare à l'image renseigné en paramètre de la fonction
# calcule la différence des normes entre les deux vecteurs des deux images, en fonction du résultat et de la marge d'erreur (tolérence)
# indique si le visage en paramètre et celui analysé sont les même ou pas
def comparImage(face_encoding_list, faces, landmarks_list, imageChoisis):
    msg=""
    try:
        face_encoding_list = face_encoding_list[0].reshape(
            face_encoding_list[0].shape[0], 1)
        face_encoding_list_known, face_known, landmarks_know = analyzeFace(
            cv.imread('img/'+imageChoisis))

        face_encoding_list_known = face_encoding_list_known[0].reshape(
            face_encoding_list_known[0].shape[0], 1)
        vectors = np.linalg.norm(face_encoding_list_known - face_encoding_list)
        print(vectors)
        tolerance = 0.6
        if (vectors <= tolerance):
            msg="[INFO] Meme personne que l'image choisis"
            print(msg)

        else:
            msg="[INFO] Personne differente"
            print(msg)
            
    #Afin d'éviter une erreur lorsqu'il n'y a pas de visage devant la webcam
    except IndexError:
        msg = "[INFO] Pas de visage(s) detecte(s)"
        print(msg)
    return msg

#fonction qui permet de comparer les visages de la webcam à ceux sur l'image choisis par l'utilisateur
def identify():
    im_verif=False
    while im_verif==False:
        try:
            imageChoisis = input(
            "écrivez le nom de l'image du dossier img que vous voulez comparez \n avec la personne devant votre webcam : ")
            im=cv.imread("img/"+imageChoisis)
            if type(im)==np.ndarray:
                im_verif=True
            cv.imshow(im)
            cv.waitKey(100)
            
        except:
            print("L'image choisis n'a pas pu être ouverte, \nêtes vous sûr que l'image choisie se situe dans le dossier 'img'")
            
    print('[INFO] Starting Webcam')
    webcam = cv.VideoCapture(0)
    # pour recuperer le flux video et pas seulement une photo
    while True:
        ret, frame = webcam.read()
        rgb_small_frame = frame[:, :, ::-1]

        # on analyse les images de la webcam afin de voir si un visage est présent,
        # si c'est le cas, ce dernier, un vecteur le caractérisant ainsi que les landmarks sont retournés
        face_encoding_list_unknown, face_unknown, landmarks_list_unknows = analyzeFace(
            rgb_small_frame)

        # on injecte les données de la webcam dans les fonctions d'identification
        msg = comparImage(face_encoding_list_unknown, face_unknown,
                    landmarks_list_unknows, imageChoisis)
        
        if len(landmarks_list_unknows) > 0:
            for (x, y) in landmarks_list_unknows[0]:
                cv.circle(frame, (x, y), 1, (0, 0, 255), -1)

        cv.rectangle(frame, (0, frame.shape[1]-250), ( frame.shape[0]-100, frame.shape[1]), (0,0,0), -1)
        cv.putText(frame, msg,  (0,int((frame.shape[1]-200))), cv.FONT_HERSHEY_SIMPLEX, 0.4,(255, 255, 255))
        cv.imshow('Identification', frame)
        
        #condition afin de fermer la webcam
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    webcam.release()
    cv.destroyAllWindows()
