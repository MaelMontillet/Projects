En français :

Mini logiciel de retouche d'images :

Contient des exemples d'images modifiées dans images_modifiees.

Prérequis : Python 3 avec les modules Pillow, tkinter et numpy.

Comment l'utiliser :

Lancez retouche_image.py
Une fenêtre s'ouvre avec en haut 16 icônes, chacune représentant un type de filtre. Il y a, dans l'ordre :

- redimensionner l'image
- filtre de couleur (17 filtres disponibles)
- changer la luminosité
- recadrer l'image
- appliquer un filtre vieillissant couleur sépia ou argentique
- augmenter le contraste de l'image en égalisant son histogramme
- tourner l'image
- appliquer du flou
- appliquer un flou de vitesse à partir d'un point de fuite
- appliquer une fonction définie par l'utilisateur grâce aux courbes de Bézier à chaque intensité de l'image
- spécialiser l'histogramme de l'image : on demande une autre image à l'utilisateur et on modifie l'histogramme de l'image originale pour qu'il ressemble à celui de la seconde image.
- effet miroir
- récupérer les contours de l'image
- appliquer un flou autour d'un cercle donné par l'utilisateur

En bas à droite, il y a les boutons choisir un fichier et choisir un dossier qui permettent respectivement de choisir le fichier à éditer et le dossier où l'enregistrer. Par défaut, les fichiers sont enregistrés dans images_modifiees. On peut aussi choisir sous quel nom enregistrer les images dans le champ de texte.

Une fois l'image chosie, cliquer sur un filtre permet de l'appliquer.
La case addition des filtre permet de savoir si on veux cumuler l'effet des filtres succéssifs.

Ensuite, quand un filtre est sélectionné, une boîte de dialogue peut s'afficher sur la droite pour modifier des options.

Pour utiliser les courbes de Bézier, cliquez sur l'icône correspondante, une fenêtre s'affiche avec courbes modifiables et le rendu de cette courbe. La courbe que vous voyez associe à chaque intensité une nouvelle valeur. Elle est initialisée à l'identité. Vous pouvez la modifier en plaçant des points (clic gauche) ou en bougeant des points existants (clic droit pour prendre un point et à nouveau clic droit pour le relâcher). Les points agissent comme des aimants qui modifient la courbe. À gauche, vous pouvez visualiser le rendu.

Ce que ce projet m'a apporté :

Ce projet m'a permis de m'initier au traitement d'images en créant des filtres. J'ai pu m'essayer aux modifications de l'image via la modification des pixels et de leurs voisins (par exemple l'effet contour n'est qu'une soustraction avec les pixels voisins) comme via la modification de l'histogramme. Les deux modifications de l'histogramme de l'image que j'ai utilisées sont l'égalisation et la spécialisation. L'égalisation permet d'obtenir un histogramme plat où toutes les couleurs sont représentées de manière égale (je l'ai utilisé pour le contraste). La spécialisation permet de modifier l'histogramme d'une image afin qu'il ressemble à celui d'une autre image. L'exemple de filtre le plus réussi qui utilise cela dans mon logiciel est le filtre vieillissant qui (outre les taches de couleur et le bruit ajouté) est l'application de l'histogramme de plusieurs photos anciennes (stockées dans les ressources) à l'image qu'on modifie. (Pour plus d'informations, voir https://fr.wikipedia.org/wiki/Histogramme_(imagerie_num%C3%A9rique) )


In english :

Image Editing Software:

Contains examples of modified images in the 'images_modifiees' folder.

Prerequisites: Python 3 with the Pillow, tkinter, and numpy modules.

How to Use:

Run 'retouche_image.py.'

A window opens with 16 icons at the top, each representing a type of filter. In order:

- Resize the image
- Color filter (17 filters available)
- Adjust brightness
- Crop the image
- Apply a vintage filter (sepia or silver)
- Increase image contrast by equalizing its histogram
- Rotate the image
- Apply blur
- Apply motion blur from a vanishing point
- Apply a user-defined function using Bézier curves at every intensity of the image
- Specialize the image histogram: request another image from the user and modify the original image's histogram to match that of the second image.
- Mirror effect
- Retrieve image contours
- Apply blur around a user-defined circle

In the bottom right, there are buttons for "Choose a File" and "Choose a Folder" to respectively select the file to edit and the folder to save it in. By default, files are saved in the 'images_modifiees' folder. You can also choose the name under which to save the images in the text field.

Once the image is chosen, clicking on a filter applies it. The "Add Filters" checkbox allows you to decide whether to accumulate the effects of successive filters.

When a filter is selected, a dialog box may appear on the right to modify options.

To use Bézier curves, click on the corresponding icon, and a window will display editable curves and the rendering of that curve. The curve associates a new value with each intensity. It is initialized as the identity function. You can modify it by adding points (left-click) or moving existing points (right-click to select a point and right-click again to release it). Points act like magnets that modify the curve. On the left, you can see the visualization.

What This Project Taught Me:

This project introduced me to image processing by creating filters. I had the opportunity to experiment with image modifications, both by adjusting pixel values and their neighbors (for example, the contour effect is simply a subtraction involving neighboring pixels) and by modifying the image's histogram. The two histogram modifications used in this project are equalization and specialization. Equalization results in a flat histogram where all colors are equally represented (I used it in the contrast effect). Specialization allows the modification of an image's histogram to resemble that of another image. The most successful example of a filter in my software that utilizes this technique is the vintage filter, which, in addition to adding color spots and noise, applies the histogram of several old photos (stored in resources) to the image being edited.
(For more information see https://fr.wikipedia.org/wiki/Histogramme_(imagerie_num%C3%A9rique) )

