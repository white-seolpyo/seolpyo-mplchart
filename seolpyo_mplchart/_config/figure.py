

class RatioData:
    def __init__(self):
        self.legend = 2
        self.price = 18
        self.volume = 5

RATIO = RatioData()

class WatermarkData:
    def __init__(self):
        self.alpha = 0.2
        self.color = 'k'
        self.fontsize = 20

WATERMARK = WatermarkData()

class AdjustData:
    def __init__(self):
        # 여백
        self.top = 0.95
        self.bottom = 0.05
        self.left = 0.01
        self.right = 0.93
        # 플롯간 간격
        self.wspace = 0
        self.hspace = 0

ADJUST = AdjustData()

class FigureData:
    def __init__(self):
        self.facecolor: str|tuple[float, float, float, float] = 'w'
        self.figsize = (14, 7)
        self.RATIO = RATIO
        self.ADJUST = ADJUST
        self.WATERMARK = WATERMARK

FIGURE = FigureData()

