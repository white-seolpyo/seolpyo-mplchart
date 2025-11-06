import json
from typing import Literal
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from ._chart import OnlyChart, CursorChart, SliderChart
from ._config import DEFAULTCONFIG, DEFAULTCONFIG_EN, SLIDERCONFIG, SLIDERCONFIG_EN, ConfigData, SliderConfigData


# __all__ = [
#     'path_samsung', 'path_apple',
#     'format_candleinfo_ko', 'format_volumeinfo_ko',
#     'format_candleinfo_en', 'format_volumeinfo_en',
#     'sample', 'switch_backend', 'show', 'close',
#     'OnlyChart', 'CursorChart', 'SliderChart',
#     'set_theme',
# ]


pkg_name = 'seolpyo_mplchart'
path_pkg = Path(__file__)
while path_pkg.name != pkg_name:
    path_pkg = path_pkg.parent
path_samsung = path_pkg / 'sample' / 'samsung.txt'
path_apple = path_pkg / 'sample' / 'apple.txt'

def sample(stock: Literal['samsung', 'apple']='samsung', chart: Literal['Chart', 'CursorChart', 'SliderChart']='SliderChart'):
    d = {
        'Chart': OnlyChart,
        'CursorChart': CursorChart,
        'SliderChart': SliderChart,
    }
    C = d[chart]
    path_file = path_samsung if stock == 'samsung' else path_apple
    if stock == 'samsung':
        if chart == 'SliderChart':
            config = SLIDERCONFIG
        else:
            config = DEFAULTCONFIG
    else:
        if chart == 'SliderChart':
            config = SLIDERCONFIG_EN
        else:
            config = DEFAULTCONFIG_EN

    CHART: SliderChart = C(config)

    with open(path_file, 'r', encoding='utf-8') as txt:
        data = json.load(txt)
    df = pd.DataFrame(data)

    CHART.set_data(df)

    show()
    close()
    return


def switch_backend(newbackend='TkAgg'):
    "call matplotlib.pyplot.switch_backend(newbackend)"
    return plt.switch_backend(newbackend)


def close(fig='all'):
    "call matplotlib.pyplot.close(fig)"
    return plt.close(fig)

def show(Close=True):
    """
    call matplotlib.pyplot.show()
    ```if Close``` if True, run matplotlib.pyplot.close('all') after window closee.
    """
    plt.show()
    if Close:
        close()
    return


def set_theme(config: ConfigData|SliderConfigData, theme: Literal['light', 'dark']='dark'):
    if theme == 'light':
        # axes
        config.FIGURE.facecolor = '#fafafa'
        config.AX.facecolor = '#fafafa'
        config.AX.TICK.edgecolor = 'k'
        config.AX.TICK.fontcolor = 'k'
        config.AX.GRID.color = '#d0d0d0'

        # candle
        config.CANDLE.line_color = 'k'
        config.CANDLE.FACECOLOR.bull_rise = '#FF2400'
        config.CANDLE.FACECOLOR.bull_fall = 'w'
        config.CANDLE.FACECOLOR.bear_fall = '#1E90FF'
        config.CANDLE.FACECOLOR.bear_rise = 'w'

        config.CANDLE.EDGECOLOR.bull_rise = '#FF2400'
        config.CANDLE.EDGECOLOR.bull_fall = '#FF2400'
        config.CANDLE.EDGECOLOR.bear_fall = '#1E90FF'
        config.CANDLE.EDGECOLOR.bear_rise = '#1E90FF'
        config.CANDLE.EDGECOLOR.doji = 'k'

        # volume
        config.VOLUME.FACECOLOR.rise = '#F27663'
        config.VOLUME.FACECOLOR.fall = '#70B5F2'
        config.VOLUME.FACECOLOR.doji = '#BEBEBE'

        config.VOLUME.EDGECOLOR.rise = '#F27663'
        config.VOLUME.EDGECOLOR.fall = '#70B5F2'
        config.VOLUME.EDGECOLOR.doji = '#BEBEBE'

        # ma
        config.MA.color_default = 'k'
        config.MA.color_list = ['#8B00FF', '#008000', '#A0522D', '#008B8B', '#FF0080']
        # text
        config.CURSOR.TEXT.BBOX.facecolor = 'w'
        config.CURSOR.TEXT.BBOX.edgecolor = 'k'
        config.CURSOR.TEXT.color = 'k'

        # box
        config.CURSOR.BOX.edgecolor = 'k'

        # line
        config.CURSOR.CROSSLINE.edgecolor = 'k'

        # wartermark
        config.FIGURE.WATERMARK.color = 'k'

        if getattr(config, 'SLIDER', None):
            config.SLIDER.NAVIGATOR.edgecolor = '#2962FF'
            config.SLIDER.NAVIGATOR.facecolor = '#0000002E'
    elif theme == 'dark':
        # axes
        config.FIGURE.facecolor = '#0f0f0f'
        config.AX.facecolor = '#0f0f0f'
        config.AX.TICK.edgecolor = '#dbdbdb'
        config.AX.TICK.fontcolor = '#dbdbdb'
        config.AX.GRID.color = '#1c1c1c'

        # candle
        config.CANDLE.line_color = 'w'
        config.CANDLE.FACECOLOR.bull_rise = '#089981'
        config.CANDLE.FACECOLOR.bull_fall = '#0f0f0f'
        config.CANDLE.FACECOLOR.bear_fall = '#f23645'
        config.CANDLE.FACECOLOR.bear_rise = '#0f0f0f'

        config.CANDLE.EDGECOLOR.bull_rise = '#089981'
        config.CANDLE.EDGECOLOR.bull_fall = '#089981'
        config.CANDLE.EDGECOLOR.bear_fall = '#f23645'
        config.CANDLE.EDGECOLOR.bear_rise = '#f23645'
        config.CANDLE.EDGECOLOR.doji = 'w'

        # volume
        config.VOLUME.FACECOLOR.rise = '#2A8076'
        config.VOLUME.FACECOLOR.fall = '#BE4F58'
        config.VOLUME.FACECOLOR.doji = '#82828A'

        config.VOLUME.EDGECOLOR.rise = '#2A8076'
        config.VOLUME.EDGECOLOR.fall = '#BE4F58'
        config.VOLUME.EDGECOLOR.doji = '#82828A'

        # ma
        config.MA.color_default = 'w'
        config.MA.color_list = ['#FFB300', '#03A9F4', '#AB47BC', '#8BC34A', '#EF5350']

        # text
        config.CURSOR.TEXT.BBOX.facecolor = '#3d3d3d'
        config.CURSOR.TEXT.BBOX.edgecolor = '#ffffff'
        config.CURSOR.TEXT.color = '#ffffff'

        # box
        config.CURSOR.BOX.edgecolor = 'w'

        # line
        config.CURSOR.CROSSLINE.edgecolor = '#9c9c9c'

        # wartermark
        config.FIGURE.WATERMARK.color = 'w'

        if getattr(config, 'SLIDER', None):
            config.SLIDER.NAVIGATOR.edgecolor = "#00A6FF"
            config.SLIDER.NAVIGATOR.facecolor = '#FFFFFF4D'

    return config

