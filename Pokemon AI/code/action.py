from __future__ import annotations
from interface import *

class Action(metaclass = abc.ABCMeta):
  """Classe qui definit un mouvement dans un jeu simultané"""
  def __init__(self, priorite):
    """Dans un jeu simultané, les deux joueurs peuvent être amené à faire
    leur choix en même temps. Ensuite un sysème de priorite permet de savoir 
    quelle action est effectuée en premier. La priorite de l'action est utile
    pour cela."""
    self.priorite = priorite
    
  @abc.abstractmethod
  def agir(self, etat):
    """Méthode appelée par un jeu pour effectuer l'action. Elle doit revoyer 
    l'ensemble des etats possibles avec leur probabilité d'advenir"""
    pass


class ChangerPoke(Action):
  """Definit l'action de changer de pokemon."""
  def __init__(self, pokemon : str):
    super().__init__(3)#prioritaire par rapport à toute les attaques
    self.remplacant = pokemon

  def agir(self, etat):
    etat.attaquant.changement = False #le dresseur ne doit plus changer
    etat.attaquant.changer_pokemon(self.remplacant.nom, etat.interface)
    return [[1, etat]]#Un seul etat possible car pas de facteur chance

  def __str__(self):
      return f'changement vers {self.remplacant}' 

  def __repr__(self):
      return f'changement vers {self.remplacant}' 