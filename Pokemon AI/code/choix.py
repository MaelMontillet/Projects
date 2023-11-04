from random import random

# choix #

def choix(liste_etats):
  """Permet de choisir un etat parmit les etats possibles en respectant 
  leur probabilité."""
  proba_totale = 0
  liste_proba = []
  dico_etat = {}
  for proba, etat in liste_etats:
    proba_totale += proba
    liste_proba.append(proba_totale)
    dico_etat[proba_totale] = etat
  choix = random()
  i = 0
  """on decoupe [0,1] en segment de taille correspondant à la probabilité
  de chaque etat. Un etat et choisit si random() tombe deans son segment."""
  while i < len(liste_proba) - 1 and liste_proba[i] <= choix:
    i += 1
  return dico_etat[liste_proba[i]]

# end #