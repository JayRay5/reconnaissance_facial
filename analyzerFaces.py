# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 12:23:36 2020

@author: Rayane Jay Bencharef
"""



import cv2 as cv
#import du modèle
face_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_alt.xml')

#liste où seront stockés les noms des images à enregistrer
galerie=[]

#fonction qui prend une image en paramètre
#detecte les visages présents sur cette derniere et crée une nouvelle image pour chaque visage
def newFaces(i):
    try:
        imA=cv.imread("img_a_ajouter/"+i) 
        imB=cv.imread("img_a_ajouter/"+i)
    except:
        print("Le fichier rentré n'a pas pu être ouvert, \nvérifier qu'il se situe bien dans le dossier 'img_a_ajouter'")
        return 
    
    cv.imshow("img",imA)
    cv.waitKey(0)
    
    
    
    imG = cv.cvtColor (imA, cv.COLOR_BGR2GRAY)
    
    faces = face_cascade.detectMultiScale(imG) 
    for(x,y,w,h) in faces:
        
        cv.rectangle(imA,(x,y),(x+w,y+h),(255,255,0),2)

    
    message='visage(s) detecte(s)'
    cv.putText(imA,message, (1, 30), cv.FONT_HERSHEY_PLAIN,1,(0, 255, 0))
    cv.imshow("img",imA)
    cv.waitKey(0)
    global galerie
    i=0
    for (x, y, w, h) in faces:
    
        crop_img = imB[y:y+h+12, x:x+w+12]

        cv.imshow('image',crop_img)
        print("Fermez l'image pour enregistrer l'enregistrer")
        cv.waitKey(0)
        lastname=input("Entrez le nom de la personne : ")
        firstname=input("Entrez le prenom de la personne : ")
        face_name=lastname+"_"+firstname+".png"
        cv.imwrite('img/'+face_name,crop_img)
        print('[INFO]image recadré enregistrée')
        galerie.append(face_name)
        i+=1
    return galerie

    

  



