En français :

Jeu avec l'algorithme A* :
Un mini-jeu où un labyrinthe est généré aléatoirement, et l'utilisateur doit battre une voiture utilisant l'algorithme de l'A* pour sortir du labyrinthe.


Prérequis :

Python 3
Importer les modules Pillow, pygame et tkinter.

Utilisation:
Lancez projet projetAetoile.py
Pour jouer au jeu, il faut lancer le programme et double-cliquer pour lancer la partie.
Vous pouvez contrôler le véhicule de gauche avec les touches z, q, s et d.
Une animation de l'algorithme A* se déroule à droite. On y voit le graphe lié au labyrinthe, avec en bleu les nœuds accessibles dans l'état actuel de l'algorithme et en rouge les nœuds qui ont été choisis pour explorer un peu plus le graphe.
Une fois la partie finie, vous pouvez relancer en double cliquant.


Éléments principaux :
Ce projet utilise la boîte à outils pour matrice réalisée dans un autre projet.
Il est l'implémentation à partir de la programmation orientée objet de deux principales fonctionnalités :

- La création aléatoire de labyrinthe ayant toujours une solution unique en utilisant l'algorithme de Kruskal.
Les murs verticaux et horizontaux sont représentés chacun par une matrice binaire (pour chaque case, 1 s'il y a un mur et 0 s'il n'y en a pas). Ensuite, on tire une cellule au hasard et on essaie d'enlever un mur avec la condition qu'on ne crée pas un chemin entre deux cellules qui sont déjà reliées (l'appartenance à un même chemin est gérée par un indice). En procédant ainsi jusqu'à relier toutes les cellules, on obtient un labyrinthe où le nombre de murs retirés est minimal.

- La résolution du labyrinthe avec l'algorithme A*.
On utilise deux distances : g-cost est la distance de Manhattan avec le point de départ et h-cost est la distance de Manhattan avec le point d'arrivée.
On crée avec cela une heuristique : f-cost = g-cost + 4 * h-cost. Le coefficient 4 ayant été trouvé en faisant des essais.
Ainsi, pour tous les points accessibles (points bleus) à partir du point de départ, on calcule le f-cost correspondant. On choisit le point qui minimise cette heuristique (point rouge) comme suivant. On stocke comme parent du suivant le point de départ. On compte comme accessibles les cellules voisines du point suivant et on recommence.
Quand on tombe sur l'arrivée du labyrinthe, on remonte le chemin en récupérant à chaque fois le parent du point courant.


In english :

Game with the A Algorithm:*
A mini-game where a maze is generated randomly, and the user must outsmart a car using the A* algorithm to navigate and escape the maze.


Prerequisites:

Python 3
Import the Pillow, pygame and tkinter modules.

How to Play the Game:
Run projetAetoile.py
To play the game, you need to run the program and double-click to start the game. You can control the left vehicle using the 'z', 'q', 's', and 'd' keys. An A* algorithm animation takes place on the right. It shows the graph related to the maze, with blue nodes representing nodes accessible in the current state of the algorithm and red nodes indicating nodes selected for further exploration of the graph.


Key Features:
This project utilizes the matrix toolbox created in another project. It implements two main functionalities using object-oriented programming:

- Random Maze Generation with a Unique Solution using Kruskal's Algorithm: Vertical and horizontal walls are each represented by a binary matrix (1 for a wall, 0 for no wall). A random cell is chosen, and an attempt is made to remove a wall, with the condition that it does not create a path between cells already connected (membership to the same path is managed by an index). By proceeding in this way until all cells are connected, a maze is obtained with the minimum number of removed walls.

- Solving the Maze with the A* Algorithm: Two distances are used - 'gcost' is the Manhattan distance from the starting point, and 'hcost' is the Manhattan distance from the destination point. This is used to create an heuristic: 'fcost' = 'gcost' + 4 * 'hcost', where the coefficient 4 has been determined through experimentation. For all accessible points (blue points) from the starting point, the corresponding 'fcost' is calculated. The next point is chosen that minimizes this heuristic (red point). The starting point becomes the parent of the next point. The neighboring cells of the next point are considered accessible, and the process continues. When the maze's exit is reached, the path is traced back by retrieving the parent of the current point each time.