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
import sys
sys.path.append('D:\WpSystem\S-1-5-21-992357890-2830550148-1038233672-1001/AppData/Local/Packages/PythonSoftwareFoundation.Python.3.9_qbz5n2kfra8p0/LocalCache/local-packages/Python39/site-packages')

face_cascade = cv.CascadeClassifier(
    cv.data.haarcascades + 'haarcascade_frontalface_alt.xml')


face_encoder = dlib.face_recognition_model_v1(
    'dlib_face_recognition_resnet_model_v1.dat')
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
detector = dlib.get_frontal_face_detector()
pose_predictor_68_point = dlib.shape_predictor(
    "shape_predictor_68_face_landmarks.dat")


# liste contenant les noms des personnes detectées sur la photos
galerie = []


# fonction qui prend en paramètre une image et qui retourne la liste des personnes présentent sur cette image
def newFaces(i):

    imA = cv.imread(i)
    imB = cv.imread(i)

    cv.imshow("img", imA)
    cv.waitKey(0)

    imG = cv.cvtColor(imA, cv.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(imG)
    for (x, y, w, h) in faces:
        cv.rectangle(imA, (x, y), (x+w, y+h), (255, 255, 0), 2)

    if (len(faces) >= 0):
        message = 'visage(s) detecte(s)'
        cv.putText(imA, message, (1, 30),
                   cv.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))

    cv.imshow("img", imA)
    cv.waitKey(0)

    i = 0
    for (x, y, w, h) in faces:

        crop_img = imB[y:y+h+12, x:x+w+12]

        cv.imshow('image', crop_img)
        cv.waitKey(0)

        name = input("Entrez le nom de la personne")
        first_name = input("Entrez le prenom de la personne")
        cv.imwrite(name + "_" + first_name, crop_img)

        print('image recadré enregistrée')

        galerie.append(name + "_" + first_name)

        i += 1
    return galerie



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
            np.array(face_encoder.compute_face_descriptor(image, landmarks)))

    return (face_encoding_list, faces, landmarks_list)


# fonction qui prend en paramètre une liste de visages encodés, une liste de visage (image) et une liste de landmarks
# et qui les compare à l'image renseigné en paramètre de la fonction
# calcule la différence des normes entre les deux vecteurs des deux images, en fonction du résultat et de la marge d'erreur (tolérence)
# indique si le visage en paramètre et celui analysé sont les même ou pas
def comparImage(face_encoding_list, faces, landmarks_list, imageChoisis):

    try:
        face_encoding_list = face_encoding_list[0].reshape(
            face_encoding_list[0].shape[0], 1)
        face_encoding_list_known, face_known, landmarks_know = analyzeFace(
            cv.imread(imageChoisis))

        face_encoding_list_known = face_encoding_list_known[0].reshape(
            face_encoding_list_known[0].shape[0], 1)
        vectors = np.linalg.norm(face_encoding_list_known - face_encoding_list)
        print(vectors)
        tolerance = 0.6
        if (vectors <= tolerance):
            print("[INFO] Même personne que l'image choisis")
        else:
            print("[INFO] Personne différente")

    except IndexError:

        print("[INFO] Pas de visage(s) détecté(s)")

#fonction qui permet de comparer les visages de la webcam à ceux sur l'image choisis par l'utilisateur
def identify():
    imageChoisis = input(
        "écrivez le nom de l'image que vous voulez comparez \n avec la personne devant votre webcam : ")
    print('[INFO] Starting Webcam')
    webcam = cv.VideoCapture(0)
    # pour recuperer le flux video et pas seulement une photo
    while True:
        ret, frame = webcam.read()
        rgb_small_frame = frame[:, :, ::-1]

        # on analyse les images de la webcam afin de voir si un visage est présent,
        # si c'est le cas, ce dernier, un vecteur le caractérisant ainsi que les landmarks sont retournés
        face_encoding_list_unknown, faces_unknown, landmarks_list_unknows = analyzeFace(
            rgb_small_frame)

        # on injecte les données de la webcam dans les fonctions d'identification
        comparImage(face_encoding_list_unknown, faces_unknown,
                    landmarks_list_unknows, imageChoisis)
        cv.imshow('Identification', frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    webcam.release()
    cv.destroyAllWindows()
