from __future__ import annotations
import abc
from fenetre import *
from time import sleep
from tkinter import WORD
from tkinter import scrolledtext


class Interface(metaclass = abc.ABCMeta):
  """Definit la structure d'une interface du jeu pokemon.
  Elle permet de faire en sorte que jeu disute à interface sans se soucier de si
  l'interface est textuelle ou graphique.
  """
  def __init__(self):
    self.verbose = ''#stocke les informations à afficher à la fin du tour.
    
  @abc.abstractmethod
  def afficher_verbose(self):
    """Affiche les information stockées par verbose"""
    pass

  @abc.abstractmethod
  def demander_joueur(self, n):
    """Demende quel est le type du joueur n parmit : l'ia aléatoire, l'ia basique
    l'ia minimax, l'ia expectiminimax et un joueur humain."""
    pass

  @abc.abstractmethod
  def demander_choix(self, dresseur):
    """Demende le choix du joueur entre attaquer, changer et demander des information"""
    pass

  @abc.abstractmethod
  def demander_pokemon(self, dresseur):
    """Demende quel pokemon un joueur choisit parmit les pokemons disponible.
    (renvoie un objet de type pokemon)
    Post-condition : le pokemon renvoyé est deisponible (ni KO ni sur le terrain)"""
    pass

  @abc.abstractmethod
  def demander_attaque(self, dresseur):
    """Demande quel attaques parmit les attaques du pokemon courant un joueur choisit.
    Post-condition : l'attaque choisie est une attaque du pokemon courant du dresseur."""
    pass

  @abc.abstractmethod
  def demander_nom(self, n):
    """Demende le nom d'un joueur."""
    pass

  def afficher(self, str_):
    """Rajoute des informations à la verbose."""
    self.verbose += f'{str_}\n'
  
  def animation_attaque(self, dresseur):
    """Appelé pour animer une attaque."""
    self.afficher(f'le {dresseur.courant.nom} de {dresseur.nom} attaque {dresseur.courant.tuple_attaque[attaque].nom}')

  
  def animation_choix_poke(self, dresseur):
    """Appelé pour animer un choix de pokemon."""
    self.afficher(f'{dresseur.nom} choisit {dresseur.courant.nom}')

  
  def etat_pokemon(self, pokemon):
    """Rajoute les informations de pokemon (statistiques, bonus et statut) à
    la verbose."""
    str_statut = [statut + ',' for statut in pokemon.statut.keys()]
    str_bonus = f'Bonus : attaque : {pokemon.bonus["att"]}, defense : {pokemon.bonus["defense"]}, \
vitesse : {pokemon.bonus["vitesse"]}'
    if str_statut == []:
      str_statut = 'aucun'
    self.afficher(f'Nom : {pokemon} : \n\tPV : {pokemon.PV} \n\tStatuts : {"".join(str_statut)}\n\t{str_bonus}')
  
  
  def etat_joueur(self, dresseur):
    """Rajoute les informations du joueur (informations des pokemons courants,
    liste des pokemons KO, statuts du joueur...) à la verbose."""
    self.afficher(f'{dresseur} :')
    ko_j1_str = [poke.nom + ',' for poke in dresseur.liste_ko]
    if ko_j1_str != []:
      ko_j1_str[-1] = ko_j1_str[-1][:-1]
    self.afficher('Pokemon Ko :' + ' '.join(ko_j1_str))
    self.afficher('Pokemon courant :')
    self.etat_pokemon(dresseur.courant)
    str_statut = [statut + ',' for statut in dresseur.statut.keys()]
    if str_statut == []:
      str_statut = 'aucun'
    else:
      str_statut = str_statut[-1][:-1]
    self.afficher(f'Statut de dresseur : {"".join(str_statut)}')
  
  def etat_jeu(self, etat):
    """Rajoute les informations des joueurs à la verbose"""
    if etat['joueur1'].est_game_over():
      self.animation_game_over(etat['joueur1'])
    elif etat['joueur2'].est_game_over():
      self.animation_game_over(etat['joueur2'])
    else:
      self.afficher('Etat du jeu : \n')
      self.etat_joueur(etat['joueur1'])
      self.etat_joueur(etat['joueur2'])
  
  def animation_game_over(self, dresseur):
    """Appelé pour animer un choix la fin de la partie."""
    self.afficher(f'{dresseur.nom} a perdu la partie.')
  
  def animation_ko(self, dresseur):
    """Appelé pour signaler quand un pokemon est KO."""
    self.afficher(f'{dresseur.courant.nom} est KO')
  
  def information(self, dresseur):
    """Ajoute les informations de tout les pokemons"""
    liste_info = [self.etat_pokemon(poke) for poke in dresseur.pokemon.values()]
    self.afficher_verbose()

  @abc.abstractmethod
  def animation_reflexion(self):
    """Appellé quand un agent Minimax réfléchit"""
    pass

  def fin_animation_reflexion(self):
    pass


