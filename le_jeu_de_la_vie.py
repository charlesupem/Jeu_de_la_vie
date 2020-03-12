#THOMAS Charles
#ROSSIGNOL Adelin
#Programme du jeu de la vie
from upemtk import *
from time import sleep

def init_plateau (nb_case):

    '''Initialise le plateau composé d'une liste de liste à 
    valeures initiales False.'''
    
    plateau = [[False]*nb_case]*nb_case 
        
    for i in range(1,nb_case):
        plateau[i]=plateau[i-1].copy()
        
    return plateau

def affichage_plateau(plateau):
    
    '''Dessine le plateau de jeu et permet le changement
     de couleur des cases.'''
     
    for i in range (len(plateau)):
        for j in range (len(plateau)):
            
            if plateau [i][j]:
                couleur ='black'
            else:
                couleur ='white'
                
            rectangle(50*i,50*j,50*(i+1),50*(j+1),couleur='black',remplissage=couleur)
            
def saisie_coord(saisie):
    '''Créer la liste des coordonnées des cellules vivantes initiales.'''
    
    coor_saisie=[]
    on = True 
    
    saisie_souris()
    iterations=input("Combien voulez vous d'itérations ? ")
    if iterations != 'inf':
        ite_intermediaires=str(input("Voulez-vous voir les itérations intermédiaires ? (o/n) "))
    else:
        ite_intermediaires = 'o'
    return iterations,ite_intermediaires

def pixel_vers_case(x,y):
    '''convertit les pixels vers l'unité des cases'''
    i=x//50
    j=y//50
    return (i,j)

def saisie_souris():
    '''Fonction gérant la saisie à la souris des cases initilaes'''
    
    var=True
    while var:
        coor_saisie=[]
        affichage_plateau(plateau)
        texte(0,0,compt_tour,couleur='red',taille=30)
        mise_a_jour()
        ev = donne_ev()
        ty = type_ev(ev)
        
        if ty=="ClicGauche":
            x,y=abscisse(ev),ordonnee(ev)
            
            i,j=pixel_vers_case(x,y)
            coor_saisie.append((i,j))
            inversion_intiale(plateau,coor_saisie)

        if ty=="ClicDroit":
            var=False

def survie(plateau):
    
    '''Définie les règles de mort ou de vie d'une case. 
    Retourne une liste de coordonnées.'''
    
    inverse=[]
    
    for i in range (0,len(plateau)):        #
        for j in range (0,len(plateau[i])): # Boucles imbriquées permettant la lecture des cases du plateau.
            
            cmpt = voisine(i,j,plateau) # Comptage du nombre de voisines de chaque case du plateau.
            case = plateau[i][j] # Définition de la case verifiée.
            
            if cmpt<2 and case == True: # Mort de la case si elle possède moins de 2 voisines.
                inverse.append((i,j))
            elif cmpt > 3 and case == True: # Mort si les voisines > 3.
                inverse.append((i,j))
            elif cmpt == 3 and case == False: # S'il y a 3 voisines apparition d'une case.
                inverse.append((i,j))
    return inverse 
    
def voisine(i,j,plateau):
    
    '''Comptage du nombre de voisines vivantes d'une case.'''
    
    cmpt=0
    
    for a in range (i-1,i+2):     #
        for b in range (j-1,j+2): # Boucles imbriquées parcourant les cases adjacentes.
            
            if 0<=a<len(plateau) and 0<=b<len(plateau[a]): #Vérification de la présence de la case sur le plateau.
                
                case = plateau [a][b] # Définition de la case adjacente.
                
                if case == True : # Si la case adjacente est vivante on la compte comme voisine.
                    cmpt+=1

    if plateau[i][j]==True: # Condition permettant de supprimer la case centrale comptée 2 fois.
        cmpt-=1

    return cmpt

def inverse(plateau):
    
    '''Fonction inversant l'état de la liste de coordonnées 
    pour l'itération suivante'''
    
    inverse=survie(plateau)

    for (k,l) in inverse: # Parcours la liste de coordonnées
        plateau[k][l] = not plateau[k][l]
        
    return plateau

def iterations_visibles(reponse):
    
    '''Gestion des itérations intermédiaires en fonction
     de la réponse de l'utilisateur.'''
     
    if reponse == 'o':
        ev = attend_ev()
        while touche(ev) != 'Return':
            ev = attend_ev()
            
    if reponse == 'n':
        sleep(0.5)
        jouer = False
        return jouer

