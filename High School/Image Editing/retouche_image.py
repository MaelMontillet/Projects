from tkinter.ttk import Combobox
import  tkinter as tk                       
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilename
from math import sqrt,cos,sin,pi,factorial
import numpy as np
import pickle
from random import random


def couleurRouge () :
    global img, im2
    enlever_bouton()
    for y in range(height):
        for x in range(width):
            pixel = img.getpixel((x,y))
            r = int((pixel[0]+pixel[1]+pixel[2])/3)
            v = 0  
            b = 0
            im2.putpixel((x,y),(r,v,b))

    save()
    
def couleurVert () :
    enlever_bouton()
    for y in range(height): # on balaie toutes les lignes de l’image source, de 0 à H-1
        for x in range(width): # pour chaque ligne on balaie toutes les colonnes, de 0 à L-1
            pixel = img.getpixel((x,y)) # en stockant le pixel (x,y) dans une liste p à tois éléments
                                # p[0] est la composante rouge, p[1] la composante verte, et p[2] la composante bleue
            r = 0
            v = pixel[1]  
            b = 0
            im2.putpixel((x,y),(r,v,b)) # on écrit le pixel modifié sur l’image destination

    save()

def couleurBleu () :
    enlever_bouton()
    for y in range(height): 
        for x in range(width): 
            pixel = img.getpixel((x,y))
            r = 0
            v = 0  
            b = pixel[2]
            im2.putpixel((x,y),(r,v,b))
            
    save()
 
def couleurCyan () :
    enlever_bouton()
    for y in range(height): 
        for x in range(width): 
            pixel = img.getpixel((x,y))
            r = 0
            v = pixel[1] 
            b = pixel[2]
            im2.putpixel((x,y),(r,v,b))

    save()

def couleurviolet () :
    enlever_bouton()
    for y in range(height): 
        for x in range(width): 
            pixel = img.getpixel((x,y))
            r = pixel [0]
            v = 0 
            b = pixel[2]
            im2.putpixel((x,y),(r,v,b))
            
    save()

def couleurgrise () :
    enlever_bouton()
    for y in range(height): 
        for x in range(width): 
            pixel = img.getpixel((x,y))
            r = pixel [0]
            v = pixel [1] 
            b = pixel [0]
            im2.putpixel((x,y),(r,v,b))
 
    save()

def couleurjaune () :
    enlever_bouton()
    for y in range(height): 
        for x in range(width): 
            pixel = img.getpixel((x,y))
            r = pixel [0]
            v = pixel[1] 
            b = 0
            im2.putpixel((x,y),(r,v,b))
 
    save()

def couleurdeux () :
    enlever_bouton()
    for y in range(height): 
        for x in range(width): 
            pixel = img.getpixel((x,y))
            r = pixel [2]
            v = pixel[1] 
            b = pixel[1]
            im2.putpixel((x,y),(r,v,b)) 
 
    save()

def couleurfondviolet () :
    enlever_bouton()
    for y in range(height): 
        for x in range(width): 
            pixel = img.getpixel((x,y))
            r = pixel [1]
            v = pixel [2]
            b = pixel[1]
            im2.putpixel((x,y),(r,v,b))
 
    save()

def couleurfondvert () :
    enlever_bouton()
    for y in range(height): 
        for x in range(width): 
            pixel = img.getpixel((x,y))
            r = pixel [2]
            v = pixel[1] 
            b = pixel [2]
            im2.putpixel((x,y),(r,v,b))
 
    save()

def couleurfondbleu () :
    enlever_bouton()
    for y in range(height): 
        for x in range(width): 
            pixel = img.getpixel((x,y))
            r = pixel [2]
            v = pixel[2] 
            b = pixel [1]
            im2.putpixel((x,y),(r,v,b))
            
    save()

def couleurnoirblanc () :
    enlever_bouton()
    for y in range(height): 
        for x in range(width): 
            pixel = img.getpixel((x,y))
            r = pixel [2]
            v = pixel[2] 
            b = pixel [2]
            im2.putpixel((x,y),(r,v,b))
 
    save()

def couleurfondrouge () :
    enlever_bouton()
    for y in range(height): 
        for x in range(width): 
            pixel = img.getpixel((x,y))
            r = pixel [0]
            v = pixel[2] 
            b = pixel [2]
            im2.putpixel((x,y),(r,v,b))

    save()

def couleurfluo () :
    enlever_bouton()
    for y in range(height): 
        for x in range(width): 
            pixel = img.getpixel((x,y))
            r = pixel [0]
            v = pixel[2] 
            b = 1
            im2.putpixel((x,y),(r,v,b))

    save()

def couleurfullviolet () :
    enlever_bouton()
    for y in range(height): 
        for x in range(width): 
            pixel = img.getpixel((x,y))
            r = pixel [2]
            v = 0
            b = pixel [0]
            im2.putpixel((x,y),(r,v,b))

    save()

def couleurjaunevert () :
    enlever_bouton()
    for y in range(height): 
        for x in range(width): 
            pixel = img.getpixel((x,y))
            r = pixel [2]
            v = pixel [0]
            b = 0
            im2.putpixel((x,y),(r,v,b)) 

    save()

def couleurfullcyan () :
    enlever_bouton()
    for y in range(height): 
        for x in range(width): 
            pixel = img.getpixel((x,y))
            r = 2
            v = pixel[2] 
            b = pixel [1]
            im2.putpixel((x,y),(r,v,b))

    save()

