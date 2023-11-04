from __future__ import annotations
from statut import *
from action import *
import copy


class Attaque(Action, metaclass = abc.ABCMeta):
  """Définit une attaque d'un pokemon."""
  def __init__(self, nom, type, degat, index):
    super().__init__(1)#priorite par default de 1, inférieure à celles
                       #des attaques prioritaires(2) et des changements(3).
    self.__type = type
    self.__nom = nom
    self.degat = degat
    self.index = index #position de l'attaque dans la liste des PP
                       #du pokemon à laquelle elle appartient.
  
  @property
  def type(self):
    return self.__type

  @property
  def nom(self):
    return self.__nom

  @abc.abstractmethod
  def effet(self, etat : Etat):
    """Appelée par la méthode agir, spécidique à l'attaque qui héritera de 
    la classe abstraite."""
    pass
  
  def agir(self, etat : Etat):
    """Méthode appliquée pour effectuer l'attaque. Elle est composé d'un corp
    commun à toute les attaques et d'une partie plus spécifique qui est effet.
    Qui lance l'attaque et qui la reçoit est définit dans l'état."""
    if etat.attaquant.courant.liste_pp[self.index] == 0:
      etat.interface.afficher(f"le {etat.attaquant.courant.nom} de {etat.attaquant.nom} veut faire l'attaque {self.nom} mais cette attaque n'a plus de pp.")
      if etat.attaquant.courant.verifier_pp():
        etat.interface.afficher(f"le {etat.attaquant.courant} n'a plus aucun pp sur toutes ses attaques. Il perd 50 PV.")
        etat.attaquant.courant.PV -= 50
        if etat.attaquant.courant.PV <=0:
          etat.attaquant.courant.PV = 0
      return [[1, etat]]
    etat.attaquant.courant.liste_pp[self.index] -= 1
    if 'paralysé' in etat.attaquant.courant.statut:
      #Si un pokemon est paralysé, il a une chance sur trois de ne pas pouvoir attaquer.
      liste_etats = []
      etat2 = copy.deepcopy(etat)
      etat2.interface.afficher(f'le {etat.attaquant.courant.nom} de {etat.attaquant.nom} attaque {self.nom}')
      for proba, etat_ in self.effet(etat2):
        liste_etats.append([proba * 2/3, etat_])
      etat.interface.afficher(f'{etat.attaquant.courant} ne peut pas attaquer à cause de sa paralysie')
      liste_etats.extend([[1/3, etat]]) #2 branches liées à la paralysie : 
                                        #(attaque et abscence d'attaque)
      return liste_etats
    etat.interface.afficher(f'le {etat.attaquant.courant.nom} de {etat.attaquant.nom} attaque {self.nom} (PP restantes: {etat.attaquant.courant.liste_pp[self.index]})')
    return self.effet(etat)

  def attaque_simple(self, etat : Etat):
    """Méthode qui permet de définir un effet qui est trés récurret dans
    les attaques : faire des dêgats."""
    #formule d'attaque (voir presention du jeu)
    cout_pv = int((etat.attaquant.courant.att/etat.defenseur.courant.defense) * self.degat * etat.defenseur.courant.type.get_coefficient(self.type)) 
    if self.type == etat.attaquant.courant.type:
      cout_pv *= 11/10 #bonus du type
    elif etat.defenseur.courant.PV >= cout_pv :
      etat.defenseur.courant.PV -= cout_pv
    else:
      etat.defenseur.courant.PV = 0
    etat.interface.afficher(str(etat.defenseur.courant) + f" perd {cout_pv} PV.")
    return [[1, etat]]

"""Les classes suivantes sont des classes qui héritent de attaque pour définir 
des attaques spécifiques."""
class Tonnerre(Attaque):

  def __init__(self, index):
    super().__init__("tonnerre", Elec(), 95, index)

  def effet(self, etat : Etat):
    return self.attaque_simple(etat)

class CageEclair(Attaque):

  def __init__(self, index):
    super().__init__('cage éclair', Elec(), 0, index)

  def effet(self, etat : Etat):
    if not isinstance(etat.defenseur.courant.type, Elec):
      etat.defenseur.courant.statut['paralysé'] = SParalysie(etat.defenseur.courant, etat.interface)
    else :
      etat.interface.afficher(f"L'attaque cage éclair n'a pas d'effet sur le type éléctrique")
    return [[1, etat]]

