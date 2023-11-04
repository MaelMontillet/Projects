import pygame.mixer
from Matrices_obj import *
from random import randint,shuffle,choice,random
from math import exp
import matplotlib.pyplot as pl
import copy
from time import time,sleep
from PIL import Image,ImageTk
import tkinter as tk

sigmoid = lambda x : 1/(1+exp(-x))

input_glob={}
entr=0
def choice_input():
    
    """ Permet de donner des valeurs entrées dans la console aux neurones pour par exemple débuger le programme.
    input_glob et entr permettent de ne pas demander 2 fois la même entrée à un neurone"""
    
    global input_glob,entr
    try:
        return input_glob[entr]
    except:
        input_glob[entr]=float(input(":"))
        return input_glob[entr]
    
def random_input():
    
    """ Même utilitée que choice_input mais avec un nombres entier aléatoire entre -5 et 5"""
    
    global input_glob,entr
    try:
        return input_glob[entr]
    except:
        input_glob[entr]=randint(0,10)-5
        return input_glob[entr]

class Neuron():
    
    """
        perceptron affine d'un reseaux de neurone
        définit une fonction f telle que :
            f : R**n->R
            f(x1,..;xn)=p1*x1+p2*x2+...+pn*xn+biais
        f est la composée d'une fonction d'activation o(x) (sigmoide dans notre cas)
    """

    def __init__(self,inputt,activation,name,last_layer="",glob='false'):
        
        """ glob : permet de diriger les poids vers leur valeur la plus logique (négative pour les prédictions d'une autre figure et positive pour la
        figure en question) Ceci permet d'atteidre un mimimum local plus intéressant.
        L'execution peut se faire grâce à des "fonction d'entrée" (ex : random pour débuguer), c'est la taille de la liste de fonction qui définit le
        nombre d'entrée.
        Pour une execution par le code, on utilise la chaine "code_value" au lieu de la fonction (répétée n fois pour n entrées)."""
        
        self.inputt=inputt
        if glob=='false':
            self.weight_list=[randint(0,8)-4 for i in range(len(inputt))]
        else :
            self.weight_list=[randint(0,2) for i in range(len(inputt))]
            if glob==1:
                rang=0
            elif glob==2:
                rang=1
            else:
                rang=2
            for i in range(len(self.weight_list)):
                if i%3!=rang:
                    self.weight_list[i]*=-1
        self.biais=randint(0,6)-3
        self.activation=activation
        self.name=name
        self.last_layer=last_layer
        
    def execute(self,exentry):
        
        """ Permet d'executer le neurone, l'entrée de cette execution dépendra de la fonction d'entrée utilisée, le plus généralement elle sera donnée
        par le code dans exentry (quand input vaut "code_value")
        input_glob et entr permettent de ne pas demander 2 fois la même entrée à un neurone (si les fonction random et choice sont utilisées)
        """
        
        global entr,input_glob
        result=0
        entry=[]
        if self.inputt[0]=="code_value":
            entry=exentry
        else :
            for i in range (len(self.inputt)):
                entr=i
                entry.append(self.inputt[i](exentry))
        for e in range(len(self.weight_list)):
            result+=self.weight_list[e]*entry[e]
        
        result=self.activation(result+self.biais)
        
        return result

    def diff(self,param,x):
        
        """ Permet de dériver la fonction d'erreur (erreur quadratique) selon un des paramètres du neurone pour une valeur donnée (x) d'un
        reseaux de neurone (doit être appelé depuis la fonction de dérivation du reseau de neurone qui globalise le tout).
        La derivation se fait par paramètre et automatiquement quelque soit le réseau de neurone.
        param est une liste qui contient le nom du neurone que l'on dérive en position 0 et le numèro du paramètre selon lequel on dérive en
        position 1(quand param[1]>nombre de poids,on dérive le biais)."""
        
        """Si on dérive le neurone dans lequel on est, on retourne la dérivée de la composée d'une fonction sigmoide et d'une fonction affine. (u'*s'(u)
        avec u la fonction affine et s la fonction sigmoide)"""
        if param[1]>=len(self.inputt) and param[0]==self.name:
            #si on dérive selon la constante, rien ne multiplie la constate donc sa dérivée (u') vaut 1 il ne reste donc plus que s'(u).
            return self.execute(x)*(1-self.execute(x))
        elif param[0]==self.name :
                if self.last_layer=="":
                    """Si on dérive selon un des poids, il est multiplié par la valeur de l'execution des neurones précédents (last_layer ou par la valeur
                    d'entrée (x), s'(u) reste le même"""
                    return x[param[1]]*self.execute(x)*(1-self.execute(x))
                else :
                    return self.last_layer[param[1]].execute(x)*self.execute(x)*(1-self.execute(x))
        else :
            """Si on ne dérive pas le neurone dans lequel on est : si on ne se trouve pas dans la dernière couche on retourne la somme des dérivées selon
            le même paramêtre pour toutes les couches precedente, si on se trouve dans la dernière couche, on revoie 0."""
            if self.last_layer!="":
                last_layer_diff=sum([self.weight_list[s]*self.last_layer[s].diff(param,x) for s in range(len(self.last_layer))])
                return last_layer_diff*self.execute(x)*(1-self.execute(x))
            else:
                return 0
        

