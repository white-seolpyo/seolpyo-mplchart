import json
from typing import Literal
from pathlib import Path

from ._chart import OnlyChart, CursorChart, SliderChart
from ._config import (
    ConfigData, DEFAULTCONFIG, DEFAULTCONFIG_EN,
    SliderConfigData, SLIDERCONFIG, SLIDERCONFIG_EN,
)
from ._utils import (
    float_to_str,
    xl_to_dataList,
    convert_num,
    float_to_str,
    convert_unit, convert_unit_en,
    data_unit_ko, data_unit_en,
    list_to_DataFrame,
    show, close,
    switch_backend,
)


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
    df = list_to_DataFrame(data)

    CHART.set_data(df)

    show(Close=True)
    return

