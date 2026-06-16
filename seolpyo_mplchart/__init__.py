from matplotlib.collections import LineCollection
import matplotlib.pyplot as plt
import matplotlib.style as mplstyle
import pandas as pd

from .utils.num import num_to_str, num_to_str_en, unit_data, unit_data_en
from .utils.formatter import Formatter, FormatterEN, FORMATTER, FORMATTER_EN
from .utils.theme import set_theme
from .utils.mpl import show, close, switch_backend
from .utils.df import list_to_DataFrame

from .canvas import CanvasMixin
from .artist import ArtistMixin
from .segment import SegmentMixin
from .legend import LegendMixin
from .draw import DrawMixin
from .data import DataMixin
from .axis import AxisMixn
from .event import EventMixn, format_info_price, format_info_volume, format_info_price_en, format_info_volume_en
from .style import Style, STYLE


try:
    plt.switch_backend('TkAgg')
except:
    pass

# 한글 깨짐 문제 방지
try:
    plt.rcParams['font.family'] ='Malgun Gothic'
except:
    pass

# 기본 툴바 비활성화
plt.rcParams['toolbar'] = 'None'
mplstyle.use('fast')


class Base(CanvasMixin, ArtistMixin, SegmentMixin, LegendMixin):
    pass

class Chart(
    Base,

    EventMixn,
    AxisMixn,
    DataMixin,
    DrawMixin,
):
    """
    Quick Start:
        import seolpyo_mplchart as mc
        chart = mc.Chart()
        chart.set_data(df) # df.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
        chart.show()

        
    # Document
    English: https://github.com/white-seolpyo/seolpyo-mplchart/tree/main

    한글: https://white.seolpyo.com/entry/147/?from=pkg
    """
    STYLE: Style
    FORMATTER: Formatter

    df: pd.DataFrame = None

    key_date = 'date'
    key_open, key_high, key_low, key_close = ('open', 'high', 'low', 'close')
    key_volume = 'volume'

    candle_on_ma = True
    fraction = False

    digit_price = 0
    digit_volume = 0

    format_info_price = format_info_price
    format_info_volume = format_info_volume

    ma_format = '{}일선'
    ma_list = [5, 20, 50, 120, 240,]

    show_slider = True
    slider_top = True

    watermark = 'seolpyo mplchart'

    limit_candle = 400
    limit_wick = 2_000
    limit_volume = 200
    limit_ma = 8_000

    min_distance = 3

    def __init__(self, STYLE=STYLE, FORMATTER=FORMATTER):
        self.STYLE = STYLE
        self.FORMATTER = FORMATTER
        super().__init__()
        return

    def refresh(self, change_xlim=False):
        self.set_canvas()

        self._set_length_text()

        self.set_segment()
        self.set_legend()

        for position in ['top', 'bottom']:
            collection: LineCollection = getattr(self, f'collection_slider_{position}')
            collection.set_segments(self.segment_slider)
            collection.set_edgecolor(self.slider_edgecolors)
            collection.set_linewidth(self.slider_linewidths)

        self.set_artist()

        self.axis_slider()

        if change_xlim:
            xlim = self.get_default_xlim()
        else:
            x0, x1 = self.get_ax_price().get_xlim()
            xlim = (int(x0), int(x1)-1)
        self.axis(*xlim)

        self.figure.canvas.draw()
        return

    def _set_length_text(self):
        func = lambda x: len(self.FORMATTER.info_price_formatter(round(x, self.digit_price), None))
        self._length_text = self.df['high'].apply(func).max()

        if self.key_volume:
            func = lambda x: len(self.FORMATTER.info_volume_formatter(round(x, self.digit_volume), None))
            lenth_volume = self.df['volume'].apply(func).max()
            # print(f'{self._length_text=}')
            # print(f'{lenth_volume=}')
            if self._length_text < lenth_volume:
                self._length_text = lenth_volume
        return

    def get_default_xlim(self):
        """
        get_default_xlim.

        space = int(self.ind_end / 20)

        Returns:
            (int, int): (-space, self.ind_end+space)
        """
        ind_end = int(self.df.index[-1]) + 1
        return (ind_end-120, ind_end+20)
        space = int(ind_end / 20)
        # print(f'{space=}')
        xmin = -space
        xmax = ind_end + space
        return (xmin, xmax)

    def show(self, *args, **kwargs):
        "call matplotlib.pyplot.show(*args, **kwargs)"
        show(*args, **kwargs)
        return

    def switch_backend(self, backend='TkAgg'):
        "call matplotlib.pyplot.switch_backend(newbackend)"
        return switch_backend(backend)

    def close(self, fig='all'):
        "call matplotlib.pyplot.close(fig)"
        return close(fig)