class Neural_Network():

    """ Définit un reseau de neurone de la taille voulue.
    Les neurone sont stockés dans un type Matrice() de Matrices_obj.py (précedent projet) c'est utile car il s'utilise comme un tableau ce qui
    rend plus facile la manipulation du réseau."""
    
    def __init__(self,inputt,activation,layer,name,glob='false'):

        """ layer : décrit la position des neurone dans le reseau : la longeur de chaque couche est définit par la longeur de cette liste et
        la largeur de la néme couche est définit par la valeur n de layer.
        Pour stocker le tout dans une Matrice, on met un 0 à chaque emplacement vide (valeur arbitraire qui signifira pas de neurone).
        Exemple:
        Pour layer=[3,2,3,1] (n=>neurone):
        [[n1,n4,n6,n9],
         [n2,n5,n7,0 ],
         [n3,0 ,n8,0 ]]
         """
        
        width=max(layer)
        self.network=Matrice([0]*width*len(layer),width,len(layer))
        cpt=0
        layer_list=[]
        #mise en place de la matrice
        for j in range(len(layer)):
            layer_list.append([""])
            for i in range (width):
                if cpt<layer[j]:
                    if j==0:
                        self.network[i][j]=Neuron(inputt,activation,f'{name}[{i},{j}]',"",glob)
                        layer_list[j].append(self.network[i][j])
                    else:
                        self.network[i][j]=Neuron([ layer_list[j-1][x].execute for x in range (1,len(layer_list[j-1]))],
                                                                                                    activation,f'{name}[{i},{j}]',layer_list[j-1][1:],glob)
                        layer_list[j].append(self.network[i][j])
                cpt+=1
            cpt=0
        self.name=name
        
    def execute(self,x=[]):
        
        #l'exécution du réseaux est l'execution de tout les neurones de sa derière couche.
        global input_glob
        result=[]
        for n in range(len(self.network)):
            if self.network[n][-1]!=0:
                result+=[self.network[n][-1].execute(x)]
        input_glob={}
        return result
    
    def diff(self,param,x,z,n):
        
        """Dérivation de l'erreur, appelle la mèthode de dérivation d'un neurone. z est la valeur attendue x l'entrée."""
        
        return 2*self.network[n][-1].diff(param,x)*(self.execute(x)[n]-z)
    
    def gradient_descent(self,n,entrvalue,expvalue,lots,learning_rate0,a,nsortie=1,ordre="alea",show="false",testvalue=[],testexp=[]):
        
        """ Descente de gradient appliquée sur tout les paramètre du reseau pendent un temps n pour les valeurs d'entrevalue à laquelle sont attendues
        les sorties d'expvalue.
        Cette descente peut se faire par le nombre de valeurs souhaité (lots) et dans l'ordre souhaité (alea,desc,asc).
        Il est possible d'utiliser des graphiques pour débugger et chercher à améliorer les paramètres (les graphiques sont affichés quand show=true,
        et on peut rajouter une courbe (généralement l'échatillon de test sur lequel le réseau ne s'est pas entrainé) via testvalue(valeurs à tester)
        et testexp (les valeurs attendues pour celles si).
        le learning rate peut être modifié à chaque tour : learning_rate_n+1=learning_rate_n/a*k+1"""
        
        if show=="true":
            abs=[0]
            ord=[self.E(entrvalue,expvalue,nsortie)]
            abs2=[0]
            ord2=[self.E(testvalue,testexp,nsortie)]
        t=time()
        k=0
        while time()<t+n:
            for v in range(int(len(entrvalue)/lots)):
                rand=[x for x in range(len(entrvalue))]
                
                if ordre=="desc":
                    rand.reverse()
                elif ordre=="alea":
                    shuffle(rand)
                    
                for ei in range(len(self.network)):
                    for ej in range(len(self.network[0])):
                        if type(self.network[ei][ej])!=int:
                            for ent in range(len(self.network[ei][ej].inputt)+1):
                                if time()<t+n:
                                    
                                    k+=1
                                    learning_rate=learning_rate0/(a*k+1)

                                    if nsortie==1:
                                        diff=[self.diff([self.network[ei][ej].name,ent],entrvalue[rand[vn]],expvalue[rand[vn]],0) for vn in range(v,v+lots)]
                                    else:
                                        diff=[self.diff([self.network[ei][ej].name,ent],entrvalue[rand[vn]],expvalue[rand[vn]][0],0)
                                                                                                                                for vn in range(v,v+lots)]
                                        diff+=[self.diff([self.network[ei][ej].name,ent],entrvalue[rand[vn]],expvalue[rand[vn]][1],1)
                                                                                                                                for vn in range(v,v+lots)]
                                        diff+=[self.diff([self.network[ei][ej].name,ent],entrvalue[rand[vn]],expvalue[rand[vn]][2],2)
                                                                                                                                for vn in range(v,v+lots)]
                                    
                                    if ent<len(self.network[ei][ej].inputt):
                                        self.network[ei][ej].weight_list[ent]-=1/lots*sum(diff)*learning_rate
                                    else:
                                        self.network[ei][ej].biais-=1/lots*sum(diff)*learning_rate
            if show=="true":
                abs+=[time()-t]
                ord+=[self.E(entrvalue,expvalue,nsortie)]
                abs2+=[time()-t]
                ord2+=[self.E(testvalue,testexp,nsortie)]
        if show=="true":
            pl.grid()
            pl.plot(abs,ord,color='blue')
            pl.plot(abs2,ord2,color='red')
            pl.show()
        
    def E(self,entrvalue,expvalue,nsortie=1):

        """Erreur quadratique (3 sorties ou 1 sorties)."""
        
        r1=0
        r2=0
        r3=0
        cpt=0
        for v in range(len(entrvalue)):
            if nsortie==1:
                r1+=(self.execute(entrvalue[v])[0]-expvalue[v])**2
            else:
                r1+=(self.execute(entrvalue[v])[0]-expvalue[v][0])**2
                r2+=(self.execute(entrvalue[v])[1]-expvalue[v][1])**2
                r3+=(self.execute(entrvalue[v])[2]-expvalue[v][2])**2
        if nsortie==1:
            return 1/len(entrvalue)*r1
        else:
            return 1/len(entrvalue)*r1,1/len(entrvalue)*r2,1/len(entrvalue)*r3


def dataset(data,vict):
    
    """Permet de transformer une liste de coups joués en données exploitables"""
    
    expdata=[]
    for e in range(len(data)-5):
        if data[e+5]==1:
            expdata.append([1,0,0])
        elif data[e+5]==2:
            expdata.append([0,1,0])
        elif data[e+5]==3:
            expdata.append([0,0,1])
    inter=[ list(int(data[x:x+5][i]) for i in range(5))+[vict[x+4]] for x in range(len(data)-4)]
    data1=inter
    data2=[]
    stk=[]
    for i in range(len(inter)):
        for j in inter[i]:
            if j==1:
                stk+=[1,-1,-1]
            elif j==2:
                stk+=[-1,1,-1]
            elif j==3:
                stk+=[-1,-1,1]
            else:
                stk+=[j]
        data2+=[stk]
        stk=[]
    return data1,data2,expdata

