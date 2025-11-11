

class Grid:
    "https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.grid.html"
    def __init__(self):
        self.visible = True
        self.linewidth = 0.7
        self.color: str|tuple[float, float, float, float] = '#d0d0d0'
        self.linestyle = '-'
        self.dashes = (1, 0)
        self.axis = 'both'

GRID = Grid()

class TickData:
    "https://matplotlib.org/stable/api/ticker_api.html"
    def __init__(self):
        self.edgecolor: str|tuple[float, float, float, float] = 'k'
        self.fontcolor: str|tuple[float, float, float, float] = 'k'

TICK = TickData()

class AxData:
    def __init__(self):
        self.facecolor: str|tuple[float, float, float, float] = '#fafafa'
        self.GRID = GRID
        self.TICK = TICK

AX = AxData()

