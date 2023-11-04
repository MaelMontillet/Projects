import abc
from random import randint
from type import *

       
class StatutPokemon(metaclass = abc.ABCMeta):
  """Définit un statut qui s'applique à un pokemon."""
  nom = "à définir"
  def __init__(self, pokemon, nb_tour):

    self.__pokemon = pokemon
    self.nb_tour = nb_tour
 
  @property
  def pokemon(self):
    return self.__pokemon

  @abc.abstractmethod
  def __call__(self, interface):
    """Applique le statut au pokemon"""
    pass

  def __str__(self):
    return self.nom



class SBrulure(StatutPokemon):
  nom = 'brulure'
  def __init__(self, pokemon, interface):
    interface.afficher(f"{pokemon} est brulé")
    super().__init__(pokemon, 6)
    self.bonus = False
    if self.pokemon.bonus['att'] > 1/3 and 'brulure' not in self.pokemon.statut:
      self.bonus = True
      self.pokemon.bonus['att'] -= 1/3

  def __call__(self, interface):
    cout_pv = int((1/8)*self.pokemon.PV_total)
    self.pokemon.PV -= cout_pv
    self.nb_tour -= 1
    interface.afficher(f'{self.pokemon} perd {cout_pv} PV à cause de sa brulure')
    if self.pokemon.PV<=0:
      self.pokemon.PV = 0
      self.nb_tour = 0
      
    def __del__(self):
      """Quand les tours de brulures sont finits, il faut enlever le malus d'attaque qui
      avait été appliqué"""
      if self.bonus:
        self.pokemon.bonus['att'] += 1/3

class SPoison(StatutPokemon):
  nom ='poison'
  def __init__(self, pokemon, interface):
    interface.afficher(f"{pokemon} est empoisonné")
    super().__init__( pokemon, 4)
    

  def __call__(self, interface):
    cout_pv = int(((5-self.nb_tour)/16)*self.pokemon.PV_total)
    self.pokemon.PV -= cout_pv
    self.nb_tour -= 1
    interface.afficher(f'{self.pokemon} est empoisonné, il perd {cout_pv} PV')
      
    if self.pokemon.PV<=0:
      self.pokemon.PV = 0
      self.nb_tour = 0
    

class SParalysie(StatutPokemon):
  nom = 'paralysé'
  def __init__(self, pokemon, interface):
    interface.afficher(f"{pokemon} est paralysé")
    super().__init__(pokemon, 10)
    self.pokemon.bonus['vitesse'] -= 1/2
    self.att = self.pokemon.bonus['att']
    
  def __call__(self, interface):
    self.nb_tour -= 1
    if self.pokemon.PV<=0:
      self.pokemon.PV = 0
      self.nb_tour = 0

class SVampigraine(StatutPokemon):
  nom = 'vampigraine'
  def __init__(self, pokemon, adversaire):
    super().__init__(pokemon, 5)
    self.pokemon.bonus['vitesse'] -= 1/2
    self.att = self.pokemon.bonus['att']
    self.adversaire = adversaire
    
  def __call__(self, interface):
    if not isinstance(self.pokemon.type, Plante):
      cout_pv = int((1/8)*self.pokemon.PV_total)
      self.pokemon.PV -= cout_pv
      if not self.adversaire.est_ko():
        self.adversaire.PV += cout_pv
        interface.afficher(f'{self.adversaire} récupère {cout_pv} PV à {self.pokemon} grâce à Vampigraine')

    self.nb_tour -= 1
      
    if self.pokemon.PV<=0:
      self.pokemon.PV = 0
      self.nb_tour = 0
      


class Statutdresseur(metaclass = abc.ABCMeta):
  """Statut qui s'applique à un dresseur donc à tout ses pokemons."""

  def __init__(self, dresseur, nb_tour):

    self.__dresseur = dresseur
    self.nb_tour = nb_tour

  @property
  def dresseur(self):
    return self.__dresseur

  @abc.abstractmethod
  def __call__(self, interface):
    pass

class ChangementImpossibleError(Exception):
  pass

class SEmprisonne(Statutdresseur):
  nom ='emprisonne'
  def __init__(self, dresseur, interface):
    super().__init__(dresseur, 6)
    interface.afficher(f"{dresseur.courant} est emprisonné")

    

  def __call__(self, interface):
    if self.nb_tour <= 0 or self.dresseur.courant.est_ko():
      self.dresseur.statut.pop(self.nom)
      interface.afficher(f"{self.dresseur.courant} n'est plus emprisonné")
    else:
      self.nb_tour -= 1
      interface.afficher(f'{self.dresseur} veut changer de pokemon mais il ne peut pas car son pokemon est emprisonne pour {self.nb_tour} tours.')
      raise ChangementImpossibleError


class SPdg(Statutdresseur):
  nom ='piège de rock'
  def __init__(self, dresseur, interface):
    super().__init__( dresseur, 30)
    interface.afficher(f"{dresseur.courant} se retrouve coincé sous les pierres")


  def __call__(self, interface):
    if self.nb_tour > 0:
      #les degâts des piège de rock dépendent du type.
      if 'sol' in self.dresseur.courant.type.faiblesse:
        cout_pv = int(0.18*self.dresseur.courant.PV_total)
      elif 'sol'in self.dresseur.courant.type.resistance:
        cout_pv = int(0.06*self.dresseur.courant.PV_total)
      elif 'sol'in self.dresseur.courant.type.imunite:
        interface.afficher(f'{self.dresseur.courant} est imunise aux pièges de rock')
        return 
      else:
        cout_pv = int(0.12*self.dresseur.courant.PV_total)
      self.dresseur.courant.PV -= cout_pv
      self.nb_tour -= 1
      interface.afficher(f'{self.dresseur.courant} subit les degats des pièges de rocks, il perd {cout_pv} PV')
    else: 
      self.dresseur.statut.pop(self.nom)
      interface.afficher(f"{self.dresseur.courant} a pu se sortir des pierres, il n'est plus coincé")
