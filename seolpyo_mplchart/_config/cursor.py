

class CrossLineData:
    def __init__(self):
        self.edgecolor = 'k'
        self.linewidth = 1
        self.linestyle = '-'

CROSSLINE = CrossLineData()

class BBoxData:
    def __init__(self):
        self.boxstyle = 'round'
        self.facecolor = 'w'
        self.edgecolor = 'k'

BBOX = BBoxData()

class Text:
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

