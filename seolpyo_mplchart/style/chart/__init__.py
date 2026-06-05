from .price import (
    PriceFaceColorData, PriceEdgeColorData, PriceData,
    PRICEFACECOLOR, PRICEEDGECOLOR, PRICE,
)
from .ma import MaData, MA
from .volume import (
    VolumeFaceColorData, VolumeEdgeColorData, VolumeData,
    VOLUMEFACECOLOR, VOLUMEEDGECOLOR, VOLUME,
)


class GridData:
    "https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.grid.html"
    "https://matplotlib.org/stable/gallery/lines_bars_and_markers/linestyles.html"
    def __init__(self):
        self.linewidth = 0.7
        self.color: str|tuple[float, float, float, float] = '#d0d0d0'
        self.linestyle = '-'
        self.axis = 'both'

GRID = GridData()


class Style:
    def __init__(self):
        self.facecolor: str|tuple[float, float, float, float] = '#fafafa'
        self.edgecolor: str|tuple[float, float, float, float] = 'k'
        self.fontcolor: str|tuple[float, float, float, float] = 'k'

        self.GRID = GRID

        self.PRICE = PRICE
        self.VOLUME = VOLUME
        self.MA = MA

STYLE = Style()

