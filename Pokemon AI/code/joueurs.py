import abc
from pokemon import *
from random import choice
from time import time
from minimax import *
import matplotlib.pyplot as plt

# Joueur #
class Joueur(metaclass = abc.ABCMeta):
  """Définit un joueur"""
  def __init__(self, joueur, nom):
    self.id = joueur #identifient
    self.historique_temps = []#historique des temps de réponse 
    self.nom = nom

  def __call__(self, jeu, etat):
    t = time()
    mvt = self.strategie(jeu, etat)#stratégie  spécifique à un joueur.
    self.historique_temps.append(time() - t)#mesure du temps de réponse
    return mvt
    
  @abc.abstractclassmethod
  def strategie(self, jeu, etat):
    pass

  def afficher_historique(self):
    x = range(len(self.historique_temps))
    y = self.historique_temps
    plt.plot(x, y, 'r')
    plt.axline((0,0), (10**-7,0), color="black", linewidth=1)
    plt.axline((0,0), (0,10**-7), color="black", linewidth=1)
    plt.xlabel('numero du choix')
    plt.ylabel('temps de reflexion (en s)')
    plt.title(f'Temps de réponse de {self.nom}')
    plt.show()

  def __str__(self):
    return self.nom
# end #

# JoueurMiniMax #
class JoueurMiniMax(Joueur):
  """Definit un joueur qui applique une stratégie utilisant le minimax.
  Voir minimax pour plus de précision sur les paramètres."""
  def appliquer_minimax(self, jeu, etat, profondeur, fonction_valeur,\
                        traitement_alea, condition_tri):
    dresseur = etat[self.id]
    etat.interface.animation_reflexion(dresseur)
    if self.id == 'joueur1':
      mouvement = minimax_joueur1(jeu, etat, profondeur, fonction_valeur,\
                                  traitement_alea, condition_tri)[0]
    else:
      mouvement = minimax_joueur2(jeu, etat, profondeur, fonction_valeur,\
                                  traitement_alea, condition_tri)[0]
    etat.interface.fin_animation_reflexion()
    return mouvement

# end #

class Humain(Joueur):

  def __init__(self, joueur):
    super().__init__(joueur, 'Humain')
  
  def strategie(self, jeu, etat):
    """Réalise l'ensemble des requêtes necessaires pour faire choisir son action à 
    l'utilisateur."""
    dresseur = etat[self.id]
    if dresseur.doit_changer:
      poke = etat.interface.demander_pokemon(dresseur)
      if poke == 'menu':
        return self(jeu, etat)
      return ChangerPoke(poke)
    choix = etat.interface.demander_choix(dresseur)
    if choix == 'attaquer':
      attaque = etat.interface.demander_attaque(dresseur)
      if attaque == 'menu':
        return self(jeu, etat)
      return attaque
    elif choix == 'changer':
      if dresseur.pokemons_dispo == []:
        print("Vous ne pouvez pas changer, il ne vous reste qu'un pokemon")
        return self(jeu, etat)
      poke = etat.interface.demander_pokemon(dresseur)
      if poke == 'menu':
        return self(jeu, etat)
      action = ChangerPoke(poke)
      return action
    else :
      raise ValueError

class JoueurAleatoire(Joueur):
  
  def __init__(self, joueur):
    super().__init__(joueur, 'Aléatoire')
  
  def strategie(self, jeu, etat):
    dresseur = etat[self.id]
    #choix aléatoire parmit les action possible du joueur.
    return choice(jeu.mouvements_autorises_dresseur(etat, dresseur))

# avantage_type #
def avantage_type(avantage : Pokemon, desavantage : Pokemon):
    """ Vrai si le pokemon avantage à un avantage de type sur 
    le pokemon desavantage 
    Remarque : deux pokemon peuvent se resister l'un à
    l'autre à l'autre en même temps et il n'y a alors pas
    d'avantage."""
    return (desavantage.type.nom in avantage.type.resistance and not\
        avantage.type.nom in desavantage.type.resistance) or \
       (desavantage.type.nom in avantage.type.imunite) or \
       avantage.type.nom in desavantage.type.faiblesse
