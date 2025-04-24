import json
from typing import Literal
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from ._draw import Chart as _BaseChart
from ._cursor import Chart as _BaseCursorChart, format_candleinfo_ko, format_volumeinfo_ko, format_candleinfo_en, format_volumeinfo_en
from ._slider import Chart as _BaseSliderChart


__all__ = [
    'path_samsung', 'path_apple',
    'format_candleinfo_ko', 'format_volumeinfo_ko',
    'format_candleinfo_en', 'format_volumeinfo_en',
    'sample', 'switch_backend', 'show', 'close',
    'OnlyChart', 'CursorChart', 'SliderChart',
    'set_theme',
]


path_samsung = Path(__file__).parent / 'sample/samsung.txt'
path_apple = Path(__file__).parent / 'sample/apple.txt'

def sample(stock: Literal['samsung', 'apple']='samsung', chart: Literal['Chart', 'CursorChart', 'SliderChart']='SliderChart'):
    C: _BaseSliderChart = {'Chart': _BaseChart, 'CursorChart': _BaseCursorChart, 'SliderChart': _BaseSliderChart}[chart]()
    path_file = path_samsung if stock == 'samsung' else path_apple
    if stock == 'samsung':
        C.format_candleinfo = format_candleinfo_ko
        C.format_volumeinfo = format_volumeinfo_ko
    else:
        C.format_candleinfo = format_candleinfo_en
        C.format_volumeinfo = format_volumeinfo_en
        C.unit_price = '$'
        C.unit_volume = 'Vol'
        C.digit_price = 3
        C.format_ma = 'ma{}'

    with open(path_file, 'r', encoding='utf-8') as txt:
        data = json.load(txt)
    df = pd.DataFrame(data)

    C.set_data(df)

    show()
    close()
    return


def switch_backend(newbackend='TkAgg'):
    "call matplotlib.pyplot.switch_backend(newbackend)"
    return plt.switch_backend(newbackend)


def show(Close=False):
    """
    call matplotlib.pyplot.show()
    ```if Close``` if True, run matplotlib.pyplot.close('all') after window closee.
    """
    plt.show()
    if Close: close()
    return


def close(fig='all'):
    "call matplotlib.pyplot.close(fig)"
    return plt.close(fig)


class OnlyChart(_BaseChart):
    r"""
    You can see the guidance document:
        Korean: https://white.seolpyo.com/entry/147/
        English: https://white.seolpyo.com/entry/148/

    Quick Start:
        ```
        import seolpyo_mplchart as mc
        chart = mc.SliderChart() # Create instance
        chart.set_data(df) # set stock price data
        mc.show() # show chart(run ```matplotlib.pyplot.show()```)
        mc.close() # run ```matplotlib.pyplot.close('close')```
        ```

    Class Variables:
        watermark: watermark text.

        figsize: Default size when creating a matplotlib window
        ratio_ax_legend, ratio_ax_price, ratio_ax_volume: Axes ratio
        adjust: figure adjust. default ```dict(top=0.95, bottom=0.05, left=0.01, right=0.93, wspace=0, hspace=0)```.
        color_background: color of background. default '#fafafa'.
        gridKwargs: kwargs applied to the grid
        color_tick, color_tick_label: Tick and tick label colors. default ('k', 'k').

        df: stock data DataFrame.
        date: date column key. default 'date'
        Open, high, low, close: price column key. default ('open', 'high', 'low', 'close')
        volume: volume column key. default 'volume'. If ```if self.volume``` is ```False```, the volume chart is not drawn.

        format_ma: moving average legend label format. default '{}일선'
        list_ma: Decide how many days to draw the moving average line. default (5, 20, 60, 120, 240)
        list_macolor: Color the moving average line. If the number of colors is greater than the moving average line, black is applied

        candle_on_ma: Decide whether to draw candles on the moving average line. default ```True```
        color_navigator_line: Color of left and right dividing lines in selected area
        color_navigator_cover: Color of unselected area.

        color_priceline: The color of the price line

        color_up: The color of the candle. When the closing price is greater than the opening price
        color_down: The color of the candle. When the opening price is greater than the opening price
        color_flat: The color of the candle. When the closing price is the same as the opening price
        color_up_down: The color of the candle. If the closing price is greater than the opening price, but is lower than the previous day's closing price
        color_down_up: The color of the candle. If the opening price is greater than the closing price, but is higher than the closing price of the previous day
        colors_volume: The color of the volume bar. default '#1f77b4'

        color_volume_up: The color of the volume. When the closing price is greater than the opening price
        color_volume_down: The color of the volume. When the opening price is greater than the opening price
        color_volume_flatt: The color of the volume. When the closing price is the same as the opening price

        candle_width_half, volume_width_half: half of the thickness of the candle and volume

        color_box: The color of the candlebox and volumebox. Used when the mouse is over a candle or volume bar. default 'k'

        limit_candle: Maximum number of candles to draw. default 800
        limit_wick:  Maximum number of candle wicks to draw. default 4,000
    """
    pass