class Rugissement(Attaque):

  def __init__(self, index):
    super().__init__('rugissement', Normal(), 0, index)

  def effet(self, etat : Etat):
    if etat.defenseur.courant.bonus['att'] > 1/4 :
      etat.defenseur.courant.bonus['att'] -= 1/4
      etat.interface.afficher(f"L'attaque du {etat.defenseur.courant} diminue")
    else:
      etat.interface.afficher(f"L'attaque du {etat.defenseur.courant} est déjà baissée au maximum, le rugissement du\
{etat.attaquant.courant} n'a pas d'effet")
    return [[1, etat]]


class ChangeEclair(Attaque):
  def __init__(self, index, changement = None):
      super().__init__('change-éclair', Elec(), 70, index)
      self.changement = changement
    
  def effet(self, etat : Etat):
    self.attaque_simple(etat)
    etat.interface.afficher("Change éclair permet de changer de pokemon")
    if not etat.attaquant.pokemons_dispo == []:
      etat.attaquant.changement = True      
    else:
      etat.interface.afficher('Pas de pokemon disponible pour le changement')
    return [[1, etat]]
  
class FouetLiane(Attaque):
  def __init__(self, index):
      super().__init__('fouetliane', Plante(), 90, index)

  def effet(self, etat : Etat):
    return self.attaque_simple(etat)

class Charge(Attaque):
  def __init__(self, index):
      super().__init__('charge', Normal(), 60, index)

  def effet(self, etat : Etat):
    return self.attaque_simple(etat)

class Vampigraine (Attaque):

  def __init__(self, index):
    super().__init__("vampigraine", Plante(), 0, index)

  def effet(self, etat : Etat):
    etat.defenseur.courant.statut['vampigraine'] = SVampigraine(etat.defenseur.courant, etat.attaquant.courant)
    etat.interface.afficher(f"{etat.defenseur.courant} est atteint par vampigraine")
    return [[1, etat]]
    

class Croissance(Attaque):

  def __init__(self, index):
    super().__init__("croissance", Normal(), 0, index)

  def effet(self, etat : Etat):
    if etat.attaquant.courant.bonus['att'] < 2 :
      etat.attaquant.courant.bonus['att'] += 1/4
      etat.interface.afficher(f"L'attaque du {etat.attaquant.courant} augmente")
    else:
      etat.interface.afficher(f"L'attaque du {etat.attaquant.courant} est déjà au maximum, la croissance du \
{etat.attaquant.courant} n'a pas d'effet")
    return [[1, etat]]


class CoudBoule(Attaque):

  def __init__(self, index):
    super().__init__("coud-boule", Normal(), 75, index)

  def effet(self, etat : Etat):
    return self.attaque_simple(etat)


class Seisme(Attaque):

  def __init__(self, index):
    super().__init__("seisme", Sol(), 100, index)

  def effet(self, etat : Etat):
    return self.attaque_simple(etat)


class PiegeDeRock(Attaque):

  def __init__(self, index):
    super().__init__("piège de rock", Sol(), 0, index)

  def effet(self, etat : Etat):
    self.attaque_simple(etat)
    etat.defenseur.statut['piège de rock'] = SPdg(etat.defenseur, etat.interface)
    return [[1, etat]]


class MimiQueue(Attaque):

  def __init__(self, index):
    super().__init__("mimi queue", Normal(), 0, index)

  def effet(self, etat : Etat):
    if etat.defenseur.courant.bonus['defense'] > 1/4:
      etat.defenseur.courant.bonus['defense'] -= 1/4
      etat.interface.afficher(f"La défense du {etat.defenseur.courant} diminue")
    else:
      etat.interface.afficher(f"La défense du {etat.defenseur.courant} est déjà au minimum, l'attaque mimi queue du \
{etat.attaquant.courant} n'a pas d'effet")
    return [[1, etat]]
      

class Exuviation(Attaque):

  def __init__(self, index):
    super().__init__("exuviation", Eau(), 0, index)

  def effet(self, etat : Etat):
    if etat.attaquant.courant.bonus['att'] < 3 :
      etat.attaquant.courant.bonus['att'] += 3/2
      etat.interface.afficher(f"L'attaque du {etat.attaquant.courant} augmente beaucoup")
      if etat.attaquant.courant.bonus['defense'] > 1/4:
        etat.attaquant.courant.bonus['defense'] -= 1/4
        etat.interface.afficher(f"La défense du {etat.attaquant.courant} diminue")
      else:
        etat.interface.afficher(f"La defense du {etat.attaquant.courant} est déjà au minimum, la defense \
du {etat.attaquant.courant} ne dimiue pas")
    else:
      etat.interface.afficher(f"L'attaque du {etat.attaquant.courant} est déjà au maximum, l'attaque \
du {etat.attaquant.courant} n'augmente pas")
    return [[1, etat]]
    

