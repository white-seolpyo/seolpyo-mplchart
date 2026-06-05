from .watermark import (
    Style as WaterMarkStyle,
    STYLE as WATRERMARKSTYLE,
)
from .crossline import CrossLineData, CROSSLINE
from .text import (
    BBoxData,
    BBOX,

    TextData, TEXT,
)
from .box import Box, BOX


class Style:
    def __init__(self):
        self.WATERMARK = WATRERMARKSTYLE
        self.CROSSLINE = CROSSLINE
        self.TEXT = TEXT
        self.BOX = BOX

STYLE = Style()

