from attaque import *


class Pokemon(metaclass = abc.ABCMeta):

  def __init__(self, nom, type, att, defense, PV, vitesse, tuple_attaque, dresseur, liste_pp):
    self.__nom = nom
    self.__type = type
    self.__att = att
    self.__defense = defense
    self.PV = PV
    self.__PV_total = PV
    self.__vitesse = vitesse
    self.statut = {}
    self.bonus = {'att': 1, 'defense' : 1, 'vitesse' : 1}
    self.tuple_attaque = tuple_attaque
    self.dresseur = dresseur
    self.liste_pp = liste_pp 

  def __str__(self):
    return f'{self.nom} de {self.dresseur}'
  
  def est_ko(self):
    return self.PV <= 0
  
  @property
  def attaque_1(self):
    return self.tuple_attaque[0]

  @property
  def attaque_2(self):
    return self.tuple_attaque[1]

  @property
  def attaque_3(self):
    return self.tuple_attaque[2]

  @property
  def attaque_4(self):
    return self.tuple_attaque[3]
  
  @property
  def nom(self):
    return self.__nom

  @property
  def type(self):
    return self.__type

  """Les property nous permettent ici de ne pas changer la valeur des statistiques 
  quand un bonus est appliqué mais de quand même accéder à la statistique modifiée
  par le bonus quand on l'utilise."""
  @property
  def att(self):
    attaque = self.__att * self.bonus['att']
    return attaque

  @property
  def defense(self):
    return self.__defense * self.bonus['defense']

  @property
  def vitesse(self):
    return self.__vitesse * self.bonus['vitesse']
  
  @property
  def PV_total(self):
    return self.__PV_total

  def verifier_statut(self):
    to_del1 = [sta.nom for sta in self.statut.values() if sta.nb_tour == 0]
    for key in to_del1 :
      del(self.statut[key])

  def verifier_pp(self):
    """Vrai si un pokemon n' plus de points de pouvoir sur ses attaques."""
    return self.liste_pp == [0, 0, 0, 0]


class Pikachou(Pokemon):
  def __init__(self, dresseur):
    super().__init__('pikachou', Elec(), 130, 110, 210, 200,(Tonnerre(0), CageEclair(1), Rugissement(2), ChangeEclair(3)), dresseur, [15, 20, 40, 20])



class Boulbizarre(Pokemon):

  def __init__(self, dresseur):
    super().__init__('boulbizarre', Plante(), 120, 120, 230, 110, (FouetLiane(0), Charge(1), Croissance(2), Vampigraine(3)), dresseur, [25, 35, 10, 20])
    

class Osselait(Pokemon):

  def __init__(self, dresseur):
    super().__init__('osselait', Sol(), 120, 200, 240, 95, (MimiQueue(0), Seisme(1), PiegeDeRock(2), CoudBoule(3)), dresseur, [15, 10, 10, 15])


class Carapuce(Pokemon):

  def __init__(self, dresseur):
    super().__init__('carapuce', Eau(), 120, 150, 230, 110, (Exuviation(0), Ebullition(1), CoudBoule(2), Toxic(3)), dresseur, [15, 15, 15, 15])


class Salameche(Pokemon):

  def __init__(self, dresseur):
    super().__init__('salamèche', Feu(), 130, 110, 220, 150, ( CrocsFeu(0), Tranche(1), GrozYeux(2), DanseFlammes(3)), dresseur, [15, 15, 20, 30])


class Etourmi(Pokemon):

  def __init__(self, dresseur):
    super().__init__('étourmi', Vol(), 130, 90, 220, 110, (ViveAttaque(0), Atterrissage(1), Rapace(2), AntiBrume(3)), dresseur, [30, 5, 10, 10])