def dataset2(datalist,dataele,datan,databot,rn):
    
    """ Permet de fournir les prédictions de chacune des stratégies pour entrainer les réseaux de neurones (ensemble des prédictions sur lesquel les
    reseaux NN4,NN5,NN6, s'entrainent)
    Il y a 10 stratégies:
    un réseau de neurone qui analyse les données brutes (5 derniers coups)
    la stratégie du quadruple coup : quand l'adversaire répéte beaucoup de fois un même coup, le robot doit jouer le coup qui le contre
    quand l'adversaire gagne, le robot doit jouer ce qui l'aurait fait perdre (il refait souvent le même coup) (strategie_delta1)
    quand l'adversaire perd, le robot doit jouer ce qui l'aurait fait gagner ou du moins pas le même (il rejoue pas souvent le même coup) (strategie_deltam1)
    quand il y a match nul, l'adversaire a tendence à jouer le même coup ou le coup qui l'aurait fait gagner (strategie_delta0)
    recherche de motif lié au contexte
    fréquence de chaque coup
    recherche des réactions suite aux coup du robot
    recherche des motifs de chagement de coup
    différence entre la frequence de chaque coup lors des 8 derniers coups et la fréquence de chaque coup."""
    
    result=[]
    datastr=''.join(str(s) for s in datalist)
    for e in range(len(datan)):
        dataelestr=''.join(str(s) for s in dataele[e][:-1])
        #rns=[rn1.execute(datan[e]),rn2.execute(datan[e]),rn3.execute(datan[e])]
        rns=rn.execute(datan[e])
        inter=[rns[0],rns[1],rns[2],quadruple_coup(dataele[e])[0],quadruple_coup(dataele[e])[1],quadruple_coup(dataele[e])[2],strategie_delta0(dataele[e])[0],
               strategie_delta0(dataele[e])[1],strategie_delta0(dataele[e])[2],strategie_deltam1(dataele[e])[0],strategie_deltam1(dataele[e])[1],
               strategie_deltam1(dataele[e])[2],strategie_delta1(dataele[e])[0],strategie_delta1(dataele[e])[1],strategie_delta1(dataele[e])[2],
               motifs(datastr[:e+5],datastr,datastr)[0],motifs(datastr[:e+5],datastr,datastr)[1],motifs(datastr[:e+5],datastr,datastr)[2],
               frequence(datalist)[0],frequence(datalist)[1],frequence(datalist)[2],motifs(databot[:e+5],datastr,databot,maxlen=4,pcontext=1)[0],
               motifs(databot[:e+5],datastr,databot,maxlen=4,pcontext=1)[1],motifs(databot[:e+5],datastr,databot,maxlen=4,pcontext=1)[2],
               motifdiff(datastr[:e+5],datastr)[0],motifdiff(datastr[:e+5],datastr)[1],motifdiff(datastr[:e+5],datastr)[2]]
                                                                  
        if e<3:
            add=[]
            for i in range(e):
                add+=[dataele[i][0]]
            inter+=[frequence(datalist)[0]-frequence(add+dataele[e])[0],frequence(datalist)[1]-frequence(add+dataele[e])[1],
                                                                                                frequence(datalist)[2]-frequence(add+dataele[e])[2]]
        else:
            add=[dataele[e-3][0],dataele[e-2][0],dataele[e-1][0]]
            inter+=[frequence(datalist)[0]-frequence(add+dataele[e])[0],frequence(datalist)[1]-frequence(add+dataele[e])[1],
                                                                                                frequence(datalist)[2]-frequence(add+dataele[e])[2]]
        result+=[inter]
    return result

def executeglob(datalist,dataele,dataelem1,dataelem2,dataelem3,datan,databot,rn):
    
    """ jeu de données fournit à NN4,NN5 et NN6 pour qu'ils prédisent le prochain coup (en donnant des pondération sur chaque prédictions de chacune des
    méthodes."""
    
    dataelestr=''.join(str(s) for s in dataele[:-1])
    datastr=''.join(str(s) for s in datalist)
    add=[dataelem3,dataelem2,dataelem1]
    return [rn.execute(datan)[0],rn.execute(datan)[1],rn.execute(datan)[2],quadruple_coup(dataele)[0],quadruple_coup(dataele)[1],quadruple_coup(dataele)[2],
            strategie_delta0(dataele)[0],strategie_delta0(dataele)[1],strategie_delta0(dataele)[2],strategie_deltam1(dataele)[0],
            strategie_deltam1(dataele)[1],strategie_deltam1(dataele)[2],strategie_delta1(dataele)[0],strategie_delta1(dataele)[1],
            strategie_delta1(dataele)[2],motifs(datastr,datastr,datastr)[0],motifs(datastr,datastr,datastr)[1],
            motifs(datastr,datastr,datastr)[2],frequence(datalist)[0],frequence(datalist)[1],frequence(datalist)[2],
            motifs(databot,datastr,databot,maxlen=4,pcontext=1)[0],motifs(databot,datastr,databot,maxlen=4,pcontext=1)[1],
            motifs(databot,datastr,databot,maxlen=4,pcontext=1)[2],motifdiff(datastr,datastr)[0],motifdiff(datastr,datastr)[1],
            motifdiff(datastr,datastr)[2],frequence(datalist)[0]-frequence(add+dataele[:-1])[0],frequence(datalist)[1]-frequence(add+dataele[:-1])[1],
            frequence(datalist)[2]-frequence(add+dataele[:-1])[2]]


def quadruple_coup(data):
    if data[1:-1]==[1,1,1,1]:
        return [1,-1,-1]
    elif data[1:-1]==[2,2,2,2]:
        return [-1,1,-1]
    elif data[1:-1]==[3,3,3,3]:
        return [-1,-1,1]
    else:
        return [0,0,0]
    
def strategie_delta0(data):
    if data[-1]==0:
        result=[-1,-1,-1]
        result[data[-2]-1]=0.5
        if data[-2]==3:
            result[0]=0.5
        else:
            result[data[-2]]=0.5
        return result
    else:
        return [0,0,0]
    
def strategie_deltam1(data):
    if data[-1]==-1:
        if data[-2]==1:
            return[-1,0.5,0.5]
        else:
            result=[0.5,0.5,0.5]
            result[data[-2]-1]=-1
            return result
    else:
        return [0,0,0]
    
def strategie_delta1(data):
    if data[-1]==1:
        if data[-2]==1:
            return[1,-1,-1]
        else:
            result=[-1,-1,-1]
            result[data[-2]-1]=1
            return result
    else:
        return [0,0,0]

def frequence(data):
    p=0
    f=0
    c=0
    for e in data:
        if e==1:
            p+=1
        elif e==2:
            f+=1
        elif e==3:
            c+=1
    return p/(p+f+c),f/(p+f+c),c/(p+f+c)

