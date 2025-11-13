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
from seolpyo_mplchart._chart.base import Chart


path_file = path_pkg / 'sample' / 'samsung.txt'
with open(path_file, 'r', encoding='utf-8') as txt:
    data = json.load(txt)
df = pd.DataFrame(data[:])


class C(Chart):
    # limit_wick = 200
    t = 'light'
    # watermark = ''
    def __init__(self):
        super().__init__()
        self.figure.canvas.mpl_connect('button_press_event', lambda x: self.theme(x))
    
    def theme(self, e):
        btn = getattr(e, 'button')
        # print(f'{str(btn)=}')
        if str(btn) == '3':
            # print('refresh')
            if self.t == 'light':
                self.t = 'dark'
            else:
                self.t = 'light'
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


