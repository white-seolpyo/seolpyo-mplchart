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
from seolpyo_mplchart.utils.xl import xl_to_dataList


path_file = path_pkg / 'sample' / 'apple.txt'
# path_file = path_pkg / 'sample' / 'samsung.txt'
with open(path_file, 'r', encoding='utf-8') as txt:
    data = json.load(txt)

df = pd.DataFrame(data[:])


# mc.STYLE.CHART.MA.linewidth = 5

class Chart(mc.Chart):
    watermark = 'Apple'
    # fraction = True
    # watermark = 0
    theme = 'light'
    limit_candle = 100
    limit_wick = 500
    # limit_ma = None
    # candle_on_ma = False
    # slider_top = False
    get_price_line_segment = mc.Chart.get_price_hl_line_segment

    def on_click(self, e):
        super().on_click(e)
        # print(f'{e.button=}')
        # print(f'{e.button.__str__()=}')
        if e.button.__str__() == '2':
            # wheel click
            # slider show/hide
            self.show_slider = (not self.show_slider)
            # volume chart show/hide
            if self.key_volume:
                self.key_volume = None
            else:
                self.key_volume = '거래량'
            self.refresh()

        if e.button.__str__() == '3':
            # right click
            # print('refresh')
            if self.theme == 'light':
                # change theme
                self.theme = 'dark'
                self.STYLE = mc.set_theme(mc.STYLE, theme=self.theme)
                # label, info text digit
                self.digit_price = 2
                # set slider bottom
                self.slider_top = False
                # use fraction in info text
                self.fraction = True

                # use english formatter
                self.FORMATTER = mc.FORMATTER_EN
                # change price info foramt
                self.price_info_format = mc.format_info_price_en
                # change volume info foramt
                self.volume_info_format = mc.format_info_volume_en
                # change ma format (legend)
                self.ma_format = 'ma {}'
                # change price element (bar)
                self.get_candle_segment = lambda _=None: mc.Chart.get_bar_segment(self)
                # change ax ratio
                self.get_ax_config_list = lambda _=None: [
                    {
                        'name': 'slider',
                        'is_px': True,
                        'size': 100,
                    },
                    {
                        'name': 'none',
                        'is_px': True,
                        'size': 40,
                    },
                    {
                        'name': 'legend',
                        'is_px': True,
                        'size': 60,
                    },
                    {
                        'name': 'price',
                        'is_px': False,
                        'size': 1,
                    },
                    {
                        'name': 'volume',
                        'is_px': False,
                        'size': 2,
                    },
                ]
            else:
                # 테마 변경
                self.theme = 'light'
                self.STYLE = mc.set_theme(mc.STYLE, theme=self.theme)
                # 정보, 라벨에 표시되는 가격 소수점 최대 자릿수
                self.digit_price = 0
                # 슬라이더를 위에 배치
                self.slider_top = True
                # 분수 표시 off
                self.fraction = False

                # 한글 포매터 사용
                self.FORMATTER = mc.FORMATTER
                # 가격 차트 정보 텍스트 포맷
                self.price_info_format = mc.format_info_price
                # 거래량 차트 정보 텍스트 포맷
                self.volume_info_format = mc.format_info_volume
                # 이평선 포맷 (legend)
                self.ma_format = '{}일선'
                # 가격 차트에서 캔들 차트를 사용
                self.get_candle_segment = lambda _=None: mc.Chart.get_candle_segment(self)
                # 차트 비율 변경
                self.get_ax_config_list = lambda _=None: mc.Chart.get_ax_config_list(self)
            self.refresh()
        return

def test():
    c = Chart()
    print('init')
    c.key_date = '기준일'
    c.key_open = '시가'
    c.key_high = '고가'
    c.key_low = '저가'
    c.key_close = '종가'
    c.key_volume = '거래량'
    # c.volume = None
    c.set_data(df)
    print('set data')
    
    plt.show()
    return


class TkChart:
    chart = None

    def __init__(self, window: tk.Tk):
        window.wm_title('seolpyo tk chart')
        self.window = window
        # self.window.option_add('맑은고딕 14')  # 모든 위젯 기본 폰트 크기 설정
        window.protocol('WM_DELETE_WINDOW', lambda *_: (mc.Chart.close('all'), window.destroy()))

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
        self.chart = Chart()
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
        # print(f'{len(data)=:,}')
        self.chart.watermark = path_file.split('/')[-1].split('.')[0]
        self.chart.watermark += f' ({len(data):,} ticks)'
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

