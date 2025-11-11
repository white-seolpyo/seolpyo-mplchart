from .nums import convert_unit, convert_unit_en


class UnitData:
    def __init__(self):
        self.price = '원'
        self.volume = '주'
        self.digit = 0
        self.digit_volume = 0
        self.func = convert_unit

UNIT = UnitData()

UNIT_EN = UnitData()
UNIT_EN.price = ' $'
UNIT_EN.volume = ' Vol'
UNIT_EN.digit = 2
UNIT_EN.func = convert_unit_en

