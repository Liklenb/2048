# create a tkinter button class prettier than the default one
# it's only a rectangle with a text inside and a hover color
import tkinter
import tkinter.font
from widgets import tools


class Button:
    def __init__(self,
                 canvas: tkinter.Canvas,
                 x: int,
                 y: int,
                 text: str,
                 text_color: tuple[int, int, int] = (0, 0, 0),
                 color: tuple[int, int, int] = (255, 255, 255),
                 hover_color: tuple[int, int, int] = (200, 200, 200),
                 hover_text_color: tuple[int, int, int] = (0, 0, 0),
                 command=None,
                 padding: tuple[int, int] = (50, 20),
                 border_radius: int = 50,
                 font: tkinter.font.Font = None,
                 anchor: str = "nw"):

        self._canvas = canvas
        self._x = x
        self._y = y
        self._text = text
        self._color = color
        self._hover_color = hover_color
        self._hover_text_color = hover_text_color
        self._command = command
        self._hover = False
        self._padding = padding
        self._border_radius = border_radius
        self._font = font
        self._text_color = text_color
        self._anchor = anchor
        # get the text size
        if not font:
            self._font = tkinter.font.Font(family="TkDefaultFont")
        self.text_size = self._font.measure(self._text), self._font.metrics("linespace")

        self.size = self.text_size[0] + padding[0], self.text_size[1] + padding[1]
        self._x, self._y = self._get_anchor_position(self._x, self._y)
        self._build()

    def _hover_on(self):
        self._hover = True
        self._canvas.itemconfig(self.button, fill=tools.rgb_to_tkinter(self._hover_color))
        self._canvas.itemconfig(self.text_canvas, fill=tools.rgb_to_tkinter(self._hover_text_color))

    def _hover_off(self):
        self._hover = False
        self._canvas.itemconfig(self.button, fill=tools.rgb_to_tkinter(self._color))
        self._canvas.itemconfig(self.text_canvas, fill=tools.rgb_to_tkinter(self._text_color))

    def _click(self):
        if self._hover:
            self._command()

    # convert the coordinates to the anchor position and update
    def move(self, x: int, y: int):
        self._x, self._y = self._get_anchor_position(x, y)
        self._hover = False
        self.update()

    # setter for all the attributes
    def config_button(self,
                      text: str = None,
                      text_color: tuple[int, int, int] = None,
                      color: tuple[int, int, int] = None,
                      hover_color: tuple[int, int, int] = None,
                      hover_text_color: tuple[int, int, int] = None,
                      command=None,
                      padding: tuple[int, int] = None,
                      border_radius: int = None,
                      font: tkinter.font.Font = None,
                      anchor: str = None):
        if color:
            self._color = color
        if hover_color:
            self._hover_color = hover_color
        if hover_text_color:
            self._hover_text_color = hover_text_color
        if padding:
            self._padding = padding
        if border_radius:
            self._border_radius = border_radius
        if font:
            self._font = font
        if text_color:
            self._text_color = text_color
        if anchor:
            self._anchor = anchor
            self._x, self._y = self._get_anchor_position(self._x, self._y)
        if text:
            self._text = text
            self.text_size = self._font.measure(self._text), self._font.metrics("linespace")
            self.size = self.text_size[0] + self._padding[0], self.text_size[1] + self._padding[1]
        if command:
            self._command = command
        self.update()

    # delete the old button and text and create a new one
    def update(self):
        self._canvas.delete(self.button)
        self._canvas.delete(self.text_canvas)
        self._build()

    # create the button, the text and bind the mouse events
    def _build(self):
        if self._hover:
            color = self._hover_color
            text_color = self._hover_text_color
        else:
            color = self._color
            text_color = self._text_color
        self.button = tools.round_rectangle(self._canvas, self._x, self._y,
                                            self._x + self.text_size[0] + self._padding[0],
                                            self._y + self.text_size[1] + self._padding[1],
                                            radius=self._border_radius, fill=tools.rgb_to_tkinter(color))
        self.text_canvas = self._canvas.create_text(self._x + (self._padding[0] + self.text_size[0]) / 2,
                                                    self._y + self._padding[1] / 2,
                                                    text=self._text,
                                                    anchor="n", fill=tools.rgb_to_tkinter(text_color),
                                                    font=self._font)

        # bind the mouse events
        self._canvas.tag_bind(self.button, "<Enter>", lambda e: self._hover_on())
        self._canvas.tag_bind(self.button, "<Leave>", lambda e: self._hover_off())
        self._canvas.tag_bind(self.button, "<Button-1>", lambda e: self._click())
        # bind the mouse events for the text
        self._canvas.tag_bind(self.text_canvas, "<Enter>", lambda e: self._hover_on())
        self._canvas.tag_bind(self.text_canvas, "<Leave>", lambda e: self._hover_off())
        self._canvas.tag_bind(self.text_canvas, "<Button-1>", lambda e: self._click())

    # convert the coordinates to the anchor
    def _get_anchor_position(self, x, y):
        if self._anchor == "center":
            x -= self.size[0] / 2
            y -= self.size[1] / 2
        elif self._anchor == "ne":
            x -= self.size[0]
        elif self._anchor == "se":
            x -= self.size[0]
            y -= self.size[1]
        elif self._anchor == "sw":
            y -= self.size[1]
        elif self._anchor == "e":
            x -= self.size[0]
            y -= self.size[1] / 2
        elif self._anchor == "w":
            y -= self.size[1] / 2
        elif self._anchor == "n":
            x -= self.size[0] / 2
        elif self._anchor == "s":
            x -= self.size[0] / 2
            y -= self.size[1]
        return x, y
