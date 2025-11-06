from .. import figure


class RatioData:
    def __init__(self):
        self.legend = 2
        self.price = 18
        self.volume = 5
        self.slider = 3
        self.none = 2

RATIO = RatioData()

class SliderFigureData(figure.FigureData):
    def __init__(self):
        super().__init__()
        self.RATIO: RatioData = RATIO

FIGURE = SliderFigureData()

