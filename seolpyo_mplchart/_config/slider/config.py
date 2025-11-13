from .. import config
from .figure import FIGURE, SliderFigureData
from .nav import NAV


class SliderData:
    def __init__(self):
        self.NAV = NAV

SLIDER = SliderData()

class SliderConfigData(config.ConfigData):
    FIGURE: SliderFigureData
    SLIDER: SliderData


SLIDERCONFIG: SliderConfigData = config.DEFAULTCONFIG
SLIDERCONFIG.FIGURE = FIGURE
SLIDERCONFIG.SLIDER = SLIDER

SLIDERCONFIG_EN: SliderConfigData = config.DEFAULTCONFIG_EN
SLIDERCONFIG_EN.FIGURE = FIGURE
SLIDERCONFIG_EN.SLIDER = SLIDER

