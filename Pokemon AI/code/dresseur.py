from pokemon import *

class Dresseur(metaclass = abc.ABCMeta):
  """Définit un dresseur de pokemons"""
  def __init__(self, nom : str, id : str):
    self.id = id #identifient de joueur : "joueur1" ou "joueur2"
    self.__nom = nom
    self.pokemon = {'pikachou' : Pikachou(self), 'boulbizarre' : Boulbizarre(self), 'osselait' : Osselait(self), 'salamèche' : Salameche(self), 'carapuce' : Carapuce(self), 'étourmi' : Etourmi(self)}#liste des pokemons
    self.__courant = None #pokemon du dresseur qui est sur le terrain.
    self.statut = {} #dictionnaire des statuts de joueurs les clefs sont
                     #les noms des statuts et les valeurs l'objet correspondant.
    self.changement = True #vrai quand un changement est imposé par une action 
                           #par exemple.
    
  @property
  def courant(self):
      """En interne, le pokemon courant est stocké sous forme du nom du pokemon
      l'utilisateur lui accède au pokemon correspondant de la liste self.pokemon
      quand il l'utilise. Cela permet de s'assurer que self.courant est bien un 
      des pokemons de self.pokemon.
    
      """
      if self.__courant is None:
          return None
      else:
          return self.pokemon[self.__courant]
    
  @property
  def doit_changer(self):
      """vrai quand le dresseur doit changer"""
      if self.courant is None:
          return True
      if self.courant.est_ko():
          return True
      else:
          return self.changement
    
  def est_game_over(self):
    """Vrai quand self à perdu la partie"""
    if all([poke.est_ko() for poke in self.pokemon.values()]):
      return True
    return False

  def changer_pokemon(self, poke : int, interface):
    """Procèdure appellée à chaque fois qu'un dresseur
    change de pokemon."""
    try : 
      #si le pokemon est emprisonné il ne peut pas changer
      if 'emprisonne' in self.statut:
        self.statut['emprisonne'](interface)
    except(ChangementImpossibleError):
      pass
    else: #Si on peut changer.
      if poke is None:
        poke = interface.demander_pokemon(self)
      self.__courant = poke
      interface.animation_choix_poke(self)
      if 'piège de rock' in self.statut:
        self.statut['piège de rock'](interface)
  
  @property
  def nom(self):
    return self.__nom

  def __str__(self):
    return self.nom

  @property
  def liste_ko(self):
    """Liste des pokemon KO"""
    return [poke for poke in self.pokemon.values() if poke.est_ko()]

  @property
  def liste_non_ko(self):
    """Liste des pokemon non KO"""
    return [poke for poke in self.pokemon.values() if not poke.est_ko()]

  @property
  def liste_changements(self):
    """Liste des action de changement de pokemon possibles."""
    return [ChangerPoke(poke_dispo) for poke_dispo in self.pokemons_dispo]

  @property
  def pokemons_dispo(self):
    """Liste des pokemon disponibles pour le changement c'est à dire
    ceux qui ne sont ni KO ni sur le terrain."""
    return [poke_dispo for poke_dispo in self.liste_non_ko if type(poke_dispo) != type(self.courant)]
