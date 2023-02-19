# On importe randint et random du package random, qui vont nous permettre de choisir aléatoirement une tuile vide.
from random import randint, random


# On définit la classe Grid, qui va nous permettre de créer une grille de jeu et de la manipuler.
class SimpleGrid:

    # On définit la méthode __init__, qui va permettre de créer une grille de jeu.
    def __init__(self):
        # On définit la grille de jeu, qui est une liste de 4 listes de 4 éléments.
        self.grid = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

    # On définit la méthode start, qui va permettre de commencer une partie.
    def start(self):

        # On fait 2x la même chose, pour avoir 2 tuiles de départ.
        for i in range(2):
            # Les variables x et y sont les coordonnées de la 1ʳᵉ tuile qui va être remplacée par un 2,
            # qui sont choisies aléatoirement. La variable x est pour les lignes et y pour les colonnes.
            x = randint(0, len(self.grid) - 1)
            y = randint(0, len(self.grid[x]) - 1)

            # On vérifie que la tuile choisie est vide.
            if self.grid[x][y] != 0:
                self.start()

            # On remplace la tuile choisie par un 2 ou un 4, avec une probabilité de 90% pour le 2 et 10% pour le 4.
            if random() < 0.9:
                self.grid[x][y] = 2
            else:
                self.grid[x][y] = 4

    def is_win(self):
        for ligne in self.grid:
            for elem in ligne:
                if elem == 2048:
                    return True
        return False

    def new_game(self):
        self.grid = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.start()

    def generate_new_tuile(self):
        # On choisit une tuile vide aléatoirement.
        x = randint(0, len(self.grid) - 1)
        y = randint(0, len(self.grid[x]) - 1)

        # On vérifie que la tuile choisie est vide.
        while self.grid[x][y] != 0:
            x = randint(0, len(self.grid) - 1)
            y = randint(0, len(self.grid[x]) - 1)

        # On remplace la tuile choisie par un 2 ou un 4, avec une probabilité de 90% pour le 2 et 10% pour le 4.
        if random() < 0.9:
            self.grid[x][y] = 2
        else:
            self.grid[x][y] = 4

    # On définit les méthodes move_up, move_down, move_left et move_right, qui vont permettre de déplacer les tuiles
    def move_up(self):
        # On définit les variables mouvement et fusion, qui vont nous permettre de savoir si une tuile a bougé ou
        # fusionné.
        mouvement, fusion = {}, {}
        # On parcourt la grille de haut en bas, de gauche à droite.
        for x in range(1, 4):
            for y in range(4):
                # On vérifie que la tuile n'est pas vide.
                if self.grid[x][y] != 0:
                    # On définit la variable next_x, qui est la case en haut de la case actuelle.
                    prev_x = x - 1
                    # Tant que la case suivante est vide, on continue de chercher.
                    while prev_x >= 0 and self.grid[prev_x][y] == 0:
                        prev_x -= 1

                    # Si on a trouvé une case non vide avec la même valeur, on la fusionne.
                    if prev_x >= 0 and self.grid[prev_x][y] == self.grid[x][y]:
                        self.grid[prev_x][y] *= 2
                        self.grid[x][y] = 0
                        fusion[(x, y), (prev_x, y)] = (prev_x, y)
                    else:
                        # Sinon, on déplace la case actuelle vers la première case vide en haut.
                        if prev_x != x - 1:
                            self.grid[prev_x + 1][y] = self.grid[x][y]
                            self.grid[x][y] = 0
                            mouvement[(x, y)] = (prev_x + 1, y)

        # On génère une nouvelle tuile si au moins une tuile a bougé ou fusionné.
        if fusion or mouvement != {}:
            self.generate_new_tuile()
        return mouvement, fusion

    def move_down(self):
        mouvement, fusion = {}, {}
        # On parcourt la grille de bas en haut, de gauche à droite (l'inverse de move_up).
        for x in range(2, -1, -1):
            for y in range(4):
                if self.grid[x][y] != 0:
                    # On définit la variable next_x, qui est la case en bas de la case actuelle.
                    prev_x = x + 1
                    while prev_x <= 3 and self.grid[prev_x][y] == 0:
                        prev_x += 1

                    if prev_x <= 3 and self.grid[prev_x][y] == self.grid[x][y]:
                        self.grid[prev_x][y] *= 2
                        self.grid[x][y] = 0
                        fusion[(x, y), (prev_x, y)] = (prev_x, y)
                    else:
                        # Sinon, on déplace la case actuelle vers la première case vide en bas.
                        if prev_x != x + 1:
                            self.grid[prev_x - 1][y] = self.grid[x][y]
                            self.grid[x][y] = 0
                            mouvement[(x, y)] = (prev_x - 1, y)

        if fusion or mouvement != {}:
            self.generate_new_tuile()
        return mouvement, fusion

    def move_left(self):
        mouvement, fusion = {}, {}
        # On parcourt la grille de gauche à droite, de haut en bas.
        for x in range(4):
            for y in range(1, 4):
                if self.grid[x][y] != 0:
                    # On cherche la première case vide à gauche.
                    prev_y = y - 1
                    while prev_y >= 0 and self.grid[x][prev_y] == 0:
                        prev_y -= 1

                    if prev_y >= 0 and self.grid[x][prev_y] == self.grid[x][y]:
                        self.grid[x][prev_y] *= 2
                        self.grid[x][y] = 0
                        fusion[(x, y), (x, prev_y)] = (x, prev_y)
                    # Sinon, on déplace la case actuelle vers la première case vide à gauche.
                    else:
                        if prev_y != y - 1:
                            self.grid[x][prev_y + 1] = self.grid[x][y]
                            self.grid[x][y] = 0
                            mouvement[(x, y)] = (x, prev_y + 1)

        if fusion or mouvement != {}:
            self.generate_new_tuile()
        return mouvement, fusion

    def move_right(self):
        mouvement, fusion = {}, {}
        # On parcourt la grille de droite à gauche, de haut en bas.
        for x in range(4):
            for y in range(2, -1, -1):
                if self.grid[x][y] != 0:
                    # On cherche la première case vide à droite.
                    prev_y = y + 1
                    while prev_y <= 3 and self.grid[x][prev_y] == 0:
                        prev_y += 1

                    if prev_y <= 3 and self.grid[x][prev_y] == self.grid[x][y]:
                        self.grid[x][prev_y] *= 2
                        self.grid[x][y] = 0
                        fusion[(x, y), (x, prev_y)] = (x, prev_y)
                    else:
                        # Sinon, on déplace la case actuelle vers la première case vide à gauche.
                        if prev_y != y + 1:
                            self.grid[x][prev_y - 1] = self.grid[x][y]
                            self.grid[x][y] = 0
                            mouvement[(x, y)] = (x, prev_y - 1)

        if fusion or mouvement != {}:
            self.generate_new_tuile()
        return mouvement, fusion
