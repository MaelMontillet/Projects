from Matrices_obj import *
from random import randint
import tkinter as tk
from PIL import Image,ImageTk
from time import time
import pygame.mixer

class Point():
    def __init__(self,y,x):
        self.x=x
        self.y=y
        #point précédent lors de l'algorithme Astar
        self.parent=[]
        #cout du point (distance de manhattan du point et l'arrivée (avec un coefficient pour donner du poid) et du point au point d'entrée)
        self.cost=[]
    def __str__(self):
        #affichage dans un print
        return str(self.x)+";"+str(self.y)
    
class Graphe():
    #détermination de la matrice nulle.
    def __init__(self):
        #matrice d'adjacence du graphe
        self.mata=Matrice([],0,0)
        #liste des points
        self.pts=[]
    def add_pts(self,pts):
        #méthode pour ajouter un point qui n'est pas définie dans Matrice_obj.py
        self.pts+=[pts]
        self.mata=list(self.mata)
        for i in range (len(self.mata)):
            self.mata[i]+=[0]
        self.mata+=[[0]*(len(self.mata)+1)]
        self.mata=Matrice(self.mata)
            
    def link(self,lpts):
        #méthode pour lier des points
        for i in range(0,len(lpts)):
            self.mata[lpts[i][0]][lpts[i][1]]+=1
            self.mata[lpts[i][1]][lpts[i][0]]+=1
    def aff(self,x,y,ca):
        #affichage en parcourant la matrice d'adjacence
        i=1
        j=0
        while i!=len(self.mata)-1 or j!=len(self.mata)-1:
            pt=self.pts[j]
            canv.create_rectangle(x+ca/2+pt.x*ca-5,ca/2+y+pt.y*ca-5,ca/2+x+pt.x*ca+5,ca/2+y+pt.y*ca+5)
            if self.mata[j][i]==1:
                pt2=self.pts[i]
                canv.create_line(x+ca/2+pt.x*ca,ca/2+y+pt.y*ca,ca/2+x+pt2.x*ca,ca/2+y+pt2.y*ca)
            if i==len(self.mata)-1 and j!=len(self.mata)-1:
                j+=1
                i=0
            i+=1