class Ebullition(Attaque):

  def __init__(self, index):
    super().__init__("ebullition", Eau() , 80, index)

  def effet(self, etat : Etat):
    """Definit l'effet de l'attaque ebullion qui faut intervenir le facteur chance."""
    self.attaque_simple(etat) #première branche : pas de brulure.
    etat2 = copy.deepcopy(etat) #seconde branche : brulure.
    etat2.defenseur.courant.statut['brulure'] = SBrulure(etat2.defenseur.courant, etat2.interface)
    return [[1/3, etat2], [2/3, etat]]#etats possibles avec leur probabilité.

class Toxic(Attaque):

  def __init__(self, index):
    super().__init__("toxic", Normal(), 0, index)

  def effet(self, etat : Etat):
    etat.defenseur.courant.statut['poison'] = SPoison(etat.defenseur.courant, etat.interface)
    return [[1, etat]]


class CrocsFeu(Attaque):

  def __init__(self, index):
    super().__init__("crocs feu", Feu(), 65, index)

  def effet(self, etat : Etat):
    self.attaque_simple(etat)
    etat2 = copy.deepcopy(etat)
    etat2.defenseur.courant.statut['brulure'] = SBrulure(etat2.defenseur.courant, etat2.interface)
    return [[1/3, etat2], [2/3, etat]]
        

class DanseFlammes(Attaque):

  def __init__(self, index):
    super().__init__("danse flammes", Feu(), 35, index)

  def effet(self, etat : Etat):
    self.attaque_simple(etat)
    etat.defenseur.statut['emprisonne'] = SEmprisonne(etat.defenseur, etat.interface)
    return [[1, etat]]

class Tranche(Attaque):

  def __init__(self, index):
    super().__init__("tranche", Normal(), 70, index)

  def effet(self, etat : Etat):
    self.attaque_simple(etat)
    return [[1, etat]]


class GrozYeux(Attaque):

  def __init__(self, index):
    super().__init__("groz yeux", Normal(), 0, index)

  def effet(self, etat : Etat):
    if etat.defenseur.courant.bonus['defense'] > 1/4:
      etat.defenseur.courant.bonus['defense'] -= 1/4
      etat.interface.afficher(f"La défense du {etat.defenseur.courant} diminue")
    else:
      etat.interface.afficher(f"La défense du {etat.defenseur.courant} est déjà au minimum")
    if etat.attaquant.courant.bonus['defense'] < 2:
      etat.attaquant.courant.bonus['defense'] += 1/4
      etat.interface.afficher(f"La défense du {etat.attaquant.courant} augmente")
    else:
      etat.interface.afficher(f"La defense du {etat.attaquant.courant} est déjà au maximum")
    return [[1, etat]]

    
class ViveAttaque(Attaque):

  def __init__(self, index):
    super().__init__("vive-attaque", Normal(), 70, index)
    self.priorite = 2

  def effet(self, etat : Etat):
    etat.interface.afficher("Vive-attaque est prioritaire")
    return self.attaque_simple(etat)

class Atterrissage(Attaque):
  
  def __init__(self, index):
    super().__init__("atterrissage", Vol(), 0, index)

  def effet(self, etat : Etat):
    PV = etat.attaquant.courant.PV
    if etat.attaquant.courant.PV < (etat.attaquant.courant.PV_total)/2:
      etat.attaquant.courant.PV += (etat.attaquant.courant.PV_total)/2
    else:
      etat.attaquant.courant.PV = etat.attaquant.courant.PV_total
    etat.interface.afficher(f'{etat.attaquant.courant} atterit et récupère  {etat.attaquant.courant.PV - PV} PV')
    return [[1, etat]]
      

class AntiBrume(Attaque):
  
  def __init__(self, index):
    super().__init__("anti-brume", Vol(), 0, index)
    self.priorite = 0

  def effet(self, etat : Etat):
    if 'piège de rock' in etat.attaquant.statut:
      etat.interface.afficher(f'AntiBrume enlève les pièges de rocks du terrain de {etat.attaquant}')
      etat.attaquant.statut.pop('piège de rock')
    else:
      etat.interface.afficher(f"il n'y a pas de piège de rock sur le terrain de {etat.attaquant}, anti-brume n'a pas d'effet")
    return [[1, etat]]

class Rapace(Attaque):

  def __init__(self, index):
    super().__init__("rapace", Vol(), 100, index)

  def effet(self, etat : Etat):
    return self.attaque_simple(etat)
    