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

from seolpyo_mplchart._utils.theme import set_theme
from seolpyo_mplchart._config import SLIDERCONFIG
from seolpyo_mplchart._chart.slider import Chart


path_file = path_pkg / 'sample' / 'samsung.txt'
with open(path_file, 'r', encoding='utf-8') as txt:
    data = json.load(txt)
df = pd.DataFrame(data[:800])


class C(Chart):
    limit_candle = 100
    limit_wick = 300
    limit_volume = 10
    limit_ma = 200
    t = 'light'
    # watermark = ''
    def __init__(self):
        super().__init__()
        # super().__init__(config=set_theme(SLIDERCONFIG, theme='dark'))
        self.figure.canvas.mpl_connect('button_press_event', lambda x: self.theme(x))

    def theme(self, e):
        btn = getattr(e, 'button')
        # print(f'{str(btn)=}')
        if str(btn) == '3':
            # print('refresh')
            if self.t == 'light':
                self.slider_top = True
                self.t = 'dark'
                # self.CONFIG.MA.linewidth = 1
                self.get_candle_segment = lambda **x: Chart.get_candle_segment(self, **x)
                self.CONFIG.CANDLE.linewidth = 0.8
            else:
                self.slider_top = False
                self.t = 'light'
                # self.CONFIG.MA.linewidth = 3
                self.get_candle_segment = self.get_bar_segment
                self.CONFIG.CANDLE.linewidth = 1.3
            # print(f'{self.t=}')
            self.CONFIG = set_theme(self.CONFIG, theme=self.t)
            self.refresh()
        return


def run():
    chart = C()
    chart.set_data(df)
    plt.show()
    plt.close()
    return


if __name__ == '__main__':
    run()


