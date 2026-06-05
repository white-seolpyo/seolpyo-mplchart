

class PriceFaceColorData:
    def __init__(self):
        self.up_rise: str|tuple[float, float, float, float] = '#FF2400'
        self.up_fall: str|tuple[float, float, float, float] = 'w'
        self.down_fall: str|tuple[float, float, float, float] = '#1E90FF'
        self.down_rise: str|tuple[float, float, float, float] = 'w'

PRICEFACECOLOR = PriceFaceColorData()


class PriceEdgeColorData:
    def __init__(self):
        self.up_rise: str|tuple[float, float, float, float] = '#FF2400'
        self.up_fall: str|tuple[float, float, float, float] = '#FF2400'
        self.down_fall: str|tuple[float, float, float, float] = '#1E90FF'
        self.down_rise: str|tuple[float, float, float, float] = '#1E90FF'
        self.flat: str|tuple[float, float, float, float] = 'k'

PRICEEDGECOLOR = PriceEdgeColorData()


class PriceData:
    def __init__(self):
        self.half_width = 0.24
        self.linewidth = 0.8
        self.line_color: str|tuple[float, float, float, float] = 'k'
        self.FACECOLOR = PRICEFACECOLOR
        self.EDGECOLOR = PRICEEDGECOLOR

PRICE = PriceData()

