from PIL import Image
from random import random,randint
from math import pi,cos,sin
import pickle

imgtemoin = [Image.open(f"argentique/a{i}.jpg") for i in range(1,4)]


class histogram():
    
    def __init__(self,image,liste=False):

        di={"r":{},"g":{},"b":{}}
        self.egalise_dico={"r":{},"g":{},"b":{}}
        nb=0
        
        for i in range(256):
                di["r"][i]=0
                di["g"][i]=0
                di["b"][i]=0
             
        for im in range(len(image)):
            widthimage,heightimage=image[im].size
            print(widthimage,heightimage)
            nb+=widthimage*heightimage

            for x in range(widthimage):
                for y in range(heightimage):
                    try:
                        pixel=image[im].getpixel((x,y))
                        di["r"][int(pixel[0])]+=1
                        di["g"][int(pixel[1])]+=1
                        di["b"][int(pixel[2])]+=1
                    except:
                        print(image[im].getpixel((x,y)))
            
        for i in range(256):
            di["r"][i]/=nb
            di["g"][i]/=nb
            di["b"][i]/=nb

        self.di=di

    def egaliser(self,c,k):
        try:
            return self.egalise_dico[c][k]
        except(KeyError):
            self.egalise_dico[c][k]=int((256-1)*sum([ self.di[c][i] for i in range(k+1)]))
        return self.egalise_dico[c][k]
    
    def creer_inverse(self):
        
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
        #print(self.inverse)
        
    def donner_inverse(self,c,p):
        
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
            self.inverse_dynamic[c][p]=self.inverse[c][self.plist[c][debut]]*coef2+self.inverse[c][self.plist[c][fin]]*coef1
            return self.inverse_dynamic[c][p]

histogramme_argentique=histogram(imgtemoin)
histogramme_argentique.creer_inverse()
fichier = open("histogramme_argentique.pkl", "wb")
print(histogramme_argentique.di["r"]==histogramme_argentique.di["g"] and histogramme_argentique.di["r"]==histogramme_argentique.di["b"])
pickle.dump(histogramme_argentique, fichier)
