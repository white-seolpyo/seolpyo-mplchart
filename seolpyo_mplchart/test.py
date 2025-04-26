import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, Path(__file__).parent.parent.__str__())
# print(f'{sys.path=}')

import seolpyo_mplchart as mc


class Chart(mc.SliderChart):
    format_candleinfo = mc.format_candleinfo_ko + '\nCustom info: {ci}'
    format_volumeinfo = mc.format_volumeinfo_ko
    min_distance = 5

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.collection_candle.set_linewidth(1.5)
        return

    def get_info_kwargs(self, is_price, **kwargs):
        if is_price:
            kwargs['ci'] = 'You can add Custom text Info or Change text info.'
            kwargs['close'] = 'You can Change close price info.'
        return kwargs

    def get_candle_segment(self, *, x, left, right, top, bottom, is_up, high, low):
        if is_up:
            return (
                (x, high),
                (x, top),
                (right, top),
                (x, top),
                (x, bottom),
                (left, bottom),
                (x, bottom),
                (x, low),
                (x, high)
            )
        else:
            return (
                (x, high),
                (x, bottom),
                (right, bottom),
                (x, bottom),
                (x, top),
                (left, top),
                (x, top),
                (x, low),
                (x, high)
            )



C = Chart()
path_file = Path(__file__).parent / 'sample/samsung.txt'
# C.format_candleinfo = mc.format_candleinfo_ko
# C.format_volumeinfo = mc.format_volumeinfo_ko
# C.volume = None


with open(path_file, 'r', encoding='utf-8') as txt:
    data = json.load(txt)
df = pd.DataFrame(data[:20])

C.set_data(df)

mc.show()
mc.close()