def saisie_int(valeur):
    
    '''Contrôle la saisie de l'utilisateur.'''
    
    valeur=int(valeur)
    while valeur<0 or valeur>19:
        valeur=int(input('Valeur incorrecte, ressaisir la valeur : '))
    
    return valeur

def inversion_intiale(plateau,coor_saisie):
    
    '''Permet l'actualisation des cases vivantes initiales.'''
    
    for (k,l) in coor_saisie:
        plateau[k][l]= not plateau[k][l]
    affichage_plateau(plateau)
    
def affiche_tout(plateau,compt_tour):
    efface_tout()
    affichage_plateau(plateau)
    
    compt_tour+=1
    texte(0,0,compt_tour,couleur='red',taille=30)
    mise_a_jour()
    return compt_tour

def affichage_menu(menu):
    '''Fonction gérant le clic dans le menu jouer'''
    ev = donne_ev()
    tev = type_ev(ev)
        
    if tev == "ClicGauche":
        if 320<=abscisse(ev)<=680 and 350<=ordonnee(ev)<=460 :
            menu= False
                
        if 320<=abscisse(ev)<=680 and 490<=ordonnee(ev)<=590 :      
            #case quitter
            ferme_fenetre()

    mise_a_jour()
    return menu

def affichage_rejouer(rejouer,menu,jouer):
    '''Fonction gérant le clic dans le menu rejouer'''
    ev = attend_ev()
    tev = type_ev(ev)

    if tev == "ClicGauche":
        if 320<=abscisse(ev)<=680 and 350<=ordonnee(ev)<=460 :
            rejouer = True
            menu = True
            jouer = True   

        if 320<=abscisse(ev)<=680 and 490<=ordonnee(ev)<=590 :      
            #case quitter
            ferme_fenetre()

    mise_a_jour()
    return rejouer,menu,jouer

def affiche_menu(taille_fenetre,menu):
    '''Gére l'affichage du menu'''
    if menu==True:
        string='Jouer'
    else:
        string='Rejouer'
    x1,y1 = taille_texte(texte(500,400,string,taille=40,ancrage='center'))
    x3,y3 = taille_texte(texte(500,530,'Quitter',taille=40,ancrage='center'))

    rectangle(320, 350, 680, 460)
    rectangle(320, 490, 680, 590)

###################################
#         BOUCLE DE JEU           #
###################################

nb_case=50
taille_case=20
saisie='auto'
jouer = True
compt_tour = 0
cree_fenetre(1000,1000)



jeu = True
menu = True
rejouer = True

efface_tout()
affiche_menu((1000,1000),menu)

while rejouer:
    plateau = init_plateau(nb_case)

    while menu :
        menu=affichage_menu(menu)
    
    efface_tout()
    affichage_plateau(plateau)
    texte(0,0,compt_tour,couleur='red',taille=30)
        
    saisie='clavier'
    if jouer==True:
        if saisie == 'clavier':
            print('clavier')
            coor_saisie,iterations,ite_intermediaires=saisie_coord(saisie)
            inversion_intiale(plateau,coor_saisie)
        else:
            iterations,ite_intermediaires=saisie_coord(saisie)

        lst_mod = ['inactif','inactif']

        if iterations == 'inf':
            while jouer:
                ev=donne_ev()
                tev=type_ev(ev)
                
                if tev == None:
                    inverse(plateau)
                    compt_tour=affiche_tout(plateau,compt_tour)
                    sleep(0.5)
                else:
                    jouer=False
            
            
        elif ite_intermediaires == 'o':

            iterations=int(iterations)
            for i in range (iterations):
                
                iterations_visibles(ite_intermediaires)
                inverse(plateau)
                compt_tour=affiche_tout(plateau,compt_tour)
            attend_ev()

        elif ite_intermediaires == 'n':
            iterations=int(iterations)
            for i in range (iterations):
                
                iterations_visibles(ite_intermediaires)
                inverse(plateau)
                compt_tour+=1
                
            compt_tour=affiche_tout(plateau,compt_tour)    
            attend_ev()
    
    efface_tout()
    affiche_menu((1000,1000),menu)

    rejouer,menu,jouer = affichage_rejouer(rejouer,menu,jouer)
    compt_tour=0

ferme_fenetre()