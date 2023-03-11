import tkinter.font

# On importe randint et random du package random.
from random import randint, random

# On importe les fonctions de tkinter, json et datetime pour enregistrer une partie.
from tkinter.filedialog import asksaveasfile, askopenfile
import json
from datetime import datetime


def Grid():
    """
    Fonction regroupant toutes les fonctions invisibles à la grille de jeu.
    """

    def start(matrix: list):
        """
        Génère deux tuiles de valeur 2 ou 4 aléatoirement sur la grille.
        :param matrix: List
        :return: matrix
        """

        # On génère deux tuiles aléatoirement.
        for i in range(2):
            generate_new_tile(matrix)

        return matrix

    def get_empty_tiles(matrix: list):
        """
        Récupère les positions vides de la grille.
        :param matrix: List
        :return: pos
        """

        pos = []
        for x in range(4):
            for y in range(4):
                if matrix[x][y] == 0:
                    pos.append((x, y))
        return pos

    def generate_new_tile(matrix: list):
        """
        Génère une nouvelle tuile de valeur 2 ou 4 aléatoirement sur la grille.
        :param matrix: List
        :return: matrix
        """

        # On récupère les positions vides de la grille et on les stocke.
        pos = get_empty_tiles(matrix)

        # On choisit aléatoirement une position vide et on génère une tuile de valeur 2 ou 4.
        if pos:
            x, y = pos[randint(0, len(pos) - 1)]
            if random() < 0.9:
                matrix[x][y] = 2
            else:
                matrix[x][y] = 4

        return matrix

    def check_win(matrix: list):
        """
        Vérifie si la partie est gagnée.
        :param matrix: List
        :return: bool
        """

        for ligne in matrix:
            for elem in ligne:
                if elem == 2048:
                    return True
        return False

    def check_lose(matrix: list):
        """
        Vérifie si on peut faire un mouvement dans la direction donnée.
        :param matrix: List
        :return: bool
        """

        if get_empty_tiles(matrix):
            return False

        # On vérifie si on peut faire un mouvement dans la direction donnée.
        for direction in config:

            # On récupère les coordonnées de départ et d'arrivée.
            dx, dy = config[direction]["dx"], config[direction]["dy"]
            x_start, x_end, x_step = config[direction]["x_start"], config[direction]["x_end"], config[direction][
                "x_step"]
            y_start, y_end, y_step = config[direction]["y_start"], config[direction]["y_end"], config[direction][
                "y_step"]

            # oN parcourt la grille.
            for x in range(x_start, x_end, x_step):
                for y in range(y_start, y_end, y_step):

                    # On vérifie si la case est vide ou si la valeur de la case est égale à la valeur de la case
                    # adjacente.
                    if matrix[x][y] == matrix[x + dx][y + dy]:
                        return False

        return True

    def update_score(matrix: list):
        """
        Met à jour le score.
        :param matrix: List
        :return: score
        """

        score = 0

        for ligne in matrix:
            for elem in ligne:
                score += elem
        return score

    def move(matrix: list, direction: str):
        """
        Déplace les tuiles dans la direction donnée.
        :param matrix: List
        :param direction: str
        :return: mouvement, fusion, matrix
        """

        data = {
            "mouvement": [],
            "fusion": [],
        }

        if check_win(matrix):
            return [data, matrix]
        elif check_lose(matrix):
            return [data, matrix]

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

                if matrix[x][y] == 0:
                    continue

                # On définit les variables qui vont nous permettre de parcourir la matrice dans la direction donnée.
                prev_x, prev_y = x + dx, y + dy

                # Tant que la case précédente est vide, on continue de parcourir la matrice dans la direction donnée.
                while (0 <= prev_x < 4 and 0 <= prev_y < 4) and matrix[prev_x][prev_y] == 0:
                    prev_x, prev_y = prev_x + dx, prev_y + dy

                # Si la case précédente est égale à la case actuelle et qu'elle n'a pas déjà fusionné, on fusionne
                # les deux cases.
                if (0 <= prev_x < 4 and 0 <= prev_y < 4) and matrix[prev_x][prev_y] == matrix[x][y] and (
                        prev_x, prev_y) not in pos:
                    matrix[prev_x][prev_y] *= 2
                    matrix[x][y] = 0

                    # On stocke les coordonnées de la case qui a fusionné.
                    data["fusion"].append({"from": (x, y), "to": (prev_x, prev_y)})
                    pos.append((prev_x, prev_y))

                # Sinon, on déplace la case actuelle vers la première case vide au-dessus.
                else:
                    if (prev_x - dx, prev_y - dy) != (x, y):
                        matrix[prev_x - dx][prev_y - dy] = matrix[x][y]
                        matrix[x][y] = 0
                        data["mouvement"].append({"from": (x, y), "to": (prev_x - dx, prev_y - dy)})

        # Génère une nouvelle tuile si une fusion ou un mouvement a eu lieu
        if data["mouvement"] or data["fusion"]:
            generate_new_tile(matrix)

        return [data, matrix]

    def save(matrix: list):
        """
        Sauvegarde la partie en cours.
        :param matrix: list
        :return: None
        """

        # On crée un dictionnaire qui va nous permettre de stocker les informations de la partie.
        data = {
            "matrix": matrix
        }

        # On ouvre l'explorateur de fichier.
        file = asksaveasfile(mode="w", defaultextension=".json", filetypes=[("JSON", "*.json")],
                             initialfile=f"2048_{datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}",
                             title="Sauvegarder la partie")

        # On sauvegarde les informations de la partie.
        with open(file.name, "w") as f:
            json.dump(data, f)

    def load():
        """
        Charge une partie sauvegardée.
        :return: Matrix
        """

        # On ouvre l'explorateur de fichier.
        file = askopenfile(mode="r", defaultextension=".json", filetypes=[("JSON", "*.json")],
                           title="Charger une partie sauvegardée")

        # On charge les informations de la partie sauvegardée.
        with open(file.name, "r") as f:
            info = json.load(f)

        return info["matrix"]

    config = {
        "up": {"dx": -1, "dy": 0, "x_start": 1, "x_end": 4, "x_step": 1, "y_start": 0, "y_end": 4, "y_step": 1},
        "down": {"dx": 1, "dy": 0, "x_start": 2, "x_end": -1, "x_step": -1, "y_start": 0, "y_end": 4, "y_step": 1},
        "left": {"dx": 0, "dy": -1, "x_start": 0, "x_end": 4, "x_step": 1, "y_start": 1, "y_end": 4, "y_step": 1},
        "right": {"dx": 0, "dy": 1, "x_start": 0, "x_end": 4, "x_step": 1, "y_start": 2, "y_end": -1, "y_step": -1},
    }

    self = {
        "start": start,
        "move": move,
        "update_score": update_score,
        "save": save,
        "load": load
    }

    return self