class InterfaceTexte(Interface):
    
  def afficher_verbose(self):
    print(self.verbose)
    self.verbose = ''
  
  def input_securise(self, question, erreur, mots_valables):
    """Tout les input sont fait via cette fonction afin de controler
    les réponses possibles.
    paramètres :
    Question : str, question posée au joueur
    erreur : str, message en cas d'entrée de l'utilisateur qui n'est pas valide
    mots_valables : liste de str, liste de valeurs valides."""
    mots_valables = [mot.lower() for mot in mots_valables]
    reponse = input(question).lower().strip()
    while reponse not in mots_valables:
      print(erreur)
      reponse = input(question).lower().strip()
    return reponse
  
  def demander_joueur(self, n):
    return self.input_securise(f'Le joueur {n} (ia alea, ia alpha beta 1, ia alpha beta 2, ia basique, humain) : ', 'Veuillez choisir entre ia alea, \
ia alpha beta 1, ia alpha beta 2, ia basique et humain.', ['ia alea', 'ia alpha beta 1', 'ia alpha beta 2', 'ia basique', 'humain'])

  def demander_nom(self, n):
    return input(f'nom du joueur {n}:')
  
  def demander_choix(self, dresseur):
    reponse = self.input_securise(f'{dresseur.nom} Voulez-vous attaquer ou changer de pokemon ? (attaquer, changer, information)', 'Veuillez choisir une instruction entre "attaquer", "changer" et "informatons:', ['attaquer', 'changer', 'information'])
    if reponse == "information":
      self.information(dresseur)
      return self.demander_choix(dresseur)
    else:
      return reponse
  
  def demander_pokemon(self, dresseur):
    liste_dispo = dresseur.pokemons_dispo 
    if len(liste_dispo) == 1:
      return liste_dispo[0]
    liste_pokemon = [poke.nom for poke in dresseur.pokemons_dispo]
    str_pokemon = [poke_dispo +', ' for poke_dispo in liste_pokemon]
    choix_str = self.input_securise(f"{dresseur.nom} Choisissez un pokemon parmi {''.join(str_pokemon)}ou menu\
pour revenir au menu: " , 'Veuillez choisir un pokemon de la liste ou "menu"', liste_pokemon + ['menu'])
    if choix_str == 'menu' :
      return 'menu'
    return liste_dispo[liste_pokemon.index(choix_str)]

  
  def demander_attaque(self, dresseur):
    liste_attaques = [attaque.nom for attaque in dresseur.courant.tuple_attaque]
    str_attaques = [nom +', ' for nom in liste_attaques]
    choix = self.input_securise(f"{dresseur.nom} Choisissez une attaque parmi {''.join(str_attaques)}ou menu pour revenir au menu: " , 'Veuillez choisir une attaque de la liste', liste_attaques + ['menu'])
    if choix == 'menu' :
      return 'menu'
    return dresseur.courant.tuple_attaque[liste_attaques.index(choix)]

  @staticmethod
  def rappel(fonction):
    sleep(0.05)  
    fonction()

  def animation_reflexion(self, dresseur):
    print(f'{dresseur} réfléchit')


