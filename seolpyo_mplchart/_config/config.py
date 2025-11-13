from . import figure, ax, candle, volume, ma, unit, cursor, format


class ConfigData:
    def __init__(self):
        self.FIGURE = figure.FIGURE
        self.UNIT = unit.UNIT
        self.AX = ax.AX
        self.CANDLE = candle.CANDLE
        self.VOLUME = volume.VOLUME
        self.MA = ma.MA
        self.CURSOR = cursor.CURSOR
        self.FORMAT = format.FORMAT

DEFAULTCONFIG = ConfigData()

DEFAULTCONFIG_EN = ConfigData()
DEFAULTCONFIG_EN.UNIT = unit.UNIT_EN
DEFAULTCONFIG_EN.MA = ma.MA_EN
DEFAULTCONFIG_EN.FORMAT = format.FORMAT_EN

