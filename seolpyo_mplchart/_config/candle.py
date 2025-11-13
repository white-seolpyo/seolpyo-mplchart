

class CandleFaceColorData:
    def __init__(self):
        self.bull_rise: str|tuple[float, float, float, float] = '#FF2400'
        self.bull_fall: str|tuple[float, float, float, float] = 'w'
        self.bear_fall: str|tuple[float, float, float, float] = '#1E90FF'
        self.bear_rise: str|tuple[float, float, float, float] = 'w'

CANDLEFACECOLOR = CandleFaceColorData()

class CandleEdgeColorData:
    def __init__(self):
        self.bull_rise: str|tuple[float, float, float, float] = '#FF2400'
        self.bull_fall: str|tuple[float, float, float, float] = '#FF2400'
        self.bear_fall: str|tuple[float, float, float, float] = '#1E90FF'
        self.bear_rise: str|tuple[float, float, float, float] = '#1E90FF'
        self.doji: str|tuple[float, float, float, float] = 'k'

CANDLEEDGECOLOR = CandleEdgeColorData()

class CandleData:
    def __init__(self):
        self.half_width = 0.24
        self.linewidth = 0.8
        self.line_color: str|tuple[float, float, float, float] = 'k'
        self.FACECOLOR = CANDLEFACECOLOR
        self.EDGECOLOR = CANDLEEDGECOLOR

CANDLE = CandleData()

