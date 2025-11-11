import sys
from pathlib import Path
name_pkg = 'seolpyo_mplchart'
path_pkg = Path(__file__)
while path_pkg.name != name_pkg:
    path_pkg = path_pkg.parent
sys.path = [path_pkg.parent.__str__()] + sys.path

import json
import tkinter as tk
from tkinter import filedialog

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import seolpyo_mplchart as mc
from seolpyo_mplchart._utils.xl import xl_to_dataList


path_file = path_pkg / 'sample' / 'apple.txt'
with open(path_file, 'r', encoding='utf-8') as txt:
    data = json.load(txt)

df = pd.DataFrame(data[:])


def test():
    import seolpyo_mplchart as mc
    class C(mc.SliderChart):
        # fraction = True
        # watermark = 0
        theme = 'light'
        limit_wick = 2000
        # limit_ma = None
        # candle_on_ma = False
        # slider_top = False
        def on_click(self, e):
            super().on_click(e)
            # print(f'{e.button=}')
            # print(f'{e.button.__str__()=}')
            if e.button.__str__() == '3':
                # print('refresh')
                if self.theme == 'light':
                    self.theme = 'dark'
                    self.CONFIG = mc.set_theme(mc.SLIDERCONFIG_EN, theme=self.theme)
                    # self.CONFIG.FIGURE.RATIO.price = 18
                    # self.CONFIG.FIGURE.RATIO.volume = 4
                else:
                    self.theme = 'light'
                    self.CONFIG = mc.set_theme(mc.SLIDERCONFIG, theme=self.theme)
                    # self.CONFIG.FIGURE.RATIO.slider = 9
                    # self.CONFIG.FIGURE.RATIO.price = 9
                    # self.CONFIG.FIGURE.RATIO.volume = 9
                    self.CONFIG.UNIT.digit = 2
                self.refresh()
            return
        # def set_segments(self):
        #     super().set_segments()
        #     self.collection_candle.set_linewidth(1.3)
        #     return
        # def get_candle_segment(self, *, is_up, x, left, right, top, bottom, high, low):
        #     if is_up:
        #         return [
        #             (x, bottom),
        #             (x, low),
        #             (x, bottom),
        #             (left, bottom),
        #             (x, bottom),
        #             (x, top),
        #             (right, top),
        #             (x, top),
        #             (x, high),
        #         ]
        #     else:
        #         return [
        #             (x, bottom),
        #             (x, low),
        #             (x, bottom),
        #             (right, bottom),
        #             (x, bottom),
        #             (x, top),
        #             (left, top),
        #             (x, top),
        #             (x, high),
        #         ]
    c = C()
    c.key_date = '기준일'
    c.key_open = '시가'
    c.key_high = '고가'
    c.key_low = '저가'
    c.key_close = '종가'
    c.key_volume = '거래량'
    # c.volume = None
    c.set_data(df)
    
    plt.show()
    return


class TkChart:
    chart = None

    def __init__(self, window: tk.Tk):
        window.wm_title('seolpyo tk chart')
        self.window = window
        # self.window.option_add('맑은고딕 14')  # 모든 위젯 기본 폰트 크기 설정
        window.protocol('WM_DELETE_WINDOW', lambda *_: (mc.close('all'), window.destroy()))

        self.add_entry()
        return

    def open_file(self):
        path_file = filedialog.askopenfilename(
            title="Select a file",
            filetypes=(("Xlsx Files", "*.xlsx"), ("All Files", "*.*"),)
        )
        # print(f'{path_file=}')
        if path_file:
            self.filname.config(state="normal")   # 잠깐 풀고
            self.filname.delete(0, tk.END)
            self.filname.insert(0, path_file)
            self.filname.config(state="readonly") # 다시 잠금
            
            if not self.chart:
                self.add_chart()
            self.set_chart(path_file)
            return path_file
        return

    def add_entry(self):
        frame = tk.Frame(self.window)
        frame.grid(column=0, row=0, sticky='w', padx=10, pady=10)

        btn = tk.Button(frame, text='파일 열기', command=lambda *_: self.open_file())
        btn.grid(column=0, row=0)

        self.filname = tk.Entry(frame, state='readonly', width=100)
        self.filname.grid(column=1, row=0, padx=10)
        return

    def add_chart(self):
        self.chart = mc.SliderChart()
        self.chart.key_date = '기준일'
        self.chart.key_open = '시가'
        self.chart.key_high = '고가'
        self.chart.key_low = '저가'
        self.chart.key_close = '종가'
        self.chart.key_volume = '거래량'

        frame = tk.Frame(self.window)
        frame.grid(column=0, row=1, sticky='ewsn')
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(1, weight=1)

        self.agg = FigureCanvasTkAgg(self.chart.figure, frame)
        widget = self.agg.get_tk_widget()
        widget.grid(column=0, row=0, sticky='ewsn')
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

        return

    def set_chart(self, path_file):
        data = xl_to_dataList(path_file)
        print(f'{len(data)=:,}')
        df = pd.DataFrame(data)
        self.chart.set_data(df)
        return


def run():
    root = tk.Tk()
    _ = TkChart(root)
    root.mainloop()
    return


def test_tk():
    run()
    return


if __name__ == '__main__':
    # test()
    test_tk()

