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
2. **4D** : Ce bouton permet de démarrer le jeu avec une grille 4D (4x2x2).
3. **Charger** : Ce bouton permet de charger une partie en utilisant un fichier JSON. Le bouton charger lancera automatiquement le mode de jeu qu'il faut (4D/Classique). Un anticheat a été intégré. Il vérifie la cohérence des données en s'assurant que les données nécessaires sont présentes et que les valeurs de la matrice correspondent aux règles du jeu 2048, selon le mode de jeu (4D ou Classique). De plus, la valeur "score" sera vérifié, il se doit d'être égal au score calculé par l'anticheat. Enfin, l'intégrité du fichier sera vérifier. Si des problèmes sont détectées, l'utilisateur est informé par un message d'erreur et la partie ne peut pas être chargée.
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
