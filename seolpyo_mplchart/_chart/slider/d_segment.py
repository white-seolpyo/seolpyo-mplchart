from matplotlib.axes import Axes
from matplotlib.backend_bases import MouseEvent
from matplotlib.collections import LineCollection
from matplotlib.text import Text
import pandas as pd
import numpy as np

from ..._config import SliderConfigData


class Base:
    CONFIG: SliderConfigData
    df: pd.DataFrame

    ax_slider: Axes
    collection_slider: LineCollection
    collection_nav: LineCollection
    collection_slider_vline: LineCollection
    artist_text_slider: Text

    set_segments: callable
    set_color_segments: callable

    slider_ymin: float
    slider_ymax: float

    slider_xmin: float
    slider_xmax: float
    _nav_width: float


class SliderMixin(Base):
    def _set_slider_collection(self):
        keys = []
        for i in reversed(self.CONFIG.MA.ma_list):
            keys.append('x')
            keys.append(f'ma{i}')

        series = self.df[keys + ['x', 'close']]
        series['x'] = series['x'] - 0.5
        segment_slider = series.values
        sizes = [segment_slider.shape[0], len(self.CONFIG.MA.ma_list)+1, 2]
        segment_slider = segment_slider.reshape(*sizes).swapaxes(0, 1)
        self.collection_slider.set_segments(segment_slider)

        linewidth = []
        ma_colors = []
        for n, _ in enumerate(self.CONFIG.MA.ma_list):
            linewidth.append(0.9)
            try:
                ma_colors.append(self.CONFIG.MA.color_list[n])
            except:
                ma_colors.append(self.CONFIG.MA.color_default)

        self.collection_slider.set_edgecolor(ma_colors + [self.CONFIG.CANDLE.line_color])

        self.collection_slider.set_linewidth(linewidth + [2.4])
        self.collection_slider.set_edgecolor(ma_colors + [self.CONFIG.CANDLE.line_color])
        return

    def _set_slider_color_collection(self):
        ma_colors = []
        for n, _ in enumerate(self.CONFIG.MA.ma_list):
            try:
                ma_colors.append(self.CONFIG.MA.color_list[n])
            except:
                ma_colors.append(self.CONFIG.MA.color_default)

        self.collection_slider.set_edgecolor(ma_colors + [self.CONFIG.CANDLE.line_color])
        return


class VlineMixin(Base):
    in_slider: bool

    def _set_slider_vline(self, e: MouseEvent):
        xdata = e.xdata
        if xdata is None:
            return
        xdata = round(xdata, 2)
        # print(f'{xdata=}')
        if not self.in_slider:
            xdata -= 0.5
        
        seg = [((xdata, self.slider_ymin), (xdata, self.slider_ymax))]
        # print(f'{seg=}')
        self.collection_slider_vline.set_segments(seg)
        return

    def _set_slider_text(self, e: MouseEvent):
        xdata = e.xdata
        if xdata is None:
            return
        idx = round(xdata)
        if idx < 0:
            return

        try:
            text = self.df.iloc[idx]['date']
        except:
            return

        self.artist_text_slider.set_text(text)
        self.artist_text_slider.set_x(round(xdata, 2))
        return 1


class NavMixin(Base):
    segment_nav: np.ndarray

    def _set_nav_segment(self, xmin, xmax):
        xmin0 = xmin - self._nav_width
        xmin1 = xmin
        xmax0 = xmax
        xmax1 = xmax + self._nav_width
        seg = [
            # 좌측 오버레이
            (
                (self.slider_xmin, self.slider_ymax),
                (xmin0, self.slider_ymax),
                (xmin0, self.slider_ymin),
                (self.slider_xmin, self.slider_ymin),
            ),
            # 우측 오버레이
            (
                (xmax1, self.slider_ymax),
                (self.slider_xmax, self.slider_ymax),
                (self.slider_xmax, self.slider_ymin),
                (xmax1, self.slider_ymin),
            ),
            # 좌측 네비게이터
            (
                (xmin1, self.slider_ymax),
                (xmin1, self.slider_ymin),
                (xmin0, self.slider_ymin),
                (xmin0, self.slider_ymax),
            ),
            # 우측 네비게이터
            (
                (xmax0, self.slider_ymin),
                (xmax0, self.slider_ymax),
                (xmax1, self.slider_ymax),
                (xmax1, self.slider_ymin),
            ),
        ]
        self.segment_nav = np.array(seg)

        self.collection_nav.set_segments(self.segment_nav)
        return


class SegmentMixin(SliderMixin, VlineMixin, NavMixin):
    segment_nav: np.ndarray

    def set_segments(self):
        super().set_segments()

        self._set_slider_collection()
        self._set_slider_color_collection()
        return

    def set_color_segments(self):
        super().set_color_segments()

        self._set_slider_color_collection()
        return