def motifs(s,data,datash,maxlen="",pcontext=10,n=1,prob=[0,0,0]):
    
    """ recherche de motif (et motif en réaction au robot/motif de changement de coup)
    On compte le nombre d'occurences de chaque figure dans le contexte s de longeur n. Si necessaire (deux figures différentes trouvés) on continue
    avec un contexte de n+1. A la fin, on donne la proportion de chaque figure trouvées selon les coups trouvés.
    data est la liste dans laquelle on cherche une occurence du contexte, datsh est la liste dans laquelle on lit les valeurs qui ont suivi les contextes
    que l'on a trouvé dans data et s sert pour le contexte.
    les resultat sont pondérés par la longeur du contexte et l'ancienneté
    maxlen permet de donner un maximum de longueur de contexte recherché
    pcontexte règle la podération de la longueur du contexte (la valeurdonnée est la valeur à partir de laquelle la donnée la plus récente compte deux
    fois plus que la plus ancienne."""

    if maxlen=="":
        maxlen=len(s)
    shearch=str(datash)
    ref=str(data)
    f=shearch[:-1].find(s[-n:])
    nbr=[0,0,0]
    position=n
    if f!=-1:
        position+=f
        nbr[int(ref[f+n])-1]+=1+1/50*position
        shearch=shearch[f+1:]
        ref=ref[f+1:]
        f=shearch[:-1].find(s[-n:])
        while f!=-1 and len(shearch)>n:
            position+=f
            nbr[int(ref[f+n])-1]+=1+1/50*position
            shearch=shearch[f+1:]
            ref=ref[f+1:]
            f=shearch[:-1].find(s[-n:])
    som=sum(nbr)
    if som!=0:
        prob=[prob[i]+nbr[i]*(1+1/pcontext*n) for i in range(3)]
    if som>=2 and n<maxlen:
        return motifs(s,data,datash,maxlen,pcontext,n+1,prob)
    else:
        if sum(prob)!=0:
            return prob[0]/sum(prob),prob[1]/sum(prob),prob[2]/sum(prob)
        else:
            return [0,0,0]

def datadiffcoup(data):
    
    """ Permet de créer une suite de 2 et de 1 ou le 2 représente un coup différent du précédent et le 1 le même coup. Cela permet de faire des recherches
    dans cette suite de 1 et de 2 pour anticiper les changements ou les répétitions de coups."""
    
    datadiff=""
    for i in range(1,len(data)):
        if data[i]==data[i-1]:
            datadiff+="1"
        else:
            datadiff+="2"
    return datadiff

def motifdiff(s,data):

    """ Recherche de motif dans la suite de 1 et de 2 qui représentes les changement ou non changement de figure. Les resultats sont donné de la manière
    suivante la proportion de coup répétés touvés pour la dernière figure et la proportion de coups différents (divisée par 2) pour les 2 autres figures."""
    
    sd=datadiffcoup(s)
    datad=datadiffcoup(data)
    m=motifs(sd,datad,datad,pcontext=5)
    result=[0,0,0]
    
    if sum(m)!=0:
        for i in range(3):
            if str(i+1)==s[-1]:
                result[i]=m[0]/sum(m)
            else:
                result[i]=m[1]/sum(m)/2
    return result

def figure(event):
    
    """ Récupération de l'événement click pour choisir la figure."""

    global joueur,click,a
    click=1
    x, y = event.x,event.y
    if a==0:
        if x>=177 and x<=264 and y>=398 and y<=481:
            joueur=1
        elif x>=276 and x<=365 and y>=398 and y<=481:
            joueur=2
        elif x>=380 and x<=461 and y>=398 and y<=481:
            joueur=3

print('pierre:  1')
print('feuille:  2')
print('ciseaux: 3')
score=0
dataele=[[]]
datalist=[]
databot=""
datan=[[]]
vict=[]
cptia=0
cptpartie=0
expdata=[]
joueur=""
a=0
click=0
liste = ('pierre','feuille','ciseaux')
NN4=Neural_Network(["code_value"]*30,sigmoid,[1],"N4",1)
NN5=Neural_Network(["code_value"]*30,sigmoid,[1],"N5",2)
NN6=Neural_Network(["code_value"]*30,sigmoid,[1],"N6",3)
NN7=Neural_Network(["code_value"]*15,sigmoid,[5,3],"N7")

racine = tk.Tk()
canv = tk.Canvas(racine, bg="Black", height=15*40, width=16*40, bd=3, highlightthickness=3)
canv.pack()
racine.bind("<Button-1>",figure)


def replay(winner,ia,player):
    global joueur,score,cptia,cptpartie,click,datalist,a
    click=0
    pregame()
    if ia==1:
        af=Image.open("img/pierre.png")
        af=ImageTk.PhotoImage(af)
        canv.aff_ia=af
        canv.create_image(12*40,6.5*40,image=af)
    elif ia==2:
        af=Image.open("img/feuille.png")
        af=ImageTk.PhotoImage(af)
        canv.aff_ia=af
        canv.create_image(12*40,6.5*40,image=af)
    else:
        af=Image.open("img/cisceaux.png")
        af=ImageTk.PhotoImage(af)
        canv.aff_ia=af
        canv.create_image(12*40,6.5*40,image=af)

    if player==1:
        af=Image.open("img/pierre.png")
        af=ImageTk.PhotoImage(af)
        canv.aff_j=af
        canv.create_image(4*40,6.5*40,image=af)
    elif player==2:
        af=Image.open("img/feuille.png")
        af=ImageTk.PhotoImage(af)
        canv.aff_j=af
        canv.create_image(4*40,6.5*40,image=af)
    else:
        af=Image.open("img/cisceaux.png")
        af=ImageTk.PhotoImage(af)
        canv.aff_j=af
        canv.create_image(4*40,6.5*40,image=af)

    if winner==1:
        v=Image.open("img/Victory.png")
        v=v.resize((150,100))
        v=ImageTk.PhotoImage(v)
        canv.victoire=v
        canv.create_image(8*40,6*40,image=v)
    elif winner==0:
        e=Image.open("img/egalite.png")
        e=e.resize((150,100))
        e=ImageTk.PhotoImage(e)
        canv.egalite=e
        canv.create_image(8*40,6*40,image=e)
    else:
        d=Image.open("img/lose.png")
        d=d.resize((150,100))
        d=ImageTk.PhotoImage(d)
        canv.defaite=d
        canv.create_image(8*40,6*40,image=d)
    canv.create_text(8*40,8.5*40,text= f"     Votre score:{score}/{cptpartie} \n (score du robot :{cptia}/{cptpartie}])",fill = '#0416b8',font = ( 'Bright Star', 10))
    if len(datalist)>=10 :
        canv.create_rectangle(0*40,9*40,16*40,13.5*40, fill = 'black',width=0)
        canv.create_text(8*40,11*40,text="Le robot réfléchit...",fill ='#ede502', font = ( 'Bright Star', 15))
        a=1
    racine.after(10,reflechit)


