from dresseur import *
from abstract_jeu import *

class JeuPokemon(Jeu):
  """Définit un jeu pokemon."""
  def __init__(self):
    super().__init__()
    rep_interface = InterfaceTexte().input_securise('Quelle interface choississez-vous (texte / graphique)?', 'Veuillez \
choisir entre texte et graphique.',  ['texte', 'graphique'])
    if rep_interface == 'texte':
      interface = InterfaceTexte()
    else :
      interface = InterfaceGraphique()
    self.interface = interface
    self.interface_inactive = None
    #
    """deplacement_phase est un dictionnaire qui à chaque phase associe
    sa fonction de déplacement."""
    self.deplacement_phase = {'debut partie' : JeuPokemon.deplacer_debut_partie, 'debut' : self.deplacer_debut, \
                              'action1' : self.deplacer_action1, 'ordre statut' : self.deplacer_ordre_statut, \
                              'action2' : self.deplacer_action2,'statut lent' :  self.deplacer_statut_lent, \
                              'statut rapide' : self.deplacer_statut_rapide, 'fin' : JeuPokemon.deplacer_fin, \
                              'intermediaire' : self.deplacer_intermediaire}
    self.mvts_autorises = {'joueur1' : {}, 'joueur2' : {}}

  @staticmethod
  def objet(reponse, joueur):
    """A partir du nom du type de joueur, renvoie une instance de l'objet correspondant."""
    if reponse == 'humain':
      return Humain(joueur)
    elif reponse == 'ia alea':
      return JoueurAleatoire(joueur)
    elif reponse == 'ia alpha beta 1':
      return JoueurAlphaBeta1(joueur)
    elif reponse == 'ia alpha beta 2':
      return JoueurAlphaBeta2(joueur)
    elif reponse == 'ia basique':
      return JoueurBasique(joueur)
    raise ValueError
  
  @property
  def dico_strategie(self):
    """Créé le dico qui à un identifient de joueur associe l'instance de 
    joueur choissie par l'utilisateur."""
    rep_joueur1 = self.interface.demander_joueur(1)
    rep_joueur2 = self.interface.demander_joueur(2)
    joueur1 = self.objet(rep_joueur1,'joueur1')
    joueur2 = self.objet(rep_joueur2,'joueur2')
    return {'joueur1': joueur1, 'joueur2' : joueur2}
    
  def initial(self, noms):
    self.historique_partie.append([])
    nom1, nom2 = noms
    dresseur1 = Dresseur(nom1, 'joueur1')
    dresseur2 = Dresseur(nom2, 'joueur2')
    #phase -> 'debut partie' action1', 'action2' 'statut lent', 'statut rapide', 'fin'
    return Etat(dresseur1, dresseur2, self.interface)

  # tri_mvt #
  def mouvements_autorises_dresseur(self, etat, dresseur, trier = False):
    """Permet de connaitre les mouvement possibles d'un joueur."""
    try:
      """On stocke les résulatats dans un dictionnaire pour ne pas avoir
        à recalculer si on recroise le même etat"""
      return self.mvts_autorises[dresseur.id][etat]
    except KeyError:
      mvts = []
      #récupération des mouvement possibles
      if dresseur.doit_changer:
        mvts = dresseur.liste_changements
      elif etat.phase == 'debut':
        liste_changements = dresseur.liste_changements
        liste_attaques = [attaque for attaque in dresseur.courant.tuple_attaque]
        mvts = liste_attaques + liste_changements
      if trier:
        #tri superficiel ou swallow search
        if dresseur.id == 'joueur1':
          mvts.sort(key = lambda mvt :  minimax_joueur1(self, etat, 1, \
            self.valeur, choix_aleatoire, lambda p : False)[1])
        else:
          mvts.sort(key = lambda mvt :  minimax_joueur2(self, etat, 1, \
            self.valeur, choix_aleatoire, lambda p : False)[1], reverse = True)
        self.mvts_autorises[dresseur.id][etat] = mvts
      return mvts
    # end #

  def mouvements_autorises (self, etat):
    """Comme le jeu est simultané, les mouvements autorisée sont 
    l'ensemble des couples des mouvements du joueur 1 et des mouvement du joueur 2."""
    return self.mouvements_autorises_dresseur(etat, etat['joueur1']), self.mouvements_autorises_dresseur(etat, etat['joueur2'])

  def est_final(self,etat):
    """Les deux joueurs ne peuvent pas """
    if etat['joueur1'].est_game_over():
      return True
    if etat['joueur2'].est_game_over():
      return True

  @staticmethod
  def test_vitesse(etat):
    """Renvoie l'ordre de rapidité des joueurs ou "alea" quand les 2
    joueurs ont la même vitesse.
    Sert pour définir l'ordre des statut et quand les attaques ont les 
    même priorite pour définir l'ordre des actions."""
    if etat['joueur1'].courant.vitesse > etat['joueur2'].courant.vitesse:
      return 'joueur1', 'joueur2'
    elif etat['joueur1'].courant.vitesse < etat['joueur2'].courant.vitesse:
      return 'joueur2', 'joueur1'
    else :
        return 'alea'

  @staticmethod
  def doit_jouer(etat):
    """Renvoie la liste des joueurs qui doivent jouer"""
    if etat.phase == 'debut' or etat.phase == 'debut partie'  \
    or (etat['joueur1'].doit_changer and etat['joueur2'].doit_changer):
      return ['joueur1', 'joueur2']
    else:
      """Si la phase n'est pas 'debut' ou 'debut_partie',alors il y a eu une 
      interruption"""
      if etat['joueur1'].doit_changer:
        return ['joueur1']
      elif etat['joueur2'].doit_changer:
        return ['joueur2']
      else:
          raise ValueError
    
  def deplacer_statut(self, etat, dresseur, prochaine_phase):
    """Deplacer la phase des statuts
    Paramètres :
    etat : Etat, dresseur :Dresseur
    prochaine phase : la prochaine phase après l'iterruption en cas de KO
    c'est un str parmit les noms de phase
    """
    for statut in dresseur.courant.statut.values():
      statut(etat.interface)
      if dresseur.courant.est_ko():
        self.procedure_changement(etat, dresseur, prochaine_phase)
        break

  @staticmethod
  def deplacer_intermediaire(etat, deplacement):
    """Permet de deplacer les remplacements des pokemon qui doivent être 
    changés après une interruption."""
    if 'joueur1' in deplacement:
      etat.attaquant_ = 'joueur1'
      deplacement['joueur1'].agir(etat)
    if 'joueur2' in deplacement:
      etat.attaquant_ = 'joueur2'
      deplacement['joueur2'].agir(etat) #changement de poke seulement donc pas de proba
    etat.phase = etat.prochaine_phase
    etat.prochaine_phase = ''
    return [[1, etat]]

  @staticmethod
  def deplacer_debut_partie(etat, deplacement):
    """Permet de déplacer le premier tour."""
    etat.attaquant_, etat.defenseur_ = 'joueur1', 'joueur2'
    deplacement['joueur1'].agir(etat)
    etat.attaquant_, etat.defenseur_ = 'joueur2', 'joueur1'
    deplacement['joueur2'].agir(etat)
    etat.fin_tour = True
    etat.phase = 'debut'
    return [[1, etat]]

  def deplacer_debut(self, etat, deplacement):
    """Permet de définir l'ordre des actions (c'est à dire si joueur1 joue en premier
    ou joueur 2) Elle a été séparée de la suite elle peut créer deux etats possibles (qui ne
    différent que d'un facteur chance qui ont un ordre différent."""
    etat.phase = 'action1'
    #système de priorite :
    #priorite des attaques:
    if (deplacement['joueur1'].priorite == deplacement['joueur1'].priorite and deplacement['joueur1'].priorite == 3) \
       or deplacement['joueur1'].priorite > deplacement['joueur2'].priorite: 
      etat.attaquant_, etat.defenseur_ = 'joueur1', 'joueur2'
      return [[1, etat]]
    elif deplacement['joueur1'].priorite < deplacement['joueur2'].priorite:
      etat.attaquant_, etat.defenseur_ = 'joueur2', 'joueur1'
    else:
      #priorite des pokemon les plus rapide
      ordre = self.test_vitesse(etat)
      if ordre == 'alea':
        # si il on la même vitesse on fait intervenir la chance ce qui créé
        #deux nouvelles branches.
        etat2 = copy.deepcopy(etat)
        etat.attaquant_, etat.defenseur_ = 'joueur1', 'joueur2'
        etat2.attaquant_, etat2.defenseur_ = 'joueur2', 'joueur1'
        return [[1/2, etat], [1/2, etat2]]
      else:
          etat.attaquant_, etat.defenseur_ = ordre
    return [[1, etat]]

  @staticmethod
  def procedure_changement(etat, dresseur, prochaine_phase):
    """Appelée pour interrompre le tour d'un etat quand un des joueurs doit
    changer de pokemon."""
    if dresseur.courant.est_ko():
      etat.interface.animation_ko(dresseur)
    etat.fin_tour = True
    etat.prochaine_phase = prochaine_phase#stocke la phase suivante afin de reprendre
                                          #le tour où il en était.
    etat.phase = 'intermediaire'

  def deplacer_action1(self, etat, deplacement):
    """Deplacement de l'action prioritaire.
    paramètres :
    deplacement : dictionnaire qui aux joueurs qui jouent
    associe leur stratégie.
    """
    etat.phase = 'action2'
    liste_etats = deplacement[etat.attaquant_].agir(etat)
    """Le deplacement peut créer plusieurs etats possibles 
    qu'il faut traiter séparement"""
    if etat.attaquant.doit_changer:
      for proba, new_etat in liste_etats:
        self.procedure_changement(etat, etat.attaquant, 'action2')     
    for proba, new_etat in liste_etats:
      if new_etat.defenseur.courant.est_ko():
        self.procedure_changement(new_etat, new_etat.defenseur, 'ordre statut')
      else:
        new_etat.attaquant_, new_etat.defenseur_ = new_etat.defenseur_, new_etat.attaquant_
        new_etat.action_manquante = deplacement[new_etat.attaquant_]
    return liste_etats

  def deplacer_action2(self, etat, deplacement):
    """Deplacement de l'action non prioritaire."""
    etat.phase = 'ordre statut'
    liste_etats = etat.action_manquante.agir(etat)
    if etat.attaquant.doit_changer:#piège de rock
      for proba, new_etat in liste_etats:
        self.procedure_changement(etat, etat.attaquant, 'ordre statut')
    for proba, new_etat in liste_etats:
      if new_etat.defenseur.courant.est_ko():
        self.procedure_changement(new_etat, new_etat.defenseur, 'ordre statut')
    return liste_etats
        
  def deplacer_ordre_statut(self, etat, deplacement):
    """Permet de définir l'ordre des statuts (c'est à dire quel joueur subit les
    statuts en premier. Elle a été séparée de la suite elle peut créer deux etats 
    possibles différent que d'un facteur chance qui ont un ordre différent.
    On ne definit l'ordre que si les deux joueurs ont des statuts, sinon on 
    effetue les statuts des joueurs qui en ont."""
    statut_j1, statut_j2 = etat['joueur1'].courant.statut == {}, etat['joueur2'].courant.statut == {}
    if statut_j1 and statut_j2:#aucun statut
      etat.fin_tour = True
      etat.phase = 'debut'
    elif not statut_j1 and not statut_j2:#statut sur les 2 joueurs
      etat.phase = 'statut lent'
      ordre = self.test_vitesse(etat)
      if ordre == 'alea':#cas où les deux joueur ont la même vitesse.
        etat2 = copy.deepcopy(etat)
        etat.rapide_, etat.lent_ = 'joueur1', 'joueur2'
        etat2.rapide_, etat2.lent_ = 'joueur2', 'joueur1'
        return [[1/2, etat], [1/2, etat2]]#creation de deux branches.
      etat.rapide_, etat.lent_ = ordre
    else:#Statut sur un seul joueur.
      etat.phase = 'fin'
      if statut_j2:
        self.deplacer_statut(etat, etat['joueur1'], 'fin')
      elif statut_j1:
        self.deplacer_statut(etat, etat['joueur2'], 'fin')
    return [[1, etat]]
  
  def deplacer_statut_lent(self, etat, deplacement):
    """deplacer les statut du joueur le plus lent"""
    etat.phase = 'statut rapide'
    self.deplacer_statut(etat, etat.lent, 'statut rapide')
    return [[1, etat]]

  def deplacer_statut_rapide(self, etat, deplacement):
    """deplacer les statut du joueur le plus rapide"""
    etat.phase = 'fin'
    self.deplacer_statut(etat, etat.rapide, 'fin')
    return [[1, etat]]

  @staticmethod
  def deplacer_fin(etat, deplacement):
    """deplacer la fin de la partie
    Permet d'enlever des statuts aux joueurs si necessaire."""
    etat['joueur1'].courant.verifier_statut()
    etat['joueur2'].courant.verifier_statut()
    etat.phase = 'debut'
    etat.fin_tour = True
    return [[1, etat]]

  def deplacer(self, etat, deplacement):
    """Permet de deplacer tout l'etat.
    Renvoie tout les etats possibles avec leur probabilité."""
    new_etat = copy.deepcopy(etat)
    #liste des etats résultant
    liste_etats = []
    #etats a deplacer
    etats_en_cours = [[1, new_etat]]
    while etats_en_cours:#tant qu'il y a des etats a deplacer
      new_list = []
      for old_proba, old_etat in etats_en_cours:
        for new_proba, new_etat in self.deplacement_phase[old_etat.phase](old_etat, deplacement):#récupération de tout les etats liés à un déplacement.
          new_couple = [old_proba * new_proba, new_etat]
          if new_etat.fin_tour:#Si un etat est finit, on le stocke dans la liste finale
            new_etat.fin_tour = False
            liste_etats.append([new_proba * old_proba, new_etat])#modifiction des probabilités
          else:
            new_list.append([new_proba * old_proba, new_etat])
        etats_en_cours = new_list #récupération des etats non finits.
    return liste_etats
    

  @staticmethod
  # valeur #
  def valeur(etat : Etat) -> int:
    PV_total_j1 = sum([poke.PV for poke in etat['joueur1'].liste_non_ko])
    PV_total_j2 = sum([poke.PV for poke in etat['joueur2'].liste_non_ko])
    return PV_total_j1 - PV_total_j2
  # end #
    
  @staticmethod
  def valeur2(etat):
    """essai de fonction de valeur qui demande trop de temps de calcul
    et trop de connaissances dans le jeu pour ajuster les coefficients."""
    poid_type = 0
    poid_statut = 20
    poid_bonus = 50
    non_ko_j1 = etat['joueur1'].liste_non_ko
    non_ko_j2 = etat['joueur2'].liste_non_ko
    PV_total_j1 = sum([poke.PV for poke in non_ko_j1])
    PV_total_j2 = sum([poke.PV for poke in non_ko_j2])
    nb_statut_j1 = sum([len(poke.statut) for poke in non_ko_j1]) + len(etat['joueur1'].statut)
    nb_statut_j2 = sum([len(poke.statut) for poke in non_ko_j2]) + len(etat['joueur2'].statut)
    bonus_j1 = sum([poke.bonus['att'] + poke.bonus['defense'] for poke in non_ko_j1])
    bonus_j2 = sum([poke.bonus['att'] + poke.bonus['defense'] for poke in non_ko_j2])
    
    if etat['joueur2'].courant.type.nom in etat['joueur1'].courant.type.imunite:
        poid_type += 120
    elif etat['joueur1'].courant.type.nom in etat['joueur2'].courant.type.imunite:
        poid_type -= 120
    else:
        if etat['joueur1'].courant.type.nom in etat['joueur2'].courant.type.resistance:
            poid_type -= 50
        if etat['joueur2'].courant.type.nom in etat['joueur1'].courant.type.resistance:
            poid_type += 50
        if etat['joueur2'].courant.type.nom in etat['joueur1'].courant.type.faiblesse:
            poid_type -= 50
        if etat['joueur1'].courant.type.nom in etat['joueur2'].courant.type.faiblesse:
            poid_type += 50
    return PV_total_j1 + nb_statut_j1 * poid_statut + bonus_j1 \
               * poid_bonus + poid_type - (PV_total_j2 + nb_statut_j2 * poid_statut+ bonus_j2 * poid_bonus)
