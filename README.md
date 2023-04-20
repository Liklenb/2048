# 2048

## Groupe de TD : LDD-BI

### Étudiants :

- [Alexandre François](https://github.com/uvsq22201695)
- [Baptiste Boisserie](https://github.com/Liklenb)
- [Arthur Borges](https://github.com/arthB23)

### Dépôt du projet GitHub :

Lien du dépôt du projet : [https://github.com/Liklenb/2048](https://github.com/Liklenb/2048)

## Utilisation du programme

Dans le menu principal, vous trouverez les éléments suivants :

1. **Classique** : Ce bouton permet de démarrer le jeu avec une grille classique (4x4).

![alt text](https://media.discordapp.net/attachments/1076178403054596166/1098732917322174504/image.png?width=1183&height=637)

2. **4D** : Ce bouton permet de démarrer le jeu avec une grille 4D (4x2x2).

![alt text](https://media.discordapp.net/attachments/1076178403054596166/1098733228661145701/image.png?width=1183&height=636)

3. **Charger** : Ce bouton permet de charger une partie en utilisant un fichier JSON. Le bouton charger lancera automatiquement le mode de jeu qu'il faut (4D/Classique). Un anticheat a été intégré. Il vérifie la cohérence des données en s'assurant que les données nécessaires sont présentes et que les valeurs de la matrice correspondent aux règles du jeu 2048, selon le mode de jeu (4D ou Classique). De plus, la valeur "score" sera vérifié, il se doit d'être égal au score calculé par l'anticheat. Enfin, l'intégrité du fichier sera vérifier. Si des problèmes sont détectées, l'utilisateur est informé par un message d'erreur et la partie ne peut pas être chargée.

![alt text](https://media.discordapp.net/attachments/1076178403054596166/1098720637134061708/image.png?width=1183&height=635)

4. **Quitter** : Ce bouton permet de fermer la fenêtre.

Après avoir cliqué sur l'un des 3 boutons (Classique, 4D ou Charger), l'interface changera. Vous verrez toujours le titre du jeu. Cependant, la grille de jeu apparaîtra maintenant avec deux tuiles de départ de valeur 2 ou 4, ainsi que quatre images de flèches à gauche de l'écran pour pouvoir se déplacer (à noter que les flèches directionnelles du clavier fonctionnent également, de plus survoler une flèche la fera changer de couleur). Le score apparaîtra juste au-dessus de la grille. De plus, à droite, nous aurons de nouveaux boutons :

- **Menu** : Permet de quitter le jeu et revenir au menu principal.
- **Quitter** : Permet de quitter le jeu et fermer la fenêtre.
- **Sauvegarder** : Permet d'enregistrer sa grille de jeu, dans un fichier json, à l'emplacement voulu par l'utilisateur, pour la reprendre plus tard.

À noter que sur la version classique, il y a un autre bouton "AI" signifiant Intelligence Artificielle qui permet de faire jouer une IA à votre place (4% de chance de faire 2048). L'IA du jeu fonctionne en évaluant les quatre directions possibles de déplacement (haut, bas, gauche et droite) en utilisant une fonction d'évaluation. Cette fonction attribue une valeur à chaque direction en tenant compte de plusieurs facteurs, tels que les poids des cases (qui permet d'encourager l'IA à déplacer les grosses tuiles sur des positions qui rapporte beaucoup de points), le nombre de cases vides, les fusions qui ont eu lieu et la valeur des cases adjacentes. Plus la valeur heuristique/découverte est élevée, plus la direction sera favorable.

Lorsque la partie est perdue, on ne peut plus jouer et l'interface de la grille devient sombre. Un message s'affiche : "Vous avez perdu !"

Le score augmentera à chaque coup. Enfin, la fenêtre a un logo.

## Règle du jeu

1. Le jeu se déroule sur une grille de 4x4 cases.
2. Au début, deux tuiles portant le chiffre 2 ou 4 apparaissent aléatoirement sur la grille.
3. Le joueur peut effectuer un mouvement en faisant glisser toutes les tuiles vers le haut, le bas, la gauche ou la droite.
4. Lorsqu'un mouvement est effectué, toutes les tuiles se déplacent dans la direction choisie jusqu'à ce qu'elles atteignent le bord de la grille ou une autre tuile.
5. Si deux tuiles de même valeur se rencontrent lors d'un mouvement, elles fusionnent en une seule tuile dont la valeur est égale à la somme des deux tuiles initiales (par exemple, deux tuiles portant le chiffre 2 fusionneront en une tuile portant le chiffre 4).
6. À chaque mouvement, une nouvelle tuile portant le chiffre 2 ou 4 apparaît aléatoirement sur une case vide de la grille.
7. Le but du jeu est de créer une tuile portant le chiffre 2048. Cependant, le joueur peut continuer à jouer après avoir atteint cet objectif pour obtenir un score encore plus élevé.
8. Le jeu se termine lorsque la grille est complètement remplie et qu'aucun mouvement ne peut être effectué, c'est-à-dire qu'aucune paire de tuiles adjacentes n'a la même valeur.

**Une variante du jeu existe avec une grille 4D (4x2x2). Dans cette variante, le score pour gagner est de 32.**

## Le fichier config

Après avoir lancé le jeu, un fichier config.json sera créé dans le dossier du jeu. Ce fichier contient les paramètres du jeu. Il est possible de modifier les paramètres du jeu en modifiant ce fichier. Les paramètres sont les suivants :
- **"tile_colors"** : Dictionnaire contenant les couleurs des tuiles. Les clés sont les valeurs des tuiles et les valeurs sont les couleurs des tuiles. Les couleurs sont des chaînes de caractères au format hexadécimal.
- **"tile_text_colors"** : Dictionnaire contenant les couleurs des textes des tuiles. Les clés sont les valeurs des tuiles et les valeurs sont les couleurs des textes des tuiles. Les couleurs sont des chaînes de caractères au format hexadécimal.

Il est donc possible de changer les couleurs et de donner ce genre de résultat :

![alt text](https://media.discordapp.net/attachments/1076178403054596166/1098732031631949906/image.png?width=1183&height=637)

ou encore :

![alt text](https://media.discordapp.net/attachments/1076178403054596166/1098734470380654642/image.png?width=1183&height=635)

- **"animation_duration"** : Durée de l'animation de déplacement des tuiles en millisecondes.
- **"animation_fps"** : Nombre d'images par seconde de l'animation de déplacement des tuiles.

Les animations chargent un nombre d'images défini par le paramètre "animation_fps", cependant si le jeu est trop lent, les images n'ayant pas eu le temps de se charger seront ignorées automatiquement. De cette manière, "animation_duration" est toujours respecté et l'animation n'est pas plus lente si le jeu est lent.

Des effets sont applicables sur les animations grâce à l'argument function de la fonction animation. Actuellement l'effet est une fonction easeInOutSine (l'animation est plus lente au début et à la fin, il est conseillé d'augmenter "animation_duration" de manière à pouvoir le voir plus clairement). Il est cependant simple de modifier cet effet en modifiant l'argument function de la fonction animation. Toutes les fonctions définies ici: https://easings.net/fr peuvent être utilisés.

## Les objets

### Le BetterButton

Cette fonction recrée le bouton par défaut de tkinter par un bouton plus esthétique. Plusieurs paramètres sont disponibles :

- **color** : Couleur du bouton.
- **text_color** : Couleur du texte du bouton.
- **hover_color** : Couleur du bouton lorsqu'on le survole avec la souris.
- **hover_text_color** : Couleur du texte du bouton lorsqu'on le survole avec la souris.
- **padding** : Espacement entre le texte et les bords du bouton. (Ce paramètre est ignoré l'argument size est défini)
- **size** : Taille du bouton.
- **font** : Police du texte du bouton.
- **text** : Texte du bouton.
- **command** : Fonction à exécuter lorsqu'on clique sur le bouton.
- **border_radius** : Défini si les coins du bouton sont plus ou moins arrondis.

### Le IconButton

Cette fonction est sensiblement la même que BetterButton, sauf qu'elle permet d'afficher une icône à la place du texte. Plusieurs paramètres sont disponibles :

- **icon** : Chemin de l'icône à afficher.
- **hover_icon** : Chemin de l'icône à afficher lorsqu'on survole le bouton avec la souris.
- **command** : Fonction à exécuter lorsqu'on clique sur le bouton.
- **size** : Taille du bouton. (si l'argument n'est pas défini, la taille de l'icône sera utilisée)

### show_message_box

Utilisé pour afficher une erreur lorsqu'un fichier json est mal formé. Plusieurs paramètres sont disponibles :

- **title** : Titre de la fenêtre.
- **message** : Message à afficher.

Ansi avec la simple ligne de code suivante :
```python
show_message_box(root=root, canvas=canvas, title="Ceci est un titre", message="Je communique une information crucial à l'utilisateur !")
```

On obtient :

![alt text](https://media.discordapp.net/attachments/1076178403054596166/1098736624197701673/image.png?width=1181&height=637)