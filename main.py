from analyse_image_webcam import *
from analyzerFaces import *



#fonction qui permet à l'utilisateur de choisir ce qu'il veut faire 
def menu():
    choice=0
    print("Pour ajouter une image tapez 1 \nPour identifier une personne devant la webcam tapez 2 \nPour arreter le programme tapez 3 ")  
    while choice!=1 | choice!=2:
        choice=int(input("Vous voulez : "))
        if choice==1:
            i=input("Entrez le nom du fichier:")
            newFaces(i)
        elif choice==2:
            print("Pour arretez le programme tapez q lorsque la fenêtre de la webcam est ouverte ")
            identify()
        elif choice==3:
            break
        else:
            print("Vous devez uniquement tapez 1 ou 2")
            menu()

#lancement du programme
menu()
