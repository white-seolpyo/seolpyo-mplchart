from .chart import (
    PRICEFACECOLOR, PRICEEDGECOLOR, PRICE,
    MA,
    VOLUMEFACECOLOR, VOLUMEEDGECOLOR, VOLUME,

    Style as ChartStyle, STYLE as CHARTSTYLE,
)
from .slider import (
    NAVSTYLE,

    STYLE as SLIDERSTYLE
)
from .artist import (
    WATRERMARKSTYLE,

    CROSSLINE,
    BOX, BBOX,
    TEXT,

    STYLE as ARTISTSTYLE
)

class Style:
    def __init__(self):
        # chart
        self.CHART = CHARTSTYLE

        # slider
        self.SLIDER = SLIDERSTYLE

        # etc artists
        self.ARTIST = ARTISTSTYLE

STYLE = Style()

