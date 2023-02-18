import tkinter


# convert the rgb tuple to a tkinter color code
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
