# 2048

## Groupe de TD : LDD-BI (Groupe A)

### Étudiants :

- Alexandre François
- Baptiste Boisserie
- Arthur Borges

### Dépôt du projet GitHub :

Lien du dépôt du projet : [https://github.com/Liklenb/2048](https://github.com/Liklenb/2048)

## Utilisation du programme

Dans le menu principal, vous trouverez les éléments suivants :

1. **Classique** : Ce bouton permet de démarrer le jeu avec une grille classique (4x4).
2. **4D** : Ce bouton permet de démarrer le jeu avec une grille 4D (4x2x2).
3. **Charger** : Ce bouton permet de charger une partie en utilisant un fichier JSON. Le programme renverra une erreur si le fichier chargé est invalide (il y a système qui permet de vérifier la cohérence des données). Le bouton charger lancera automatiquement le mode de jeu qu'il faut (4D/Classique).
4. **Quitter** : Ce bouton permet de fermer la fenêtre.

Après avoir cliqué sur l'un des 3 boutons (Classique, 4D ou Charger), l'interface changera. Vous verrez toujours le titre du jeu. Cependant, la grille de jeu apparaîtra maintenant avec deux tuiles de départ de valeur 2 ou 4, ainsi que quatre images de flèches à gauche de l'écran pour pouvoir se déplacer (à noter que les flèches directionnelles du clavier fonctionnent également, de plus survoler une flèche la fera changer de couleur). Le score apparaîtra juste au-dessus de la grille. De plus, à droite, nous aurons de nouveaux boutons :

- **Menu** : Permet de quitter le jeu et revenir au menu principal.
- **Quitter** : Permet de quitter le jeu et fermer la fenêtre.
- **Sauvegarder** : Permet d'enregistrer sa grille de jeu pour la reprendre plus tard.

À noter que sur la version classique, il y a un autre bouton "AI" signifiant Intelligence Artificielle qui permet de faire jouer une IA à votre place

Lorsque la partie est perdue, on ne peut plus jouer et l'interface de la grille devient sombre. Un message s'affiche : "Vous avez perdu !"

Enfin, la fenêtre a un logo.