def pregame():
    canv.delete("all")
    canv.create_text(8*40,40,text="IA PIERRE-FEUILLE-CISEAUX",fill = '#0416b8', font = ( 'BatmanForeverAlternate', 25))
    canv.create_text(8*40,2*40,text="Cliquez sur les figures pour jouer ",fill = '#ede502', font = ( 'Bright Star', 13))
    canv.create_text(4*40,4*40,text="Vous",fill = '#ede502', font = ( 'Bright Star', 15,))
    canv.create_text(12*40,4*40,text="Le robot",fill = '#ede502', font = ( 'Bright Star', 15,))
    pfc=Image.open("img/chifoumi.png")
    pfc=ImageTk.PhotoImage(pfc)
    canv.create_rectangle(2.5*40,5*40,5.5*40,8*40, fill = '#0416b8',width=3)
    canv.create_rectangle(10.5*40,5*40,13.5*40,8*40, fill = '#0416b8',width=3)
    canv.create_image(8*40,11*40,image=pfc)
    canv.create_rectangle(4.5*40-2,10*40-2,11.5*40+2,12*40,width=3)
    canv.create_text(8*40,14*40,text="Maël, Nicolas, Pierre, Quentin, Célia",fill = '#ede502', font = ( 'Bright Star', 10))
    canv.pfc=pfc

pregame()

def reflechit():
    global dataele,datalist,databot,datan,expdata,NN4,NN5,NN6,NN7,a
    if len(datalist)>=10 :
        if len(datalist)<60:
            time=0.2+1/75*len(datalist)
        else:
            time=1
        exp1=[expdata[x][0] for x in range(len(expdata))]
        exp2=[expdata[x][1] for x in range(len(expdata))]
        exp3=[expdata[x][2] for x in range(len(expdata))]
        if len(datalist)%3==0 or len(datalist)==10:
            NN7.gradient_descent(time*3,datan[:-1],expdata,1,3,10**-4,3)
        else:
            d1=dataset2(datalist,dataele[:-1],datan[:-1],databot,NN7)            
            NN4.gradient_descent(time,d1,exp1,1,1,10**-3,1)
            NN5.gradient_descent(time,d1,exp2,1,1,10**-3,1)
            NN6.gradient_descent(time,d1,exp3,1,1,10**-3,1)
        pfc=Image.open("img/chifoumi.png")
        pfc=ImageTk.PhotoImage(pfc)
        canv.create_image(8*40,11*40,image=pfc)
        canv.create_rectangle(4.5*40-2,10*40-2,11.5*40+2,12*40,width=3)
        canv.pfc=pfc
        #print("dataele=",dataele,"datalist=",datalist,"dataelebot=",dataelebot,"databot=",databot,"datan=",datan,"vict=",vict)
        a=0
    racine.after(10,game)

def game():
    
    """ déroulement du jeu / récupération des données """
    
    global score,dataele,datalist,databot,datan,vict,cptia,cptpartie,expdata,NN4,NN5,NN6,joueur,liste,click,NN7
    p1=0
    p2=0
    p3=0
    if len(datalist)>=10 :
        pred=executeglob(datalist,dataele[-1],str(dataele[-2][0]),str(dataele[-3][0]),str(dataele[-4][0]),datan[-1],databot,NN7)
        p1=NN4.execute(pred)[0]
        p2=NN5.execute(pred)[0]
        p3=NN6.execute(pred)[0]
    elif len(datalist)>=6:
        datastr=''.join(str(s) for s in datalist)
        p1,p2,p3=motifs(datastr,datastr,datastr)
        
    if len(datalist)<6:
        ia = choice((1,2,3))
    else:
        #le choix final de la figure est un aléatoire avec une répartition des probabilités selon les prédictions pour chaque figure
        limit=random()*(p1+p2+p3)
        if limit<p1:
            ia=2
        elif limit<p1+p2:
            ia=3
        else:
            ia=1

    if joueur!="":
        cptpartie+=1
        print(f'vous avez choisi:{liste[joueur-1]}')
        print(f'Le robot a choisi:{liste[ia-1]} \n')
    
    
    
        if joueur==1 and ia==3:
            score+=1
            vict+=[1]
            print("victoire")
        elif joueur==3 and ia==1:
            vict+=[-1]
            print("défaite")
            cptia+=1
        elif joueur<ia :
            vict+=[-1]
            print("défaite")
            cptia+=1
        elif joueur>ia:
            score+=1
            vict+=[1]
            print("victoire")
        else:
            vict+=[0]
            print("egalité")
        print()
        datalist+=[joueur]
        databot+=str(ia)
        if len(dataele[0])<4:
            dataele[0]+=[joueur]
            if joueur==1:
                datan[0]+=[1,-1,-1]
            elif joueur==2:
                datan[0]+=[-1,1,-1]
            else:
                datan[0]+=[-1,-1,1]
        else:
            if len(dataele[0])>5:
                dataele+=[dataele[-1][1:-1]+[joueur]]
                if joueur==1:
                    datan+=[datan[-1][3:-1]+[1,-1,-1]]
                elif joueur==2:
                    datan+=[datan[-1][3:-1]+[-1,1,-1]]
                else:
                    datan+=[datan[-1][3:-1]+[-1,-1,1]]
            else:
                dataele[0]+=[joueur]
                if joueur==1:
                    datan[0]+=[1,-1,-1]
                elif joueur==2:
                    datan[0]+=[-1,1,-1]
                else:
                    datan[0]+=[-1,-1,1]
            dataele[-1]+=[vict[-2]]
            datan[-1]+=[vict[-2]]
        if len(datalist)>=6:
            if datalist[-1]==1:
                expdata+=[[1,0,0]]
            elif datalist[-1]==2:
                expdata+=[[0,1,0]]
            else:
                expdata+=[[0,0,1]]
        replay(vict[-1],int(ia),int(joueur))
        joueur=""
    else:
        joueur=""
        racine.after(100,game)

def musique():
    if pygame.mixer.get_busy():
        pygame.mixer.stop()
    pygame.mixer.init()
    pygame.mixer.music.load("musique/chifoumi_music.mp3")
    pygame.mixer.music.play()
    racine.after(200000,musique)

