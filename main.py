import os
import time
import tkinter.font

import math
from PIL import Image, ImageTk

from random import randint, random

from tkinter.filedialog import asksaveasfile, askopenfile
from datetime import datetime
import json


def load():
    """
    Charge une partie sauvegardée.
    :return bool: False si la partie sauvegardée n'est pas valide.
    :return dict data: Dictionnaire contenant la grille de jeu et le type de jeu.
    """

    # On ouvre l'explorateur de fichier.
    file = askopenfile(mode="r", defaultextension=".json", filetypes=[("JSON", "*.json")],
                       title="Charger une partie sauvegardée")

    # Si l'utilisateur annule, on arrête la fonction.
    if file is None:
        return False

    # On charge les informations de la partie sauvegardée.
    with open(file.name, "r") as f:
        # Si le fichier n'est pas valide, on arrête la fonction.
        try:
            info = json.load(f)
        except json.decoder.JSONDecodeError:
            return False

    # On vérifie que type et matrix sont présents.
    if "type" not in info and "matrix" not in info:
        return False

    # On vérifie que la partie sauvegardée est valide.
    if len(info["matrix"]) != 4:
        return False

    if info["type"] == "4D":
        score_verify = 0

        for x in range(4):

            if len(info["matrix"] != 2):
                return False

            for y in range(2):

                if len(info["matrix"][x][y]) != 2:
                    return False

                for z in range(2):
                    if info["matrix"][x][y][z] not in [0, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]:
                        return False

                    score_verify += info["matrix"][x][y][z]

        if score_verify != info["score"]:
            return False

        data = {"type": "4D", "matrix": info["matrix"], "score": info["score"]}

        return data

    elif info["type"] == "simple":
        score_verify = 0

        for x in range(4):

            if len(info["matrix"][x]) != 4:
                return False

            for y in range(4):

                if info["matrix"][x][y] not in [0, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]:
                    return False

                score_verify += info["matrix"][x][y]

        if score_verify != info["score"]:
            return False

        data = {"type": "simple", "matrix": info["matrix"], "score": info["score"]}

        return data

    else:
        return False


def save(matrix: list, matrix_type: str, score: int):
    """
    Sauvegarde la partie en cours.
    :param list matrix: Liste contenant la grille de jeu.
    :param str matrix_type: Type de jeu.
    :param int score: Score du jeu.
    :return bool: False si l'utilisateur annule la sauvegarde.
    """

    # On crée un dictionnaire qui va nous permettre de stocker les informations de la partie.
    data = {
        "type": f"{matrix_type}",
        "matrix": matrix,
        "score": score
    }

    # On ouvre l'explorateur de fichier.
    file = asksaveasfile(mode="w", defaultextension=".json", filetypes=[("JSON", "*.json")],
                         initialfile=f"2048_{matrix_type}_grid_{datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}",
                         title="Sauvegarder la partie")

    # Si l'utilisateur annule, on arrête la fonction.
    if file is None:
        return False

    # On sauvegarde les informations de la partie.
    with open(file.name, "w") as f:
        json.dump(data, f)


