import sys
from pathlib import Path
name_pkg = 'seolpyo_mplchart'
path_pkg = Path(__file__)
while path_pkg.name != name_pkg:
    path_pkg = path_pkg.parent
sys.path = [path_pkg.parent.__str__()] + sys.path

import json

import pandas as pd
import matplotlib.pyplot as plt


path_file = path_pkg / 'sample' / 'samsung.txt'
with open(path_file, 'r', encoding='utf-8') as txt:
    data = json.load(txt)
df = pd.DataFrame(data[:100])

def test_base():
    from seolpyo_mplchart._chart._base import Base
    Base()
    plt.show()
    return

def test_draw():
    from seolpyo_mplchart._chart._draw import Chart
    c = Chart()
    # c.CONFIG.CANDLE.FACECOLOR.bull_fall = 'y'
    # c.CONFIG.CANDLE.EDGECOLOR.bull_fall = 'k'
    # c.CONFIG.CANDLE.FACECOLOR.bear_rise = 'k'
    # c.CONFIG.CANDLE.EDGECOLOR.bear_rise = 'pink'
    # c.CONFIG.VOLUME.EDGECOLOR.rise = 'k'
    # c.CONFIG.AX.facecolor = 'k'
    # c.CONFIG.AX.TICK.edgecolor = 'yellow'
    # c.CONFIG.AX.TICK.fontcolor = 'pink'
    # c.set_color()
    # c.volume = None
    c.set_data(df)
    plt.show()
    return


def test_cursor():
    from seolpyo_mplchart._chart._cursor._info import Chart
    from seolpyo_mplchart._config import DEFAULTCONFIG_EN
    c = Chart()
    # c.CONFIG = DEFAULTCONFIG_EN
    c.refresh()
    c.fraction = True
    c.set_data(df)
    plt.show()
    return

def test_slider():
    from seolpyo_mplchart._chart._slider import Chart
    c = Chart()
    c.set_data(df)
    plt.show()
    return


if __name__ == '__main__':
    # test_base()
    # test_draw()
    # test_cursor()
    test_slider()


import seolpyo_mplchart as mc


# class Chart(mc.SliderChart):
#     format_candleinfo = mc.format_candleinfo_ko + '\nCustom info: {ci}'
#     format_volumeinfo = mc.format_volumeinfo_ko
#     min_distance = 2

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.collection_candle.set_linewidth(1.5)
#         return

#     def get_info_kwargs(self, is_price, **kwargs):
#         if is_price:
#             kwargs['ci'] = 'You can add Custom text Info or Change text info.'
#             kwargs['close'] = 'You can Change close price info.'
#         return kwargs

#     def get_candle_segment(self, *, x, left, right, top, bottom, is_up, high, low):
#         if is_up:
#             return (
#                 (x, top), (right, top), (x, top),
#                 (x, high),
#                 (x, low),
#                 (x, bottom), (left, bottom), (x, bottom),
#             )
#         else:
#             return (
#                 (x, bottom), (right, bottom), (x, bottom),
#                 (x, high),
#                 (x, low),
#                 (x, top), (left, top), (x, top),
#             )



# C = Chart()
# path_file = Path(__file__).parent / 'sample/samsung.txt'
# # C.format_candleinfo = mc.format_candleinfo_ko
# # C.format_volumeinfo = mc.format_volumeinfo_ko
# # C.volume = None


# with open(path_file, 'r', encoding='utf-8') as txt:
#     data = json.load(txt)
# df = pd.DataFrame(data[:100])

# C.set_data(df)

# mc.show()
# mc.close()