class CursorChart(_BaseCursorChart):
    r"""
    You can see the guidance document:
        Korean: https://white.seolpyo.com/entry/147/
        English: https://white.seolpyo.com/entry/148/

    Quick Start:
        ```
        import seolpyo_mplchart as mc
        chart = mc.SliderChart() # Create instance
        chart.set_data(df) # set stock price data
        mc.show() # show chart(run ```matplotlib.pyplot.show()```)
        mc.close() # run ```matplotlib.pyplot.close('close')```
        ```

    Class Variables:
        watermark: watermark text.

        unit_price, unit_volume: price and volume unit. default ('원', '주').
        digit_price, digit_volume: display decimal places when displaying price and volume. default (0, 0),

        figsize: Default size when creating a matplotlib window
        ratio_ax_legend, ratio_ax_price, ratio_ax_volume: Axes ratio
        adjust: figure adjust. default ```dict(top=0.95, bottom=0.05, left=0.01, right=0.93, wspace=0, hspace=0)```.
        color_background: color of background. default '#fafafa'.
        gridKwargs: kwargs applied to the grid
        color_tick, color_tick_label: Tick and tick label colors. default ('k', 'k').

        df: stock data DataFrame.
        date: date column key. default 'date'
        Open, high, low, close: price column key. default ('open', 'high', 'low', 'close')
        volume: volume column key. default 'volume'. If ```if self.volume``` is ```False```, the volume chart is not drawn.

        format_ma: moving average legend label format. default '{}일선'
        list_ma: Decide how many days to draw the moving average line. default (5, 20, 60, 120, 240)
        list_macolor: Color the moving average line. If the number of colors is greater than the moving average line, black is applied

        candle_on_ma: Decide whether to draw candles on the moving average line. default ```True```
        color_navigator_line: Color of left and right dividing lines in selected area
        color_navigator_cover: Color of unselected area.

        color_priceline: The color of the price line

        color_up: The color of the candle. When the closing price is greater than the opening price
        color_down: The color of the candle. When the opening price is greater than the opening price
        color_flat: The color of the candle. When the closing price is the same as the opening price
        color_up_down: The color of the candle. If the closing price is greater than the opening price, but is lower than the previous day's closing price
        color_down_up: The color of the candle. If the opening price is greater than the closing price, but is higher than the closing price of the previous day
        colors_volume: The color of the volume bar. default '#1f77b4'

        color_volume_up: The color of the volume. When the closing price is greater than the opening price
        color_volume_down: The color of the volume. When the opening price is greater than the opening price
        color_volume_flatt: The color of the volume. When the closing price is the same as the opening price

        candle_width_half, volume_width_half: half of the thickness of the candle and volume

        color_box: The color of the candlebox and volumebox. Used when the mouse is over a candle or volume bar. default 'k'

        lineKwargs: kwarg applied to lines drawn based on mouse cursor position
        textboxKwargs: kwarg applied to the info text bbox drawn on the chart. When this is applied, the following occurs: ```textKwargs['bbox'] = textboxKwargs```
        textKwargs: A kwarg that applies to the informational text drawn on the chart. When this is applied, the following occurs: ```textKwargs['bbox'] = textboxKwargs```

        fraction: Decide whether to express information as a fraction. default False
        format_candleinfo: Candle information text format. default '{dt}\n\n종가:　 {close}\n등락률: {rate}\n대비:　 {compare}\n시가:　 {open}({rate_open})\n고가:　 {high}({rate_high})\n저가:　 {low}({rate_low})\n거래량: {volume}({rate_volume})'
        format_volumeinfo: Volume information text format. default '{dt}\n\n거래량:　　　 {volume}\n거래량증가율: {rate_volume}\n대비:　　　　 {compare}'

        limit_candle: Maximum number of candles to draw. default 800
        limit_wick:  Maximum number of candle wicks to draw. default 4,000
    """
    pass