class Laby():
    def __init__(self,t):
        #t : la taille
        self.t=t
        #Matrice des murs verticaux (1 : mur, 0 : ouverture)
        self.mat0=Matrice([1 for x in range(t**(t+1))],t,t+1)
        #Matrice des murs horizontaux
        self.mat1=Matrice([1 for x in range(t**(t+1))],t+1,t)

    def kurskal(self):
        #Matrice des indices (permet de vérifier que les cellule que l'on veut joindre ne font pas déjà parti du même chemin, même indice = même chemin)
        #On inicialise avec un indice différent pour chaque cellule
        matind=Matrice([x for x in range(self.t**2)],self.t,self.t)
        #nombre de transfert
        ntransf=0
        while ntransf!=self.t**2-1 :
            #on choisit une cellule au hasard (indx : coordonnée x, indy: coordonnée y
            indx=randint(0,self.t-1)
            indy=randint(0,self.t-1)
            #Si la cellule est au bord du labyrinthe, on enlève la posibilité d'enlever ce bord.
            l=[0,1,2,3]
            #Ouest
            if indx==0:
                l.remove(0)
            #Nord
            if indy==0:
                l.remove(1)
            #Est
            if indx==self.t-1:
                l.remove(2)
            #Sud
            if indy==self.t-1:
                l.remove(3)
            #Pour gagner en efficacité, si on ne peut pas ouvrir le mur on essaye d'en ouvrir un autre
            mur="false"
            while mur=="false" and len(l)!=0:
                side=l[randint(0,len(l)-1)]
                if side==0 or side==2:
                    #On verifie à chaque fois que les deux cellule ne font pas parte du même chemin.
                    if matind[indy][indx]!=matind[indy][indx+side-1]:
                        mur="true"
                    else:
                        l.remove(side)
                elif side==1:
                    if matind[indy][indx]!=matind[indy-1][indx]:
                        mur="true"
                    else:
                        l.remove(side)
                elif side==3:
                    if matind[indy][indx]!=matind[indy+1][indx]:
                        mur="true"
                    else:
                        l.remove(side)
            #si la liste est vide on ne peut pas ouvrir de mur
            if len(l)==0:
                side=""
            #sinon on ouvre le mur et on change les indices
            if side==0 or side==2:
                ind1=matind[indy][indx]
                ind2=matind[indy][indx+side-1]
                for i in range(len(matind)):
                      for j in range(len(matind)):
                          if matind[i][j]==ind2:
                              matind[i][j]=ind1
                if side==0:
                    self.mat0[indy][indx]=0
                else:
                    self.mat0[indy][indx+1]=0
                ntransf+=1
                
            elif side==1 :
                ind1=matind[indy][indx]
                ind2=matind[indy-1][indx]
                for i in range(len(matind)):
                      for j in range(len(matind)):
                          if matind[i][j]==ind2:
                                matind[i][j]=ind1
                self.mat1[indy][indx]=0
                ntransf+=1
                
            elif side==3:
                ind1=matind[indy][indx]
                ind2=matind[indy+1][indx]
                for i in range(len(matind)):
                      for j in range(len(matind)):
                        if matind[i][j]==ind2:
                              matind[i][j]=ind1
                self.mat1[indy+1][indx]=0
                ntransf+=1

    def graphe(self,xentr,xsortie):
        #méthode pour créer le graphe liée au labyrinte
        lineh=[[[-1,xsortie]],[[7,xentr]]]
        linev=[]
        self.mat1bis=Matrice([[0 for x in range(len(self.mat1[0]))]]+list(self.mat1)+[[0 for x in range(len(self.mat1[0]))]])
        stk=[]
        i=1
        j=0
        #on récupére les ligne corespondant à une succession d'espace vide
        #ligne verticales
        while i!=len(self.mat0[0])-1 or j!=len(self.mat0)-1:
            while self.mat0[j][i]==0:
                if [j,i-1] not in stk:
                    stk.append([j,i-1])
                stk.append([j,i])
                if j!=len(self.mat0)-1 or i!=len(self.mat0[0])-1:
                    i+=1
            if len(stk)>1:
                lineh.append(stk)
                stk=[]
            if i==len(self.mat0[0])-1 and j!=len(self.mat0)-1:
                i=0
                j+=1
            if j!=len(self.mat0)-1 or i!=len(self.mat0[0])-1:
                i+=1
        i=0
        j=0
        stk=[]
        #ligne horizontales
        while i!=len(self.mat1bis[0])-1 or j!=len(self.mat1bis)-1:
            cut="false"
            while self.mat1bis[j][i]==0 and cut=="false":
                if [j-1,i] not in stk:
                    stk.append([j-2,i])
                stk.append([j-1,i])
                if j==len(self.mat1bis)-1:
                    cut="true"
                if ((j!=len(self.mat1bis)-1 or i!=len(self.mat1bis[0])-1)) and cut=="false":
                    j+=1
            if len(stk)>1:
                linev.append(stk)
                stk=[]
            if i!=len(self.mat1bis[0])-1 and j==len(self.mat1bis)-1:
                i+=1
                j=0
            else:
                if j!=len(self.mat1bis)-1 or i!=len(self.mat1bis[0])-1:
                    j+=1
        st=[]
        self.g=Graphe()
        reussi=0
        #On met des point à l'intersection de 2 ligne
        for l1 in range(len(lineh)):
            for e1 in range(len(lineh[l1])):
                for l2 in range(len(linev)):
                    for e2 in range(len(linev[l2])) :
                        if lineh[l1][e1]==linev[l2][e2]:
                            pt=Point(lineh[l1][e1][0],lineh[l1][e1][1])
                            n=len((self.g.pts))
                            self.g.add_pts(pt)
                            st+=[[lineh[l1][e1],l1,l2,n]]
                            if lineh[l1][e1][0]==-1:
                                self.s=n
                            elif lineh[l1][e1][0]==7:
                                reussi=1
                                self.e=n
        #On lie les 2 points d'une même ligne               
        for k in range(len(st)):
            for m in range(k+1,len(st)):
                if st[k][1]==st[m][1] or st[k][2]==st[m][2]:
                    self.g.link([[st[k][3],st[m][3]]])
                
                        

def labaff(h,v,x,y,c):
    #Affichage du labyrinthe par parcour des matrices
    for i in range(len(h)):
        for j in range(len(h[0])):
            if h[i][j]==1:
                canv.create_line(j*c+x, i*c+y, j*c+x,i*c+y+c, fill="black", width=1)
                
    for i in range(len(v)):
        for j in range(len(v[0])):
            if v[i][j]==1:
                canv.create_line(j*c+x, i*c+y, j*c+x+c,i*c+y, fill="black", width=1)

def v_absolue(x):
    if x>=0:
        return x
    else:
        return -x

def d_manathan(p1,p2):
    #distance avec des valeur absolue plus simple à gérer
    return v_absolue(p1.x-p2.x)+v_absolue(p1.y-p2.y)

