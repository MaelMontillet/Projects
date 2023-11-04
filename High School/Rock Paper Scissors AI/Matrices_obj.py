class Matrice:

    def __init__(self,l,n="",p=""):
        self.l=list(l)
        #initialisation de la matrice.
        if p=="" and n=="":
            if l[0]==[]:
                self.m=[]
            else:
                self.m=l
            #premier mode d'initialisation, on donne la matrice déjà prête.
        elif p=="":
            #initialisation des matrices carrés.
            Matrice.__init__(self,l,n,n)
            #mode habitueel avec une liste et le nombre de lignes et colonnes.
        else:
            result=[]
            for i in range (n):
                result+=[l[0:p]]
                del l[0:p]
            self.m=result

    def __str__(self):
        # Affichage de la matrice.
        if len(self.m)==1:
            ch=str(self[0])
        elif len(self.m)==0:
            ch="[]"
        else:
            ch="\n / "+str(self[0])+" \ "+"\n "
            for i in range(1,len(self)-1):
                ch+="| "+str(self[i])+" |"
                ch+="\n"
            ch+=" \ "+str(self[-1])+" / "
        return ch

    def __getitem__(self,it):
        # Définition de la récup d'un item.
        return self.m[it]
    
    def __len__(self):
        #permet de donner la taille de la matrice.
        return len(self.m)
    
    def __add__(self,m2):
        #permet d'additioner deux matrices.
        if type(m2)==int:
            print(f"On ne peut additionner des type Matrices et de {type(m2)}")
            #determination si addition possible
        else:
            #addition de la matrice
            result=[]
            if len(self)==len(m2) and len(self[0])==len(m2[0]):
                stk=[]
                for i in range (len (self)):
                    for j in range (len(self[0])):
                        stk.append(self[i][j]+m2[i][j])
                    result+=[stk]
                    stk=[]
                return Matrice(result)
            
    def __mul__(self,m2):
        #multiplication de matrices.
        if type(m2)==int or type(m2)==float :
            #multiplication avec un scalaire.
            result=[list(x)for x in self]
            for n in range(len(self)):
                for p in range(len(self[0])):
                    result[n][p]=self[n][p]*m2
            return Matrice(result)
        #multiplication avec une matrice.
        elif type(m2)==Matrice or type(m2)==MatriceNulle or type(m2)==MatriceIdentite:
            result=MatriceNulle(len(self),len(m2[0])).m
            if len(self[0])!=len(m2):
                print("matrices icompatibles")
                #condition de multiplication si matrices compatibles.
            else:
                for pm2 in range(len(m2[0])):
                    for nm1 in range (len(self)):
                        stk=0
                        for pm1nm2 in range (len(m2)):
                            stk+=self[nm1][pm1nm2]*m2[pm1nm2][pm2]
                        result[nm1][pm2]=stk
                return Matrice(result)
            
    def __sub__(self,m2):
        #soustraction de matrices.
        return self+m2*(-1)

    def __pow__(self,i):
        #puissance des matrices.
        if type(i)==int:
            if len(self)==len(self[0]):
                if i==1:
                    return self
                else:
                    return self*self.__pow__(i-1)
            else:
                print("la matrice n'est pas carré")

    def delij(self,di,dj):
        # supprimer une ligne et une colonne.
        result=[list(x) for x in self]
        del result[di]
        for i in range(len(result)):
            for j in range(len(result[0])):
                if j==dj:
                    del result[i][j]
        return Matrice(result)
    
    def det(self):
        #determination du déterminant.
        if len(self)==len(self[0]):
            if len(self.m)==2:
                return self[0][0]*self[1][1]-self[0][1]*self[1][0]
            else:
                result=[]
                result=[(-1)**(1+j+1)*self[0][j]*self.delij(0,j).det() for j in range(len(self))]
                result=sum(result)
                return result
        else :
            print("la matrice n'est pas une matrice carré")
            
    def comatrice(self):
        #détermination de la comatrice utile pour la division.
        if len(self)==len(self[0]):
            result=MatriceNulle(len(self),len(self)).m
            for i in range(len(self)):
                for j in range(len(self)):
                    result[i][j]=(-1)**(i+j)*self.delij(i,j).det()
            return Matrice(result)
        else :
            print("la matrice n'est pas une matrice carré")

    def tA(self):
        #transposition de matrice.
        result=MatriceNulle(len(self),len(self)).m
        for i in range(len(self)):
            for j in range(len(self[0])):
                result[j][i] = self[i][j]
        return Matrice(result)
    
    def inverse(self):
        #inversion de matrice.
        if len(self)!=len(self[0]):
            print("la matrice n'est pas carré elle ne peut donc pas s'inverser !")
        elif self.det()==0:
            print("la matrice a un determinant égal à 0 elle ne peut donc pas s'inverser !")
        else:
            return (self.comatrice()* (1/(self.det()))).tA()
                           
    def __truediv__(self,m2):
        #division de matrices.
        if type(m2)==int:
            return self*1/m2
        elif type(m2)==Matrice or type(m2)==MatriceNulle or type(m2)==MatriceIdentite:
            return self*m2.inverse()

    def __eq__(self,m2):
        #égalité entre deux matrices.
        if type(m2)==Matrice or type(m2)==MatriceNulle or type(m2)==MatriceIdentite:
            if len(self)!=len(m2) or len(self)!=len(m2[0]):
                return "false"
            else:
                ind=0
                for n in range(len(self)):
                    for p in range (len(self[0])):
                        if self[n][p]!=m2[n][p]:
                            ind=1
                if ind == 1:
                    return "false"
                else:
                    return "true"
        else :
            print(f"Vous ne pouvez pas comparer de Matrices et des {type(m2)}")

class MatriceNulle(Matrice):
    #détermination de la matrice nulle.
    def __init__(self,p,n):
        Matrice.__init__(self,[0 for x in range(p*n)],p,n)

class MatriceIdentite(Matrice):
    #détermination de la matrice identité.
    def __init__(self,n):
        result=MatriceNulle(n,n)
        for i in range(n):
            for j in range(n):
                if i==j:
                    result[i][j]=1
        Matrice.__init__(self,result)



#batterie de test.
m1=Matrice([-1,2,4,1,5,1,2,3,5],3)
m2=Matrice([0,1,-1,3,0,1,0,2,4,1,0,-2,3,0,1],3,5)
m3=Matrice([-1,2,5,1,2,3,-2,8,10],3)
m4=Matrice([2,0,1,-3,-1,4,-7,2,0,3,5,0,-2,1,0,6],4)
m5=MatriceNulle(3,3)
m6=MatriceIdentite(3)
m7=Matrice([],00,00)