class SliderChart(_BaseSliderChart):
    r"""
    You can see the guidance document:
        Korean: https://white.seolpyo.com/entry/147/
        English: https://white.seolpyo.com/entry/148/

    Quick Start:
        ```
        import seolpyo_mplchart as mc
        chart = mc.SliderChart() # Create instance
        chart.set_data(df) # set stock price data
        mc.show() # show chart(run ```matplotlib.pyplot.show()```)
        mc.close() # run ```matplotlib.pyplot.close('close')```
        ```

    Class Variables:
        watermark: watermark text.

        unit_price, unit_volume: price and volume unit. default ('원', '주').
        digit_price, digit_volume: display decimal places when displaying price and volume. default (0, 0),

        figsize: Default size when creating a matplotlib window
        slider_top: ax_slider is located at the top or bottom. default ```True```.
        ratio_ax_slider, ratio_ax_legend, ratio_ax_price, ratio_ax_volume: Axes ratio
        ratio_ax_none: Ratio between volume chart and slider. Used only when ```self.slider_top``` is ```False```
        adjust: figure adjust. default ```dict(top=0.95, bottom=0.05, left=0.01, right=0.93, wspace=0, hspace=0)```.
        color_background: color of background. default '#fafafa'.
        gridKwargs: kwargs applied to the grid
        color_tick, color_tick_label: Tick and tick label colors. default ('k', 'k').

        df: stock data DataFrame.
        date: date column key. default 'date'
        Open, high, low, close: price column key. default ('open', 'high', 'low', 'close')
        volume: volume column key. default 'volume'. If ```if self.volume``` is ```False```, the volume chart is not drawn.

        format_ma: moving average legend label format. default '{}일선'
        list_ma: Decide how many days to draw the moving average line. default (5, 20, 60, 120, 240)
        list_macolor: Color the moving average line. If the number of colors is greater than the moving average line, black is applied

        candle_on_ma: Decide whether to draw candles on the moving average line. default ```True```
        color_navigator_line: Color of left and right dividing lines in selected area
        color_navigator_cover: Color of unselected area.

        color_priceline: The color of the price line

        color_up: The color of the candle. When the closing price is greater than the opening price
        color_down: The color of the candle. When the opening price is greater than the opening price
        color_flat: The color of the candle. When the closing price is the same as the opening price
        color_up_down: The color of the candle. If the closing price is greater than the opening price, but is lower than the previous day's closing price
        color_down_up: The color of the candle. If the opening price is greater than the closing price, but is higher than the closing price of the previous day
        colors_volume: The color of the volume bar. default '#1f77b4'

        color_volume_up: The color of the volume. When the closing price is greater than the opening price
        color_volume_down: The color of the volume. When the opening price is greater than the opening price
        color_volume_flatt: The color of the volume. When the closing price is the same as the opening price

        candle_width_half, volume_width_half: half of the thickness of the candle and volume

        color_box: The color of the candlebox and volumebox. Used when the mouse is over a candle or volume bar. default 'k'

        lineKwargs: kwarg applied to lines drawn based on mouse cursor position
        textboxKwargs: kwarg applied to the info text bbox drawn on the chart. When this is applied, the following occurs: ```textKwargs['bbox'] = textboxKwargs```
        textKwargs: A kwarg that applies to the informational text drawn on the chart. When this is applied, the following occurs: ```textKwargs['bbox'] = textboxKwargs```

        fraction: Decide whether to express information as a fraction. default False
        format_candleinfo: Candle information text format. default '{dt}\n\n종가:　 {close}\n등락률: {rate}\n대비:　 {compare}\n시가:　 {open}({rate_open})\n고가:　 {high}({rate_high})\n저가:　 {low}({rate_low})\n거래량: {volume}({rate_volume})'
        format_volumeinfo: Volume information text format. default '{dt}\n\n거래량:　　　 {volume}\n거래량증가율: {rate_volume}\n대비:　　　　 {compare}'

        min_distance: Minimum number of candles that can be selected with the slider. default 30
        limit_candle: Maximum number of candles to draw. default 800
        limit_wick:  Maximum number of candle wicks to draw. default 4,000
        limit_volume: Maximum number of volume bars to draw. default 200. Applies only to drawing candle wicks or price line.
        limit_ma: If the number of displayed data is more than this, the price moving average line is not drawn. default 8,000

        color_navigator_line: Navigator divider color. default '#1e78ff'
        color_navigator_cover: Unselected slider area color. default = 'k'
    """
    pass