def maxs(l):
    #liste des maximums d'une liste
    m=[l[0]]
    for i in range(1,len(l)):
        if l[i]>=m[0]:
            m=[l[i]]
        else :
            m+=l[i]
    return m

def Aetoile(la):
    #algorithme Astar
    laff=[]
    g=la.g
    p=la.e
    #closedl formés du minimum de openlcost choisit à chaque tour de boucle
    closedl=[]
    #openl liste des points visités et openlcost liste du coup des point (un point non visité à un coût fixé à 1000 pour ne pas qu'il intérfère avec le chemin.
    openl=[]
    openlcost=[1000 for x in range (len(g.pts))]
    #tant que le point n'est pas le point de sortie
    while p!=la.s:
        for i in range(len(g.mata)):
            if i not in closedl:
                #on récupére les points accesibles depuis le point courant et on définit leur coût.
                if g.mata[p][i]==1:
                    gcost=d_manathan(g.pts[i],g.pts[la.e])
                    hcost=4*d_manathan(g.pts[i],g.pts[la.s])
                    fcost=hcost+gcost
                    if i not in openl:
                        openlcost[i]=fcost
                        openl+=[i]
                        laff+=[["o",i]]
                        g.pts[i].cost=[gcost,hcost,fcost]
                        g.pts[i].parent=[p]+g.pts[p].parent
                        

                    elif g.pts[i].cost[2]<fcost or (g.pts[i].cost[2]==fcost and g.pts[i].cost[1]<hcost):
                        openlcost[i]=fcost
                        g.pts[i].cost=[gcost,hcost,fcost]
                        g.pts[i].parent=p
        #on cherche le minimum de openl (si cout égaux on privilégie le distance à l'arrivée)
        minp=min(openlcost)
        l2=list(openlcost)
        lindex=[]
        if openlcost.index(minp) in closedl:
            a=1
            while a==1:
                for c in range(len(openlcost)):
                    if openlcost[c]==minp and c not in closedl:
                        a=0
                if a==1:
                    while min(l2)==minp:
                        l2.remove(minp)
                    minp=min(l2)
                    
        for t in range (len(openlcost)):
            if openlcost[t]==minp and t not in closedl:
                lindex+=[t]
        maxi=lindex[0]
        if len(lindex)>1:
            for m in (1,len(lindex)-1):
                if g.pts[lindex[m]].cost[1]<g.pts[maxi].cost[1]:
                    if lindex not in closedl:
                        if lindex[m] not in closedl:
                            maxi=lindex[m]
        closedl+=[maxi]
        laff+=[["c",maxi]]
        p=maxi
    #une fois la sortie trouvée on peut reconstituer le chemin à partir des parents de la sortie.
    la.di=0
    for ch in range (1,len(g.pts[p].parent)):
        la.di+=d_manathan(g.pts[g.pts[p].parent[ch-1]],g.pts[g.pts[p].parent[ch]])
    return laff
           
                
def animation():
    global i,l,cx,cy,ca,lab,ind,z,score,fin
    """animation du robot (animation Astar, animation de la voiture avec la fonction tkinter after qui permet d'appeler une fonction avec un décalge de temps
    les fonction d'annimation sont donc pensées comme des fonction recursives"""
    if fin==0:
        if l[i][0]=="o":
            canv.create_rectangle(3+cx+ca/2+lab.g.pts[l[i][1]].x*ca,3+cy+ca/2+lab.g.pts[l[i][1]].y*ca,cx+ca/2+lab.g.pts[l[i][1]].x*ca-3,cy+ca/2+lab.g.pts[l[i][1]].y*ca-3,fill="blue")
        else:
            canv.create_rectangle(3+cx+ca/2+lab.g.pts[l[i][1]].x*ca,3+cy+ca/2+lab.g.pts[l[i][1]].y*ca,cx+ca/2+lab.g.pts[l[i][1]].x*ca-3,cy+ca/2+lab.g.pts[l[i][1]].y*ca-3,fill="red")
        i+=1
        if i<=len(l)-1:
            racine.after(int(400/score),animation)
        else:
            for ch in range (1,len(lab.g.pts[lab.s].parent)):
                canv.create_line(cx+ca/2+lab.g.pts[lab.g.pts[lab.s].parent[ch-1]].x*ca,cy+ca/2+lab.g.pts[lab.g.pts[lab.s].parent[ch-1]].y*ca,cx+ca/2+lab.g.pts[lab.g.pts[lab.s].parent[ch]].x*ca,cy+ca/2+lab.g.pts[lab.g.pts[lab.s].parent[ch]].y*ca,fill="red",width=5)
            canv.create_line(cx+ca/2+lab.g.pts[lab.g.pts[lab.s].parent[0]].x*ca,cy+ca/2+lab.g.pts[lab.g.pts[lab.s].parent[0]].y*ca,cx+ca/2+lab.g.pts[lab.s].x*ca,cy+ca/2+lab.g.pts[lab.s].y*ca,fill="red",width=5)
            i=0
            if ind[4]!=100:
                ind[4]+=1
            if ind[4]<4:
                l=Aetoile(ind[ind[4]])
                lab=ind[ind[4]]
                if ind[4]==1:
                    cx=ca+7*ca+2*ca+14*ca
                    cy=ca
                elif ind[4]==2:
                    cx=ca+2*ca+14*ca
                    cy=ca+7*ca
                elif ind[4]==3:
                    cx=ca+2*ca+14*ca
                    cy=ca
                racine.after(int(400/score),animation)
            else:
                choix_cote()
            
