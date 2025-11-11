from fractions import Fraction

from matplotlib.axes import Axes
from matplotlib.collections import LineCollection
from matplotlib.text import Text
from matplotlib.backend_bases import MouseEvent
import pandas as pd

from ..._config import ConfigData
from ..._utils.nums import float_to_str
from ..base.a_canvas import Figure


class Base:
    CONFIG: ConfigData

    key_volume: str
    _length_text: int
    df: pd.DataFrame

    watermark: str

    v0: int
    v1: int
    vmiddle: int
    vxmin: int
    vxmax: int
    price_ymin: int
    price_ymax: int
    volume_ymax: int

    figure: Figure
    ax_legend: Axes
    ax_price: Axes
    ax_volume: Axes
    artist_watermark: Text
    collection_candle: LineCollection
    collection_volume: LineCollection
    collection_ma: LineCollection

    collection_price_crossline: LineCollection
    collection_volume_crossline: LineCollection

    artist_label_x: Text
    artist_label_y: Text

    collection_box_price: LineCollection
    collection_box_volume: LineCollection

    artist_info_candle: Text
    artist_info_volume: Text

    in_chart_price: bool
    in_chart_volume: bool


class CrosslineMixin(Base):
    def _set_crossline(self, e: MouseEvent,):
        x, y = (e.xdata, e.ydata)

        if self.in_chart_price:
            seg = [
                [
                    (x, self.price_ymin),
                    (x, self.price_ymax),
                ],
                [
                    (self.vxmin, y),
                    (self.vxmax, y),
                ]
            ]
            self.collection_price_crossline.set_segments(seg)
            seg = [
                [
                    (x, 0),
                    (x, self.volume_ymax),
                ]
            ]
            self.collection_volume_crossline.set_segments(seg)
        elif self.in_chart_volume:
            seg = [
                [
                    (x, self.price_ymin),
                    (x, self.price_ymax),
                ]
            ]
            self.collection_price_crossline.set_segments(seg)
            seg = [
                [
                    (x, 0),
                    (x, self.volume_ymax),
                ],
                [
                    (self.vxmin, y),
                    (self.vxmax, y)
                ]
            ]
            self.collection_volume_crossline.set_segments(seg)

        return


class LabelMixin(Base):
    def _set_label_x(self, e: MouseEvent):
        xdata, ydata = (e.xdata, e.xdata)
        # print(f'{(x, xdata)=}')

        if xdata < 0 or xdata is None:
            return

        try:
            text = self.df.iloc[int(xdata)]['date']
        except:
            return
        # print(f'{text=}')

        display_coords = e.inaxes.transData.transform((xdata, ydata))
        figure_coords = self.figure.transFigure.inverted()\
            .transform(display_coords)
        # print(f'{figure_coords=}')

        artist = self.artist_label_x

        artist.set_text(text)
        artist.set_x(figure_coords[0])
        self._set_label_x_position()
        return 1

    def _set_label_x_position(self):
        artist = self.artist_label_x
        renderer = self.figure.canvas.renderer

        # Axes 하단 경계 좌표
        boundary = self.ax_volume.get_position()\
            .y0
        # print(f'{y0=}')

        if not artist.get_text():
            artist.set_text(' ')

        # Text bbox 너비
        bbox = artist.get_bbox_patch()\
            .get_window_extent(renderer)
        bbox_size = bbox.height
        # 밀어야 하는 값
        fig_size = self.figure.bbox.height
        offset = (bbox_size + 10) / fig_size
        # print(f'{box_width_fig=}')

        # x축 값(가격 또는 거래량)
        # self.artist_label_y.set_x(x1)
        y = boundary - (offset / 2)
        # print(f'{(x1, x)=}')
        artist.set_y(y)
        return

    def _set_label_y(self, e: MouseEvent, *, is_price_chart):
        xdata, ydata = (e.xdata, e.ydata)
        artist = self.artist_label_y

        if is_price_chart:
            text = float_to_str(ydata, digit=self.CONFIG.UNIT.digit) + self.CONFIG.UNIT.price
        else:
            text = float_to_str(ydata, digit=self.CONFIG.UNIT.digit_volume) + self.CONFIG.UNIT.volume

        display_coords = e.inaxes.transData.transform((xdata, ydata))
        figure_coords = self.figure.transFigure.inverted().transform(display_coords)

        artist.set_text(text)
        artist.set_y(figure_coords[1])
        self._set_label_y_position()
        return

    def _set_label_y_position(self):
        artist = self.artist_label_y
        renderer = self.figure.canvas.renderer

        # Axes 우측 경계 좌표
        boundary = self.ax_volume.get_position()\
            .x1
        # print(f'{boundary=}')

        if not artist.get_text():
            artist.set_text(' ')

        # Text bbox 너비
        bbox = artist.get_bbox_patch()\
            .get_window_extent(renderer)
        bbox_size = bbox.width
        # 밀어야 하는 값
        fig_size = self.figure.bbox.width
        offset = (bbox_size + 8) / fig_size
        # print(f'{box_width_fig=}')

        # x축 값(가격 또는 거래량)
        # self.artist_label_y.set_x(x1)
        x = boundary + (offset / 2)
        # print(f'{(x1, x)=}')
        artist.set_x(x)
        return


