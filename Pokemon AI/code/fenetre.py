
from tkinter import * 
from PIL import Image, ImageTk


class Fenetre(Tk):
    """Definit la fenêtre dans laquelle sera fait tout les affichages graphiques.
    Elle hérite de Tk (les fenêtres de tkinter) et sera donc considérée comme une 
    fenêtre avec specifique à notre jeu."""
    w3 = 0
    w2 = 0
    h = 0
    w = 0
    h_poke = 0
    w_poke = 0
    x_poke_face = 0
    y_poke_face = 0
    x_poke_dos = 0
    y_poke_dos = 0
    
    def __init__(self):
        Tk.__init__(self)
        #variable qui fait l'intermediaire entre la fenêtre et l'interface.
        self.choix = StringVar(self) 
        #Récupération des dimension de l'écran.
        Fenetre.h = self.winfo_screenheight()
        Fenetre.w = self.winfo_screenwidth() 
        #definition des principaux éléments de la fenêtre
        Fenetre.w2 = int(Fenetre.w*7/9)
        Fenetre.w3 = int(Fenetre.w*2/9)
        Fenetre.h_poke = int(Fenetre.h*(35/100))
        Fenetre.w_poke = int(Fenetre.w2*(25/100))
        Fenetre.x_poke_face = int(Fenetre.w2*(57/100))
        Fenetre.y_poke_face = int(Fenetre.h*(65/100))
        Fenetre.x_poke_dos = int(Fenetre.w2*(15/100))
        Fenetre.y_poke_dos = int(Fenetre.h*(99/100))
        self.geometry(f"{Fenetre.h}x{Fenetre.w}") #dimensions fixées
        
        self._f_droite = None #frame avec les boutons.
                              #elle change en fonction des demandes.
        self.f_gauche = Frame(bd = 1) #frame avec le fond et les pokemons.

        #Récupération de l'image du décor.
        image = Image.open('images/decor.png')
        image_resize = image.resize((Fenetre.w2, Fenetre.h))
        self.decor = ImageTk.PhotoImage(image_resize)
        self.carte = Canvas(self.f_gauche, width = Fenetre.w2, height = Fenetre.h)   
        self.carte.pack(fill = BOTH, expand = True)
        #positionement du fond et de la frame gauche.
        self.carte.create_image(0, 0, anchor=NW, image = self.decor)
        self.f_gauche.place(x = 0, y = 0, width = Fenetre.w2, height = Fenetre.h)
    
    def switch_frame(self, frame_class, dresseur):
        """Permet de changer la frame de droite en fonction du jeu de bouton
        qu'on souhaite afficher.
        Paramètres:
        frame_class : Type Frame, la frame qu'on veut afficher
        dresseur : Dresseur (pour afficher son nom)"""
        new_frame = frame_class(self, dresseur) #inicialisation de la fenêtre.
        if self._f_droite is not None:
            self._f_droite.destroy()#destruction de l'ancienne fenêtre
        self._f_droite = new_frame
        #positionnement de la nouvelle.
        self._f_droite.place(x = Fenetre.w2, y = 0, height = Fenetre.h, width = Fenetre.w3)
    
    def placer_poke_dos(self, dos):
        """Permet de changer les image des pokemon de dos (joueur1)
        dos : str, chemin d'accés à l'image
        """
        #Récupértion de la nouvelle image
        image_d = Image.open(dos)
        image_d_resize = image_d.resize((Fenetre.w_poke, Fenetre.h_poke))
        self.Image_dos = ImageTk.PhotoImage(image_d_resize)
        #Positionnement de l'image
        self.carte.create_image(Fenetre.x_poke_dos, Fenetre.y_poke_dos, anchor = SW, image = self.Image_dos)
    
  
    def placer_poke_face(self, face):
      image_f= Image.open(face)
      image_f_resize= image_f.resize((Fenetre.w_poke, Fenetre.h_poke))
      self.Image_face = ImageTk.PhotoImage(image_f_resize)
      self.carte.create_image(Fenetre.x_poke_face, Fenetre.y_poke_face, anchor = SW, image = self.Image_face)

    def placer_poke(self, dresseur, pokemon):
        """Permet d'actualiser l'image d'un dresseur pour qu'elle corresponde à son 
        pokemon courant."""
        if dresseur.id == 'joueur2':
            self.placer_poke_face(f'images/{pokemon}_face.png')
        else:
            self.placer_poke_dos(f'images/{pokemon}_dos.png')
        
    
#En suivant : les frames utilisées dans notre jeu.
class Attaquef(Frame):
    """La frame pour choisir les attaques"""
    def __init__(self, parent, dresseur):
        Frame.__init__(self, parent)
        Label(self, text=f'{dresseur.nom},\nquelle attaque\nchoisissez-vous ?', font=("Arial", 20)).pack(side = TOP, pady = 40)
    
        """Chaque pokemon set la veriable choix à une valeur précise qui est récupérée
        par l'interface."""
        for attaque in dresseur.courant.tuple_attaque:
          Button(self, text = attaque.nom, font=("Arial", 14), command = lambda choix = attaque.nom: parent.choix.set(choix)).pack(side = TOP, padx = Fenetre.w3*3/10, pady =30)
        Button(self, text = 'Revenir au menu', font = ('Arial', 14), command = lambda choix = 'menu': \
               parent.choix.set(choix)).pack(side = BOTTOM, padx = Fenetre.w3*1/5, pady = 100)