def choix_cote():
    global i,l,cx,cy,ca,lab,ind,z,fin,score
    if fin==0:
        if ind[4]!=100:
            if ind[0].di+ind[1].di>=ind[2].di+ind[3].di and ind[4]!=100:
                ind[0],ind[1],ind[2],ind[3]=ind[2],ind[3],ind[0],ind[1]
                canv.move(canv.image,-30,-7)
            else:
                canv.move(canv.image,10,-7)
            ptfin=Point(ind[0].g.pts[ind[0].s].y+1,ind[0].g.pts[ind[0].s].x)
        else:
            ptfin=Point(ind[0].g.pts[ind[0].s].y,ind[0].g.pts[ind[0].s].x)
        ind[0].g.add_pts(ptfin)
        ind[0].g.pts[ind[0].s].parent.insert(0,len(ind[0].g.pts)-1)
        z=len(ind[0].g.pts[ind[0].s].parent)-1
        racine.after(int(400/score),animation2)
    
        

def animation2():
    #suite de l'animation
    global ca,ind,z,cpt,fin,score,fin
    if fin==0:
        if z>0:
            if ind[0].g.pts[ind[0].g.pts[ind[0].s].parent[z-1]].x<ind[0].g.pts[ind[0].g.pts[ind[0].s].parent[z]].x:
                if cpt>v_absolue(ind[0].g.pts[ind[0].g.pts[ind[0].s].parent[z-1]].x-ind[0].g.pts[ind[0].g.pts[ind[0].s].parent[z]].x)*2-1:
                    cpt=v_absolue(ind[0].g.pts[ind[0].g.pts[ind[0].s].parent[z-1]].x-ind[0].g.pts[ind[0].g.pts[ind[0].s].parent[z]].x)*2-1
                    rotate("q",1)
                if cpt>=0:
                    canv.move(canv.image,-0.5*ca,0)
                    cpt-=1
                else:
                    z-=1
                    cpt=100
                racine.after(int(400/score),animation2)
            elif ind[0].g.pts[ind[0].g.pts[ind[0].s].parent[z-1]].x>ind[0].g.pts[ind[0].g.pts[ind[0].s].parent[z]].x:
                if cpt>v_absolue(ind[0].g.pts[ind[0].g.pts[ind[0].s].parent[z-1]].x-ind[0].g.pts[ind[0].g.pts[ind[0].s].parent[z]].x)*2-1:
                    cpt=v_absolue(ind[0].g.pts[ind[0].g.pts[ind[0].s].parent[z-1]].x-ind[0].g.pts[ind[0].g.pts[ind[0].s].parent[z]].x)*2-1
                    rotate("d",1)
                if cpt>=0:
                    canv.move(canv.image,0.5*ca,0)
                    cpt-=1
                else:
                    z-=1
                    cpt=100
                racine.after(int(400/score),animation2)
            elif ind[0].g.pts[ind[0].g.pts[ind[0].s].parent[z-1]].y<ind[0].g.pts[ind[0].g.pts[ind[0].s].parent[z]].y:
                if cpt>v_absolue(ind[0].g.pts[ind[0].g.pts[ind[0].s].parent[z-1]].y-ind[0].g.pts[ind[0].g.pts[ind[0].s].parent[z]].y)*2-1:
                    cpt=v_absolue(ind[0].g.pts[ind[0].g.pts[ind[0].s].parent[z-1]].y-ind[0].g.pts[ind[0].g.pts[ind[0].s].parent[z]].y)*2-1
                    rotate("z",1)
                if cpt>=0:
                    canv.move(canv.image,0,-0.5*ca)
                    cpt-=1
                else:
                    z-=1
                    cpt=100
                racine.after(int(400/score),animation2)
            elif ind[0].g.pts[ind[0].g.pts[ind[0].s].parent[z-1]].y>ind[0].g.pts[ind[0].g.pts[ind[0].s].parent[z]].y:
                if cpt>v_absolue(ind[0].g.pts[ind[0].g.pts[ind[0].s].parent[z-1]].y-ind[0].g.pts[ind[0].g.pts[ind[0].s].parent[z]].y)*2-1:
                    cpt=v_absolue(ind[0].g.pts[ind[0].g.pts[ind[0].s].parent[z-1]].y-ind[0].g.pts[ind[0].g.pts[ind[0].s].parent[z]].y)*2-1
                    rotate("s",1)
                if cpt>=0:
                    canv.move(canv.image,0,0.5*ca)
                    cpt-=1
                else:
                    z-=1
                    cpt=100
                racine.after(int(400/score),animation2)
            else:
                z-=1
                racine.after(0,animation2)
        else:
            if ind[4]!=100:
                ind[0],ind[1]=ind[1],ind[0]
                rotate("z",1)
                z=len(ind[0].g.pts[ind[0].s].parent)-1
                ind[4]=100
                racine.after(0,choix_cote)
            else:
                replay('bot')