musique()
game()
racine.mainloop()

"""exemple de descente de gradient de 10 secondes (ce sont 100 coups réalisés, on analyse les 50 premiers et le graphique montre l'évolution de l'erreur en fonction
du temps (la courbe blue représente l'erreur pour les coups sur lesquels le robot s'entraine et la rouge représente les 50 autres).
Le premier graphique est l'analyse brute des données et les autres sont l'analyse globale avec toutes les stratégies.
Pour les afficher, il faut mettre en commentaire game() et racine.mainloop()."""

dataele= [[1, 1, 2, 1, 3, 0], [1, 2, 1, 3, 2, 0], [2, 1, 3, 2, 3, 0], [1, 3, 2, 3, 3, 1], [3, 2, 3, 3, 1, 0], [2, 3, 3, 1, 1, 0], [3, 3, 1, 1, 3, 1],
          [3, 1, 1, 3, 3, 0], [1, 1, 3, 3, 2, 1], [1, 3, 3, 2, 2, -1], [3, 3, 2, 2, 1, -1], [3, 2, 2, 1, 1, 0], [2, 2, 1, 1, 3, 1], [2, 1, 1, 3, 2, -1],
          [1, 1, 3, 2, 3, 1], [1, 3, 2, 3, 1, -1], [3, 2, 3, 1, 1, -1], [2, 3, 1, 1, 1, 0], [3, 1, 1, 1, 2, 0], [1, 1, 1, 2, 1, 1], [1, 1, 2, 1, 3, -1],
          [1, 2, 1, 3, 3, 0], [2, 1, 3, 3, 2, 0], [1, 3, 3, 2, 2, -1], [3, 3, 2, 2, 3, 1], [3, 2, 2, 3, 3, 1], [2, 2, 3, 3, 3, -1], [2, 3, 3, 3, 1, 1],
          [3, 3, 3, 1, 2, 0], [3, 3, 1, 2, 2, 0], [3, 1, 2, 2, 1, 0], [1, 2, 2, 1, 3, 0], [2, 2, 1, 3, 3, 1], [2, 1, 3, 3, 3, 0], [1, 3, 3, 3, 2, 0],
          [3, 3, 3, 2, 1, 0], [3, 3, 2, 1, 1, 0], [3, 2, 1, 1, 2, 0], [2, 1, 1, 2, 3, -1], [1, 1, 2, 3, 3, 1], [1, 2, 3, 3, 3, -1], [2, 3, 3, 3, 1, 1],
          [3, 3, 3, 1, 2, -1], [3, 3, 1, 2, 2, 1], [3, 1, 2, 2, 1, 1], [1, 2, 2, 1, 3, -1], [2, 2, 1, 3, 2, -1], [2, 1, 3, 2, 1, 1], [1, 3, 2, 1, 1, 1],
          [3, 2, 1, 1, 3, 0], [2, 1, 1, 3, 3, -1], [1, 1, 3, 3, 2, 0], [1, 3, 3, 2, 3, 1], [3, 3, 2, 3, 3, 0], [3, 2, 3, 3, 1, -1], [2, 3, 3, 1, 1, 0],
          [3, 3, 1, 1, 2, -1], [3, 1, 1, 2, 3, 1], [1, 1, 2, 3, 2, -1], [1, 2, 3, 2, 1, 0], [2, 3, 2, 1, 3, 0], [3, 2, 1, 3, 2, 1], [2, 1, 3, 2, 2, 1],
          [1, 3, 2, 2, 1, -1], [3, 2, 2, 1, 3, 0], [2, 2, 1, 3, 3, 1], [2, 1, 3, 3, 1, -1], [1, 3, 3, 1, 1, 0], [3, 3, 1, 1, 2, -1], [3, 1, 1, 2, 1, 0],
          [1, 1, 2, 1, 3, 0], [1, 2, 1, 3, 3, -1], [2, 1, 3, 3, 2, 0], [1, 3, 3, 2, 1, -1], [3, 3, 2, 1, 1, 1], [3, 2, 1, 1, 1, -1], [2, 1, 1, 1, 2, 1],
          [1, 1, 1, 2, 2, -1], [1, 1, 2, 2, 3, 1], [1, 2, 2, 3, 3, -1], [2, 2, 3, 3, 1, -1], [2, 3, 3, 1, 2, 0], [3, 3, 1, 2, 1, 0], [3, 1, 2, 1, 3, 0],
          [1, 2, 1, 3, 2, 1], [2, 1, 3, 2, 1, -1], [1, 3, 2, 1, 3, 1], [3, 2, 1, 3, 3, 1], [2, 1, 3, 3, 2, -1], [1, 3, 3, 2, 3, 1], [3, 3, 2, 3, 3, 0],
          [3, 2, 3, 3, 1, -1], [2, 3, 3, 1, 1, 0], [3, 3, 1, 1, 2, -1], [3, 1, 1, 2, 2, -1], [1, 1, 2, 2, 3, 1]]

datalist= [1, 1, 2, 1, 3, 2, 3, 3, 1, 1, 3, 3, 2, 2, 1, 1, 3, 2, 3, 1, 1, 1, 2, 1, 3, 3, 2, 2, 3, 3, 3, 1, 2, 2, 1, 3, 3, 3, 2, 1, 1, 2, 3, 3, 3, 1, 2, 2,
           1, 3, 2, 1, 1, 3, 3, 2, 3, 3, 1, 1, 2, 3, 2, 1, 3, 2, 2, 1, 3, 3, 1, 1, 2, 1, 3, 3, 2, 1, 1, 1, 2, 2, 3, 3, 1, 2, 1, 3, 2, 1, 3, 3, 2, 3, 3, 1,
           1, 2, 2, 3]


databot= "3121322313323313111211123331212122123321132122112113113131121121213121122113332331111212332113112313"

