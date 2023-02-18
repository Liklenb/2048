from foreground import menu, example
import tkinter


class Controller:
    def __init__(self, root: tkinter.Tk):
        self.root = root
        self.example = example.Example(self)

        # end with the top frame
        self.menu = menu.Menu(self)
