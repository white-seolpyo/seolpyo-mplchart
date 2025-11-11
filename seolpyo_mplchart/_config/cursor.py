

class CrossLineData:
    "https://matplotlib.org/stable/gallery/lines_bars_and_markers/linestyles.html"
    def __init__(self):
        self.edgecolor = 'k'
        self.linewidth = 1
        self.linestyle = '-'

CROSSLINE = CrossLineData()

class BBoxData:
    "https://matplotlib.org/stable/api/_as_gen/matplotlib.patches.FancyBboxPatch.html#matplotlib.patches.FancyBboxPatch"
    def __init__(self):
        self.boxstyle = 'round'
        self.facecolor = 'w'
        self.edgecolor = 'k'

BBOX = BBoxData()

class Text:
    "https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.text.html"
    def __init__(self):
        self.color = 'k'
        self.BBOX = BBOX

    def to_dict(self):
        data = {}
        for k, v in self.__dict__.items():
            if k == 'BBOX':
                k = k.lower()
                v = self.BBOX.__dict__
            data[k] = v
        return data

TEXT = Text()

class Box:
    "https://matplotlib.org/stable/gallery/lines_bars_and_markers/linestyles.html"
    def __init__(self):
        self.edgecolor = 'k'
        self.linewidth = 1.2

BOX = Box()

class Cursor:
    def __init__(self):
        self.CROSSLINE = CROSSLINE
        self.TEXT = TEXT
        self.BOX = BOX

CURSOR = Cursor()