datan= [[1, -1, -1, 1, -1, -1, -1, 1, -1, 1, -1, -1, -1, -1, 1, 0], [1, -1, -1, -1, 1, -1, 1, -1, -1, -1, -1, 1, -1, 1, -1, 0],
        [-1, 1, -1, 1, -1, -1, -1, -1, 1, -1, 1, -1, -1, -1, 1, 0], [1, -1, -1, -1, -1, 1, -1, 1, -1, -1, -1, 1, -1, -1, 1, 1],
        [-1, -1, 1, -1, 1, -1, -1, -1, 1, -1, -1, 1, 1, -1, -1, 0], [-1, 1, -1, -1, -1, 1, -1, -1, 1, 1, -1, -1, 1, -1, -1, 0],
        [-1, -1, 1, -1, -1, 1, 1, -1, -1, 1, -1, -1, -1, -1, 1, 1], [-1, -1, 1, 1, -1, -1, 1, -1, -1, -1, -1, 1, -1, -1, 1, 0],
        [1, -1, -1, 1, -1, -1, -1, -1, 1, -1, -1, 1, -1, 1, -1, 1], [1, -1, -1, -1, -1, 1, -1, -1, 1, -1, 1, -1, -1, 1, -1, -1],
        [-1, -1, 1, -1, -1, 1, -1, 1, -1, -1, 1, -1, 1, -1, -1, -1], [-1, -1, 1, -1, 1, -1, -1, 1, -1, 1, -1, -1, 1, -1, -1, 0],
        [-1, 1, -1, -1, 1, -1, 1, -1, -1, 1, -1, -1, -1, -1, 1, 1], [-1, 1, -1, 1, -1, -1, 1, -1, -1, -1, -1, 1, -1, 1, -1, -1],
        [1, -1, -1, 1, -1, -1, -1, -1, 1, -1, 1, -1, -1, -1, 1, 1], [1, -1, -1, -1, -1, 1, -1, 1, -1, -1, -1, 1, 1, -1, -1, -1],
        [-1, -1, 1, -1, 1, -1, -1, -1, 1, 1, -1, -1, 1, -1, -1, -1], [-1, 1, -1, -1, -1, 1, 1, -1, -1, 1, -1, -1, 1, -1, -1, 0],
        [-1, -1, 1, 1, -1, -1, 1, -1, -1, 1, -1, -1, -1, 1, -1, 0], [1, -1, -1, 1, -1, -1, 1, -1, -1, -1, 1, -1, 1, -1, -1, 1],
        [1, -1, -1, 1, -1, -1, -1, 1, -1, 1, -1, -1, -1, -1, 1, -1], [1, -1, -1, -1, 1, -1, 1, -1, -1, -1, -1, 1, -1, -1, 1, 0],
        [-1, 1, -1, 1, -1, -1, -1, -1, 1, -1, -1, 1, -1, 1, -1, 0], [1, -1, -1, -1, -1, 1, -1, -1, 1, -1, 1, -1, -1, 1, -1, -1],
        [-1, -1, 1, -1, -1, 1, -1, 1, -1, -1, 1, -1, -1, -1, 1, 1], [-1, -1, 1, -1, 1, -1, -1, 1, -1, -1, -1, 1, -1, -1, 1, 1],
        [-1, 1, -1, -1, 1, -1, -1, -1, 1, -1, -1, 1, -1, -1, 1, -1], [-1, 1, -1, -1, -1, 1, -1, -1, 1, -1, -1, 1, 1, -1, -1, 1],
        [-1, -1, 1, -1, -1, 1, -1, -1, 1, 1, -1, -1, -1, 1, -1, 0], [-1, -1, 1, -1, -1, 1, 1, -1, -1, -1, 1, -1, -1, 1, -1, 0],
        [-1, -1, 1, 1, -1, -1, -1, 1, -1, -1, 1, -1, 1, -1, -1, 0], [1, -1, -1, -1, 1, -1, -1, 1, -1, 1, -1, -1, -1, -1, 1, 0],
        [-1, 1, -1, -1, 1, -1, 1, -1, -1, -1, -1, 1, -1, -1, 1, 1], [-1, 1, -1, 1, -1, -1, -1, -1, 1, -1, -1, 1, -1, -1, 1, 0],
        [1, -1, -1, -1, -1, 1, -1, -1, 1, -1, -1, 1, -1, 1, -1, 0], [-1, -1, 1, -1, -1, 1, -1, -1, 1, -1, 1, -1, 1, -1, -1, 0],
        [-1, -1, 1, -1, -1, 1, -1, 1, -1, 1, -1, -1, 1, -1, -1, 0], [-1, -1, 1, -1, 1, -1, 1, -1, -1, 1, -1, -1, -1, 1, -1, 0],
        [-1, 1, -1, 1, -1, -1, 1, -1, -1, -1, 1, -1, -1, -1, 1, -1], [1, -1, -1, 1, -1, -1, -1, 1, -1, -1, -1, 1, -1, -1, 1, 1],
        [1, -1, -1, -1, 1, -1, -1, -1, 1, -1, -1, 1, -1, -1, 1, -1], [-1, 1, -1, -1, -1, 1, -1, -1, 1, -1, -1, 1, 1, -1, -1, 1],
        [-1, -1, 1, -1, -1, 1, -1, -1, 1, 1, -1, -1, -1, 1, -1, -1], [-1, -1, 1, -1, -1, 1, 1, -1, -1, -1, 1, -1, -1, 1, -1, 1],
        [-1, -1, 1, 1, -1, -1, -1, 1, -1, -1, 1, -1, 1, -1, -1, 1], [1, -1, -1, -1, 1, -1, -1, 1, -1, 1, -1, -1, -1, -1, 1, -1],
        [-1, 1, -1, -1, 1, -1, 1, -1, -1, -1, -1, 1, -1, 1, -1, -1], [-1, 1, -1, 1, -1, -1, -1, -1, 1, -1, 1, -1, 1, -1, -1, 1],
        [1, -1, -1, -1, -1, 1, -1, 1, -1, 1, -1, -1, 1, -1, -1, 1], [-1, -1, 1, -1, 1, -1, 1, -1, -1, 1, -1, -1, -1, -1, 1, 0],
        [-1, 1, -1, 1, -1, -1, 1, -1, -1, -1, -1, 1, -1, -1, 1, -1], [1, -1, -1, 1, -1, -1, -1, -1, 1, -1, -1, 1, -1, 1, -1, 0],
        [1, -1, -1, -1, -1, 1, -1, -1, 1, -1, 1, -1, -1, -1, 1, 1], [-1, -1, 1, -1, -1, 1, -1, 1, -1, -1, -1, 1, -1, -1, 1, 0],
        [-1, -1, 1, -1, 1, -1, -1, -1, 1, -1, -1, 1, 1, -1, -1, -1], [-1, 1, -1, -1, -1, 1, -1, -1, 1, 1, -1, -1, 1, -1, -1, 0],
        [-1, -1, 1, -1, -1, 1, 1, -1, -1, 1, -1, -1, -1, 1, -1, -1], [-1, -1, 1, 1, -1, -1, 1, -1, -1, -1, 1, -1, -1, -1, 1, 1],
        [1, -1, -1, 1, -1, -1, -1, 1, -1, -1, -1, 1, -1, 1, -1, -1], [1, -1, -1, -1, 1, -1, -1, -1, 1, -1, 1, -1, 1, -1, -1, 0],
        [-1, 1, -1, -1, -1, 1, -1, 1, -1, 1, -1, -1, -1, -1, 1, 0], [-1, -1, 1, -1, 1, -1, 1, -1, -1, -1, -1, 1, -1, 1, -1, 1],
        [-1, 1, -1, 1, -1, -1, -1, -1, 1, -1, 1, -1, -1, 1, -1, 1], [1, -1, -1, -1, -1, 1, -1, 1, -1, -1, 1, -1, 1, -1, -1, -1],
        [-1, -1, 1, -1, 1, -1, -1, 1, -1, 1, -1, -1, -1, -1, 1, 0], [-1, 1, -1, -1, 1, -1, 1, -1, -1, -1, -1, 1, -1, -1, 1, 1],
        [-1, 1, -1, 1, -1, -1, -1, -1, 1, -1, -1, 1, 1, -1, -1, -1], [1, -1, -1, -1, -1, 1, -1, -1, 1, 1, -1, -1, 1, -1, -1, 0],
        [-1, -1, 1, -1, -1, 1, 1, -1, -1, 1, -1, -1, -1, 1, -1, -1], [-1, -1, 1, 1, -1, -1, 1, -1, -1, -1, 1, -1, 1, -1, -1, 0],
        [1, -1, -1, 1, -1, -1, -1, 1, -1, 1, -1, -1, -1, -1, 1, 0], [1, -1, -1, -1, 1, -1, 1, -1, -1, -1, -1, 1, -1, -1, 1, -1],
        [-1, 1, -1, 1, -1, -1, -1, -1, 1, -1, -1, 1, -1, 1, -1, 0], [1, -1, -1, -1, -1, 1, -1, -1, 1, -1, 1, -1, 1, -1, -1, -1],
        [-1, -1, 1, -1, -1, 1, -1, 1, -1, 1, -1, -1, 1, -1, -1, 1], [-1, -1, 1, -1, 1, -1, 1, -1, -1, 1, -1, -1, 1, -1, -1, -1],
        [-1, 1, -1, 1, -1, -1, 1, -1, -1, 1, -1, -1, -1, 1, -1, 1], [1, -1, -1, 1, -1, -1, 1, -1, -1, -1, 1, -1, -1, 1, -1, -1],
        [1, -1, -1, 1, -1, -1, -1, 1, -1, -1, 1, -1, -1, -1, 1, 1], [1, -1, -1, -1, 1, -1, -1, 1, -1, -1, -1, 1, -1, -1, 1, -1],
        [-1, 1, -1, -1, 1, -1, -1, -1, 1, -1, -1, 1, 1, -1, -1, -1], [-1, 1, -1, -1, -1, 1, -1, -1, 1, 1, -1, -1, -1, 1, -1, 0],
        [-1, -1, 1, -1, -1, 1, 1, -1, -1, -1, 1, -1, 1, -1, -1, 0], [-1, -1, 1, 1, -1, -1, -1, 1, -1, 1, -1, -1, -1, -1, 1, 0],
        [1, -1, -1, -1, 1, -1, 1, -1, -1, -1, -1, 1, -1, 1, -1, 1], [-1, 1, -1, 1, -1, -1, -1, -1, 1, -1, 1, -1, 1, -1, -1, -1],
        [1, -1, -1, -1, -1, 1, -1, 1, -1, 1, -1, -1, -1, -1, 1, 1], [-1, -1, 1, -1, 1, -1, 1, -1, -1, -1, -1, 1, -1, -1, 1, 1],
        [-1, 1, -1, 1, -1, -1, -1, -1, 1, -1, -1, 1, -1, 1, -1, -1], [1, -1, -1, -1, -1, 1, -1, -1, 1, -1, 1, -1, -1, -1, 1, 1],
        [-1, -1, 1, -1, -1, 1, -1, 1, -1, -1, -1, 1, -1, -1, 1, 0], [-1, -1, 1, -1, 1, -1, -1, -1, 1, -1, -1, 1, 1, -1, -1, -1],
        [-1, 1, -1, -1, -1, 1, -1, -1, 1, 1, -1, -1, 1, -1, -1, 0], [-1, -1, 1, -1, -1, 1, 1, -1, -1, 1, -1, -1, -1, 1, -1, -1],
        [-1, -1, 1, 1, -1, -1, 1, -1, -1, -1, 1, -1, -1, 1, -1, -1], [1, -1, -1, 1, -1, -1, -1, 1, -1, -1, 1, -1, -1, -1, 1, 1]]