def median(l):
    l2=list(l)
    l2.sort()
    return l2[len(l)//2]

def distance_eucl(xa,ya,xb,yb):
    return sqrt((xa-xb)**2+(ya-yb)**2)


def appel_vitesse():
    global global_button, hauteur_ecran, longueur_ecran
    enlever_bouton()
    text = fenetre.create_text(longueur_ecran*7/8, hauteur_ecran*0.4,
                            text="Faites un click gauche pour donner le \n point de fuite (aprés avoir valider)")
    valider=tk.Button(root, text="valider", command=previtesse)
    valider.place(y=hauteur_ecran*0.6, x=longueur_ecran*7/8)
    global_button = [text,valider]
    

def previtesse():
    global vitesse_coords
    vitesse_coords = True

def vitesse(xp, yp):
    #xp, yp les coordonées du point de fuite
    global vitesse_coords
    vitesse_coords = False
    for x in range(width):
        for y in range(height):
            if x==xp and y==yp:
                new=img.getpixel((x, y))
            elif yp-y!=0:
                #on définit la droite allant du point de fuite au point courant
                #d:a*xv+b*yv+c=0
                #vecteur:
                xv=xp-x
                yv=yp-y
                #coefficient
                if xv==0:
                    a=0
                    b=1
                    c=-y
                else:
                    a=1
                    b=-xv/yv
                    c=-(x+b*y)
                droite_get_y = lambda x : (-a/b) * x -(c/b)
                rgb=[img.getpixel((x, y))]
                pixelmedr = [rgb[0][0]]
                pixelmedg = [rgb[0][1]]
                pixelmedb = [rgb[0][2]]
                distance_x = abs(xv)/50
                if xv < 0:
                    pas = -1
                else:
                    pas = 1
                #Calcul de la position des points de la droite sur une distance liée à la distance en x et en allant vers le point
                for xi in range(1, int(distance_x)+1, 1):
                    try:
                        y_droite = droite_get_y(x+xi*pas)
                        rgb=img.getpixel((x+xi*pas, int(y_droite)))
                        pixelmedr.append(rgb[0])
                        pixelmedg.append(rgb[1])
                        pixelmedb.append(rgb[2])
                    except(IndexError):
                        pass
                #On fait une moyenne de pixels de la droite sur la distance considérée
                new=(int(moy(pixelmedr)),int(moy(pixelmedg)),int(moy(pixelmedb)))
            else:
                try:
                    rgb=[img.getpixel((x, y+3)), img.getpixel((x, y+2)),img.getpixel((x, y+1)),img.getpixel((x, y)), img.getpixel((x, y-1)),
                         img.getpixel((x, y-2)), img.getpixel((x, y-3))]
                    pixelmedr = [rgb[i][0] for i in range(8)]
                    pixelmedg = [rgb[i][1] for i in range(8)]
                    pixelmedb = [rgb[i][2] for i in range(8)]
                except(IndexError):
                    pass
                new=(int(moy(pixelmedr)),int(moy(pixelmedg)),int(moy(pixelmedb)))
                
            im2.putpixel((x,y), new)

    save()
    enlever_bouton()

def appel_focus():
    global global_button
    enlever_bouton()
    echelleflou = tk.Scale(root, from_=2, to=8, orient='horizontal', label="flou", length = 150)
    echelleflou.place(y=hauteur_ecran/2, x=longueur_ecran*13/16)
    rayonmax = max((width,height))
    text = fenetre.create_text(longueur_ecran*7/8, hauteur_ecran*0.35,
                            text="Faites un click gauche pour donner le centre \n et un click droit pour donner le point \n définissant le rayon (aprés avoir validé)")
    valider=tk.Button(root, text="valider", command=focus_intermediaire)
    valider.place(y=hauteur_ecran*0.6, x=longueur_ecran*7/8)
    global_button = [echelleflou, valider, text]

    

def focus_intermediaire():
    global focus_coords, global_button
    focus_coords = True
    global_button[1].destroy()

def focus(xp, yp, r):
    global focus_coords, global_button
    #xp, yp position du centre du cercle
    focus_coords = False
    flou = global_button[0].get()
    enlever_bouton()
    flou=[-int(flou/2),flou-int(flou/2)]
    for x in range(width):
        for y in range(height):
            #si le point cosidéré n'est pas à l'intérieur du cercle, on le floute
            distance=distance_eucl(xp,yp,x,y)
            rgb=img.getpixel((x, y))
            pixelmedr = [rgb[0]]
            pixelmedg = [rgb[1]]
            pixelmedb = [rgb[2]]
            if distance>=r:
                for xi in range(flou[0],flou[1],1):
                    for yi in range(flou[0],flou[1],1):
                        try:
                            rgb=img.getpixel((x+xi, y+yi))
                            pixelmedr.append(rgb[0])
                            pixelmedg.append(rgb[1])
                            pixelmedb.append(rgb[2])
                        except(IndexError):
                            pass
            new=(int(sum(pixelmedr)/len(pixelmedr)),int(sum(pixelmedg)/len(pixelmedg)),int(sum(pixelmedb)/len(pixelmedb)))
            im2.putpixel((x,y), new)


    save()
    enlever_bouton()
    
def rota_gauche():
    global im2, img, width, height, new_width, new_height
    enlever_bouton()
    taille = img.size
    largeur = taille[0] -1
    hauteur = taille[1] -1
    ludo=img.load()
    rendu=Image.new(("RGB"),(hauteur + 1,largeur + 1),(255, 255, 255))
    ludorendu=rendu.load()
    for x in range (hauteur):
        for y in range (largeur):
            ludorendu[x, y]=ludo[largeur - y, x]
    im2=rendu
    img=im2
    get_new_size()
    save()
   

def retourner ():
    enlever_bouton()
    img=rota_gauche()
    img=rota_gauche()
    
def miroir():
    enlever_bouton()
    global im2, img
    taille = img.size
    largeur = taille[0] -1
    hauteur = taille[1] -1
    ludo=img.load()
    rendu=Image.new(("RGB"),(largeur + 1,hauteur +  1),(255, 255, 255))
    ludorendu=rendu.load()
    for x in range (largeur):
        for y in range (hauteur):
            ludorendu[x,y]=ludo[largeur-x,y]
    im2=rendu
    save()
    
def rota_droite():
    global im2, img, width, height, new_width, new_height
    enlever_bouton()
    taille = img.size
    largeur = taille[0] -1
    hauteur = taille[1] -1
    ludo=img.load()
    rendu=Image.new(("RGB"),(hauteur + 1,largeur +  1),(255, 255, 255))
    ludorendu=rendu.load()
    for x in range (hauteur):
        for y in range (largeur):
            ludorendu[x,y]=ludo[y, -x]
    im2=rendu
    img=im2
    get_new_size()
    save()
    
def appel_redimensionner():
    global global_button
    enlever_bouton()
    fenetre.txt_x= tk.StringVar()
    fenetre.txt_y= tk.StringVar()
    entreex_redimension=tk.Entry(root, textvariable=fenetre.txt_x)
    entreex_redimension.place(y=hauteur_ecran*0.4, x=longueur_ecran*7/8)
    entreey_redimension=tk.Entry(root, textvariable=fenetre.txt_y)
    entreey_redimension.place(y=hauteur_ecran*0.5, x=longueur_ecran*7/8)
    fenetre.txt_x.set('valeur_x')
    fenetre.txt_y.set('valeur_y')
    valider=tk.Button(root, text="valider", command=redimension_button)
    valider.place(y=hauteur_ecran*0.6, x=longueur_ecran*7/8)
    global_button = [entreex_redimension,entreey_redimension, valider]

def redimension_button():
    global im2,img
    valuex=int(fenetre.txt_x.get())
    valuey=int(fenetre.txt_y.get())
    im2=redimension(valuex, valuey)
    img=im2
    get_new_size()
    save()
    enlever_bouton()

def redimension(xfinal,yfinal):
    global im2, img
    im2np=im2.load()
    a0,b0 = im2.size

    # Dimensions finales (modifiables)
    a1,b1 = xfinal,yfinal

    ratio_lignes = a0/a1
    ratio_colonnes = b0/b1

    image_sortie=Image.new(("RGB"),(a1,b1),(255, 255, 255))
    image_sortie_np=image_sortie.load()
    for ligne in range(a1): 
        for col in range(b1):
            for i in range(3):
                image_sortie_np[ligne,col] =im2np[ int(ligne*ratio_lignes),  int(col*ratio_colonnes) ]
    return image_sortie

def specialiser(c, k, histo1, histo2, mode = 'approximation'):
    """ permet d'appliquer à une image l'histogramme d'une autre image :
    Soient E(x) et E(z) les répartition d'intensité des  pixel de 2 images avec E l'opération d'égalisation
    (Elles associent à une intensité la probabilté de la trouver dans une image qui a subit une égalisation)
    On a E(x) = E(z)
    Soit, f1(x) = E**-1(z)"""
    
    return histo1.donner_inverse(c, histo2.egaliser(c,k), mode)

class histogram():
    
    """ Histogramme des couleurs d'une image"""
    
    def __init__(self,image):
        widthimage,heightimage=image.size
        nb=widthimage*heightimage
        di={"r":{},"g":{},"b":{}}
        self.egalise_dico={"r":{},"g":{},"b":{}}
    
        for i in range(256):
            di["r"][i]=0
            di["g"][i]=0
            di["b"][i]=0

        for x in range(widthimage):
            for y in range(heightimage):
                pixel=image.getpixel((x,y))
                di["r"][int(pixel[0])]+=1
                di["g"][int(pixel[1])]+=1
                di["b"][int(pixel[2])]+=1
            
        for i in range(256):
            di["r"][i]/=nb
            di["g"][i]/=nb
            di["b"][i]/=nb

        self.di=di

    def egaliser(self,c,k):
        """ Permet d'égaliser les nivaux d'une image"""
        try:
            return self.egalise_dico[c][k]
        except(KeyError):
            self.egalise_dico[c][k]=int((256-1)*sum([ self.di[c][i] for i in range(k+1)]))
        return self.egalise_dico[c][k]
    
    def creer_inverse(self):
        """ Crée un dictionnaire correspond à E**-1(x) avec E(x) la fonction d'égalisation"""
        self.inverse_dynamic={"r":{},"g":{},"b":{}}
        self.inverse={"r":{},"g":{},"b":{}}
        self.plist={"r":[],"g":[],"b":[]}
        for pix in range(256):
            self.inverse["r"][self.egaliser("r",pix)]=pix
            self.plist["r"].append(self.egaliser("r",pix))
            self.inverse["g"][self.egaliser("g",pix)]=pix
            self.plist["g"].append(self.egaliser("g",pix))
            self.inverse["b"][self.egaliser("b",pix)]=pix
            self.plist["b"].append(self.egaliser("b",pix))
            
        self.plist["r"].sort()
        self.plist["g"].sort()
        self.plist["b"].sort()
        
    def donner_inverse(self, c, p, mode = 'approximation'):
        """ Pour un intensité donné, renvoie de quel intensité elle est l'égalisation """
        #On effectue une recherche par dichotomie pour trouver entre quelle valeurs connue l'entrée est comprise
        try :
            return self.inverse_dynamic[c][p]
        except(KeyError):
            debut=0
            fin=len(self.plist[c])-1
            if p<=self.plist[c][debut]:
                self.inverse_dynamic[c][p]=self.plist[c][debut]
                return self.inverse_dynamic[c][p]
            elif p>=self.plist[c][fin]:
                self.inverse_dynamic[c][p]=self.plist[c][fin]
                return self.inverse_dynamic[c][p]
            while debut-fin>1:
                milieu = (fin+debut)//2                
                if p<self.plist[c][milieu]:
                    fin=milieu
                elif p>self.plist[c][milieu]:
                    debut=milieu
                else:
                    debut,fin=milieu,milieu
            coef1=abs(p-self.plist[c][debut])/(abs(p-self.plist[c][debut])+abs(p-self.plist[c][fin]))
            coef2=abs(p-self.plist[c][fin])/(abs(p-self.plist[c][debut])+abs(p-self.plist[c][fin]))
            """ On se sert de l'intervalle trouvé pour donner une approximation de la valeur de
            l'image ou renvoyer l'image de la borne de l'intervalle la plus proche"""
            if mode == 'approximation':
                self.inverse_dynamic[c][p] = self.inverse[c][self.plist[c][debut]]*coef2+self.inverse[c][self.plist[c][fin]]*coef1
            elif coef1 >coef2:
                self.inverse_dynamic[c][p] = self.inverse[c][self.plist[c][fin]]
            else:
                self.inverse_dynamic[c][p] = self.inverse[c][self.plist[c][debut]]
            return self.inverse_dynamic[c][p]

def appel_echange_histogramme():
    global global_button
    enlever_bouton()
    fenetre.select = tk.StringVar()
    stock = ('approximation', 'Points existant')
    choix = tk.ttk.Combobox(root, textvariable = fenetre.select, values = stock)
    choix.place(y=hauteur_ecran*0.5, x=longueur_ecran*7/8)
    valider=tk.Button(root, text="valider", command=echange_histogramme)
    valider.place(y=hauteur_ecran*0.6, x=longueur_ecran*7/8)
    global_button = [choix, valider]

def echange_histogramme():
    """ applique l'histogramme d'une image à une autre image """
    global img, im2
    choix_mode = fenetre.select.get()
    enlever_bouton()
    file_name = tk.filedialog.askopenfilename(title="Sélectionner votre image",filetypes=[('jpeg files','.jpeg'),('jpg files','.jpg'),('png files','.png')])
    img_echange = Image.open(file_name)
    histo_im2 = histogram(img)
    histo_echange = histogram(img_echange)
    histo_echange.creer_inverse()
    for x in range(width):
        for y in range(height):
            rgb = img.getpixel((x, y))
            im2.putpixel((x, y), (int(specialiser("r",rgb[0],histo_echange, histo_im2, choix_mode)),
                    int(specialiser("g",rgb[1], histo_echange, histo_im2, choix_mode)),
                    int( specialiser("b", rgb[2], histo_echange, histo_im2, choix_mode))))
    save()

def contraste():
    """ augmente le contraste en égalisant l'histgramme de l'image"""
    enlever_bouton()
    histo_img=histogram(img)
    for y in range(height): 
        for x in range(width):
            pixel=img.getpixel((x,y))
            r=histo_img.egaliser('r',pixel[0])
            g=histo_img.egaliser('g',pixel[1])
            b=histo_img.egaliser('b',pixel[2])
            im2.putpixel((x,y),(r,g,b))
    save()

def moy(l):
    return sum(l)/len(l)

def contour():
    """ cree une nouvelle image avec seulement les contour de l'image de départ.
    L'image d'arrivée est en fait la "dérivée première" de l'image de départ"""
    enlever_bouton()
    for x in range(0,width):
        for y in range(0,height):
            try:
                N=moy(img.getpixel((x, y-1)))
                S=moy(img.getpixel((x, y+1)))
                E=moy(img.getpixel((x+1, y)))
                W=moy(img.getpixel((x-1, y)))
                G=int(abs(E-W)+abs(N-S))
                im2.putpixel((x,y),(G,G,G))
            except(IndexError):
                pass
    save()

def moyimg():
    global filename
    im_res = Image.new('RGB', (width,height), (255,255,255))
    for x in range(0,width):
        for y in range(0,height):
            new=int(moy(img.getpixel((x, y))))
            im_res.putpixel((x,y),(new,new,new))
    return im_res

def appel_sepia():
    appel_ancien('sepia')

def appel_argentique():
    appel_ancien('argentique')

def appel_ancien(couleur):
    global global_button
    enlever_bouton()
    echelleflou = tk.Scale(root, from_=1, to=8,orient='horizontal', label="flou", length = 170)
    echelleflou.place(y=hauteur_ecran*0.5, x=longueur_ecran*13/16)
    
    echellelum = tk.Scale(root, from_=-100, to=100,orient='horizontal', label="luminosité", length = 170)
    echellelum.place(y=hauteur_ecran*0.4, x=longueur_ecran*13/16)
    
    echelledefaults = tk.Scale(root, from_=0, to=14,orient='horizontal', label="quantité des défaults ", length = 170)
    echelledefaults.place(y=hauteur_ecran*0.3, x=longueur_ecran*13/16)
    
    echelletache = tk.Scale(root, from_=0, to=100,orient='horizontal', label="intensité des taches de lumière", length = 170)
    echelletache.place(y=hauteur_ecran*0.2, x=longueur_ecran*13/16)
    
    echelle_prob_bruit = tk.Scale(root, from_=0, to=100,orient='horizontal',
                                          label="probabilité du bruit (px/1000)", length = 180)
    echelle_prob_bruit.place(y=hauteur_ecran*0.6, x=longueur_ecran*13/16)

    echellebruit = tk.Scale(root, from_=0, to=100,orient='horizontal', label="intensité du bruit", length = 170)
    echellebruit.place(y=hauteur_ecran*0.7, x=longueur_ecran*13/16)
    
    valider=tk.Button(root, text="valider", command=ancien)
    valider.place(y=hauteur_ecran*0.8, x=longueur_ecran*7/8)
    fenetre.couleur=couleur
    global_button = [echelleflou, echellelum, echelledefaults, echelletache, echelle_prob_bruit, echellebruit, valider]
            
def ancien():
    """ Simule l'ancienneté d'une image """
    flou = global_button[0].get()
    intensite_bruit = global_button[5].get()
    proba_bruit = global_button[4].get()
    lum = global_button[1].get()
    numdefault = global_button[2].get()
    intensite_tache = global_button[3].get()
    enlever_bouton()
    img_nb = moyimg()
    histo_im2=histogram(img_nb)
    """On récupére l'histogramme prétrété d'autentiques vielles images
    (c'est les image choisis pour l'histogramme qui détermine la couleur : sepia/argentique)"""
    fichier=open(f'ressources/histogramme_{fenetre.couleur}.pkl','rb')
    histo_temoin=pickle.load(fichier)
    numdefault/=100
    
    for x in range(0,width):
        for y in range(0,height):

            #On applique un flou
            pixelmed = [img_nb.getpixel((x, y))[0]]
            debut=-int(flou/2)
            fin=int(flou/2)
            for xi in range(debut,fin,1):
                for yi in range(debut,fin,1):
                    try:
                        pixelmed.append(img_nb.getpixel((x+xi, y+yi))[0])
                    except (IndexError):
                        pass
            #Une fonstion trigonométrique permet de créer des taches plus sombres ou plus éclairés (défault dans le dévelloppement de l'image notament)          
            tache=intensite_tache*1/4*(cos(2*pi/width*x)+sin(2*pi/width*x)-3/2*cos(4*pi/height*x)+sin(4*pi/width*y))
            pixel=moy(pixelmed)
            bruit=0
            #ajout de bruit
            if random() <= proba_bruit/1000:
                bruit=(random()*2-1)*intensite_bruit
                
            pixelrgb=[]
            pixel_bruit=pixel+bruit
            if 0 > pixel_bruit:
                pixel_bruit=0
            elif 255 < pixel_bruit:
                pixel_bruit=255

            #spécification de l'histogramme de l'image : on y applique l'histogramme de vielles images
            if fenetre.couleur == "argentique":
                pixelrgb=[specialiser("r",int(pixel_bruit),histo_temoin,histo_im2),specialiser("r",int(pixel_bruit),histo_temoin,histo_im2),
                    specialiser("r",int(pixel_bruit),histo_temoin,histo_im2)]
            else:
                pixelrgb=[specialiser("r",int(pixel_bruit),histo_temoin,histo_im2),specialiser("g",int(pixel_bruit),histo_temoin,histo_im2),
                    specialiser("b",int(pixel_bruit),histo_temoin,histo_im2)]
            
            newrgb=[(pixelrgb[n]+lum+tache) for n in range (3)]

            """ajout de defaults (image abimée ce sont des pixels gris qui apparaissent aléatoirement mais
            la probabilité de leur apparition est plus grande quand il y a déjà des pixels adjacents liés à des défaults""" 
            if 0<x<width-2 and 0<y<height-2:
                if random()<=numdefault/1000:
                    default.putpixel((x,y), (0,0,0))
                    newrgb=[180]*3
                else:
                    
                    change=False
                    voisin=[default.getpixel((x+1, y)),default.getpixel((x+1, y-1)),default.getpixel((x+1, y+1)),default.getpixel((x, y+1)),
                            default.getpixel((x-1, y+1)),default.getpixel((x, y-1)),default.getpixel((x-1, y)),default.getpixel((x-2, y)),
                            default.getpixel((x+2, y)),default.getpixel((x, y-2)),default.getpixel((x, y-2))]
                    cpt=0
                    for i in voisin:
                        if i==(0,0,0) :
                            cpt+=1
                    if random()<=numdefault*cpt*1.1:
                        newrgb=[180]*3
                        change=True
                    if change==True:
                        default.putpixel((x,y), (0,0,0))
                    else:
                        default.putpixel((x,y), (255,255,255))
            
            im2.putpixel((x,y), (int(newrgb[0]),int(newrgb[1]),int(newrgb[2])))
            
    save()


def appelflou():
    global global_button
    enlever_bouton()
    echelleflou = tk.Scale(root, from_=2, to=8,orient='horizontal', label="flou")
    echelleflou.place(y=hauteur_ecran/2, x=longueur_ecran*7/8)
    valider=tk.Button(root, text="valider", command=flou)
    valider.place(y=hauteur_ecran*0.6, x=longueur_ecran*7/8)
    global_button = [echelleflou, valider]

def flou():
    """ pour chaque pixel, on met la moyenne des pixels voisins pris à une distance donnée"""
    flou=global_button[0].get()
    for x in range(0,width):
        for y in range(0,height):
            pixelr = [im2.getpixel((x, y))[0]]
            pixelg = [im2.getpixel((x, y))[1]]
            pixelb = [im2.getpixel((x, y))[2]]
            debut=-int(flou/2)
            fin=flou-int(flou/2)
            for xi in range(debut,fin,1):
                for yi in range(debut,fin,1):
                    try:
                        pixelr.append(img.getpixel((x+xi, y+yi))[0])
                        pixelg.append(img.getpixel((x+xi, y+yi))[1])
                        pixelb.append(img.getpixel((x+xi, y+yi))[2])
                    except (IndexError):
                        pass
            im2.putpixel((x,y),(int(moy(pixelr)),int(moy(pixelg)),int(moy(pixelb))))
    enlever_bouton()
    save()

def appel_lum():
    global global_button
    enlever_bouton()
    fenetre.var_rouge = tk.IntVar()
    fenetre.var_vert = tk.IntVar()
    fenetre.var_bleu = tk.IntVar()
    rouge_button_lum = tk.Checkbutton(root, text='rouge',variable=fenetre.var_rouge, onvalue=1, offvalue=0)
    rouge_button_lum.place(y=hauteur_ecran*0.2, x=longueur_ecran*7/8)
    
    vert_button_lum = tk.Checkbutton(root, text='vert',variable=fenetre.var_vert, onvalue=1, offvalue=0)
    vert_button_lum.place(y=hauteur_ecran*0.3, x=longueur_ecran*7/8)
    
    bleu_button_lum = tk.Checkbutton(root, text='bleu',variable=fenetre.var_bleu, onvalue=1, offvalue=0)
    bleu_button_lum.place(y=hauteur_ecran*0.4, x=longueur_ecran*7/8)
    
    echelle_const = tk.Scale(root, from_=-200, to=200,orient='horizontal', label="constante ajoutée", length = 140)
    echelle_const.place(y=hauteur_ecran/2, x=longueur_ecran*7/8)
    
    echelle_coefficient= tk.Scale(root, from_=0.1, to=2,orient='horizontal', resolution=0.01, label="coefficient multiplicateur", length = 140)
    echelle_coefficient.place(y=hauteur_ecran*0.6, x=longueur_ecran*7/8)
    echelle_coefficient.set(1)
    
    valider=tk.Button(root, text="valider", command=luminosite)
    valider.place(y=hauteur_ecran*0.7, x=longueur_ecran*7/8)
    global_button = [echelle_const, echelle_coefficient,rouge_button_lum, bleu_button_lum, vert_button_lum, valider]

def luminosite():
    """ effectue une opération affine à l'image"""
    global global_button, fenetre
    rouge = fenetre.var_rouge.get()
    vert = fenetre.var_vert.get()
    bleu = fenetre.var_bleu.get()
    const=global_button[0].get()
    coef=global_button[1].get()
    for x in range(0,width):
        for y in range(0,height):
            pixelr = im2.getpixel((x, y))[0]
            pixelg = im2.getpixel((x, y))[1]
            pixelb = im2.getpixel((x, y))[2]
            if rouge == 1:
                pixelr = int(coef*pixelr)+const
            if vert == 1:
                pixelg = int(coef*pixelg)+const
            if bleu == 1:
                pixelb = int(coef*pixelb)+const
            im2.putpixel((x,y),(pixelr, pixelg, pixelb))
    enlever_bouton()
    save()

def appel_rogner():
    global doit_rogner, global_button
    enlever_bouton()
    doit_rogner=True
    text = fenetre.create_text(longueur_ecran*7/8, hauteur_ecran*0.35,
                text="Click gauche : point supérieur gauche, \n click droit : point inférieur droit")
    global_button=[text]

def rogner():
    global landing_x, landing_y, origine_x, origine_y, new_height, new_width, im2, img, width, height

    landing_x = int(landing_x * width/new_width)
    landing_y = int(landing_y * height/new_height)
    origine_x = int(origine_x * width/new_width)
    origine_y = int(origine_y * height/new_height)
    im2 = Image.new('RGB',(landing_x-origine_x, landing_y-origine_y), (0, 0, 0))
    for i in range(origine_x,landing_x):
        for j in range(origine_y,landing_y):
            pix = img.getpixel((i, j))
            im2.putpixel((i-origine_x, j-origine_y),pix)
    get_new_size()
    img=im2
    save()
    origine_x, origine_y, landing_x, landing_y = "", "", "", ""
    doit_rogner=False
    enlever_bouton()

def binomial(k,n):
    if n==k or k==0:
        return 1
    elif k==1:
        return n
    else:
        return binomial(k,n-1)+binomial(k-1,n-1)

def Bernstein(i,m,t):
    return binomial(i,m)*t**(i)*(1-t)**(m-i)

def appel_courbe():
    global ptclick, change, dictf, longueur_ecran, hauteur_ecran, canv, root2, global_button
    enlever_bouton()
    ptclick=[[longueur_ecran*0.5, hauteur_ecran * 0.75],[longueur_ecran * 0.9, hauteur_ecran * 0.15]]
    change=[]
    dictf={}
    root2 = tk.Toplevel()
    canv = tk.Canvas(root2, width=longueur_ecran, height=hauteur_ecran, background='white')
    canv.grid(row=2,column=0,columnspan=18)
    root2.bind('<Button-1>', click_courbe)    
    root2.bind('<Button-3>', click_g_courbe)
    root2.bind('<Motion>', motion_courbe)
    fenetre.var_rouge = tk.IntVar()
    fenetre.var_vert = tk.IntVar()
    fenetre.var_bleu = tk.IntVar()
    rouge_button = tk.Checkbutton(root, text='rouge',variable=fenetre.var_rouge, onvalue=1, offvalue=0)
    rouge_button.place(y=hauteur_ecran*0.3, x=longueur_ecran*7/8)
    vert_button = tk.Checkbutton(root, text='vert',variable=fenetre.var_vert, onvalue=1, offvalue=0)
    vert_button.place(y=hauteur_ecran*0.4, x=longueur_ecran*7/8)
    bleu_button = tk.Checkbutton(root, text='bleu',variable=fenetre.var_bleu, onvalue=1, offvalue=0)
    bleu_button.place(y=hauteur_ecran*0.5, x=longueur_ecran*7/8)
    echelle_courbe = tk.Scale(root, from_=0.01, to=1.5, resolution=0.01,orient='horizontal', label="coefficient multiplicateur", length = 140)
    echelle_courbe.place(y=hauteur_ecran*0.2, x=longueur_ecran*7/8)
    echelle_courbe.set(1)
    valider=tk.Button(root, text="valider", command=appliquer_courbe)
    valider.place(y=hauteur_ecran*0.6, x=longueur_ecran*7/8)
    global_button = [rouge_button, vert_button, bleu_button, valider, echelle_courbe]
    courbe_bezier(ptclick)

def appliquer_courbe():
    global dictf,im2, canv, root2
    courbe_bezier(ptclick,100000)
    rouge = fenetre.var_rouge.get()
    vert = fenetre.var_vert.get()
    bleu = fenetre.var_bleu.get()
    root2.destroy()
    for x in range(width):
        for y in range(height):
            pixel=img.getpixel((x,y))
            pr,pv,pb=pixel
            if rouge==1:
                pr=int(pixel[0]+dictf[pixel[0]])
            if vert==1:
                pv=int(pixel[1]+dictf[pixel[1]])
            if bleu==1:
                pb=int(pixel[2]+dictf[pixel[2]])        
            im2.putpixel((x,y), (pr,pv,pb))
    save()
    enlever_bouton()


def courbe_bezier(pts,precision=1000):

    """ crée une courbe de bézier"""
    
    global dictf, ptclick, canv, root2, longeur_ecran, hauteur_ecran, global_button

    point0_x = longueur_ecran * 0.5
    point0_y = hauteur_ecran * 0.75
    dernier_point_x = longueur_ecran * 0.9
    dernier_point_y = hauteur_ecran * 0.15
    echelle1_x = 255 / (longueur_ecran * 0.4)
    echelle1_y = 255 / (hauteur_ecran * 0.6)
    echelle2_x = longueur_ecran * 0.2 / 256
    echelle2_y = hauteur_ecran * 0.4 / 256
    coefficient = global_button[4].get()

    canv.create_text(longueur_ecran*0.7, hauteur_ecran * 0.75+25, text="Coube à modifier")
    canv.create_text(longueur_ecran*0.2, hauteur_ecran * 0.7+25, text="rendu de la courbe")
    
    canv.create_line(longueur_ecran * 0.5, hauteur_ecran * 0.75, longueur_ecran * 0.9 + 3, hauteur_ecran * 0.75, arrow='last')
    canv.create_line(longueur_ecran * 0.5, hauteur_ecran * 0.75, longueur_ecran * 0.5, hauteur_ecran * 0.15 -3, arrow='last')
    canv.create_text(longueur_ecran * 0.5-15, hauteur_ecran * 0.75+15, text = "0")
    canv.create_text(longueur_ecran * 0.5-15, hauteur_ecran * 0.15, text = "255")
    canv.create_text(longueur_ecran * 0.9, hauteur_ecran * 0.75+15, text = "255")
    
    canv.create_line(longueur_ecran * 0.1, hauteur_ecran * 0.7, longueur_ecran * 0.3+3, hauteur_ecran * 0.7, arrow='last')
    canv.create_line(longueur_ecran * 0.1, hauteur_ecran * 0.7, longueur_ecran * 0.1, hauteur_ecran * 0.3-3, arrow='last')
    canv.create_text(longueur_ecran * 0.1-15, hauteur_ecran * 0.7+15, text = "0")
    canv.create_text(longueur_ecran * 0.3, hauteur_ecran * 0.7+15, text = "255")
    canv.create_text(longueur_ecran * 0.1-15, hauteur_ecran * 0.3, text = "255")

    pas1_x = (longueur_ecran *0.4) / 256
    pas1_y = (hauteur_ecran *0.6) / 256
    pas2_x = (longueur_ecran *0.2) / 256
    pas2_y = (hauteur_ecran *0.4) / 256
    
    for g in range(0,256,5):
        
        canv.create_line(longueur_ecran * 0.5 -2, hauteur_ecran * 0.75 - g * pas1_y , longueur_ecran * 0.5 +2,
                                                    hauteur_ecran * 0.75 - g * pas1_y)
        
        canv.create_line(longueur_ecran * 0.5 + g * pas1_x, hauteur_ecran * 0.75-2,
                                                    longueur_ecran * 0.5 + g * pas1_x ,hauteur_ecran * 0.75 + 2)
        
        canv.create_line(longueur_ecran * 0.1 - 2, hauteur_ecran * 0.7 - g * pas2_y, longueur_ecran * 0.1 + 2,
                                                    hauteur_ecran * 0.7 - g * pas2_y)
        
        canv.create_line(longueur_ecran * 0.1 + g * pas2_x, hauteur_ecran * 0.7 -2,
                                                    longueur_ecran * 0.1 + g * pas2_x, hauteur_ecran * 0.7 +2)
        
        
    
    dico_ecart = {}
    check=[]
    n=len(pts)
    # Calcul de la position des point de la courbe en fonction des points guidant la courbe
    for p in range(n):
        canv.create_rectangle(pts[p][0]-10,pts[p][1]-10,pts[p][0]+10,pts[p][1]+10)
    for t in range(precision):
        pt=[0,0]
        for i in range(n):
            pt[0]+=Bernstein(i,n-1,t/precision)*pts[i][0]
            pt[1]+=Bernstein(i,n-1,t/precision)*pts[i][1]
            
        valeur_x = (pt[0]-longueur_ecran * 0.5) * echelle1_x
        ecart_x = abs(valeur_x - int(valeur_x))
        """La coordonée y des points ayant une abscisse entre 0 et 255 permet de calculer leur image
        par la fonction décrite par la courbe comme les coordonnée en x ne sont pas des entiers,
        on essaye de se rapprocher le plus des valeur entière en ne retenant que les points les plus proche
        de la valeur entière (minimiser ecart_x). La précision permet d'augmenterle nombre de points calculés
        en fonction du besion et donc diminuer cet écart. Ensuite, dictf correspond à la fonction associant aux
        points racontrées dont les valeurs aprochées sont comprises entre 0 et 255 l'image par la courbe.
        Les image sont en fait l'écart à la droite identité ce qui permet de gérer l'amplitude avec une
        constante multiplicatrice."""

        if int(valeur_x) not in check or ecart_x < dico_ecart[int(valeur_x)]:

            dico_ecart[int(valeur_x)]=ecart_x
        
            valeur_y = (hauteur_ecran * 0.75 - pt[1]) * echelle1_y
            ecart_fonction_identite = (valeur_y - int(valeur_x)) * coefficient
            resultat = ecart_fonction_identite
            dictf[int(valeur_x)] = resultat
            canv.create_rectangle(pt[0]-2,pt[1]-2,pt[0]+2,pt[1]+2)
            
        if int(valeur_x) not in check :
            check.append(int(valeur_x))
    """si il y a des valeurs entre 0 et 255 qui ne sont pas pries en compte par dictf on en donne une
    approximation grâce au valeurs proches de la valeur manquante que l'on connait."""
    for i in range(256):
        pt[0]=i
        if i in check:
            pt[1]=dictf[i]
        else:
            test_droite=255
            test_gauche=0
            if i!=0:
                test_gauche=i-1
            elif i!=255:
                test_droite=i+1
            while test_gauche not in check and test_droite not in check :
                if test_droite != 255:
                    test_droite+=1
                if test_gauche != 0:
                    test_gauche-=1
                if test_droite == 255 and test_gauche == 0:
                    print("erreur plage")
                    pt[1] = 1
                    break
            if test_droite in check and test_gauche in check:
                pt[1] = (dictf[test_droite]+dictf[test_gauche])/2
            elif test_droite in check:
                pt[1] = dictf[test_droite]
            else:
                pt[1] = dictf[test_gauche]
            dictf[i] = pt[1]
            
        image = pt[0] + pt[1]
        coord_x = longueur_ecran*0.1 + pt[0] * echelle2_x
        coord_y = hauteur_ecran * 0.7 - image * echelle2_y
        
        canv.create_rectangle( coord_x - 1, coord_y - 1, coord_x + 1, coord_y + 1)

def click_courbe(event):
    global ptclick, canv, root2
    canv.delete("all")
    x, y = event.x,event.y
    ptclick.insert(-1,[x,y])
    courbe_bezier(ptclick)

def click_g_courbe(event):
    global ptclick, canv, change, root2
    x, y = event.x,event.y
    if change==[]:
        for i in range(len(ptclick)):
            if x-10 < ptclick[i][0] < x+10 and y-10 < ptclick[i][1] < y+10:
                change=i
                break
    else:
        canv.delete("all")
        if change != 0 and change != len(ptclick)-1:
            ptclick[change]=[x,y]
        else:
            ptclick[change][1]=y
        change=[]
        courbe_bezier(ptclick)

def motion_courbe(event):
    global ptclick, change, cpt, dictf, canv, root2
    x, y = event.x, event.y
    if change!=[]:
        cpt=0
        canv.delete("all")
        if change != 0 and change != len(ptclick)-1:
            ptclick[change]=[x,y]
        else:
            ptclick[change][1]=y
        courbe_bezier(ptclick,500)

def enlever_bouton():
    global global_button, doit_rogner, focus_coords, vitesse_coords
    doit_rogner = False
    focus_coords = False
    vitesse_coords = False
    for widget in global_button:
        try:
            widget.destroy()
        except:
            fenetre.delete(widget)

def save():
    global im2, new_width, new_height, longueur_ecran, hauteur_ecran, addition, img, txt_save, dossier
    add = addition.get()
    nom = txt_save.get()
    if add == 1:
        img = im2
    fenetre.create_rectangle(0,0,longueur_ecran,hauteur_ecran, fill="white", outline="white")
    if dossier != "":
        im2.save(f'{dossier}/{nom}.jpeg','jpeg')
    else:
        im2.save(f'images_modifiees/{nom}.jpeg','jpeg')
    imgtk=ImageTk.PhotoImage(redimension(new_width,new_height))
    fenetre.im= imgtk
    fenetre.create_image(new_width*0.5,new_height*0.5,image=imgtk)

dossier=""

def parcourir_dossier():
    global dossier
    dossier = tk.filedialog.askdirectory(initialdir="/",title='Choisissez un repertoire')

def parcourir_fichier():
    global filename, img, im2, width, height, new_width, new_height, longueur_ecran, hauteur_ecran, default
    filename= tk.filedialog.askopenfilename()
    img = Image.open(f"{filename}")
    im2 = Image.open(f"{filename}")
    fenetre.create_rectangle(0,0,longueur_ecran,hauteur_ecran, fill="white", outline="white")
    get_new_size()
    default=Image.new('RGB', (width,height), (255,255,255))
    imgtk=ImageTk.PhotoImage(redimension(new_width,new_height))
    fenetre.im= imgtk
    fenetre.create_image(new_width*0.5,new_height*0.5,image=imgtk)

def get_new_size():
    global im2, img, width, height, longueur_ecran, hauteur_ecran, new_width, new_height
    width,height = im2.size
    new_width,new_height = im2.size
    while new_width<longueur_ecran*0.7 and new_height<hauteur_ecran*0.75:
        new_width*=1.05
        new_height*=1.05
    
    while new_width>longueur_ecran*0.75 or new_height>hauteur_ecran*0.8:
        new_width*=0.95
        new_height*=0.95
    new_width=int(new_width)
    new_height=int(new_height)

ptclick=[]
change=[]
dictf={}
canv, root2 = 0, 0

root = tk.Tk()
    
# On donne un titre à cette fenêtre
root.title('PhotoBled')
#root.iconbitmap("crayon.ico")

longueur_ecran = root.winfo_screenwidth()
hauteur_ecran = root.winfo_screenheight()

# On crée la fenêtre d'affichage
fenetre = tk.Canvas(root, width=longueur_ecran, height=hauteur_ecran, background='white')
fenetre.grid(row=2,column=0,columnspan=18)


#sauvegarder
parcourir = tk.Button(root, text = "choisir un dossier", command = parcourir_dossier)
parcourir.place(y=hauteur_ecran*0.85, x=longueur_ecran*6.7/8)
txt_save= tk.StringVar()
entree_save=tk.Entry(root, textvariable=txt_save)
entree_save.place(y=hauteur_ecran*0.8, x=longueur_ecran*6/8)
txt_save.set('nom_image_editée')

parcourir2 = tk.Button(root, text = "choisir un fichier", command = parcourir_fichier)
parcourir2.place(y=hauteur_ecran*0.85, x=longueur_ecran*6/8)

#fenetre.config(background='#D14343')
filename = ""
img = ""
img2 = ""
new_width = 0
newheight = 0
width = 0
height = 0

global_button=[]

#extension= presentation.format

#Boutton addition des filtres
addition = tk.IntVar()
addition_button = tk.Checkbutton(root, text='addition des filtres', variable = addition, onvalue=1, offvalue=0)
addition_button.place(y=hauteur_ecran*0.15, x=longueur_ecran*7/8)
addition_button.select()

#Bouton Rogner
PhotoRogner = tk.PhotoImage(file = "icones/rogner.png")
PhotoRogner = PhotoRogner.subsample(1, 1)
BoutonRogner = tk.Button(root, image = PhotoRogner, borderwidth = 0)
BoutonRogner  = tk.Button(root, image = PhotoRogner, cursor = "top_left_arrow", command = appel_rogner).grid(row = 0, column = 4)

#Bouton Luminosité
PhotoLuminosite = tk.PhotoImage(file = "icones/luminosite.png")
PhotoLuminosite = PhotoLuminosite.subsample(1, 1)
BoutonLuminosite = tk.Button(root, image = PhotoLuminosite, borderwidth = 0)
BoutonLuminosite  = tk.Button(root, image = PhotoLuminosite, cursor = "top_left_arrow", command = appel_lum).grid(row = 0, column = 3)

#Bouton Couleur + menu deroulant

PhotoCouleur = tk.PhotoImage(file = "icones/logocouleur.png")
PhotoCouleur = PhotoCouleur.subsample(1, 1)
Boutoncouleur = tk.Menubutton(root, image=PhotoCouleur)
Boutoncouleur.grid(row = 0, column = 2)
Boutoncouleur.menu = tk.Menu(Boutoncouleur, tearoff=0)
Boutoncouleur['menu']= Boutoncouleur.menu
Boutoncouleur.menu.add_command(label='Rouge', command = couleurRouge)
Boutoncouleur.menu.add_command(label="Vert", command = couleurVert )
Boutoncouleur.menu.add_command(label="Blue", command = couleurBleu)
Boutoncouleur.menu.add_command(label="Cyan", command = couleurCyan)
Boutoncouleur.menu.add_command(label="Violet", command = couleurviolet)
Boutoncouleur.menu.add_command(label="Fluo", command = couleurfluo)
Boutoncouleur.menu.add_command(label="Gris", command = couleurgrise)
Boutoncouleur.menu.add_command(label="Jaune", command = couleurjaune)
Boutoncouleur.menu.add_command(label="Noir et Blanc", command = couleurnoirblanc)
Boutoncouleur.menu.add_command(label="Fond Cyan", command = couleurdeux)
Boutoncouleur.menu.add_command(label="Fond Violet", command = couleurfondviolet)
Boutoncouleur.menu.add_command(label="Fond Vert", command = couleurviolet)
Boutoncouleur.menu.add_command(label="Fond Blue", command = couleurfondbleu)
Boutoncouleur.menu.add_command(label="FondRouge", command = couleurfondrouge)
Boutoncouleur.menu.add_command(label="Full Violet ", command = couleurfullviolet)
Boutoncouleur.menu.add_command(label="Full Fluo", command = couleurjaunevert)
Boutoncouleur.menu.add_command(label="Full Blue", command = couleurfullcyan)

#Bouton sablier
Photoancien = tk.PhotoImage(file = "icones/ancien.png")
Photoancien = Photoancien.subsample(1, 1)
Boutonancien = tk.Menubutton(root, image = Photoancien, borderwidth = 5)
Boutonancien.grid(row = 0, column = 5)
Boutonancien.menu = tk.Menu(Boutonancien, tearoff=0)
Boutonancien['menu']= Boutonancien.menu
Boutonancien.menu.add_command(label='sepia', command = appel_sepia)
Boutonancien.menu.add_command(label='argentique', command = appel_argentique)

#Boutonancien = tk.Button(root, image = Photoancien, cursor = "top_left_arrow", command = ancien).grid(row = 0, column = 5)

#Bouton Vitesse
PhotoVitesse = tk.PhotoImage(file = "icones/vitesse.png")
PhotoVitesse = PhotoVitesse.subsample(1, 1)
BoutonVitesse = tk.Button(root, image = PhotoVitesse, borderwidth = 0)
BoutonVitesse  = tk.Button(root, image = PhotoVitesse, cursor = "top_left_arrow", command=appel_vitesse).grid(row = 0, column = 11 )

#Bouton Flou
PhotoFlou = tk.PhotoImage(file = "icones/flou.png")
PhotoFlou = PhotoFlou.subsample(1, 1)
BoutonFlou = tk.Button(root, image = PhotoFlou, borderwidth = 0)
BoutonFlou  = tk.Button(root, image = PhotoFlou, cursor = "top_left_arrow", command = appelflou).grid(row = 0, column = 10)

#Bouton contraste 
PhotoContraste = tk.PhotoImage(file = "icones/contraste.png")
PhotoContratse = PhotoContraste.subsample(1, 1)
BoutonContraste = tk.Button(root, image = PhotoContraste, borderwidth = 5)
BoutonContraste = tk.Button(root, image = PhotoContraste, cursor = "top_left_arrow" , command = contraste).grid(row = 0, column = 6)

#Bouton Rota360
PhotoRota = tk.PhotoImage(file = "icones/Rotation360.png")
PhotoRota= PhotoRota.subsample(1, 1)
BoutonRota = tk.Button(root, image = PhotoRota, borderwidth = 5)
BoutonRota  = tk.Button(root, image = PhotoRota,cursor = "top_left_arrow",command= retourner).grid(row = 0, column = 8)

#Bouton Rotationgauche
PhotoRotag = tk.PhotoImage(file = "icones/gauche.png")
PhotoRotag = PhotoRotag.subsample(1, 1)
BoutonRotag  = tk.Button(root, image = PhotoRotag, borderwidth = 5)
BoutonRotag  = tk.Button(root, image = PhotoRotag, cursor = "top_left_arrow", command= rota_gauche).grid(row = 0, column = 7)

#Bouton Rotationdroite
PhotoRotad = tk.PhotoImage(file = "icones/droite.png")
PhotoRotad = PhotoRotad.subsample(1, 1)
BoutonRotad = tk.Button(root, image = PhotoRotad, borderwidth = 5)
BoutonRotad = tk.Button(root, image = PhotoRotad, cursor = "top_left_arrow", command= rota_droite).grid(row = 0, column =9 )

#Bouton échange d'histogramme
Photohistogramme = tk.PhotoImage(file = "icones/histogramme.png")
Photohistogramme = Photohistogramme.subsample(1, 1)
Boutonhistogramme = tk.Button(root, image = Photohistogramme, borderwidth = 5)
Boutonhistogramme = tk.Button(root, image = Photohistogramme, cursor = "top_left_arrow", command = appel_echange_histogramme).grid(row = 0, column = 13)

#Bouton Courbedebezier
Photocourbe = tk.PhotoImage(file = "icones/Bezier.png")
Photocourbe = Photocourbe.subsample(1, 1)
Boutoncourbe = tk.Button(root, image = Photocourbe, borderwidth = 5)
Boutoncourbe = tk.Button(root, image = Photocourbe, cursor = "top_left_arrow", command = appel_courbe).grid(row = 0, column = 12)

#Bouton Miroir
Photomiroir = tk.PhotoImage(file = "icones/miroir.png")
Photomiroir = Photomiroir.subsample(1, 1)
Boutonmiroir = tk.Button(root, image = Photomiroir, borderwidth = 5)
Boutonmiroir = tk.Button(root, image = Photomiroir, cursor = "top_left_arrow",command = miroir).grid(row = 0, column = 14)

#Bouton Contour
Photocontour = tk.PhotoImage(file = "icones/contour.png")
Photocontour = Photocontour.subsample(1, 1)
Boutoncontour = tk.Button(root, image = Photocontour, borderwidth = 5)
Boutoncontour = tk.Button(root, image = Photocontour, cursor = "top_left_arrow", command = contour).grid(row = 0, column = 15)

#Bouton Focus
Photofocus = tk.PhotoImage(file = "icones/Focus.png")
Photofocus = Photofocus.subsample(1, 1)
Boutonfocus = tk.Button(root, image = Photofocus, borderwidth = 5)
Boutonfocus = tk.Button(root, image = Photofocus, cursor = "top_left_arrow", command = appel_focus).grid(row = 0, column = 16)

#Bouton Redimensionner
PhotoRedimensionner = tk.PhotoImage(file = "icones/Redimensionner.png")
PhotoRedimensionner = PhotoRedimensionner.subsample(1, 1)
BoutonRedimensionner = tk.Button(root, image = PhotoRedimensionner, borderwidth = 5)
BoutonRedimensionner = tk.Button(root, image = PhotoRedimensionner, cursor = "top_left_arrow", command=appel_redimensionner).grid(row = 0, column = 1)


origine_x, origine_y, landing_x, landing_y, doit_rogner = "", "", "", "", False
vitesse_coords = False
focus_coords = False
xp_focus, yp_focus = "", ""


def click(event):
    global origine_x, origine_y, vitesse_coords,focus_coords, new_width, new_height,xp_focus, yp_focus
    x, y = event.x, event.y
    if 0 <= x <= new_width and 0 <= y <= new_height:
        if doit_rogner:
            origine_x, origine_y = x, y
        if vitesse_coords:
            vitesse(int(x * width/new_width), int(y * height/new_height))
        if focus_coords:
            xp_focus, yp_focus = int(x * width/new_width), int(y * height/new_height)
    
root.bind('<Button-1>', click)

def click_g(event):
    global landing_x, landing_y, origine_x, origine_y, xp_focus, yp_focus, new_width, new_height
    x, y = event.x, event.y
    if 0 <= x <= new_width and 0 <= y <= new_height:
        if doit_rogner:
            landing_x, landing_y = x, y
            rogner()
        if focus_coords:
            xr, yr = int(x * width/new_width), int(y * height/new_height)
            r = distance_eucl(xp_focus, yp_focus, xr, yr)
            focus(xp_focus, yp_focus, r)

   
root.bind('<Button-3>', click_g)

root.mainloop()