def SimpleGrid() -> dict:
    """
    Fonction regroupant toutes les fonctions invisibles à la grille de jeu simple.
    :return dict self: Dictionnaire contenant la grille de jeu.
    """

    def start(self: dict):
        """
        Génère deux tuiles de valeur 2 ou 4 aléatoirement sur la grille.
        :param dict self: Dictionnaire contenant la grille de jeu.
        """

        for i in range(2):
            generate_new_tile(self)

    def get_empty_tiles(self: dict) -> list:
        """
        Récupère les positions vides de la grille.
        :param dict self: Dictionnaire contenant la grille de jeu.
        :return list empty_tiles: Liste des positions vides.
        """

        empty_tiles = []
        for x in range(4):
            for y in range(4):
                if self["matrix"][x][y] == 0:
                    empty_tiles.append((x, y))

        return empty_tiles

    def generate_new_tile(self: dict):
        """
        Génère une nouvelle tuile de valeur 2 ou 4 aléatoirement sur la grille.
        :param dict self: Dictionnaire contenant la grille de jeu.
        """

        empty_tiles = get_empty_tiles(self)

        if empty_tiles:
            x, y = empty_tiles[randint(0, len(empty_tiles) - 1)]
            if random() < 0.9:
                self["matrix"][x][y] = 2
            else:
                self["matrix"][x][y] = 4

            self["score"] += self["matrix"][x][y]

    def check_win(self: dict) -> bool:
        """
        Vérifie si la partie est gagnée.
        :param dict self: Dictionnaire contenant la grille de jeu.
        :return bool: True si la partie est gagnée, False sinon.
        """

        for row in self["matrix"]:
            for elem in row:
                if elem == 2048:
                    return True
        return False

    def check_lose(self: dict, empty_tiles: list) -> bool:
        """
        Vérifie si on peut faire un mouvement dans la direction donnée.
        :param dict self: Dictionnaire contenant la grille de jeu.
        :param list empty_tiles: Liste des positions vides.
        :return bool: True si la partie est perdue, False sinon.
        """

        if empty_tiles:
            return False

        for direction in config:

            # On récupère les coordonnées de départ et d'arrivée.
            dx, dy = config[direction]["dx"], config[direction]["dy"]
            x_start, x_end, x_step = config[direction]["x_start"], config[direction]["x_end"], config[direction][
                "x_step"]
            y_start, y_end, y_step = config[direction]["y_start"], config[direction]["y_end"], config[direction][
                "y_step"]

            for x in range(x_start, x_end, x_step):
                for y in range(y_start, y_end, y_step):

                    # On vérifie si la case est vide ou si la valeur de la case est égale à la valeur de la case
                    # adjacente.
                    if self["matrix"][x][y] == self["matrix"][x + dx][y + dy]:
                        return False

        return True

    def move(self: dict, direction: str) -> dict:
        """
        Déplace les tuiles dans la direction donnée.
        :param dict self: Dictionnaire contenant la grille de jeu.
        :param str direction: Direction dans laquelle on veut déplacer les tuiles.
        :return dict data: Dictionnaire contenant les informations sur le mouvement.
        """

        data = {
            "mouvement": [],
            "fusion": [],
        }

        if check_lose(self, get_empty_tiles(self)):
            return data

        pos = []

        # On récupère les informations de la direction donnée.
        info = config[direction]
        # On récupère les coordonnées de départ et d'arrivée.
        dx, dy = info["dx"], info["dy"]
        x_start, x_end, x_step = info["x_start"], info["x_end"], info["x_step"]
        y_start, y_end, y_step = info["y_start"], info["y_end"], info["y_step"]

        # On parcourt la grille.
        for x in range(x_start, x_end, x_step):
            for y in range(y_start, y_end, y_step):

                if self["matrix"][x][y] == 0:
                    continue

                # On définit les variables qui vont nous permettre de parcourir la matrice dans la direction donnée.
                prev_x, prev_y = x + dx, y + dy

                # Tant que la case précédente est vide, on continue de parcourir la matrice dans la direction donnée.
                while (0 <= prev_x < 4 and 0 <= prev_y < 4) and self["matrix"][prev_x][prev_y] == 0:
                    prev_x, prev_y = prev_x + dx, prev_y + dy

                # Si la case précédente est égale à la case actuelle et qu'elle n'a pas déjà fusionné, on fusionne
                # les deux cases.
                if (0 <= prev_x < 4 and 0 <= prev_y < 4) and self["matrix"][prev_x][prev_y] == self["matrix"][x][
                    y] and (
                        prev_x, prev_y) not in pos:
                    self["matrix"][prev_x][prev_y] *= 2
                    self["matrix"][x][y] = 0

                    # On stocke les coordonnées de la case qui a fusionné.
                    data["fusion"].append({"from": (x, y), "to": (prev_x, prev_y)})
                    pos.append((prev_x, prev_y))

                # Sinon, on déplace la case actuelle vers la première case vide au-dessus.
                else:
                    if (prev_x - dx, prev_y - dy) != (x, y):
                        self["matrix"][prev_x - dx][prev_y - dy] = self["matrix"][x][y]
                        self["matrix"][x][y] = 0
                        data["mouvement"].append({"from": (x, y), "to": (prev_x - dx, prev_y - dy)})

        # Génère une nouvelle tuile si une fusion ou un mouvement a eu lieu
        if data["mouvement"] or data["fusion"]:
            generate_new_tile(self)

        return data

    def heuristic(self: dict, data: dict) -> int:
        """
        Calcule la valeur heuristique de la direction donnée. Plus la valeur heuristique est élevée,
        plus la direction est bonne. Le concept du poids des cases est tiré de Google, mais le code est entièrement de
        moi.
        :param dict self: Dictionnaire contenant la grille de jeu.
        :param dict data: Dictionnaire contenant les informations de la direction donnée.
        :return int value: Valeur heuristique de la direction donnée.
        """

        # On définit les poids des cases.
        weight = [[2 ** 15, 2 ** 14, 2 ** 10, 2 ** 6],
                  [2 ** 14, 2 ** 10, 2 ** 6, 2 ** 4],
                  [2 ** 10, 2 ** 6, 2 ** 4, 2 ** 2],
                  [2 ** 6, 2 ** 4, 2 ** 2, 2 ** 0]]

        # On initialise la valeur qui va servir de score.
        value = 0

        # On ajoute la valeur de chaque case à la valeur heuristique.
        for x in range(4):
            for y in range(4):
                value += self["matrix"][x][y] * weight[x][y]

        # On augmente value si la case est vide.
        for x in range(4):
            for y in range(4):
                if self["matrix"][x][y] == 0:
                    value += 2 ** 30

        # On augmente value si une fusion a eu lieu.
        for i in range(len(data["fusion"])):
            value += 2 ** 30

        # On augmente value si deux cases adjacentes ont la même valeur.
        for x in range(4):
            for y in range(4):
                if x > 0 and self["matrix"][x][y] == self["matrix"][x - 1][y]:
                    value += 2 ** 15
                if x < 3 and self["matrix"][x][y] == self["matrix"][x + 1][y]:
                    value += 2 ** 15
                if y > 0 and self["matrix"][x][y] == self["matrix"][x][y - 1]:
                    value += 2 ** 15
                if y < 3 and self["matrix"][x][y] == self["matrix"][x][y + 1]:
                    value += 2 ** 15

        return value

    def ai(self: dict):
        """
        Fonction qui permet à l'IA de jouer.
        :param dict self: Dictionnaire contenant la grille de jeu.
        """

        # On détermine la meilleure direction à prendre.
        best_move = {"up": 0, "down": 0, "left": 0, "right": 0}

        # On sauvegarde la matrice actuelle.
        save_matrix = [row[:] for row in self["matrix"]]

        # On teste toutes les directions.
        for direction in ["up", "down", "left", "right"]:

            # On déplace la tuile dans la direction donnée et on récupère les données.
            data = move(self, direction)

            # Si la matrice a changé, on calcule la valeur heuristique de la direction donnée.
            if self["matrix"] != save_matrix:
                # On stocke la valeur heuristique de la direction donnée.
                best_move[direction] = heuristic(self, data)

                # On remet la matrice à son état initial.
                self["matrix"] = [row[:] for row in save_matrix]

        # On déplace la tuile dans la direction qui a la meilleure valeur heuristique.
        data = move(self, max(best_move, key=best_move.get))

        return data

    config = {

        "up": {
            "dx": -1, "dy": 0,
            "x_start": 1, "x_end": 4, "x_step": 1,
            "y_start": 0, "y_end": 4, "y_step": 1
        },

        "down": {
            "dx": 1, "dy": 0,
            "x_start": 2, "x_end": -1, "x_step": -1,
            "y_start": 0, "y_end": 4, "y_step": 1
        },

        "left": {
            "dx": 0, "dy": -1,
            "x_start": 0, "x_end": 4, "x_step": 1,
            "y_start": 1, "y_end": 4, "y_step": 1
        },

        "right": {
            "dx": 0, "dy": 1,
            "x_start": 0, "x_end": 4, "x_step": 1,
            "y_start": 2, "y_end": -1, "y_step": -1
        },
    }

    self = {
        "matrix": [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
        "score": 0,
        "start": start,
        "move": move,
        "check_win": check_win,
        "check_lose": check_lose,
        "get_empty_tiles": get_empty_tiles,
        "ai": ai
    }

    return self


def Grid4D():
    """
    Fonction regroupant toutes les fonctions invisibles à la grille de jeu 4D.
    :return dict self: Dictionnaire contenant la grille de jeu.
    """

    def start(self: dict):
        """
        Génère deux tuiles de valeur 2 ou 4 aléatoirement sur la grille.
        :param dict self: Dictionnaire contenant la grille de jeu.
        """

        for i in range(2):
            generate_new_tile(self, get_empty_tiles(self))

    def get_empty_tiles(self: dict) -> list:
        """
        Récupère les positions vides de la grille.
        :param dict self: Dictionnaire contenant la grille de jeu.
        :return list empty_tiles: Liste des positions vides de la grille.
        """

        empty_tiles = []

        for x in range(4):
            for y in range(2):
                for z in range(2):
                    if self["matrix"][x][y][z] == 0:
                        empty_tiles.append((x, y, z))

        return empty_tiles

    def generate_new_tile(self: dict, empty_tiles: list):
        """
        Génère une nouvelle tuile de valeur 2 ou 4 aléatoirement sur la grille.
        :param dict self: Dictionnaire contenant la grille de jeu.
        :param list empty_tiles: Liste des positions vides de la grille.
        """

        if empty_tiles:
            x, y, z = empty_tiles[randint(0, len(empty_tiles) - 1)]
            if random() < 0.9:
                self["matrix"][x][y][z] = 2
            else:
                self["matrix"][x][y][z] = 4

            self["score"] += self["matrix"][x][y][z]

    def check_win(self: dict) -> bool:
        """
        Vérifie si la partie est gagnée.
        :param dict self: Dictionnaire contenant la grille de jeu.
        :return bool: True si la partie est gagnée, False sinon.
        """

        for x in self["matrix"]:
            for y in x:
                for elem in y:
                    if elem == 2048:
                        return True
        return False

    def check_lose(self: dict, empty_tiles: list) -> bool:
        """
        Vérifie si on peut faire un mouvement dans la direction donnée.
        :param dict self: Dictionnaire contenant la grille de jeu.
        :param list empty_tiles: Liste des positions vides de la grille.
        :return bool: True si la partie est perdue, False sinon.
        """

        if empty_tiles:
            return False

        for direction in config:

            # On récupère les coordonnées de départ et d'arrivée.
            dy, dz = config[direction]["dy"], config[direction]["dz"]
            y_start, y_end, y_step = config[direction]["y_start"], config[direction]["y_end"], config[direction][
                "y_step"]
            z_start, z_end, z_step = config[direction]["z_start"], config[direction]["z_end"], config[direction][
                "z_step"]

            for x in range(4):
                for y in range(y_start, y_end, y_step):
                    for z in range(z_start, z_end, z_step):
                        if self["matrix"][x][y][z] == self["matrix"][x][y + dy][z + dz]:
                            return False
        return True

    def move(self: dict, direction: str) -> dict:
        """
        Déplace les tuiles dans la direction donnée.
        :param dict self: Dictionnaire contenant la grille de jeu.
        :param str direction: Direction dans laquelle on veut déplacer les tuiles.
        :return dict data: Dictionnaire contenant les informations sur le mouvement.
        """

        data = {
            "mouvement": [],
            "fusion": [],
        }

        empty_tiles = get_empty_tiles(self)

        if check_win(self):
            return data
        elif check_lose(self, empty_tiles):
            return data

        pos = []

        # On récupère les informations de la direction donnée.
        info = config[direction]
        # On récupère les coordonnées de départ et d'arrivée.
        dy, dz = info["dy"], info["dz"]
        y_start, y_end, y_step = info["y_start"], info["y_end"], info["y_step"]
        z_start, z_end, z_step = info["z_start"], info["z_end"], info["z_step"]

        # On parcourt la grille.
        for x in range(4):
            for y in range(y_start, y_end, y_step):
                for z in range(z_start, z_end, z_step):

                    if self["matrix"][x][y][z] == 0:
                        continue

                    # On définit les variables qui vont nous permettre de parcourir la matrice dans la direction donnée.
                    prev_y, prev_z = y + dy, z + dz

                    # Tant que la case précédente est vide, on continue de parcourir la matrice dans la direction
                    # donnée.
                    while (0 <= prev_y < 2 and 0 <= prev_z < 2) and self["matrix"][x][prev_y][prev_z] == 0:
                        prev_y, prev_z = prev_y + dy, prev_z + dz

                    # Si la case précédente est égale à la case actuelle et qu'elle n'a pas déjà fusionné, on fusionne
                    # les deux cases.
                    if (0 <= prev_y < 2 and 0 <= prev_z < 2) and self["matrix"][x][prev_y][prev_z] == \
                            self["matrix"][x][y][z] \
                            and (x, prev_y, prev_z) not in pos:
                        self["matrix"][x][prev_y][prev_z] *= 2
                        self["matrix"][x][y][z] = 0

                        # On stocke les coordonnées de la case qui a fusionné.
                        data["fusion"].append({"from": (x, y, z), "to": (x, prev_y, prev_z)})
                        pos.append((x, prev_y, prev_z))

                    # Sinon, on déplace la case actuelle vers la première case vide au-dessus.
                    else:
                        if (prev_y - dy, prev_z - dz) != (y, z):
                            self["matrix"][x][prev_y - dy][prev_z - dz] = self["matrix"][x][y][z]
                            self["matrix"][x][y][z] = 0
                            data["mouvement"].append({"from": (x, y, z), "to": (x, prev_y - dy, prev_z - dz)})

        # Génère une nouvelle tuile si une fusion ou un mouvement a eu lieu
        if data["mouvement"] or data["fusion"]:
            generate_new_tile(self, get_empty_tiles(self))

        return data

    config = {

        "up": {
            "dy": -1, "dz": 0,
            "y_start": 1, "y_end": 2, "y_step": 1,
            "z_start": 0, "z_end": 2, "z_step": 1,
        },

        "down": {
            "dy": 1, "dz": 0,
            "y_start": 0, "y_end": -1, "y_step": -1,
            "z_start": 0, "z_end": 2, "z_step": 1,
        },

        "left": {
            "dy": 0, "dz": -1,
            "y_start": 0, "y_end": 2, "y_step": 1,
            "z_start": 1, "z_end": 2, "z_step": 1,
        },

        "right": {
            "dy": 0, "dz": 1,
            "y_start": 0, "y_end": 2, "y_step": 1,
            "z_start": 0, "z_end": -1, "z_step": -1,
        },
    }

    self = {
        "matrix": [[[0, 0], [0, 0]], [[0, 0], [0, 0]], [[0, 0], [0, 0]], [[0, 0], [0, 0]]],
        "score": 0,
        "start": start,
        "move": move,
        "check_win": check_win,
        "check_lose": check_lose,
        "get_empty_tiles": get_empty_tiles
    }

    return self


def rgb_to_tkinter(rgb: tuple[int, int, int]):
    """
    translates a rgb tuple of int to a tkinter friendly color code
    """
    return f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'


# create a round rectangle
def round_rectangle(canvas: tkinter.Canvas, x1: int, y1: int, x2: int, y2: int, radius: int = 25, **kwargs) -> int:
    """
    Generate a round rectangle.
    Code found on
    https://stackoverflow.com/questions/44099594/how-to-make-a-tkinter-canvas-rectangle-with-rounded-corners
    :param canvas:
    :param x1:
    :param y1:
    :param x2:
    :param y2:
    :param radius:
    :param kwargs:
    :return:
    """
    points = [x1 + radius, y1,
              x1 + radius, y1,
              x2 - radius, y1,
              x2 - radius, y1,
              x2, y1,
              x2, y1 + radius,
              x2, y1 + radius,
              x2, y2 - radius,
              x2, y2 - radius,
              x2, y2,
              x2 - radius, y2,
              x2 - radius, y2,
              x1 + radius, y2,
              x1 + radius, y2,
              x1, y2,
              x1, y2 - radius,
              x1, y2 - radius,
              x1, y1 + radius,
              x1, y1 + radius,
              x1, y1]
    return canvas.create_polygon(points, **kwargs, smooth=True)


def BetterButton(canvas: tkinter.Canvas,
                 x: int,
                 y: int,
                 text: str,
                 text_color: tuple[int, int, int] = (0, 0, 0),
                 color: tuple[int, int, int] = (255, 255, 255),
                 hover_color: tuple[int, int, int] = (200, 200, 200),
                 hover_text_color: tuple[int, int, int] = (0, 0, 0),
                 command=lambda: None,
                 padding: tuple[int, int] = (50, 20),
                 size: tuple[int, int] = None,
                 border_radius: int = 50,
                 font: tkinter.font.Font = None,
                 anchor: str = "nw", ) -> dict:
    """
    Create a button with a better look.
    :param canvas: the canvas on which the button will be drawn
    :param x: the x position of the button
    :param y: the y position of the button
    :param text: the text of the button
    :param text_color: the color of the text
    :param color: the color of the button
    :param hover_color: the color of the button when the mouse is over it
    :param hover_text_color: the color of the text when the mouse is over the button
    :param command: the command to execute when the button is clicked
    :param padding: the space between the text and the border of the button
    :param size: the size of the button (overrides the padding)
    :param border_radius: the radius of the border
    :param font: the font of the text
    :param anchor: the anchor of the button
    :return: the button
    """

    # define all default values of the button
    self = {"canvas": canvas, "x": x, "y": y, "text": text, "color": color, "hover_color": hover_color,
            "hover_text_color": hover_text_color, "command": command, "hover": False, "padding": padding,
            "border_radius": border_radius, "font": font, "text_color": text_color, "anchor": anchor}

    def hover_on(self: dict) -> None:
        """
        Change the color of the button when the mouse is over it
        :param self: the button
        :return:
        """
        self["hover"] = True
        self["canvas"].itemconfig(self["text_canvas"], fill=rgb_to_tkinter(self["hover_text_color"]))
        self["canvas"].itemconfig(self["button"], fill=rgb_to_tkinter(self["hover_color"]))

    def hover_off(self: dict) -> None:
        """
        Change the color of the button when the mouse is not over it
        :param self: the button
        :return:
        """
        self["hover"] = False
        self["canvas"].itemconfig(self["button"], fill=rgb_to_tkinter(self["color"]))
        self["canvas"].itemconfig(self["text_canvas"], fill=rgb_to_tkinter(self["text_color"]))

    def click(self: dict) -> None:
        """
        Execute the command of the button when it is clicked
        :param self: the button
        :return:
        """
        if self["hover"]:
            self["command"]()

    def get_anchor_position(self: dict, x: int, y: int) -> tuple[int, int]:
        """
        Transpose the position from the given anchor to the nw anchor
        :param self: the button
        :param x: the x position at the given anchor
        :param y: the y position at the given anchor
        :return: the x and y position at the nw anchor
        """
        if self["anchor"] == "center":
            x -= self["size"][0] / 2
            y -= self["size"][1] / 2
        elif self["anchor"] == "ne":
            x -= self["size"][0]
        elif self["anchor"] == "se":
            x -= self["size"][0]
            y -= self["size"][1]
        elif self["anchor"] == "sw":
            y -= self["size"][1]
        elif self["anchor"] == "e":
            x -= self["size"][0]
            y -= self["size"][1] / 2
        elif self["anchor"] == "w":
            y -= self["size"][1] / 2
        elif self["anchor"] == "n":
            x -= self["size"][0] / 2
        elif self["anchor"] == "s":
            x -= self["size"][0] / 2
            y -= self["size"][1]
        return x, y

    def build(self: dict) -> None:
        """
        Build the button on the canvas
        :param self: the button
        :return:
        """
        # check if the mouse is over the button and choose the right color
        if self["hover"]:
            color = self["hover_color"]
            text_color = self["hover_text_color"]
        else:
            color = self["color"]
            text_color = self["text_color"]

        # create the button
        self["button"] = round_rectangle(self["canvas"], self["x"], self["y"],
                                         self["x"] + self["text_size"][0] + self["padding"][0],
                                         self["y"] + self["text_size"][1] + self["padding"][1],
                                         radius=self["border_radius"], fill=rgb_to_tkinter(color))
        # create the text
        self["text_canvas"] = self["canvas"].create_text(self["x"] + (self["padding"][0] + self["text_size"][0]) / 2,
                                                         self["y"] + self["padding"][1] / 2,
                                                         text=self["text"],
                                                         anchor="n", fill=rgb_to_tkinter(text_color),
                                                         font=self["font"])

        # bind the mouse events for the text
        self["canvas"].tag_bind(self["text_canvas"], "<Enter>", lambda e: self["hover_on"](self))
        self["canvas"].tag_bind(self["text_canvas"], "<Leave>", lambda e: self["hover_off"](self))
        self["canvas"].tag_bind(self["text_canvas"], "<Button-1>", lambda e: self["click"](self))
        # bind the mouse events
        self["canvas"].tag_bind(self["button"], "<Enter>", lambda e: self["hover_on"](self))
        self["canvas"].tag_bind(self["button"], "<Leave>", lambda e: self["hover_off"](self))
        self["canvas"].tag_bind(self["button"], "<Button-1>", lambda e: self["click"](self))

    # add all the methods to the button
    self["hover_on"] = hover_on
    self["hover_off"] = hover_off
    self["click"] = click
    self["get_anchor_position"] = get_anchor_position
    self["build"] = build

    # get the text size
    if not font:
        self["font"] = tkinter.font.Font(family="TkDefaultFont")
    self["text_size"] = self["font"].measure(self["text"]), self["font"].metrics("linespace")

    if size:
        # if the size is specified, use it
        self["padding"] = size[0] - self["text_size"][0], size[1] - self["text_size"][1]
    self["size"] = self["text_size"][0] + self["padding"][0], self["text_size"][1] + self["padding"][1]
    # get the position of the button with nw anchor
    self["x"], self["y"] = self["get_anchor_position"](self, self["x"], self["y"])
    # build the button
    self["build"](self)

    # return the button
    return self


def IconButton(canvas: tkinter.Canvas,
               x: int,
               y: int,
               icon: str,
               hover_icon: str = None,
               command=lambda: None,
               size: tuple[int, int] = None,
               border_radius: int = 50,
               anchor: str = "nw", ):
    """
    Create an icon button
    :param canvas: the canvas where the button will be created
    :param x: the x position of the button
    :param y: the y position of the button
    :param icon: the path of the icon
    :param hover_icon: the path of the icon when the mouse is over the button
    :param command: the command of the button
    :param size: the size of the button (if not specified, the size of the icon will be used)
    :param border_radius: the border radius of the button
    :param anchor: the anchor of the button
    :return: the button
    """

    # define the default values
    self = {"canvas": canvas, "x": x, "y": y, "icon": icon,
            "hover_icon": hover_icon, "command": command, "hover": False,
            "border_radius": border_radius, "anchor": anchor, "size": size}

    def hover_on(self: dict) -> None:
        """
        Change the icon of the button when the mouse is over it
        :param self: the button
        :return:
        """
        self["hover"] = True
        self["canvas"].itemconfig(self["button"],
                                  image=self["hover_textureTk"])

    def hover_off(self: dict) -> None:
        """
        Change the icon of the button when the mouse is not over it
        :param self: the button
        :return:
        """
        self["hover"] = False
        self["canvas"].itemconfig(self["button"],
                                  image=self["textureTk"])

    def click(self: dict) -> None:
        """
        Execute the command of the button
        :param self: the button
        :return:
        """
        if self["hover"]:
            self["command"]()

    def get_anchor_position(self: dict, x: int, y: int) -> tuple[int, int]:
        """
        Transpose the position from the given anchor to the nw anchor
        :param self: the button
        :param x: the x position at the given anchor
        :param y: the y position at the given anchor
        :return: the x and y position at the nw anchor
        """
        if self["anchor"] == "center":
            x -= self["size"][0] / 2
            y -= self["size"][1] / 2
        elif self["anchor"] == "ne":
            x -= self["size"][0]
        elif self["anchor"] == "se":
            x -= self["size"][0]
            y -= self["size"][1]
        elif self["anchor"] == "sw":
            y -= self["size"][1]
        elif self["anchor"] == "e":
            x -= self["size"][0]
            y -= self["size"][1] / 2
        elif self["anchor"] == "w":
            y -= self["size"][1] / 2
        elif self["anchor"] == "n":
            x -= self["size"][0] / 2
        elif self["anchor"] == "s":
            x -= self["size"][0] / 2
            y -= self["size"][1]
        return x, y

    def build(self: dict) -> None:
        """
        Build the button
        :param self: the button
        :return:
        """

        # check if the mouse is over the button and choose the right icon
        if self["hover"]:
            image = "hover_textureTk"
        else:
            image = "textureTk"
        # create the button
        self["button"] = self["canvas"].create_image(self["x"], self["y"], image=self[image], anchor="nw")
        # bind the mouse events
        self["canvas"].tag_bind(self["button"], "<Enter>", lambda e: self["hover_on"](self))
        self["canvas"].tag_bind(self["button"], "<Leave>", lambda e: self["hover_off"](self))
        self["canvas"].tag_bind(self["button"], "<Button-1>", lambda e: self["click"](self))

    # add all the methods to the button
    self["hover_on"] = hover_on
    self["hover_off"] = hover_off
    self["click"] = click
    self["get_anchor_position"] = get_anchor_position
    self["build"] = build

    # load the icon
    self["texture"] = Image.open(self["icon"])
    if not self["hover_icon"]:
        self["hover_icon"] = self["icon"]
    # load the hover icon
    self["hover_texture"] = Image.open(self["hover_icon"])

    if not size:
        # get the size of the icon
        self["size"] = self["texture"].size
    # get the position of the button with nw anchor
    self["x"], self["y"] = self["get_anchor_position"](self, self["x"], self["y"])
    # resize the icons
    self["textureTk"] = ImageTk.PhotoImage(self["texture"].resize(self["size"]))
    self["hover_textureTk"] = ImageTk.PhotoImage(self["hover_texture"].resize(self["size"]))
    # build the button
    self["build"](self)

    # return the button
    return self


# making the menu
def Menu(root: tkinter.Tk):
    """Fait une fenetre Menu grâce à Tkinter."""
    self = {"frame": tkinter.Frame(root)}
    self["frame"].grid(row=0, column=0)
    self["canvas"] = tkinter.Canvas(self["frame"], width=root.winfo_width(), height=root.winfo_height(), bg="#a39489")
    self["canvas"].pack()
    self["grid"] = SimpleGrid()
    self["canvas"].create_text(root.winfo_width() // 2, 20, anchor="n", text="2048",
                               font=tkinter.font.Font(family="Roboto",
                                                      size=int(root.winfo_height() * 0.25), weight="bold"),
                               fill="#776e65")
    point = int(root.winfo_width() // 2), int(root.winfo_height() // 2.35)
    BetterButton(self["canvas"], point[0], point[1], "Classique", anchor="n",
                 size=(400, 80), command=lambda: Game(root, False, ), text_color=(255, 255, 255), color=(119, 110, 101),
                 hover_color=(150, 140, 130), font=tkinter.font.Font(size=50), border_radius=90)
    BetterButton(self["canvas"], point[0], point[1] + 90, "4D",
                 size=(400, 80),
                 anchor="n", command=lambda: Game4D(root, False),
                 text_color=(255, 255, 255), color=(119, 110, 101), hover_color=(150, 140, 130),
                 font=tkinter.font.Font(size=50), border_radius=90)
    BetterButton(self["canvas"], point[0], point[1] + 270, "Quitter",
                 anchor="n",
                 size=(400, 80), command=root.destroy, text_color=(255, 255, 255), color=(119, 110, 101),
                 hover_color=(150, 140, 130), font=tkinter.font.Font(size=50), border_radius=90)
    # Button to load the game
    BetterButton(self["canvas"], point[0], point[1] + 180, "Charger",
                 anchor="n",
                 size=(400, 80), command=lambda: verify_load(root), text_color=(255, 255, 255),
                 color=(119, 110, 101),
                 hover_color=(150, 140, 130), font=tkinter.font.Font(size=50), border_radius=90)


def verify_load(root: tkinter.Tk):
    data = load()
    if not data:
        pass
    elif data["type"] == "4D":
        Game4D(root, True, data)
    elif data["type"] == "simple":
        Game(root, True, data)


def Game(root: tkinter.Tk, isload: bool, data=None):
    """
    Fait une fenetre de jeu grâce à Tkinter.
    """
    self = {
        "frame": tkinter.Frame(root),
    }
    self["frame"].grid(row=0, column=0)
    self["canvas"] = tkinter.Canvas(self["frame"], width=root.winfo_width(), height=root.winfo_height(), bg="#F3E6E4")
    self["canvas"].pack()
    self["canvas"].create_text(root.winfo_width() // 2, 20, anchor="n", text="2048", font='Helvetica 80 bold',
                               fill="#776e65")
    BetterButton(self["canvas"], int(root.winfo_width() // 1.2), root.winfo_height() // 2, "Menu", anchor="n",
                 size=(200, 50), command=lambda: Menu(root), text_color=(255, 255, 255), color=(119, 110, 101),
                 hover_color=(150, 140, 130))
    point = int(root.winfo_width() // 1.2), int(root.winfo_height() // 2)
    BetterButton(self["canvas"], point[0], point[1] + 60, "Quitter", anchor="n",
                 size=(200, 50), command=root.destroy, text_color=(255, 255, 255), color=(119, 110, 101),
                 hover_color=(150, 140, 130))
    # Button to save the game
    BetterButton(self["canvas"], point[0], point[1] + 120, "Sauvegarder",
                 command=lambda: save(self["grid"]["matrix"], "simple"),
                 size=(200, 50), anchor="n", text_color=(255, 255, 255), color=(119, 110, 101),
                 hover_color=(150, 140, 130))

    def ai_update():
        if not self["grid"]["check_lose"](self["grid"], self["grid"]["get_empty_tiles"](self["grid"])):
            if not self["guard_rail"]:
                self["guard_rail"] = True
                move_data = self["grid"]["ai"](self["grid"])
                animation_duration = 100

                self["canvas"].itemconfig(self["score"], text=self["grid"]["score"])

                for movement in move_data["mouvement"]:
                    self["animation"](self, movement["from"], movement["to"], animation_duration, fps=144,
                                      function=lambda x: -(math.cos(math.pi * x) - 1) / 2)
                for fusion in move_data["fusion"]:
                    self["animation"](self, fusion["from"], fusion["to"], animation_duration, fps=144,
                                      function=lambda x: -(math.cos(math.pi * x) - 1) / 2)

                self["canvas"].after(animation_duration + 10, self["ai_update"])
            else:
                self["canvas"].after(10, self["ai_update"])

    # making a background for the game that is centered
    center = root.winfo_width() // 2
    self["size"] = root.winfo_height() // 7
    self["padding"] = 15
    self["height"] = int(root.winfo_height() // 3.5)
    round_rectangle(self["canvas"], int(center - (2.5 * self["padding"] + 2 * self["size"])), self["height"],
                    int(center + (2.5 * self["padding"] + 2 * self["size"])),
                    self["height"] + (4 * self["size"] + 5 * self["padding"]),
                    radius=10, fill="#bbada0")

    # create empty tiles for the grid
    self["tiles"] = [[None, None, None, None], [None, None, None, None], [None, None, None, None],
                     [None, None, None, None]]
    self["texts"] = [[None, None, None, None], [None, None, None, None], [None, None, None, None],
                     [None, None, None, None]]

    for i in range(4):
        for j in range(4):
            round_rectangle(self["canvas"],
                            int(center - (
                                    1.5 * self["padding"] + 2 * self["size"]) + i * (
                                        self["size"] + self["padding"])),
                            self["height"] + j * (self["size"] + self["padding"]) + self[
                                "padding"],
                            int(center - (
                                    1.5 * self["padding"] + 2 * self["size"]) + i * (
                                        self["size"] + self["padding"]) + self["size"]),
                            self["height"] + j * (self["size"] + self["padding"]) + self["size"] +
                            self["padding"],
                            fill="#cdc1b4", outline="#cdc1b4", radius=10)

    # update the tiles with the right color and text when the matrix change
    # update the tiles with the new matrix
    def update(self):
        """Met à jour les tuiles avec la nouvelle matrice en supprimant l'ancienne."""
        for i in range(4):
            for j in range(4):
                self["canvas"].delete(self["tiles"][i][j])
                self["canvas"].delete(self["texts"][i][j])
                # self["canvas"].itemconfig(self["tiles"][i][j], text=self["grid"]["matrix"][i][j])
                if self["grid"]["matrix"][i][j] != 0:
                    self["tiles"][i][j] = round_rectangle(self["canvas"],
                                                          int(center - (
                                                                  1.5 * self["padding"] + 2 * self["size"]) + i * (
                                                                      self["size"] + self["padding"])),
                                                          self["height"] + j * (self["size"] + self["padding"]) + self[
                                                              "padding"],
                                                          int(center - (
                                                                  1.5 * self["padding"] + 2 * self["size"]) + i * (
                                                                      self["size"] + self["padding"]) + self["size"]),
                                                          self["height"] + j * (self["size"] + self["padding"]) +
                                                          self["size"] +
                                                          self["padding"],
                                                          fill=self["color"][self["grid"]["matrix"][i][j]],
                                                          outline=self["color"][self["grid"]["matrix"][i][j]],
                                                          radius=10)
                    self["texts"][i][j] = self["canvas"].create_text(
                        int(center - (1.5 * self["padding"] + 2 * self["size"]) + i * (self["size"] + self["padding"]) +
                            self["size"] // 2),
                        self["height"] + j * (self["size"] + self["padding"]) + self["padding"] + self["size"] // 2,
                        text=self["grid"]["matrix"][i][j], font='Helvetica 40 bold',
                        fill="#776e65")

        # if the player lose we show a black background with a text
        if self["grid"]["check_lose"](self["grid"], self["grid"]["get_empty_tiles"](self["grid"])):
            # let's fade the grid with a pil image
            self["lose_fade"] = self["canvas"].create_image(center, self["height"], image=self["fade_frames"][0],
                                                            anchor="n")
            self["canvas"].after(5, self["fade"], 1)
            # creating the text
            self["canvas"].create_text(center, self["height"] + self["size"] * 2 + self["padding"] * 3,
                                       text="vous avez perdu !", font='Helvetica 40 bold',
                                       fill="white")

    def fade(current_opacity: int):
        self["canvas"].itemconfig(self["lose_fade"], image=self["fade_frames"][current_opacity])
        if current_opacity < len(self["fade_frames"]) - 1:
            self["canvas"].after(5, self["fade"], current_opacity + 1)

    # generating images for the fade
    image = Image.new("RGBA", (self["size"] * 4 + self["padding"] * 5, self["size"] * 4 + self["padding"] * 5),
                      (0, 0, 0, 0))
    self["fade_frames"] = []
    for i in range(0, 170, 10):
        image.putalpha(i)
        self["fade_frames"].append(ImageTk.PhotoImage(image))

    def animation(self: dict, start: tuple[int, int], end: tuple[int, int], duration: int, function=lambda x: x,
                  fps=60):
        """Génère une animation."""
        frame_count = int(duration * fps / 1000)
        movement = (end[0] - start[0], end[1] - start[1])
        pixel_gap = self["size"] + self["padding"]
        frames = []
        for i in range(frame_count):
            pourcentage = function(i / frame_count)
            frames.append((int(movement[0] * pourcentage * pixel_gap),
                           int(movement[1] * pourcentage * pixel_gap)))
        begin = time.time()
        self["animate"](self, frames, start, self["canvas"].coords(self["tiles"][start[0]][start[1]]),
                        self["canvas"].coords(self["texts"][start[0]][start[1]]), len(frames) - 1, duration, begin, fps)

    def animate(self: dict, frames: list[tuple[int, int]], start: tuple[int, int], start_coords: tuple[int, int],
                text_start_coords: tuple[int, int], frames_length: int, duration: int,
                begin: float, fps=60):
        """Anime les tuiles."""
        if (time.time() - begin) * 1000 < duration:
            self["canvas"].after(1,
                                 lambda: self["animate"](self, frames, start, start_coords, text_start_coords,
                                                         frames_length, duration, begin, fps))
        else:
            self["update"](self)
            self["guard_rail"] = False
            return
        frame = int(((time.time() - begin) * 1000) / duration * frames_length)
        self["canvas"].moveto(self["tiles"][start[0]][start[1]],
                              frames[frame][0] + start_coords[0] - 12,
                              frames[frame][1] + start_coords[1], )
        self["canvas"].coords(self["texts"][start[0]][start[1]],
                              frames[frame][0] + text_start_coords[0],
                              frames[frame][1] + text_start_coords[1])

    # make tiles move with Grid()
    # get the move() function from Grid()
    self["grid"] = SimpleGrid()
    self["animation"] = animation
    self["animate"] = animate
    self["update"] = update
    self["fade"] = fade
    self["ai_update"] = ai_update
    self["guard_rail"] = False

    if isload:
        self["grid"]["matrix"] = data["matrix"]
    else:
        self["grid"]["start"](self["grid"])

    self["animating"] = False

    # Color of the tiles.
    self["color"] = {2: "#eee4da", 4: "#ede0c8", 8: "#f2b179", 16: "#f59563", 32: "#f67c5f", 64: "#f65e3b",
                     128: "#edcf72",
                     256: "#edcc61", 512: "#edc850", 1024: "#edc53f", 2048: "#edc22e", 4096: "#3c3a32",
                     8192: "#3c3a32",
                     16384: "#3c3a32", 32768: "#3c3a32", 65536: "#3c3a32", 131072: "#3c3a32", 262144: "#3c3a32",
                     524288: "#3c3a32",
                     1048576: "#3c3a32", 2097152: "#3c3a32", 4194304: "#3c3a32", 8388608: "#3c3a32",
                     16777216: "#3c3a32",
                     33554432: "#3c3a32", 67108864: "#3c3a32", 134217728: "#3c3a32", 268435456: "#3c3a32"}

    # button for ai
    BetterButton(self["canvas"], point[0], point[1] + 180, "AI",
                 anchor="n",
                 size=(200, 50), command=self["ai_update"], text_color=(255, 255, 255),
                 color=(119, 110, 101),
                 hover_color=(150, 140, 130))

    # make the tiles with the matrix

    update(self)

    # make a score
    self["score"] = self["canvas"].create_text(root.winfo_width() // 2, root.winfo_height() // 4.5, anchor="n",
                                               text="Score : " + str(self["grid"]["score"]), font='Helvetica 30 bold',
                                               fill="#776e65")

    # functions for the keys

    def action(self, direction):
        """Fonction qui fait bouger les tuiles et qui met à jour le score."""
        if self["guard_rail"]:
            return
        animation_duration = 100
        move_data = self["grid"]["move"](self["grid"], direction)
        if not (len(move_data["mouvement"]) == 0 and len(move_data["fusion"]) == 0):
            self["guard_rail"] = True
        for movement in move_data["mouvement"]:
            self["animation"](self, movement["from"], movement["to"], animation_duration, fps=144,
                              function=lambda x: -(math.cos(math.pi * x) - 1) / 2)
        for fusion in move_data["fusion"]:
            self["animation"](self, fusion["from"], fusion["to"], animation_duration, fps=144,
                              function=lambda x: -(math.cos(math.pi * x) - 1) / 2)

        # print(direction, self["grid"]["matrix"])
        # update(self)
        # update the score
        self["canvas"].itemconfig(self["score"], text="Score : " + str(self["grid"]["score"]))

    # make buttons for the keys
    icon_button_size = 50
    icon_button_padding = 20
    left_padding = 0.5 * (center - (2 * self["size"] +
                                    2.5 * self["padding"])) - icon_button_size * 1.5 - icon_button_padding
    pos_y = int(self["height"] + 3 * self["size"] + 3.5 * self["padding"] +
                0.5 * icon_button_size + 1 * icon_button_padding)
    IconButton(self["canvas"], left_padding + icon_button_padding + icon_button_size, pos_y,
               "down.png", command=lambda: action(self, "right"), size=(icon_button_size, icon_button_size),
               hover_icon="down_hover.png")
    IconButton(self["canvas"], 2 * icon_button_size + left_padding + 2 * icon_button_padding,
               int(pos_y - icon_button_padding - icon_button_size),
               "right.png", command=lambda: action(self, "down"), size=(icon_button_size, icon_button_size),
               hover_icon="right_hover.png")
    IconButton(self["canvas"], left_padding, int(pos_y - icon_button_padding - icon_button_size),
               "left.png", command=lambda: action(self, "up"), size=(icon_button_size, icon_button_size),
               hover_icon="left_hover.png")
    IconButton(self["canvas"], left_padding + icon_button_padding + icon_button_size,
               int(pos_y - 2 * icon_button_padding - 2 * icon_button_size),
               "up.png", command=lambda: action(self, "left"), size=(icon_button_size, icon_button_size),
               hover_icon="up_hover.png")

    # bind the keys
    root.bind("<KeyPress-Up>", lambda event: action(self, "left"))
    root.bind("<KeyPress-Down>", lambda event: action(self, "right"))
    root.bind("<KeyPress-Left>", lambda event: action(self, "up"))
    root.bind("<KeyPress-Right>", lambda event: action(self, "down"))

    # check if the game was loaded from a save
    if self["grid"]["matrix"] == [[0 for _ in range(4)] for _ in range(4)]:
        self["grid"]["add_tile"](self["grid"])
        self["grid"]["add_tile"](self["grid"])
        update(self)


# making the 2048 4D window
def Game4D(root: tkinter.Tk, isload: bool, data=None) -> dict:
    """
    Fonction qui crée la fenêtre du jeu 2048 4D.
    :param root: The tkinter window
    :param isload: Whenever the game is loaded from a save or not
    :param data: grid to load if isload is True
    :return: The Game4D object
    """
    self = {
        "frame": tkinter.Frame(root),
        "guard_rail": False
    }
    self["frame"].grid(row=0, column=0)
    self["canvas"] = tkinter.Canvas(self["frame"], width=root.winfo_width(), height=root.winfo_height(), bg="#F3E6E4")
    self["canvas"].pack()
    self["canvas"].create_text(root.winfo_width() // 2, 20, anchor="n", text="2048", font='Helvetica 80 bold',
                               fill="#776e65")
    # making a background for the game that is centered
    center = root.winfo_width() // 2
    self["size"] = root.winfo_height() // 7
    self["padding"] = 15
    height = int(root.winfo_height() // 3.5)
    self["height"] = height
    round_rectangle(self["canvas"], int(center - (3 * self["padding"] + 2 * self["size"])),
                    height,
                    int(center + (3 * self["padding"] + 2 * self["size"])),
                    height + (4 * self["size"] + 6 * self["padding"]),
                    radius=10, fill="#bbada0")

    # Buttons to go back to main menu and to quit
    BetterButton(self["canvas"], int(root.winfo_width() // 1.2), root.winfo_height() // 2, "Menu", anchor="n",
                 size=(200, 50), command=lambda: Menu(root), text_color=(255, 255, 255), color=(119, 110, 101),
                 hover_color=(150, 140, 130))
    point = int(root.winfo_width() // 1.2), int(root.winfo_height() // 2)
    BetterButton(self["canvas"], point[0], point[1] + 60, "Quitter", anchor="n",
                 size=(200, 50), command=root.destroy, text_color=(255, 255, 255), color=(119, 110, 101),
                 hover_color=(150, 140, 130))
    # Button to save the game
    BetterButton(self["canvas"], point[0], point[1] + 120, "Sauvegarder",
                 command=lambda: save(self["grid"]["matrix"], "4D"),
                 size=(200, 50), anchor="n", text_color=(255, 255, 255), color=(119, 110, 101),
                 hover_color=(150, 140, 130))
    # create empty tiles for the grid

    # make buttons for the keys
    icon_button_size = 50
    icon_button_padding = 20
    left_padding = 0.5 * (
                center - (2 * self["size"] + 2.5 * self["padding"])) - icon_button_size * 1.5 - icon_button_padding
    pos_y = int(
        self["height"] + 3 * self["size"] + 3.5 * self["padding"] + 0.5 * icon_button_size + 1 * icon_button_padding)
    IconButton(self["canvas"], left_padding + icon_button_padding + icon_button_size, pos_y,
               "down.png", command=lambda: action(self, "down"), size=(icon_button_size, icon_button_size),
               hover_icon="down_hover.png")
    IconButton(self["canvas"], 2 * icon_button_size + left_padding + 2 * icon_button_padding,
               int(pos_y - icon_button_padding - icon_button_size),
               "right.png", command=lambda: action(self, "right"), size=(icon_button_size, icon_button_size),
               hover_icon="right_hover.png")
    IconButton(self["canvas"], left_padding, int(pos_y - icon_button_padding - icon_button_size),
               "left.png", command=lambda: action(self, "left"), size=(icon_button_size, icon_button_size),
               hover_icon="left_hover.png")
    IconButton(self["canvas"], left_padding + icon_button_padding + icon_button_size,
               int(pos_y - 2 * icon_button_padding - 2 * icon_button_size),
               "up.png", command=lambda: action(self, "up"), size=(icon_button_size, icon_button_size),
               hover_icon="up_hover.png")

    self["tiles"] = [[[None, None], [None, None]], [[None, None], [None, None]], [[None, None], [None, None]],
                     [[None, None], [None, None]]]
    self["texts"] = [[[None, None], [None, None]], [[None, None], [None, None]], [[None, None], [None, None]],
                     [[None, None], [None, None]]]
    # create the grid
    spacex = 10
    spacey = 0
    # making a 2048 4D grid while adding space in between every block of 4 tiles
    current_x = center - 2 * self["padding"] - 2 * self["size"]
    current_y = self["height"] + self["padding"]
    for i in range(4):
        for j in range(2):
            for k in range(2):
                round_rectangle(self["canvas"],
                                current_x,
                                current_y,
                                current_x + self["size"],
                                current_y + self["size"],
                                fill="#cdc1b4")
                current_x += self["padding"] + self["size"]
            current_x -= 2 * self["padding"] + 2 * self["size"]
            current_y += self["size"] + self["padding"]
        if i % 2 == 0:
            current_x += 2 * self["size"] + 3 * self["padding"]
            current_y -= 2 * self["size"] + 2 * self["padding"]
        if i == 1:
            current_x -= 2 * self["size"] + 3 * self["padding"]
            current_y += self["padding"]
    # show the tiles on the grid
    self["grid"] = Grid4D()
    if isload:
        self["grid"]["matrix"] = data["matrix"]
    else:
        self["grid"]["start"](self["grid"])

    # Color of the tiles. Same as the normal game.
    self["color"] = {0: "#cdc1b4", 2: "#eee4da", 4: "#ede0c8", 8: "#f2b179", 16: "#f59563", 32: "#f67c5f",
                     64: "#f65e3b",
                     128: "#edcf72",
                     256: "#edcc61", 512: "#edc850", 1024: "#edc53f", 2048: "#edc22e"}

    # show the tiles when the game starts
    # update the tiles with the right color and text when the matrix change
    # update the tiles with the new matrix
    def update(self):
        """Fonction qui place les tuiles sur la grille 4D."""
        current_x = center - 2 * self["padding"] - 2 * self["size"]
        current_y = self["height"] + self["padding"]
        for i in range(4):
            for j in range(2):
                for k in range(2):
                    self["canvas"].delete(self["tiles"][i][j][k])
                    self["canvas"].delete(self["texts"][i][j][k])
                    if self["grid"]["matrix"][i][j][k] != 0:
                        self["tiles"][i][j][k] = round_rectangle(self["canvas"],
                                                                 current_x,
                                                                 current_y,
                                                                 current_x + self["size"],
                                                                 current_y + self["size"],
                                                                 fill=self["color"][self["grid"]["matrix"][i][j][k]])
                        self["texts"][i][j][k] = self["canvas"].create_text(current_x + self["size"] // 2, current_y
                                                                            + self["size"] // 2,
                                                                            text=self["grid"]["matrix"][i][j][k],
                                                                            anchor="center",
                                                                            font=tkinter
                                                                            .font.Font(size=40,
                                                                                       family="Helvetica",
                                                                                       weight=tkinter.font.BOLD),
                                                                            fill="#776e65")
                    current_x += self["padding"] + self["size"]
                current_x -= 2 * self["padding"] + 2 * self["size"]
                current_y += self["size"] + self["padding"]
            if 0 == i % 2:
                current_x += 2 * self["size"] + 3 * self["padding"]
                current_y -= 2 * self["size"] + 2 * self["padding"]
            elif i == 1:
                current_x -= 2 * self["size"] + 3 * self["padding"]
                current_y += self["padding"]

        # if the player lose we show a black background with a text
        if self["grid"]["check_lose"](self["grid"], self["grid"]["get_empty_tiles"](self["grid"])):
            # let's fade the grid with a pil image
            self["lose_fade"] = self["canvas"].create_image(center, self["height"],
                                                            image=self["fade_frames"][0],
                                                            anchor="n")
            self["canvas"].after(5, self["fade"], 1)
            # creating the text
            self["canvas"].create_text(center, self["height"] + self["size"] * 2 + self["padding"] * 3,
                                       text="vous avez perdu !", font='Helvetica 40 bold',
                                       fill="white")

    def animation(self: dict, start: tuple[int, int], end: tuple[int, int], duration: int, function=lambda x: x,
                  fps=60):
        """Génère une animation."""
        frame_count = int(duration * fps / 1000)
        movement = (end[2] - start[2], end[1] - start[1])
        pixel_gap = self["size"] + self["padding"]
        frames = []
        for i in range(frame_count):
            pourcentage = function(i / frame_count)
            frames.append((int(movement[0] * pourcentage * pixel_gap),
                           int(movement[1] * pourcentage * pixel_gap)))
        begin = time.time()
        self["animate"](self, frames, start, self["canvas"].coords(self["tiles"][start[0]][start[1]][start[2]]),
                        self["canvas"].coords(self["texts"][start[0]][start[1]][start[2]]), len(frames) - 1, duration,
                        begin, fps)

    def animate(self: dict, frames: list[tuple[int, int]], start: tuple[int, int], start_coords: tuple[int, int],
                text_start_coords: tuple[int, int], frames_length: int, duration: int,
                begin: float, fps=60):
        """Anime les tuiles."""
        if (time.time() - begin) * 1000 < duration:
            self["canvas"].after(1,
                                 lambda: self["animate"](self, frames, start, start_coords, text_start_coords,
                                                         frames_length, duration, begin, fps))
        else:
            self["update"](self)
            self["guard_rail"] = False
            return
        frame = int(((time.time() - begin) * 1000) / duration * frames_length)
        self["canvas"].moveto(self["tiles"][start[0]][start[1]][start[2]],
                              frames[frame][0] + start_coords[0] - 26,
                              frames[frame][1] + start_coords[1], )
        self["canvas"].coords(self["texts"][start[0]][start[1]][start[2]],
                              frames[frame][0] + text_start_coords[0],
                              frames[frame][1] + text_start_coords[1])

    self["score"] = self["canvas"].create_text(root.winfo_width() // 2, root.winfo_height() // 4.5, anchor="n",
                                               text="Score : " + str(self["grid"]["score"]), font='Helvetica 30 bold',
                                               fill="#776e65")

    def action(self, direction):
        """Fonction qui fait bouger les tuiles et qui met à jour le score."""
        # move the tiles
        if self["guard_rail"]:
            return
        move_data = self["grid"]["move"](self["grid"], direction)
        if move_data["mouvement"] == [] and move_data["fusion"] == []:
            return
        animation_duration = 100
        self["guard_rail"] = True
        # update the tiles
        for movement in move_data["mouvement"]:
            self["animation"](self, movement["from"], movement["to"], animation_duration, fps=144,
                              function=lambda x: -(math.cos(math.pi * x) - 1) / 2)
        for fusion in move_data["fusion"]:
            self["animation"](self, fusion["from"], fusion["to"], animation_duration, fps=144,
                              function=lambda x: -(math.cos(math.pi * x) - 1) / 2)

    def fade(current_opacity: int):
        self["canvas"].itemconfig(self["lose_fade"], image=self["fade_frames"][current_opacity])
        if current_opacity < len(self["fade_frames"]) - 1:
            self["canvas"].after(1, self["fade"], current_opacity + 1)

    # generating images for the fade
    image = Image.new("RGBA", (self["size"] * 4 + self["padding"] * 6, self["size"] * 4 + self["padding"] * 6),
                      (0, 0, 0, 0))
    self["fade_frames"] = []
    for i in range(0, 170, 10):
        image.putalpha(i)
        self["fade_frames"].append(ImageTk.PhotoImage(image))
    # update the score
    # self["score"]["text"] = "Score : " + str(self["grid"]["score"])

    self["action"] = action
    self["animate"] = animate
    self["update"] = update
    self["animation"] = animation
    self["fade"] = fade

    # bind the keys to the grid
    root.bind("<KeyPress-Up>", lambda event: [self["action"](self, "up")])
    root.bind("<KeyPress-Down>", lambda event: [self["action"](self, "down")])
    root.bind("<KeyPress-Left>", lambda event: [self["action"](self, "left")])
    root.bind("<KeyPress-Right>", lambda event: [self["action"](self, "right")])

    # update the tiles when the matrix change
    self["update"](self)


def main():
    # create the root
    root = tkinter.Tk()
    # set the title and the size
    root.title('2048')
    # update the root to get the size later
    root.update()
    root.state('zoomed')
    root.resizable(False, False)
    root.iconphoto(False, ImageTk.PhotoImage(file="2048.png"))

    Menu(root)

    root.mainloop()


if __name__ == '__main__':
    main()
