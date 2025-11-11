from matplotlib.axes import Axes
from matplotlib.text import Text
import pandas as pd

from ..._config import ConfigData


class Base:
    CONFIG: ConfigData
    df: pd.DataFrame

    key_date = 'date'
    key_open, key_high, key_low, key_close = ('open', 'high', 'low', 'close')
    key_volume = 'volume'

    ax_slider: Axes

    index_list: list[int] = []

    artist_text_slider: Text

    axis: callable
    get_default_xlim: callable
    set_variables: callable

    _set_slider_collection: callable
    vxmin: int
    vxmax: int


class SliderMixin(Base):
    min_distance = 5

    def get_default_xlim(self):
        xmax = self.index_list[-1] + 1
        xmin = xmax - 120
        if xmin < 0:
            xmin = 0
        return (xmin, xmax)

    def set_variables(self):
        super().set_variables()

        self._set_slider()
        return

    def _set_slider(self):
        # print('_set_slider')
        self._set_slider_xtick()

        xmax = self.index_list[-1]
        # 슬라이더 xlim
        xdistance = round(xmax / 30)
        self.slider_xmin, self.slider_xmax = (-xdistance, xmax+xdistance)
        self.ax_slider.set_xlim(self.slider_xmin, self.slider_xmax)

        # 네비게이터 경계선 두께
        self._nav_width = round((self.slider_xmax - self.slider_xmin) / 250, 2)

        # 슬라이더 ylim
        ymin, ymax = (self.df['low'].min(), self.df['high'].max())
        ysub = ymax - ymin
        ydistance = round(ysub / 5, self.CONFIG.UNIT.digit+2)
        self.slider_ymin, self.slider_ymax = (ymin-ydistance, ymax+ydistance)
        self.ax_slider.set_ylim(self.slider_ymin, self.slider_ymax)

        self._set_slider_collection()
        self._set_slider_text_position()

        return

    def _set_slider_text_position(self):
        # 슬라이더 텍스트 y
        self.artist_text_slider.set_y(self.df['high'].max())
        return

    def _set_slider_xtick(self):
        indices = [0, self.index_list[-1]]
        # print(f'{indices=}')

        date_list = [self.df.iloc[idx]['date'] for idx in indices]
        # print(f'{date_list=}')
        # xtick 설정, major tick과 겹쳐서 무시되는 것 방지
        self.ax_slider.set_xticks([idx+0.01 for idx in indices], labels=date_list, minor=True)

        labels = self.ax_slider.get_xticklabels(minor=True)
        # print(f'{labels=}')
        for label, align in zip(labels, ['center', 'center']):
            # 라벨 텍스트 정렬
            label.set_horizontalalignment(align)
        return


class DataMixin(SliderMixin):
    min_distance = 5
    _nav_width: float

    slider_xmin: int
    slider_xmax: int
    slider_ymin: float
    slider_ymax: float