# end #

# basique #

class JoueurBasique(Joueur):
  """Joueur qui suit un ensemble de règles prédéfinies."""
  def __init__(self, joueur):
    super().__init__(joueur, 'Basique')

  def changer(self, dresseur, adversaire, attaque_possible = True):
    """ Selection de l'agent si l'agent decide de changer de
    pokemon en priorite
    Precondition : dresseur peut changer de pokemon c'est à dire
    dresseur.pokemons_dispo != []"""
    # choix en priorite d'un pokemon qui a un avantage de type
    liste_changement = [poke for poke in dresseur.pokemons_dispo \
                        if avantage_type(poke, adversaire.courant)]
    if liste_changement != []:
      return ChangerPoke(choice(liste_changement))
    else:
      # Sinon un pokemon qui n'a pas de desavantage de type
      liste_changement = [poke for poke in dresseur.pokemons_dispo \
                          if not avantage_type(adversaire.courant, poke)]
      if liste_changement != []:
        return ChangerPoke(choice(liste_changement))
      else:
        #A default de changement convenable, on attaque.
        if self.attaque_possible:
            return self.attaquer(dresseur, adversaire)
        """si on a plus de PP ou si on doit changer malgrés
        qu'on ne peut faire que des changements desavantageux
        on fait un changement au hazard"""
        return ChangerPoke(choice(dresseur.pokemons_dispo))

  def attaquer(self, dresseur, adversaire):
    """ Selection de l'agent si l'agent decide d'attaquer
    en priorite"""
    attaques = [attaque for attaque in dresseur.courant.tuple_attaque \
                if dresseur.courant.liste_pp[attaque.index] > 0]
    if attaques != []:
      #On effectue en priorite l'attaque qui fait le plus de degat parmit
      #celles qui ont des PP.
      attaques.sort(key = lambda attaque : attaque.degat, reverse = True)
      return attaques[0]
    else:
      #si il n'y a plus de PP dans toutes les attaques, l'ordre importe peu.
      return dresseur.courant.attaque_1

  def strategie(self, jeu, etat):
    #recuperation des rôles des joueurs.
    dresseur = etat[self.id]
    if self.id == 'joueur1':
      adversaire = etat['joueur2']
    else:
      adversaire = etat['joueur1']
    if etat.phase == 'debut partie':
      #choix de pokemon aleatoire en début de partie
      return choice(list(jeu.mouvements_autorises_dresseur(etat, dresseur)))
    #Verification du nombre de PP dans les attaques
    self.attaque_possible = not dresseur.courant.verifier_pp()
    if dresseur.doit_changer:
      self.attaque_possible = False
      return self.changer(dresseur, adversaire)
    if (not self.attaque_possible) and dresseur.pokemons_dispo != []:
      #si il n'y a plus de PP on change de pokemon si possible
      return self.changer(dresseur, adversaire)
    if "emprisonne" not in dresseur.statut and dresseur.pokemons_dispo != [] \
       and avantage_type(adversaire.courant, dresseur.courant):
      #si il y a un desavantage de type, on change de pokemon
      return self.changer(dresseur, adversaire)
    return self.attaquer(dresseur, adversaire)

# end #

# JoueurAlphaBeta1 #

class JoueurAlphaBeta1(JoueurMiniMax):
  """Joueur qui applique l'algorithme du minimax avec elagage alpha beta."""
  def __init__(self, joueur):
    super().__init__(joueur, 'Minimax')
  
  def strategie(self, jeu, etat):
    mvt = super().appliquer_minimax(jeu, etat, 2, jeu.valeur, choix_aleatoire, lambda p : False)
    return mvt

# end #

# JoueurAlphaBeta2 #

class JoueurAlphaBeta2(JoueurMiniMax):
  """Joueur qui applique l'algorithme du minimax avec elagage alpha beta."""
  def __init__(self, joueur):
    super().__init__(joueur, 'Expectiminimax')
  
  def strategie(self, jeu, etat):
    mvt = super().appliquer_minimax(jeu, etat, 2, jeu.valeur, esperance, lambda p : False)
    return mvt

# end #