def rotate(dire,user):
    #fonction pour tourner l'image du skin.
    global xbot,ybot,xuser,yuser,refuser,refbot,ca
    decalx,decaly,deform=0,0,1
    if user==1:
        xcoo,ycoo,decalx,decaly=canv.coords(canv.image)[0]+xbot,canv.coords(canv.image)[1]+ybot,0,0
        xbot,ybot=0,0
    else:
        xcoo,ycoo,decalx,decaly=canv.coords(canv.image2)[0]+xuser,canv.coords(canv.image2)[1]+yuser,0,0
        xuser,yuser=0,0,
    x,y=0,0
    if dire=="q":
        if user==2 and refuser=="image/skin2.png" or refuser=="image/skin3.png":
            deform=0
        elif user==1 and refbot=="image/skin2.png" or refuser=="image/skin3.png":
            deform=0
        a=90
        x-=4
        decalx+=4
        y+=8.5
        decaly-=8.5
    elif dire=="s":
        a=180
        x+=10
        y+=7
        decalx-=10
        decaly-=7
    elif dire=="d":
        if user==2 and refuser=="image/skin2.png" or refuser=="image/skin3.png":
            deform=0
        elif user==1 and refbot=="image/skin2.png" or refuser=="image/skin3.png":
            deform=0
        a=270
        x+=4
        decalx-=4
        y-=8.5
        decaly+=8.5
    else:
        a=0
        x-=10
        y-=7
        decalx+=10
        decaly+=7
    if user==1:
        canv.delete(canv.image)
        if deform==0:
            if dire=="d":
                canv.img=ImageTk.PhotoImage(canv.imgod.resize((ca,int(ca/2))))
            else:
                canv.img=ImageTk.PhotoImage(canv.imgod.resize((ca,int(ca/2))).rotate(180))
        else:
            canv.img=ImageTk.PhotoImage(canv.imgo.rotate(a))
        canv.image=canv.create_image(xcoo+decalx,ycoo+decaly,image=canv.img)
        xbot+=x
        ybot+=y
    else:
        canv.delete(canv.image2)
        if deform==0:
            if dire=="d":
                canv.img2=ImageTk.PhotoImage(canv.imgo2d.resize((ca,int(ca/2))))
            else:
                canv.img2=ImageTk.PhotoImage(canv.imgo2d.resize((ca,int(ca/2))).rotate(180))
        else:
            canv.img2=ImageTk.PhotoImage(canv.imgo2.rotate(a))
        canv.image2=canv.create_image(xcoo+decalx,ycoo+decaly,image=canv.img2)
        xuser+=x
        yuser+=y
        
def wallcheck(labyrinthe,direction,decalage1,decalage2):
    #vérifie si il y a un mur dans la diretion où l'utilisateur souhaite aller
    global ca
    x=int((canv.coords(canv.image2)[0]-ca-decalage1)/ca)
    y=int((canv.coords(canv.image2)[1]-ca-decalage2)/ca)
    if direction=="bas" and labyrinthe.mat1[y+1][x]==1:
        return True
    elif direction=="haut" and labyrinthe.mat1[y][x]==1:
        return True
    elif direction=="gauche" and labyrinthe.mat0[y][x]==1:
        return True
    elif direction=="droite" and labyrinthe.mat0[y][x+1]==1:
        return True
    else:
        return False