class BoxMixin(Base):
    def _set_box_candle(self, segment):
        self.collection_box_price.set_segments(segment)
        return

    def _set_box_volume(self, segment):
        self.collection_box_volume.set_segments(segment)
        return


class InfoMixin(Base):
    fraction = False

    def _set_info_candle(self, ind):
        text = self._get_info(ind, is_price=True)
        self.artist_info_candle.set_text(text)

        # 정보 텍스트를 중앙에 몰리게 설정할 수도 있지만,
        # 그런 경우 차트를 가리므로 좌우 끝단에 위치하도록 설정
        if self.vmiddle < ind:
            self.artist_info_candle.set_x(self.v0)
        else:
            # self.artist_info_candle.set_x(self.vmax - self.x_distance)
            # self.artist_info_candle.set_horizontalalignment('right')
            # 텍스트박스 크기 가져오기
            bbox = self.artist_info_candle.get_window_extent()\
                .transformed(self.ax_price.transData.inverted())
            width = bbox.x1 - bbox.x0
            self.artist_info_candle.set_x(self.v1 - width)

        self.artist_info_candle.draw(self.figure.canvas.renderer)
        return

    def _set_info_volume(self, ind):
        text = self._get_info(ind, is_price=False)
        self.artist_info_volume.set_text(text)

        if self.vmiddle < ind:
            self.artist_info_volume.set_x(self.v0)
        else:
            # self.artist_info_volume.set_x(self.vmax - self.x_distance)
            # self.artist_info_volume.set_horizontalalignment('right')
            # 텍스트박스 크기 가져오기
            bbox = self.artist_info_volume.get_window_extent()\
                .transformed(self.ax_price.transData.inverted())
            width = bbox.x1 - bbox.x0
            self.artist_info_volume.set_x(self.v1 - width)

        self.artist_info_volume.draw(self.figure.canvas.renderer)
        return

    def get_info_kwargs(self, is_price: bool, **kwargs)-> dict:
        """
        get text info kwargs

        Args:
            is_price (bool): is price chart info or not

        Returns:
            dict[str, any]: text info kwargs
        """
        return kwargs

    def _get_info(self, ind: int, is_price=True):
        # print(f'{self._length_text=}')
        series = self.df.iloc[ind]

        dt = series['date']
        if not self.key_volume:
            v, vr = ('-', '-')
        else:
            v, vr = series.loc[['volume', 'rate_volume']]
            # print(f'{self.CONFIG.UNIT.digit_volume=}')
            v = float_to_str(v, digit=self.CONFIG.UNIT.digit_volume)
            # if not v % 1:
            #     v = int(v)
            vr = f'{vr:+06,.2f}'

        if is_price:
            o, h, l, c = (series['open'], series['high'], series['low'], series['close'])
            rate, compare = (series['rate'], series['compare'])
            r = f'{rate:+06,.2f}'
            Or, hr, lr = (series['rate_open'], series['rate_high'], series['rate_low'])

            if self.fraction:
                data = {}
                c = round(c, self.CONFIG.UNIT.digit)
                for value, key in [
                    [c, 'close'],
                    [compare, 'compare'],
                    [o, 'open'],
                    [h, 'high'],
                    [l, 'low'],
                ]:
                    div = divmod(value, 1)
                    if div[1]:
                        if div[0]:
                            data[key] = f'{float_to_str(div[0])} {Fraction((div[1]))}'
                        else:
                            data[key] = f'　 {Fraction((div[1]))}'
                    else:
                        data[key] = float_to_str(div[0])
                # print(f'{data=}')

                kwargs = self.get_info_kwargs(
                    is_price=is_price,
                    dt=dt,
                    close=f'{data["close"]:>{self._length_text}}{self.CONFIG.UNIT.price}',
                    rate=f'{r:>{self._length_text}}%',
                    compare=f'{data["compare"]:>{self._length_text}}{self.CONFIG.UNIT.price}',
                    open=f'{data["open"]:>{self._length_text}}{self.CONFIG.UNIT.price}', rate_open=f'{Or:+06,.2f}%',
                    high=f'{data["high"]:>{self._length_text}}{self.CONFIG.UNIT.price}', rate_high=f'{hr:+06,.2f}%',
                    low=f'{data["low"]:>{self._length_text}}{self.CONFIG.UNIT.price}', rate_low=f'{lr:+06,.2f}%',
                    volume=f'{v:>{self._length_text}}{self.CONFIG.UNIT.volume}', rate_volume=f'{vr}%',
                )
                text = self.CONFIG.FORMAT.candle.format(**kwargs)
            else:
                o, h, l, c = (
                    float_to_str(o, digit=self.CONFIG.UNIT.digit),
                    float_to_str(h, digit=self.CONFIG.UNIT.digit),
                    float_to_str(l, digit=self.CONFIG.UNIT.digit),
                    float_to_str(c, digit=self.CONFIG.UNIT.digit),
                )
                com = float_to_str(compare, digit=self.CONFIG.UNIT.digit, plus=True)

                kwargs = self.get_info_kwargs(
                    is_price=is_price,
                    dt=dt,
                    close=f'{c:>{self._length_text}}{self.CONFIG.UNIT.price}',
                    rate=f'{r:>{self._length_text}}%',
                    compare=f'{com:>{self._length_text}}{self.CONFIG.UNIT.price}',
                    open=f'{o:>{self._length_text}}{self.CONFIG.UNIT.price}', rate_open=f'{Or:+06,.2f}%',
                    high=f'{h:>{self._length_text}}{self.CONFIG.UNIT.price}', rate_high=f'{hr:+06,.2f}%',
                    low=f'{l:>{self._length_text}}{self.CONFIG.UNIT.price}', rate_low=f'{lr:+06,.2f}%',
                    volume=f'{v:>{self._length_text}}{self.CONFIG.UNIT.volume}', rate_volume=f'{vr}%',
                )
                text = self.CONFIG.FORMAT.candle.format(**kwargs)
        elif self.key_volume:
            compare = self.df.loc[ind, 'compare_volume']
            com = float_to_str(compare, digit=self.CONFIG.UNIT.digit_volume, plus=True)
            kwargs = self.get_info_kwargs(
                is_price=is_price,
                dt=dt,
                volume=f'{v:>{self._length_text}}{self.CONFIG.UNIT.volume}',
                rate_volume=f'{vr:>{self._length_text}}%',
                compare=f'{com:>{self._length_text}}{self.CONFIG.UNIT.volume}',
            )
            text = self.CONFIG.FORMAT.volume.format(**kwargs)
        else:
            text = ''

        return text


class SegmentMixin(CrosslineMixin, LabelMixin, BoxMixin, InfoMixin):
    fraction = False

