

class RatioData:
    def __init__(self):
        self.price = 5
        self.volume = 5

RATIO = RatioData()

class WatermarkData:
    def __init__(self):
        self.alpha = 0.2
        self.color = 'k'
        self.fontsize = 20

WATERMARK = WatermarkData()

class AdjustData:
    "https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.subplots_adjust.html"
    def __init__(self):
        # 여백
        self.top = 0.98
        self.bottom = 0.05
        self.left = 0.01
        self.right = 0.93
        # 플롯간 간격
        self.wspace = 0
        self.hspace = 0

ADJUST = AdjustData()

class FigureData:
    def __init__(self):
        self.facecolor: str|tuple[float, float, float, float] = '#fafafa'
        self.figsize = (14, 7)
        self.RATIO = RATIO
        self.ADJUST = ADJUST
        self.WATERMARK = WATERMARK

FIGURE = FigureData()