def wall(direction):
    #cherche le labyrinthe dans lequel est l'utilisateur
    global labuser,ca
    x,y=canv.coords(canv.image2)
    if ca<x<7*ca+ca and ca<y<7*ca+ca:
        return wallcheck(labuser[0],direction,0,0)
    elif ca+7*ca<x<ca+14*ca and ca<y<7*ca+ca:
        return wallcheck(labuser[1],direction,7*ca,0)
    elif ca<x<7*ca+ca and 7*ca+ca<y<14*ca+ca:
        return wallcheck(labuser[2],direction,0,7*ca)
    elif ca+7*ca<x<ca+14*ca and 7*ca+ca<y<14*ca+ca:
        return wallcheck(labuser[3],direction,7*ca,7*ca)
    else:
        return False
  
i,z,cpt,ind,labuser,lab,ca,cx,cy,xbot,ybot,xuser,yuser,fin,score,play,refuser=0,0,100,[],[],0,40,0,0,0,0,0,0,0,1,0,"image/skin1.png"
lref=["image/skin1.png","image/skin2.png","image/skin3.png"]
refbot=lref[randint(0,2)]

racine = tk.Tk()
canv = tk.Canvas(racine, bg="white", height=16*ca, width=31*ca)
canv.bind("<Button-2>")
canv.pack()

def get_skins(cox=ca+7.5*ca-10,coy=ca+14.5*ca+7):
    #récupérer les skins (il sont effacés lors du redémarrage.
    global refuser,refbot
    imgo2=Image.open(refuser)
    if refuser=="image/skin2.png":
        imgo2=imgo2.resize((int(ca/2),ca))
        imgo2d=Image.open("image/skin2d.png")
        canv.imgo2d=imgo2d.resize((ca,int(ca/2)))
    elif refuser=="image/skin3.png":
        imgo2=imgo2.resize((int(ca/2),ca))
        imgo2d=Image.open("image/skin3d.png")
        canv.imgo2d=imgo2d.resize((ca,int(ca/2)))
    else:
        imgo2=imgo2.resize((100,100))
    canv.imgo2=imgo2
    img2=ImageTk.PhotoImage(imgo2)
    canv.img2=img2
    image2=canv.create_image(int(cox),int(coy),image=img2)
    canv.image2=image2
    imgo=Image.open(refbot)
    if refbot=="image/skin2.png":
        imgo=imgo.resize((int(ca/2),ca))
        imgod=Image.open("image/skin2d.png")
        canv.imgod=imgod.resize((ca,int(ca/2)))
    elif refbot=="image/skin3.png":
        imgo=imgo.resize((int(ca/2),ca))
        imgod=Image.open("image/skin3d.png")
        canv.imgod=imgod.resize((ca,int(ca/2)))
    else:
        imgo=imgo.resize((100,100))
    canv.imgo=imgo
    img=ImageTk.PhotoImage(imgo)
    canv.img=img
    image=canv.create_image(ca+7.5*ca-10+2*ca+14*ca,ca+14.5*ca+7,image=img)
    canv.image=image

compt=0

def deplacement_bas(event):
    global ca,fin,compt
    if fin==0:
        x,y=canv.coords(canv.image2)
        if y!=ca+14.5*ca+7:
            rotate("s",2)
            if wall("bas")==False and fin==0 and compt==0:
                racine.after(0,deplacement2bas)

def deplacement2bas():
    global compt
    canv.move(canv.image2,0,ca/4)
    if compt<3:
        racine.after(50,deplacement2bas)
        compt+=1
    else:
        compt=0
    
racine.bind('<KeyPress-s>',deplacement_bas)

#déplacement en 4 temps pour donner un effet moins sacadé
def deplacement_haut(event):
    global ca,fin
    if fin==0:
        x,y=canv.coords(canv.image2)
        if y!=ca+14.5*ca+7:
            rotate("z",2)
            if wall("haut")==False and fin==0 and compt==0:
                racine.after(0,deplacement2haut)
                if y<2*ca:
                    replay('user')

def deplacement2haut():
    global compt
    canv.move(canv.image2,0,-ca/4)
    if compt<3:
        racine.after(50,deplacement2haut)
        compt+=1
    else:
        compt=0

    
racine.bind('<KeyPress-z>',deplacement_haut)

