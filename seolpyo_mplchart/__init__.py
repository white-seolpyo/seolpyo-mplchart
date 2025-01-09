"""
This software includes Matplotlib, which is licensed under the BSD License.
Matplotlib Copyright (c) 2012- Matplotlib Development Team.
Full license can be found in the LICENSE file or at https://matplotlib.org/stable/users/license.html
"""


import json
from pathlib import Path
from typing import Literal

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import pandas as pd


from .slider import Chart as CM


__all__ = [
    'pd',
    'plt',

    'Chart',

    'sample',
    'show',
    'close',
]


class Chart(CM):
    r"""
    You can see the guidance document:
        Korean: https://white.seolpyo.com/entry/147/
        English: https://white.seolpyo.com/entry/148/

    Variables:
        unit_price, unit_volume: unit for price and volume. default ('원', '주').

        figsize: figure size if you use plt.show(). default (12, 6).
        ratio_ax_slider, ratio_ax_legend, ratio_ax_price, ratio_ax_volume: Axes ratio. default (3, 2, 18, 5).
        adjust: figure adjust. default dict(top=0.95, bottom=0.05, left=0.01, right=0.93, wspace=0, hspace=0).
        slider_top: ax_slider is located at the top or bottom. default True.
        color_background: color of background. default '#fafafa'.
        color_grid: color of grid. default '#d0d0d0'.

        df: stock data.
        date: date column key. default 'date'
        Open, high, low, close: price column key. default ('open', 'high', 'low', 'close')
        volume: volume column key. default 'volume'

        label_ma: moving average legend label format. default '{}일선'
        list_ma: Decide how many days to draw the moving average line. default (5, 20, 60, 120, 240)
        list_macolor: Color the moving average line. If the number of colors is greater than the moving average line, black is applied. default ('darkred', 'fuchsia', 'olive', 'orange', 'navy', 'darkmagenta', 'limegreen', 'darkcyan',)

        candle_on_ma: Decide whether to draw candles on the moving average line. default True
        color_sliderline: Color of closing price line in ax_slider. default 'k'
        color_navigatorline: Color of left and right dividing lines in selected area. default '#1e78ff'
        color_navigator: Color of unselected area. default 'k'

        color_up: The color of the candle. When the closing price is greater than the opening price. default '#fe3032'
        color_down: The color of the candle. When the opening price is greater than the opening price. default '#0095ff'
        color_flat: The color of the candle. WWhen the closing price is the same as the opening price. default 'k'
        color_up_down: The color of the candle. If the closing price is greater than the opening price, but is lower than the previous day's closing price. default 'w'
        color_down_up: The color of the candle. If the opening price is greater than the closing price, but is higher than the closing price of the previous day. default 'w'
        colors_volume: The color of the volume bar. default '#1f77b4'

        lineKwargs: Options applied to horizontal and vertical lines drawn along the mouse position. default dict(edgecolor='k', linewidth=1, linestyle='-')
        textboxKwargs: Options that apply to the information text box. dufault dict(boxstyle='round', facecolor='w')

        fraction: Decide whether to express information as a fraction. default False
        candleformat: Candle information text format. default '{dt}\n\n종가:　 {close}\n등락률: {rate}\n대비:　 {compare}\n시가:　 {open}({rate_open})\n고가:　 {high}({rate_high})\n저가:　 {low}({rate_low})\n거래량: {volume}({rate_volume})'
        volumeformat: Volume information text format. default '{dt}\n\n거래량　　　: {volume}\n거래량증가율: {rate_volume}'
        digit_price, digit_volume: Number of decimal places expressed in informational text. default (0, 0)

        min_distance: Minimum number of candles that can be selected with the slider. default 30
        simpler: Decide whether to display candles simply when moving the chart. default False
        limit_volume: Maximum number of volume bars drawn when moving the chart. default 2_000
    """
    pass


_name = {'samsung', 'apple'}
def sample(name: Literal['samsung', 'apple']='samsung'):
    if name not in _name:
        print('name should be either samsung or apple.')
        return
    file = Path(__file__).parent / f'data/{name}.txt'
    with open(file, 'r', encoding='utf-8') as txt:
        data = json.load(txt)
    data = data
    df = pd.DataFrame(data)

    c = Chart()
    if name == 'apple':
        c.unit_price = '$'
        c.unit_volume = ' vol'
        c.digit_price = 3
        c.label_ma = 'ma{}'
        c.candleformat = '{}\n\nend:     {}\nrate:    {}\ncompare: {}\nopen:    {}({})\nhigh:    {}({})\nlow:     {}({})\nvolume:  {}({})'
        c.volumeformat = '{}\n\nvolume:      {}\nvolume rate: {}'
    c.set_data(df)
    show()
    close()
    return


def show():
    return plt.show()


def close(fig: int|str|Figure|None='all'):
    return plt.close(fig)


if __name__ == '__main__':
    sample('apple')