def rgb_to_tkinter(rgb: tuple[int, int, int]):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    return f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'


# create a round rectangle
def round_rectangle(canvas: tkinter.Canvas, x1: int, y1: int, x2: int, y2: int, radius: int = 25, **kwargs):
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
                 anchor: str = "nw", ):
    self = {"canvas": canvas, "x": x, "y": y, "text": text, "color": color, "hover_color": hover_color,
            "hover_text_color": hover_text_color, "command": command, "hover": False, "padding": padding,
            "border_radius": border_radius, "font": font, "text_color": text_color, "anchor": anchor}

    def hover_on(self: dict):
        self["hover"] = True
        self["canvas"].itemconfig(self["text_canvas"], fill=rgb_to_tkinter(self["hover_text_color"]))
        self["canvas"].itemconfig(self["button"], fill=rgb_to_tkinter(self["hover_color"]))

    def hover_off(self: dict):
        self["hover"] = False
        self["canvas"].itemconfig(self["button"], fill=rgb_to_tkinter(self["color"]))
        self["canvas"].itemconfig(self["text_canvas"], fill=rgb_to_tkinter(self["text_color"]))

    def click(self: dict):
        if self["hover"]:
            self["command"]()

    def get_anchor_position(self: dict, x: int, y: int):
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

    def build(self: dict):
        if self["hover"]:
            color = self["hover_color"]
            text_color = self["hover_text_color"]
        else:
            color = self["color"]
            text_color = self["text_color"]
        self["button"] = round_rectangle(self["canvas"], self["x"], self["y"],
                                         self["x"] + self["text_size"][0] + self["padding"][0],
                                         self["y"] + self["text_size"][1] + self["padding"][1],
                                         radius=self["border_radius"], fill=rgb_to_tkinter(color))
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
        padding = size[0] - self["text_size"][0], size[1] - self["text_size"][1]
    self["size"] = self["text_size"][0] + padding[0], self["text_size"][1] + padding[1]
    self["x"], self["y"] = self["get_anchor_position"](self, self["x"], self["y"])
    self["build"](self)

    return self


def Menu(root: tkinter.Tk):
    self = {"frame": tkinter.Frame(root)}
    self["frame"].grid(row=0, column=0)
    self["canvas"] = tkinter.Canvas(self["frame"], width=root.winfo_width(), height=root.winfo_height())
    self["canvas"].pack()
    self["canvas"].create_text(root.winfo_width() // 2, 20, anchor="n", text="2048", font=tkinter.font.Font(size=100))
    BetterButton(self["canvas"], root.winfo_width() // 2, root.winfo_height() // 2, "Commencer", anchor="s",
                 size=(200, 50))


def main():
    # create the root
    root = tkinter.Tk()
    # set the title and the size
    root.title('2048')
    # update the root to get the size later
    root.update()
    root.state('zoomed')
    root.resizable(False, False)

    Menu(root)

    root.mainloop()


if __name__ == '__main__':
    main()