vict= [1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, -1, -1, 0, 1, -1, 1, -1, -1, 0, 0, 1, -1, 0, 0, -1, 1, 1, -1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, -1, 1, -1, 1, -1,
       1, 1, -1, -1, 1, 1, 0, -1, 0, 1, 0, -1, 0, -1, 1, -1, 0, 0, 1, 1, -1, 0, 1, -1, 0, -1, 0, 0, -1, 0, -1, 1, -1, 1, -1, 1, -1, -1, 0, 0, 0, 1, -1, 1, 1,
       -1, 1, 0, -1, 0, -1, -1, 1, 0]

expdata=dataset(datalist,vict)[2]
exp1=[expdata[x][0] for x in range(len(expdata))]
exp2=[expdata[x][1] for x in range(len(expdata))]
exp3=[expdata[x][2] for x in range(len(expdata))]


NN7.gradient_descent(10,datan[:50],expdata[:50],1,3,10**-4,3,show="true",testvalue=datan[50:-1],testexp=expdata[50:])
d1=dataset2(datalist[:50],dataele[:50],datan[:50],databot[:50],NN7)
d2=dataset2(datalist[50:],dataele[50:-1],datan[50:-1],databot[50:],NN7)
NN4.gradient_descent(10,d1,exp1[:50],5,1,10**-3,1,show="true",testvalue=d2,testexp=exp1[50:])
NN5.gradient_descent(10,d1,exp2[:50],5,1,10**-3,1,show="true",testvalue=d2,testexp=exp2[50:])
NN6.gradient_descent(10,d1,exp3[:50],5,1,10**-3,1,show="true",testvalue=d2,testexp=exp3[50:])



