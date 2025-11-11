from matplotlib.axes import Axes
from matplotlib.backend_bases import MouseEvent
from matplotlib.collections import LineCollection
from matplotlib.text import Text
import pandas as pd

from ..base.a_canvas import Figure


class Base:
    figure: Figure
    ax_price: Axes
    ax_volume: Axes

    key_volume: str
    df: pd.DataFrame

    vxmin: int
    vxmax: int
    price_ymin: float
    price_ymax: float
    volume_ymax: float

    collection_box_price: LineCollection
    collection_box_volume: LineCollection
    collection_price_crossline: LineCollection

    index_list: list

    min_height_box_candle: float
    min_height_box_volume: float

    connect_events: callable

    artist_label_x: Text
    artist_label_y: Text

    in_chart = False
    in_chart_price = False
    in_chart_volume = False

    in_candle = False
    in_volume = False

    _restore_region: callable

    _set_crossline: callable
    _draw_crossline: callable
    _set_label_x: callable
    _draw_label_x: callable

    _set_label_y: callable
    _draw_label_y: callable

    _set_box_candle: callable
    _draw_box_candle: callable
    _set_box_volume: callable
    _draw_box_volume: callable

    _set_info_candle: callable
    _draw_info_candle: callable
    _set_info_volume: callable
    _draw_info_volume: callable


class AxMixin(Base):
    def _check_ax(self, e: MouseEvent):
        ax = e.inaxes
        # print(f'{ax=}')
        self.in_chart = False
        self.in_chart_price, self.in_chart_volume = (False, False)

        if e.xdata is None or e.ydata is None:
            return

        if self.vxmin <= e.xdata and e.xdata <= self.vxmax:
            if ax is self.ax_price and (
                self.price_ymin <= e.ydata and e.ydata <= self.price_ymax
            ):
                self.in_chart = True
                self.in_chart_price = True
            elif ax is self.ax_volume and (
                0 <= e.ydata and e.ydata <= self.volume_ymax
            ):
                self.in_chart = True
                self.in_chart_volume = True
        return


class BoxMixin(Base):
    def _draw_box_artist(self, e: MouseEvent):
        xdata, ydata = (e.xdata, e.ydata)
        ind = int(xdata)

        self.in_candle, self.in_volume = (False, False)

        if self.in_chart_price:
            series = self.df.iloc[ind]
            # print(f'{series=}')
            # 박스 크기
            high = series['box_candle_top']
            low = series['box_candle_bottom']
            height = series['box_candle_height']
            # print(f'{(low, high)=}')
            # print(f'{height=}')

            # 박스 높이 보정
            if height < self.min_height_box_candle:
                sub = (self.min_height_box_candle - height) / 2
                high, low = (high+sub, low-sub)

            # 커서가 캔들 사이에 있는지 확인
            if low <= ydata and ydata <= high:
                self.in_candle = True

                # 캔들 강조
                x0, x1 = (ind-0.3, ind+1.3)
                segment = [(
                    (x0, high),
                    (x1, high),
                    (x1, low),
                    (x0, low),
                    (x0, high)
                )]
                self._set_box_candle(segment)
                self._draw_box_candle()

                return 1
        elif self.in_chart_volume and self.key_volume:
            # 박스 크기
            high = self.df.iloc[ind]['box_volume_top']
            low = 0
            if high < self.min_height_box_volume:
                high = self.min_height_box_volume

            if low <= ydata and ydata <= high:
                # 거래량 강조
                self.in_volume = True

                x0, x1 = (ind-0.3, ind+1.3)
                segment = [(
                    (x0, high),
                    (x1, high),
                    (x1, low),
                    (x0, low),
                    (x0, high)
                )]
                self._set_box_volume(segment)
                self._draw_box_volume()

                return 1
        return


class InfoMixin(Base):
    def _draw_info_artist(self, e: MouseEvent):
        return


class Mixin(AxMixin, BoxMixin, InfoMixin):
    _in_mouse_move = False

    def need_restore(self):
        if self.collection_price_crossline.get_segments():
            self.collection_price_crossline.set_segments([])
            return True
        return

    def _on_move(self, e: MouseEvent):
        # print(f'{not self._in_mouse_move=}')
        if not self._in_mouse_move:
            self._in_mouse_move = True
            # print(f'{(e.xdata, e.ydata)=}')
            self.on_move(e)
            self._in_mouse_move = False
        return

    def on_move(self, e: MouseEvent):
        self._check_ax(e)
        self._on_move_action(e)
        return

    def _set_and_draw_crossline(self, e: MouseEvent):
        self._set_crossline(e)
        self._draw_crossline()

        if self._set_label_x(e):
            # print('draw label x')
            self._draw_label_x()
            if self._draw_box_artist(e):
                ind = int(e.xdata)
                if self.in_chart_price:
                    self._set_info_candle(ind)
                    self._draw_info_candle()
                else:
                    self._set_info_volume(ind)
                    self._draw_info_volume()
        self._set_label_y(e, is_price_chart=self.in_chart_price)
        self._draw_label_y()

        return

    def _on_move_action(self, e: MouseEvent):
        if self.in_chart:
            self._restore_region()

            self._set_and_draw_crossline(e)

            self.figure.canvas.blit()
            self.figure.canvas.flush_events()
        elif self.need_restore():
            self._restore_region()
            self.figure.canvas.blit()
            self.figure.canvas.flush_events()
        return


class EventMixin(Mixin):
    in_chart = False
    in_chart_price = False
    in_chart_volume = False

    in_candle = False
    in_volume = False

    _in_mouse_move = False

    def connect_events(self):
        super().connect_events()

        self.figure.canvas.mpl_connect('motion_notify_event', lambda x: self._on_move(x))
        return

