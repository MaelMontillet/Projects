import abc
import matplotlib.pyplot as plt
from choix import choix
from joueurs import *
import sys

class Etat:
    """ classe qui définit un etat du jeu pokemon """
    def __init__(self, dresseur1, dresseur2, interface):
        """ 
        Tye des parametres : 
        dresseur1, dresseur 2 : Dresseur.
        interface : Interface
        """
        self.joueurs ={'joueur1' : dresseur1, 'joueur2' : dresseur2}
        self.phase = 'debut partie'
        self.action_manquante = None #Permet l'action du joueur qui joue en second
                                    # en cas d'interruption
        self.lent_ = None #ordre des statuts
        self.rapide_ = None #ordre des statuts
        self.attaquant_ = None #ordre des attaques (str parmit 'joueur1' et 'joueur2')
        self.defenseur_ = None #ordre des attaque (str parmit 'joueur1' et 'joueur2')
        self.fin_tour = False
        self.interface = interface
        self.prochaine_phase = ''#stocker la phase avant une interruption.

    """Les information correspondant aux variables :attaquant defenseur, rapide et lent
    sont stockées en interne comme l'identifiant du joueur mais l'utilisateur récupére le 
    dresseur qui y correspond quand il les utilise.
    Cela permet d'être sûr que quand l'etat est deepcopié, attaquant se refere toujours à
    un des deux dresseurs de self.joueurs"""
    @property
    def attaquant(self):  
        return self[self.attaquant_]
    
    @property
    def defenseur(self):
        return self[self.defenseur_]
    
    @property
    def rapide(self):
        return self[self.rapide_]
    
    @property
    def lent(self):
        return self[self.lent_]

    """Etat peut être vu comme un dictionnaire, pour connaitre l'etat d'un joueur il suffit 
    d'indexer l'etat par son information. De plus les deux dresseurs correspondent aux 
    seules information axquelles les agents ont accés."""
    def __getitem__(self, key):
        return self.joueurs[key]
    
    def __setitem__(self, key, value):
        self.joueurs[key] = value
    

class Jeu(metaclass = abc.ABCMeta):
  """Classe abstraite jeu qui a été reprise tel quel du cours."""
  def __init__(self):
    self.historique_partie = []#permet d'afficher les graphiques
  
  @property
  @abc.abstractmethod
  def initial(self):
    pass
  
  @abc.abstractmethod
  def mouvements_autorises (self,etat):
    """retourne un dictionnaire des mouvements autorises dans l'etat"""
    
  @abc.abstractmethod
  def deplacer(self,mouvement,etat):
    """retourne l'etat qui resulte de mouvement dans l'etat"""
    pass

  @abc.abstractmethod
  def valeur(self,etat,joueur):
    """retourne la valeur de l'etat pour joueur"""
    pass

  @abc.abstractmethod
  def est_final(self,etat):
    pass

  @abc.abstractmethod
  def doit_jouer(self,etat):
    """retourne le joueur qui doit jouer dans cet etat"""
    pass

  @abc.abstractmethod
  def suivants(self, etat):
    """retourne la liste des etats suivants suite aux mouvements autorisées"""
    pass

  def afficher(self,etat):
    pass
    
  def __repr__(self):
    pass
    
  def __str__(self):
    pass
    
  def afficher_graphes(self, fonction_valeur, joueur1, joueur2):
    """affiche le graphe de la valeur de la partie en fonction du nombre de tours."""
    for n, partie in enumerate(self.historique_partie):
      x = range(len(partie))
      y = [fonction_valeur(etat) for etat in partie]
      plt.plot(x, y, 'r')
      plt.axline((0,0), (1,0), color="black", linewidth=1)
      plt.axline((0,0), (0,1), color="black", linewidth=1)
      plt.xlabel('numero du choix')
      plt.ylabel('valeur de la partie')
      plt.title(f'partie {n} : joueur 1 :{joueur1}, joueur 2 :{joueur2}')
      plt.show()
    
    

# jouer_jeu #

def jouer_jeu(jeu, strategies, nb_partie, noms, verbose = True):
  """fonction pour jouer au jeu donné en paramètre. 
  Paramètres:
  srategie : dictionnaire qui à chaque joueur associe une instence de Joueur.
  nb_partie : int
  noms : liste de deux str qui stocke les noms des joueurs
  verbose : vrai si on souhaite afficher l'etat des tours à la fin de ceux-ci.
  """
  sys.setrecursionlimit(7000)
  etat = jeu.initial(noms)
  tour(jeu, etat, strategies, nb_partie, noms, verbose)
  """Pas de while mais de la récursivité
  car tkiter est en multithreading et il faut passer par racine.after 
  pour ne pas créer de problèmes."""
    

def tour(jeu, etat, strategies, nb_partie, noms, verbose):
  """Effectue un tour du jeu et appèle le tour suivant pas récursivité."""
  deplacement = {}#dictionnaire qui va stocker les action des joueurs qui jouent.
  #liste des joueurs qui doivent jouer.
  liste_joueur = jeu.doit_jouer(etat)
  #On récupére la strategie de tout les joueurs.
  for joueur in liste_joueur:
    deplacement[joueur] = strategies[joueur](jeu, etat)
  etats = jeu.deplacer(etat, deplacement)
  etat = choix(etats)#On choisit un etat parmit les etats possibles.
  if verbose:
    #mise à jour les infos sur le tour.
    etat.interface.etat_jeu(etat)
    etat.interface.afficher(f'\nvaleur du jeu estimée : {jeu.valeur(etat)}')
    #affichage des infos via l'interface.
    etat.interface.afficher_verbose()
    jeu.historique_partie[-1].append(etat)
  if not jeu.est_final(etat):
    etat.interface.rappel(lambda : tour(jeu, etat, strategies, nb_partie, \
                                        noms, verbose))
  else:
    nb_partie -= 1
    if nb_partie > 0:
      etat = jeu.initial(noms)
      etat.interface.rappel(lambda : tour(jeu, etat, strategies, nb_partie, \
                                        noms, verbose))
    else:
      #affichage des graphes (1 graphe par partie pour la valeur et un pour 
      #toutes les partie pour le temps)
      jeu.afficher_graphes(jeu.valeur, strategies['joueur1'], strategies['joueur2'])
      strategies['joueur1'].afficher_historique()
      strategies['joueur2'].afficher_historique()
    
    
    