def deplacement_gauche(event):
    global ca,fin
    if fin==0:
        x,y=canv.coords(canv.image2)
        rotate("q",2)
        if y==ca+14.5*ca+7:
            canv.move(canv.image2,-30,-7)
        else:
            if wall("gauche")==False and fin==0 and compt==0:
                racine.after(50,deplacement2gauche)

def deplacement2gauche():
    global compt
    canv.move(canv.image2,-ca/4,0)
    if compt<3:
        racine.after(50,deplacement2gauche)
        compt+=1
    else:
        compt=0
    
racine.bind('<KeyPress-q>',deplacement_gauche)

def deplacement_droite(event):
    global ca,fin
    if fin==0:
        x,y=canv.coords(canv.image2)
        rotate("d",2)
        if y==ca+14.5*ca+7:
            canv.move(canv.image2,10,-7)
        else:
            if wall("droite")==False and fin==0 and compt==0:
                racine.after(50,deplacement2droite)

def deplacement2droite():
    global compt
    canv.move(canv.image2,ca/4,0)
    if compt<3:
        racine.after(50,deplacement2droite)
        compt+=1
    else:
        compt=0
    
racine.bind('<KeyPress-d>',deplacement_droite)

def replay(winner):
    #fonction qui reinisialise les variables aux valeurs souhaitées et affiche l'écran de victoire/défaite
    global i,z,cpt,ind,labuser,lab,ca,cx,cy,xbot,ybot,xuser,yuser,fin,score,play,compt
    fin=1
    canv.delete("all")
    voiture=Image.open("image/voiture.png")
    voiture=voiture.resize((500,500))
    voiture=ImageTk.PhotoImage(voiture)
    canv.voiture=voiture
    if winner=="bot":
        lose=Image.open("image/lose.png")
        lose=lose.resize((250,150))
        lose=ImageTk.PhotoImage(lose)
        canv.lose=lose
        canv.create_image(15*40,8*40+40,image=voiture)
        canv.create_image(11.5*40+40,100+40,image=lose)
        canv.create_text(11.5*40,100+40+120,text=f"score:{score-1}",fill = 'red', font = ( 'courier', 20))
    else:
        score+=1
        victoire=Image.open("image/Victory.png")
        victoire=victoire.resize((300,250))
        victoire=ImageTk.PhotoImage(victoire)
        canv.victoire=victoire
        canv.create_image(15*40,8*40+40,image=voiture)
        canv.create_image(11.5*40,100+30,image=victoire)
        canv.create_text(11.5*40,100+30+40,text=f"score:{score-1}",fill = 'blue', font = ( 'courier', 20))
    i,z,cpt,ind,labuser,ca,cx,cy,xbot,ybot,xuser,yuser,play,compt=0,0,100,[],[],40,0,0,0,0,0,0,1,0
    canv.button=racine.bind('<Double-1>',pregame)

def pregame(event):
    #écran de chargement
    canv.delete("all")
    chargement=Image.open("image/chargement.png")
    chargement=chargement.resize((600,350))
    canv.chargemento=chargement
    chargement=ImageTk.PhotoImage(chargement)
    canv.chargementphoto=chargement
    canv.chargement=canv.create_image(15.5*ca,8*ca,image=chargement)
    racine.after(10,game)
    
def game():
    global i,l,cx,cy,ca,lab,ind,labuser,fin,game,play
    #déroulement d'une partie : on crée les labyrinthes, on enlève l'écran de chargement, on affiche le labyrinthe et lance les aétoile et les animations
    canv
    ca=40
    cx=40
    cy=40
    e=Laby(7)
    e.kurskal()
    f=Laby(7)
    f.kurskal()
    g=Laby(7)
    g.kurskal()
    h=Laby(7)
    h.kurskal()
    o=[randint(0,6) for x in range(4)]
    e.mat1[7][o[0]]=0
    e.mat1[0][o[1]]=0
    g.mat1[7][o[2]]=0
    g.mat1[0][o[3]]=0
    h.mat1[7][0]=0
    h.mat1[0][o[2]]=0
    f.mat1[7][6]=0
    f.mat1[0][o[0]]=0
    e.graphe(o[0],o[1])
    f.graphe(6,o[0])
    g.graphe(o[2],o[3])
    h.graphe(0,o[2])
    if play==0:
        play=1
        game_musique()
    fin=0
    canv.delete("all")
    get_skins()
    labaff(e.mat0,e.mat1,ca,ca,ca)
    labaff(f.mat0,f.mat1,ca,ca+7*ca,ca)
    labaff(g.mat0,g.mat1,ca+7*ca,ca,ca)
    labaff(h.mat0,h.mat1,ca+7*ca,ca+7*ca,ca)
    labaff(e.mat0,e.mat1,ca+2*ca+14*ca,ca,ca)
    labaff(f.mat0,f.mat1,ca+2*ca+14*ca,ca+7*ca,ca)
    labaff(g.mat0,g.mat1,ca+7*ca+2*ca+14*ca,ca,ca)
    labaff(h.mat0,h.mat1,ca+7*ca+2*ca+14*ca,ca+7*ca,ca)
    e.g.aff(cy+2*ca+14*ca,ca,ca)
    h.g.aff(ca+7*ca+2*ca+14*ca,ca+7*ca,ca)
    f.g.aff(ca+2*ca+14*ca,ca+7*ca,ca)
    g.g.aff(cx+7*ca+2*ca+14*ca,cy,ca)
    ind=[h,g,f,e,0]
    labuser=[e,g,f,h]
    l=Aetoile(h)
    cx=ca+7*ca+2*ca+14*ca
    cy=ca+7*ca
    lab=h
    racine.after(150,animation)