# suivant #  
  def suivants_joueur1(self, etat, mvt_j2 = None, doit_jouer_j2 = False, trier = False):
    """Renvoie la les etats suivants les actions disponibles du joueur1 sachant si le 
    joueur2 joue et quel action il fait dans ce cas."""
    liste_suivant = []
    deplacement={}
    for mvt_j in self.mouvements_autorises_dresseur(etat, etat['joueur1'], trier):
      deplacement['joueur1'] = mvt_j
      if doit_jouer_j2:
        deplacement['joueur2'] = mvt_j2
      liste_suivant.append((mvt_j, mvt_j2, self.deplacer(etat, deplacement)))
    return liste_suivant
# end #

  def suivants_joueur2(self, etat, mvt_j1 = None, doit_jouer_j1 = False, trier = False):
    liste_suivant = []
    deplacement={}
    for mvt_j in self.mouvements_autorises_dresseur(etat, etat['joueur2'], trier):
      deplacement['joueur2'] = mvt_j
      if doit_jouer_j1:
        deplacement['joueur1'] = mvt_j1
      liste_suivant.append((mvt_j1, mvt_j, self.deplacer(etat, deplacement)))
    return liste_suivant

  def suivants_deux_joueurs(self, etat, trier = False):
    """Renvoie les etats issus du deplacement de tout les couple possibles d'action 
    des deux joueurs."""
    liste_suivant = []
    for mvt_j1 in self.mouvements_autorises_dresseur(etat, etat['joueur1'], trier):
      deplacement = {}
      for mvt_j2 in self.mouvements_autorises_dresseur(etat, etat['joueur2'], trier):
        deplacement['joueur1'] = mvt_j1
        deplacement['joueur2'] = mvt_j2
        liste_suivant.append((mvt_j1, mvt_j2, self.deplacer(etat, deplacement)))
    return liste_suivant

  def suivants(self, etat):
    liste_joueur = self.doit_jouer(etat)
    if len(liste_joueur) == 2:
      return self.suivants_deux_joueurs(etat)
    elif liste_joueur[0] == 'joueur1':
      return self.suivants_joueur1(etat)
    elif liste_joueur[0] == 'joueur2':
      return self.suivants_joueur2(etat)
  
    
def lancer(nb_partie = 1):
  """Lance une partie de Pokemon"""
  jeu = JeuPokemon()
  strategies = jeu.dico_strategie
  nom1 = jeu.interface.demander_nom(1)
  nom2 = jeu.interface.demander_nom(2)
  jouer_jeu(jeu, strategies, nb_partie, [nom1, nom2])
