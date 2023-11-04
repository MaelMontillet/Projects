from __future__ import annotations

class Type:
  def __init__(self, nom, coefficient : dict):
    self.__nom = nom
    self.__coefficient_def = coefficient

  def get_coefficient(self, type_attaquant):
    return self.__coefficient_def[type_attaquant.__nom]
  
  @property
  def nom(self):
      return self.__nom
  
  def __str__(self):    
    return self.__nom

  @property
  def faiblesse(self):
    return [couple[0] for couple in self.__coefficient_def.items() if couple[1]==2]

  @property
  def resistance(self):
    return [couple[0] for couple in self.__coefficient_def.items() if couple[1]==1/2]
  
  @property
  def imunite(self):
    return [couple[0] for couple in self.__coefficient_def.items() if couple[1]==0]

class Eau(Type):

  def __init__(self):
    coefficient_def = {
      'eau' : 1/2,
      'feu' : 1/2,
      'elec' : 2,
      'plante' : 2,
      'sol' : 1,
      'vol' : 1,
      'normal' : 1
    }
    super().__init__("eau", coefficient_def)

class Feu(Type):

  def __init__(self):
    coefficient_def = {
      'eau' : 2,
      'feu' : 1/2,
      'elec' : 1,
      'plante' : 1/2,
      'sol' : 2,
      'vol' : 1,
      'normal' : 1
    }
    super().__init__("feu", coefficient_def)

class Elec(Type):
  
  def __init__(self):
    coefficient_def = {
      'eau' : 1,
      'feu' : 1,
      'elec' : 1/2,
      'plante' : 1,
      'sol' : 2,
      'vol' : 1/2,
      'normal' : 1
    }
    super().__init__("elec", coefficient_def)

class Normal(Type):

  def __init__(self):
    coefficient_def = {
      'eau' : 1,
      'feu' : 1,
      'elec' : 1,
      'plante' : 1,
      'sol' : 1,
      'vol' : 1,
      'normal' : 1
    }
    super().__init__("normal", coefficient_def)

class Plante(Type):

  def __init__(self):
    coefficient_def = {
      'eau' : 1/2,
      'feu' : 2,
      'elec' : 1/2,
      'plante' : 1,
      'sol' : 1/2,
      'vol' : 2,
      'normal' : 1
    }
    super().__init__("plante", coefficient_def)

class Sol(Type):

  def __init__(self):
    coefficient_def = {
      'eau' : 2,
      'feu' : 1,
      'elec' : 0,
      'plante' : 2,
      'sol' : 1,
      'vol' : 1,
      'normal' : 1
    }
    super().__init__("sol", coefficient_def)
    

class Vol(Type):

  def __init__(self):
    coefficient_def = {
      'eau' : 1,
      'feu' : 1,
      'elec' : 2,
      'plante' : 1/2,
      'sol' : 0,
      'vol' : 1,
      'normal' : 1
    }
    super().__init__("vol", coefficient_def)

