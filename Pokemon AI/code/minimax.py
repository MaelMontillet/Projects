from choix import choix

# esperance #
def esperance(liste_etats, fonction) -> int:
  """ Calcule l'esperence des valeur de fonction(etat)
    param:
        liste_etats : liste de couple d'entier et Etat. L'entier
        représente la probabilité d'un etat.
        fonction : callable qui prend en parametre un etat en renvoie
        un entier."""
  return sum([proba * fonction(etat) for proba, etat in liste_etats])
# end #

# alea #
def choix_aleatoire(liste_etats, fonction):
  """ Renvoie la valeur d'un des etats prit au hazard."""
  return fonction(choix(liste_etats))
# end #

# interface #
def minimax_joueur1(jeu, etat, profondeur, fonction_valeur, traitement_alea, \
                    condition_tri, alpha = -10**5, beta = 10**5):
  """Fonction qui effectue l'interface entre le fonction minvaleur et
    maxvaleur afin d'effectuer l'algorithme du minimax pour le joueur 1
    (le joueur max).
    param :
        jeu : instance de Jeu.
        etat : instance d'Etat
        profondeur : nombre de choix sur lequel on fait le minimax
        fonction_valeur : callable qui prend en paramètre un etat et
        renvoie une estimation de son utilité (int)
        traitement_alea : fonction de traitement de l'aléatoire, à un
        ensemble d'état possibles, elle associe une valeur espérée.
        condition_tri : condition pour trier les mouvement via une
        recherche superficielle, c'est un callable qui prend en entrée
        un entier et renvoie un booléen.
        alpha, beta : entier qui stockent respectivement la plus grande
        valeur trouvée par le max et la plus petite trouvée par le min,
        sert à l'élagage.
    Renvoie:
     Si le joueur 1 doit jouer, le mouvement qui maximise la valeur et \
     la valeur associée.
     Si le joueur 1 ne doit pas jouer, le mouvement du joueur 2 qui minimise
     la valeur et la valeur associée.
    """
  if profondeur == 0 or jeu.est_final(etat):
    return None, fonction_valeur(etat)
  profondeur -= 1
  liste_joueur = jeu.doit_jouer(etat)
  if len(liste_joueur) == 2:
    v = -10**5
    mvt = None
    """On choisit l'action qui est la meilleure même si l'adversaire 
    choisissait le meilleur contre"""
    for mvt_j1 in jeu.mouvements_autorises_dresseur(etat, etat['joueur1'], \
                                                    condition_tri(profondeur)):
      """récupération du meilleur contre : c'est l'action qui minimise l'utilité
        sachant que le joueur 1 joue mvt_j1."""
      new_v = minvaleur(jeu, etat, profondeur, minimax_joueur1, fonction_valeur, \
                        traitement_alea, condition_tri, alpha, beta, mvt_j1, True)[1]
      #On garde la valeur maximale de toute les valeurs issue du meilleur contre.
      if new_v > v:
        v = new_v
        mvt = mvt_j1
        if v >= beta:
          return mvt, v
        alpha = max(v, alpha)
    return mvt, v
  #dans le cas ou un seul joueur doit joueur c'est un minimax normal
  elif liste_joueur[0] == 'joueur1':
    return maxvaleur(jeu, etat, profondeur, minimax_joueur1, fonction_valeur, \
                     traitement_alea, condition_tri, alpha, beta)
  else:
    return minvaleur(jeu, etat, profondeur, minimax_joueur1, fonction_valeur, \
                     traitement_alea, condition_tri, alpha, beta)
# end #

def minimax_joueur2(jeu, etat, profondeur, fonction_valeur, traitement_alea, condition_tri, alpha = -10**5, beta = 10**5):
  if profondeur == 0 or jeu.est_final(etat):
    return None, fonction_valeur(etat)
  profondeur -= 1
  liste_joueur = jeu.doit_jouer(etat)
  if len(liste_joueur) == 2:
    v = 10**5
    mvt = None
    for mvt_j2 in jeu.mouvements_autorises_dresseur(etat, etat['joueur2'], condition_tri(profondeur)):
      new_v = maxvaleur(jeu, etat, profondeur, minimax_joueur2, fonction_valeur, traitement_alea, condition_tri, alpha, beta, mvt_j2, True)[1]
      if new_v < v:
        v = new_v
        mvt = mvt_j2
        if v <= alpha:
          return mvt, v
      beta = max(alpha, v)
    return mvt, v
  elif liste_joueur[0] == 'joueur1':
    return maxvaleur(jeu, etat, profondeur, minimax_joueur2, fonction_valeur, traitement_alea, condition_tri, alpha, beta)
  else:
    return minvaleur(jeu, etat, profondeur, minimax_joueur2, fonction_valeur, traitement_alea, condition_tri, alpha, beta)

# max #
def maxvaleur(jeu, etat, profondeur, fonction_interface, fonction_valeur,\
              traitement_alea, condition_tri, alpha, beta, mvt_min = None,\
              doit_jouer_min = False):
  """ Trouve le mouvement qui maximise la valeur et la valeur associée
    sachant quel mouvement à été choisit par le joueur min si celui-ci doit
    aussi jouer.
    Precondition : Le joueur 1 doit joueur dans le tour.
    Si le joueur 2 doit aussi, le mouvement qu'il joue est
    donné par mvt_min.
    param:
        jeu, etat, profondeur, fonction_valeur, tratement_alea,
        condition tri, alpha et beta : voir minimax_joueur1
        fonction_interface : fonction qui fait l'interface entre
        minvaleur et maxvaleur.
        mvt_min : mouvement choisit par le min
        doit_jouer_min : vrai si le min doit aussi jouer dans
        le tour.
  """
  v = -10**5 #quoi qu'il arrive la valeur est au dessus de -1500
  mvt = None
  """jeu.suivant_joueur1 renvoie les triplets représentant dans l'ordre :
    l'ensemble des mouvement suivant du joueur1, du joueur 2 et l'etat associe
    sachant que joueur2 à choisit mvt_min si il doit jouer"""
  for (a, _, s) in jeu.suivants_joueur1(etat, mvt_min, doit_jouer_min, condition_tri(profondeur)):
    """On passe par l'interface et on évalue la valeur de l'etat comme l'ensemble des
    etats possibles traités par traitement_alea"""
    new_v = traitement_alea(s, lambda etat_ : fonction_interface(jeu, etat_,\
    profondeur,fonction_valeur, traitement_alea, condition_tri, alpha, beta)[1])
    if new_v > v:
      v = new_v
      mvt = a
      if v >= beta:
        return mvt, v
    alpha = max(alpha, v)
  return mvt, v
# end #

def minvaleur(jeu, etat, profondeur, fonction_interface, fonction_valeur, traitement_alea, condition_tri, alpha, beta, mvt_max = None, doit_jouer_max = False):
  v = 10**5
  mvt = None
  for (_, a, s) in jeu.suivants_joueur2(etat, mvt_max, doit_jouer_max, condition_tri(profondeur)):
    new_v = traitement_alea(s, lambda etat_ : fonction_interface(jeu, etat_, profondeur, fonction_valeur, traitement_alea, condition_tri, alpha, beta)[1])
    if new_v < v:
      v = new_v
      mvt = a
      if v <= alpha:
        return mvt, v
      beta = min(v, beta)
  return mvt, v