class InterfaceGraphique(Interface):
  """Il a été choisit de mettre root en attribut de classe pour ne pas avoir deux 
  fenetres pour le même jeu.
  L'interface graphique discute avec la fenètre via l'attribut choix de fenetre.
  A chaque fois qu'il faut demender quelque chose à l'utilisateur, on change la 
  frame de droite (avec la méthode switch_frame) pour qu'elle affiche les bons
  boutons et on attend que l'utilisateur en choisisse un grâce a la méthode tkinter
  root.wait_variable qui stoppe l'execution jusqu'à ce que la variable donnée en 
  paramètre soit set. Puis on get la valeur de choix qui est renvoyée."""
  root = None
  pass_anim = False
  
  def __init__(self):
      super().__init__()
      InterfaceGraphique.root = Fenetre()
      self.choisit = None
      self.delai = 5000
      self.animation_graphique = True

  def demander_nom(self, n):
    InterfaceGraphique.root.switch_frame(Demander_nom, n)
    InterfaceGraphique.root.wait_variable(InterfaceGraphique.root.choix)
    reponse = InterfaceGraphique.root.choix.get()
    InterfaceGraphique.root.choix.set('')
    return reponse
  
  @staticmethod
  def rappel(fonction):
    InterfaceGraphique.root.after(50, fonction)
  
  def est_choisit(self, j):
    InterfaceGraphique.root.choix.set(j)

  def demander_joueur(self, n):
    InterfaceGraphique.root.switch_frame(Choix_joueur, n)
    InterfaceGraphique.root.wait_variable(InterfaceGraphique.root.choix)
    reponse = InterfaceGraphique.root.choix.get()
    return reponse       
  
  def demander_choix(self, dresseur):
    InterfaceGraphique.root.switch_frame(IHM, dresseur)
    InterfaceGraphique.root.wait_variable(InterfaceGraphique.root.choix)
    reponse = InterfaceGraphique.root.choix.get()
    if reponse == 'information':
      self.information(dresseur)
      return self.demander_choix(dresseur)
    return reponse
    
  def afficher_verbose(self):
    InterfaceGraphique.root.switch_frame(Etat_jeu, None)
    txt = Text(InterfaceGraphique.root._f_droite, wrap = WORD, height = InterfaceGraphique.root.h)
    txt.insert(INSERT, self.verbose)
    txt.pack()
    self.verbose = ''
    InterfaceGraphique.root.after(50, self.wait)

  def wait(self):
    InterfaceGraphique.root.after(self.delai)

    
  def demander_pokemon(self, dresseur):
    liste_dispo = dresseur.pokemons_dispo 
    if len(liste_dispo) == 1:
      return liste_dispo[0]
    InterfaceGraphique.root.switch_frame(Changer_poke, dresseur)
    liste_pokemon = [poke.nom for poke in dresseur.pokemons_dispo]
    InterfaceGraphique.root.wait_variable(InterfaceGraphique.root.choix)
    choix_str = InterfaceGraphique.root.choix.get()
    if choix_str == 'menu' :
      return 'menu'
    return liste_dispo[liste_pokemon.index(choix_str)]


  def demander_attaque(self, dresseur):
    InterfaceGraphique.root.switch_frame(Attaquef, dresseur)
    liste_attaques = [attaque.nom for attaque in dresseur.courant.tuple_attaque]
    InterfaceGraphique.root.wait_variable(InterfaceGraphique.root.choix)
    choix = InterfaceGraphique.root.choix.get()
    if choix == 'menu' :
      return 'menu'
    return dresseur.courant.tuple_attaque[liste_attaques.index(choix)]

  def animation_choix_poke(self, dresseur):
      super().animation_choix_poke(dresseur)
      if not InterfaceGraphique.pass_anim :
        InterfaceGraphique.root.placer_poke(dresseur, dresseur.courant.nom)

  def information(self, dresseur):
    InterfaceGraphique.root.switch_frame(Information, dresseur)
    liste_info = [self.etat_pokemon(poke) for poke in dresseur.pokemon.values()]
    txt = Text(InterfaceGraphique.root._f_droite, wrap = WORD)
    txt.insert(INSERT, self.verbose)
    txt.pack()
    InterfaceGraphique.root.wait_window(InterfaceGraphique.root._f_droite)
    self.verbose = ''
    
  def animation_reflexion(self, dresseur):
    InterfaceGraphique.pass_anim = True

  def fin_animation_reflexion(self):
    InterfaceGraphique.pass_anim = False

      
      