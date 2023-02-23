import tkinter.font
# On importe randint et random du package random, qui vont nous permettre de choisir aléatoirement une tuile vide.
from random import randint, random


def Grid():
    """
    Fonction regroupant toutes les fonctions invisibles à la grille de jeu.
    """

    def start(grid: list):
        """
        Génère deux tuiles de valeur 2 ou 4 aléatoirement sur la grille.
        :param: grid: list
        :return: grid
        """

        # On génère deux tuiles aléatoirement.
        for i in range(2):
            self["generate_new_tile"](grid)

        return grid

    def new_game():
        """
        Crée une nouvelle grille de jeu et lance la partie.
        :return: grid
        """

        # On crée une grille vierge.
        grid = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        # On appelle la fonction start pour générer deux tuiles aléatoires.
        self["start"](grid)
        return grid

    def generate_new_tile(grid: list):
        """
        Génère une nouvelle tuile de valeur 2 ou 4 aléatoirement sur la grille.
        :param grid: list
        :return: grid
        """

        # On récupère les positions vides de la grille et on les stocke dans une liste.
        pos = []
        for x in range(4):
            for y in range(4):
                if grid[x][y] == 0:
                    pos.append((x, y))

        # On choisit aléatoirement une position vide et on génère une tuile de valeur 2 ou 4.
        if pos:
            x, y = pos[randint(0, len(pos) - 1)]
            if random() < 0.9:
                grid[x][y] = 2
            else:
                grid[x][y] = 4

        return grid

    def is_win(grid: list):
        for ligne in grid:
            for elem in ligne:
                if elem == 2048:
                    return True
        return False

    def move_up(grid: list):
        """"
        Déplace les tuiles vers le haut.
        :param grid: list
        :return: mouvement, fusion, grid
        """

        # On crée trois dictionnaires vides qui vont nous permettre de stocker les mouvements, les fusions et les cases
        # ayant déjà fusionné.
        mouvement, fusion, hasfusion = {}, {}, {}

        # On parcourt la grille de haut en bas, de gauche à droite.
        for x in range(1, 4):
            for y in range(4):

                # Si la case actuelle n'est pas vide.
                if grid[x][y] != 0:

                    # On définit la variable prev_x, qui est la case au-dessus de la case actuelle.
                    prev_x = x - 1

                    # Tant que la case au-dessus est vide, on continue de monter.
                    while prev_x >= 0 and grid[prev_x][y] == 0:
                        prev_x -= 1

                    # Si la case au-dessus est égale à la case actuelle et qu'elle n'a pas déjà fusionné, on fusionne
                    # les deux cases, on supprime la case actuelle, on ajoute la case fusionnée à la liste des cases
                    # fusionnées.
                    if prev_x >= 0 and grid[prev_x][y] == grid[x][y] and (prev_x, y) not in hasfusion:
                        grid[prev_x][y] *= 2
                        grid[x][y] = 0
                        fusion[(x, y), (prev_x, y)] = (prev_x, y)
                        hasfusion[(prev_x, y)] = True

                    # Sinon, on déplace la case actuelle vers la première case vide au-dessus.
                    else:
                        if prev_x != x - 1:
                            grid[prev_x + 1][y] = grid[x][y]
                            grid[x][y] = 0
                            mouvement[(x, y)] = (prev_x + 1, y)

        # Si une fusion ou un mouvement a eu lieu, on génère une nouvelle tuile.
        if fusion or mouvement != {}:
            self["generate_new_tile"](grid)

        return [mouvement, fusion, grid]

    def move_down(grid: list):
        """
        Déplace les tuiles vers le bas.
        :param grid: list
        :return: mouvement, fusion, grid
        """

        mouvement, fusion, hasfusion = {}, {}, {}

        # On parcourt la grille de bas en haut, de gauche à droite (l'inverse de move_up).
        for x in range(2, -1, -1):
            for y in range(4):
                if grid[x][y] != 0:

                    prev_x = x + 1
                    while prev_x <= 3 and grid[prev_x][y] == 0:
                        prev_x += 1

                    if prev_x <= 3 and grid[prev_x][y] == grid[x][y] and (prev_x, y) not in hasfusion:
                        grid[prev_x][y] *= 2
                        grid[x][y] = 0
                        fusion[(x, y), (prev_x, y)] = (prev_x, y)
                        hasfusion[(prev_x, y)] = True
                    else:
                        if prev_x != x + 1:
                            grid[prev_x - 1][y] = grid[x][y]
                            grid[x][y] = 0
                            mouvement[(x, y)] = (prev_x - 1, y)

        if fusion or mouvement != {}:
            self["generate_new_tile"](grid)

        return [mouvement, fusion, grid]

    def move_left(grid: list):
        """
        Déplace les tuiles vers la gauche.
        :param grid: list
        :return: mouvement, fusion, grid
        """

        mouvement, fusion, hasfusion = {}, {}, {}

        # On parcourt la grille de gauche à droite, de haut en bas.
        for x in range(4):
            for y in range(1, 4):
                if grid[x][y] != 0:

                    prev_y = y - 1
                    while prev_y >= 0 and grid[x][prev_y] == 0:
                        prev_y -= 1

                    if prev_y >= 0 and grid[x][prev_y] == grid[x][y] and (x, prev_y) not in hasfusion:
                        grid[x][prev_y] *= 2
                        grid[x][y] = 0
                        fusion[(x, y), (x, prev_y)] = (x, prev_y)
                        hasfusion[(x, prev_y)] = True
                    else:
                        if prev_y != y - 1:
                            grid[x][prev_y + 1] = grid[x][y]
                            grid[x][y] = 0
                            mouvement[(x, y)] = (x, prev_y + 1)

        if fusion or mouvement != {}:
            self["generate_new_tile"](grid)

        return [mouvement, fusion, grid]

    def move_right(grid: list):
        mouvement, fusion, hasfusion = {}, {}, {}

        # On parcourt la grille de droite à gauche, de haut en bas.
        for x in range(4):
            for y in range(2, -1, -1):
                if grid[x][y] != 0:

                    prev_y = y + 1
                    while prev_y <= 3 and grid[x][prev_y] == 0:
                        prev_y += 1

                    if prev_y <= 3 and grid[x][prev_y] == grid[x][y] and (x, prev_y) not in hasfusion:
                        grid[x][prev_y] *= 2
                        grid[x][y] = 0
                        fusion[(x, y), (x, prev_y)] = (x, prev_y)
                        hasfusion[(x, prev_y)] = True
                    else:
                        if prev_y != y + 1:
                            grid[x][prev_y - 1] = grid[x][y]
                            grid[x][y] = 0
                            mouvement[(x, y)] = (x, prev_y - 1)

        if fusion or mouvement != {}:
            self["generate_new_tile"](grid)

        return [mouvement, fusion, grid]

    self = {
        "start": start,
        "new_game": new_game,
        "generate_new_tile": generate_new_tile,
        "is_win": is_win,
        "move_up": move_up,
        "move_down": move_down,
        "move_left": move_left,
        "move_right": move_right
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
                 padding=(200, 50))


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