class IHM(Frame):
    """La frame pour choisir entre attaquer et changer."""
    def __init__(self, parent, dresseur):
        Frame.__init__(self, parent)
        
        Label(self, text=f'{dresseur.nom},\nque voulez vous faire ?', font=("Arial", 20)).pack(side = TOP, pady = 50)
        Button(self, text='Attaquer', font=("Arial", 14), command = lambda choix = 'attaquer': parent.choix.set(choix)).pack(side = TOP, padx = Fenetre.w3*3/10, pady =50)
        Button(self, text='Changer', font=("Arial", 14), command = lambda choix = 'changer': parent.choix.set(choix)).pack(side = TOP, padx = Fenetre.w3*3/10, pady =50)
        Button(self, text='Information', font=("Arial", 14), command = lambda choix = 'information': \
               parent.choix.set(choix)).pack(side = TOP, padx = Fenetre.w3*3/10, pady =50)



class Changer_poke(Frame):
    """La frame pour choisir un pokemon."""
    def __init__(self, parent, dresseur):
        Frame.__init__(self, parent)
        
        Label(self, text=f'{dresseur.nom},\nquel pokemon\nchoisissez-vous ?', font=("Arial", 20)).pack(side = TOP, pady = 25, padx = 3/10)

        liste_dispo = dresseur.pokemons_dispo
        for poke in liste_dispo:
          Button(self, text = poke.nom, font=("Arial", 14), command = lambda nom = poke.nom: parent.choix.set(nom)).pack(side = TOP, \
                                                                                                                         padx = Fenetre.w3*3/10, pady =25)
        Button(self, text = 'Revenir au menu', font = ('Arial', 14), command = lambda choix = 'menu': \
               parent.choix.set(choix)).pack(side = BOTTOM, padx = Fenetre.w3*1/5, pady = 100)

          
class Etat_jeu(Frame):
    """La frame pour afficher l'etat du jeu."""
    def __init__(self, parent, dresseur = None):
        Frame.__init__(self, parent)
        
        
        
class Information(Frame):
    """La frame pour afficher les information d'un dresseur."""
    def __init__(self, parent, dresseur = None):
        Frame.__init__(self, parent)
        Button(self, text = 'Revenir au menu', font = ('Arial', 14), command = self.destroy).pack(side = TOP, padx = Fenetre.w3*1/5, pady = 15)

class Choix_joueur(Frame):
    """La frame pour choisir qui joue (entre les ia et humain)"""
    def __init__(self, parent, n):
        Frame.__init__(self, parent)
        Label(self, text=f'Le joueur {n} est :', font=("Arial", 20)).pack(side = TOP, pady = 50)
        Button(self, text='un humain', font=("Arial", 15), command = lambda choix = 'humain': parent.choix.set(choix)).pack(side = TOP, \
                                                                                                                         padx = Fenetre.w3*3/10, pady = 20)
        Button(self, text='une ia\naléatoire', font=("Arial", 15), command = lambda choix = 'ia alea': parent.choix.set(choix)).pack(side = TOP, \
                                                                                                                         padx = Fenetre.w3*3/10, pady = 20)
        Button(self, text='une ia\nbasique', font=("Arial", 15), command = lambda choix = 'ia basique': parent.choix.set(choix)).pack(side = TOP, \
                                                                                                                         padx = Fenetre.w3*3/10, pady = 20)
        Button(self, text='une ia alpha\nbeta 1.0', font=("Arial", 15), command = lambda choix = 'ia alpha beta 1': parent.choix.set(choix)).pack(side = TOP, \
                                                                                                                         padx = Fenetre.w3*3/10, pady = 20)
        Button(self, text='une ia alpha\nbeta 2.0', font=("Arial", 15), command = lambda choix = 'ia alpha beta 2': parent.choix.set(choix)).pack(side = TOP, padx = Fenetre.w3*3/10, pady = 20)
                        

class Demander_nom(Frame):
    """La frame pour demander son nom au joueur via un widjet Entry."""
    def __init__(self, parent, n):
        Frame.__init__(self, parent)
        self.parent = parent
        Label(self, text=f'Quel est le nom \ndu joueur {n} ?', font = ("Arial", 20)).pack(side = TOP, pady = 50)
        self.nom = StringVar()
        self.nom.set('nom du joueur')
        self.e = Entry(self, textvariable=self.nom, bd = 5)
        self.e.pack(side = TOP)#
     
        self.e.bind("<Return>", self.getValue)

    def getValue(self, event):
        nom_joueur = self.e.get()
        self.parent.choix.set(nom_joueur)