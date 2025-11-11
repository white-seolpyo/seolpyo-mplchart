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
from seolpyo_mplchart._chart.cursor import Chart
from seolpyo_mplchart._config import DEFAULTCONFIG, DEFAULTCONFIG_EN

path_file = path_pkg / 'sample' / 'samsung.txt'
with open(path_file, 'r', encoding='utf-8') as txt:
    data = json.load(txt)
df = pd.DataFrame(data[:300])


class C(Chart):
    # limit_candle = 200
    # limit_wick = 200
    t = 'light'
    # watermark = ''
    def __init__(self):
        super().__init__()
        self.figure.canvas.mpl_connect('button_press_event', lambda x: self.theme(x))
        self.CONFIG.FORMAT.candle += '\nCustom: {custom}'

    def get_info_kwargs(self, is_price, **kwargs):
        kwargs = super().get_info_kwargs(is_price, **kwargs)
        kwargs['close'] = 'Cusotom close value'
        kwargs['custom'] = 'this is custom add info kwargs'
        return kwargs

    def theme(self, e):
        btn = getattr(e, 'button')
        # print(f'{str(btn)=}')
        if str(btn) == '3':
            # print('refresh')
            if self.t == 'light':
                self.t = 'dark'
                self.CONFIG = set_theme(DEFAULTCONFIG_EN, theme=self.t)
            else:
                self.t = 'light'
                self.CONFIG = set_theme(DEFAULTCONFIG, theme=self.t)
            # print(f'{self.t=}')
            # self.CONFIG.MA.ma_list = []
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