def game_musique():
    global play
    if play==1:
        if pygame.mixer.get_busy():
            pygame.mixer.stop()
        pygame.mixer.init()
        pygame.mixer.music.load("musique/Musique_principale.wav")   
        pygame.mixer.music.play()
        racine.after(134000,game_musique)
def musique_menu():
    global play
    if play==0:
        if pygame.mixer.get_busy():
            pygame.mixer.stop()
        pygame.mixer.init()
        pygame.mixer.music.load("musique/musique_menu_fini.mp3")   
        pygame.mixer.music.play()
        racine.after(21000,musique_menu)

def musique_fin():
    global play
    if play==2:
        if pygame.mixer.get_busy():
            pygame.mixer.stop()
        pygame.mixer.init()
        pygame.mixer.music.load("musique/musique_fin.mp3")   
        pygame.mixer.music.play()
        racine.after(73000,musique_fin)


menu = Image.open("image/giphy_voiture.gif")
menu=menu.resize((31*ca,16*ca))
photo = ImageTk.PhotoImage(menu)
canv.create_image(0, 0, anchor='nw', image=photo)
canv.create_text(15.5*ca,7*ca, text = 'Bienvenue sur Laby Car 2.0 !', fill = 'red', font = ( 'courier', 40))
#canv.create_rectangle(50,5)
canv.button=racine.bind('<Double-1>',pregame)

#pour changer de skin
def skin1(event):
    global refuser
    refuser="image/skin1.png"
    get_skins(canv.coords(canv.image2)[0],canv.coords(canv.image2)[1])

def skin2(event):
    global refuser,xuser,yuser
    refuser="image/skin2.png"
    get_skins(canv.coords(canv.image2)[0],canv.coords(canv.image2)[1])

def skin3(event):
    global refuser
    refuser="image/skin3.png"
    get_skins(canv.coords(canv.image2)[0],canv.coords(canv.image2)[1])

racine.bind('<KeyPress-1>',skin1)
racine.bind('<KeyPress-2>',skin2)
racine.bind('<KeyPress-3>',skin3)

def credit(event):
    global fin,play
    #écran des crédits en appuyant sur c
    fin=1
    canv.delete("all")
    couleur=Image.open("image/couleur.png")
    couleur=couleur.resize((31*ca,16*ca))
    couleur=ImageTk.PhotoImage(couleur)
    canv.couleur=couleur
    canv.chargement=canv.create_image(15.5*ca,8*ca,image=couleur)
    merci=ImageTk.PhotoImage(Image.open("image/credits.jpg"))
    canv.credit=merci
    canv.create_rectangle(15.5*ca-170,8*ca-160,15.5*ca+170,8*ca+160, fill = 'black')
    canv.merci=canv.create_image(15.5*ca,8*ca,image=merci)
    canv.create_text(6*ca,5*ca, text = 'Quentin : skins,code,idée ! ', fill = 'white', font = ( '', 15))
    canv.create_text(24*ca,5*ca, text ='Nicolas : musique,skins,idée !', fill = 'white', font = ( '', 15))
    canv.create_text(6*ca,10*ca, text ='Pierre : code,idée !', fill = 'white', font = ( '', 15))
    canv.create_text(24*ca,10*ca, text ='Maël : code,idée !', fill = 'white', font = ( '', 15))
    play=2
    musique_fin()
    
    

racine.bind('<KeyPress-c>',credit)
musique_menu()
canv.create_text(15.5*ca,2*ca, text = 'Double cliquez pour jouer !', fill = 'red', font = ( 'courier', 20))
racine.mainloop()