def set_theme(chart: SliderChart|CursorChart|OnlyChart, theme: Literal['light', 'dark']='dark'):
    initialized = hasattr(chart, 'ax_price')

    if theme == 'dark':
        chart.color_background = '#000000'
        chart.color_tick, chart.color_tick_label = ('w', 'w')
        chart.gridKwargs = {'color': '#FFFFFF'}

        chart.color_priceline = 'w'
        chart.color_up, chart.color_down = ('#00FF00', '#FF0000')
        chart.color_flat = 'w'
        chart.color_up_down, chart.color_down_up = ('#000000', '#000000')

        chart.color_volume_up, chart.color_volume_down = ('#32CD32', '#FF4500')
        chart.color_volume_flat = 'w'

        chart.list_macolor = ('#1E90FF', '#FFA500', '#FF1493', '#FFFF00', '#00CED1')

        chart.lineKwargs = {'edgecolor': 'w'}
        chart.color_box = 'w'
        chart.textboxKwargs = {'facecolor': 'k', 'edgecolor': 'w'}
        chart.textKwargs = {'color': 'w'}
        chart.color_navigator_cover, chart.color_navigator_line = ('k', '#FF2400')

        if initialized:
            chart.change_background_color('k')
            chart.change_tick_color('w')
            chart.change_line_color('w')
            if hasattr(chart, 'navigator'): chart.collection_navigator.set_edgecolor([chart.color_navigator_cover, chart.color_navigator_line])

            if hasattr(chart, 'df'):
                chart.set_data(chart.df, sort_df=False, calc_ma=False, set_candlecolor=True, set_volumecolor=True, calc_info=False, change_lim=False)
                chart.draw_canvas()
    elif theme == 'light':
        chart.color_background = '#fafafa'
        chart.color_tick, chart.color_tick_label = ('k', 'k')
        chart.gridKwargs = {'color': '#d0d0d0'}

        chart.color_priceline = 'k'
        chart.color_up, chart.color_down = ('#FF2400', '#1E90FF')
        chart.color_flat = 'k'
        chart.color_up_down, chart.color_down_up = ('w', 'w')

        chart.color_volume_up, chart.color_volume_down = ('#FF6666', '#5CA8F4')
        chart.color_volume_flat = '#808080'

        chart.list_macolor = ('#006400', '#8B008B', '#FFA500', '#0000FF', '#FF0000')

        chart.lineKwargs = {'edgecolor': 'k'}
        chart.color_box = 'k'
        chart.textboxKwargs = {'facecolor': 'w', 'edgecolor': 'k'}
        chart.textKwargs = {'color': 'k'}
        chart.color_navigator_cover, chart.color_navigator_line = ('k', '#1E78FF')

        if initialized:
            chart.change_background_color('#fafafa')
            chart.change_tick_color('k')
            chart.change_line_color('k')
            if hasattr(chart, 'navigator'): chart.collection_navigator.set_edgecolor([chart.color_navigator_cover, chart.color_navigator_line])

            if hasattr(chart, 'df'):
                chart.set_data(chart.df, sort_df=False, calc_ma=False, set_candlecolor=True, set_volumecolor=True, calc_info=False, change_lim=False)
                chart.draw_canvas()
    else: raise ValueError(f'You send wrong arg.\n{theme=}')

    return chart
