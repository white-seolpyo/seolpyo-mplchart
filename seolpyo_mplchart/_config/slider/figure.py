from .. import figure


class RatioData:
    def __init__(self):
        self.price = 9
        self.volume = 3
        self.none = 2
        self.slider = 1.5

RATIO = RatioData()

class SliderFigureData(figure.FigureData):
    def __init__(self):
        super().__init__()
        self.RATIO: RatioData = RATIO

FIGURE = SliderFigureData()

