from fractions import Fraction

from matplotlib.backend_bases import MouseEvent
from matplotlib.collections import LineCollection
from matplotlib.text import Text
import pandas as pd

from ._draw import BaseMixin as BM, Mixin as M
from .utils import float_to_str


class Mixin(M):
    def on_move(self, e):
        "If mouse move event active, This method work."
        return


class CollectionMixin(BM):
    lineKwargs = {}
    textboxKwargs = {}
    textKwargs = {}
    color_box = 'k'

    def _add_collection(self):
        super()._add_collection()

        lineKwargs = {'edgecolor': 'k', 'linewidth': 1, 'linestyle': '-'}
        lineKwargs.update(self.lineKwargs)
        lineKwargs.update({'segments': [], 'animated': True})
        textboxKwargs = {'boxstyle': 'round', 'facecolor': 'w'}
        textboxKwargs.update(self.textboxKwargs)
        textKwargs = self.textKwargs
        textKwargs.update({'animated': True, 'bbox': textboxKwargs, 'horizontalalignment': '', 'verticalalignment': ''})
        (textKwargs.pop('horizontalalignment'), textKwargs.pop('verticalalignment'))

        self.collection_price_crossline = LineCollection(**lineKwargs)
        self.ax_price.add_artist(self.collection_price_crossline)
        self.artist_text_date_price = Text(**textKwargs, horizontalalignment='center', verticalalignment='bottom')
        self.ax_price.add_artist(self.artist_text_date_price)
        self.artist_text_price = Text(**textKwargs, horizontalalignment='left', verticalalignment='center')
        self.ax_price.add_artist(self.artist_text_price)

        self.collection_volume_crossline = LineCollection(**lineKwargs)
        self.ax_volume.add_artist(self.collection_volume_crossline)
        self.artist_text_date_volume = Text(**textKwargs, horizontalalignment='center', verticalalignment='top')
        self.ax_volume.add_artist(self.artist_text_date_volume)
        self.artist_text_volume = Text(**textKwargs, horizontalalignment='left', verticalalignment='center')
        self.ax_volume.add_artist(self.artist_text_volume)

        self.collection_price_box = LineCollection([], animated=True, linewidth=1.2, edgecolor=self.color_box)
        self.ax_price.add_artist(self.collection_price_box)
        self.artist_text_price_info = Text(**textKwargs, horizontalalignment='left', verticalalignment='top')
        self.ax_price.add_artist(self.artist_text_price_info)

        self.collection_volume_box = LineCollection([], animated=True, linewidth=1.2, edgecolor=self.color_box)
        self.ax_volume.add_artist(self.collection_volume_box)
        self.artist_text_volume_info = Text(**textKwargs, horizontalalignment='left', verticalalignment='top')
        self.ax_volume.add_artist(self.artist_text_volume_info)
        return

    def change_background_color(self, color):
        super().change_background_color(color)

        self.artist_text_price.set_backgroundcolor(color)
        self.artist_text_volume.set_backgroundcolor(color)

        self.artist_text_date_price.set_backgroundcolor(color)
        self.artist_text_date_volume.set_backgroundcolor(color)

        self.artist_text_price_info.set_backgroundcolor(color)
        self.artist_text_volume_info.set_backgroundcolor(color)
        return

    def change_text_color(self, color):
        super().change_text_color(color)

        self.artist_text_price.set_color(color)
        self.artist_text_volume.set_color(color)

        self.artist_text_date_price.set_color(color)
        self.artist_text_date_volume.set_color(color)

        self.artist_text_price_info.set_color(color)
        self.artist_text_volume_info.set_color(color)
        return

    def change_line_color(self, color):
        self.collection_price_crossline.set_edgecolor(color)
        self.collection_volume_crossline.set_edgecolor(color)

        self.collection_price_box.set_edgecolor(color)
        self.collection_volume_box.set_edgecolor(color)

        self.artist_text_price.get_bbox_patch().set_edgecolor(color)
        self.artist_text_volume.get_bbox_patch().set_edgecolor(color)

        self.artist_text_date_price.get_bbox_patch().set_edgecolor(color)
        self.artist_text_date_volume.get_bbox_patch().set_edgecolor(color)

        self.artist_text_price_info.get_bbox_patch().set_edgecolor(color)
        self.artist_text_volume_info.get_bbox_patch().set_edgecolor(color)
        return


_set_key = {
    'compare', 'rate',
    'rate_open', 'rate_high', 'rate_low',
    'compare_volume', 'rate_volume',
    'space_box_candle',
    'bottom_box_candle', 'top_box_candle',
    'max_box_volume',
}

class DataMixin(CollectionMixin):
    def _validate_column_key(self, df):
        super()._validate_column_key(df)

        for i in ('date', 'Open', 'high', 'low', 'close', 'volume'):
            v = getattr(self, i)
            if v in _set_key: raise Exception(f'you can not set "{i}" to column key.\nself.{i}={v!r}')
        return

    def set_data(self, df, sort_df=True, calc_ma=True, set_candlecolor=True, set_volumecolor=True, calc_info=True, *args, **kwargs):
        super().set_data(df, sort_df, calc_ma, set_candlecolor, set_volumecolor, calc_info, *args, **kwargs)
        return

    def _generate_data(self, df: pd.DataFrame, sort_df, calc_ma, set_candlecolor, set_volumecolor, calc_info, *_, **__):
        super()._generate_data(df, sort_df, calc_ma, set_candlecolor, set_volumecolor, *_, **__)

        if not calc_info:
            keys = set(df.keys())
            list_key = ['compare', 'rate', 'rate_open', 'rate_high', 'rate_low',]
            if self.volume: list_key += ['compare_volume', 'rate_volume',]
            for i in list_key:
                if i not in keys:
                    raise Exception(f'"{i}" column not in DataFrame.\nadd column or set calc_info=True.')
        else:
            self.df['compare'] = (self.df[self.close] - self.df['close_pre']).fillna(0)
            self.df['rate'] = (self.df['compare'] / self.df[self.close] * 100).__round__(2).fillna(0)
            self.df['rate_open'] = ((self.df[self.Open] - self.df['close_pre']) / self.df[self.close] * 100).__round__(2).fillna(0)
            self.df['rate_high'] = ((self.df[self.high] - self.df['close_pre']) / self.df[self.close] * 100).__round__(2).fillna(0)
            self.df['rate_low'] = ((self.df[self.low] - self.df['close_pre']) / self.df[self.close] * 100).__round__(2).fillna(0)
            if self.volume:
                self.df['compare_volume'] = (self.df[self.volume] - self.df[self.volume].shift(1)).fillna(0)
                self.df['rate_volume'] = (self.df['compare_volume'] / self.df[self.volume].shift(1) * 100).__round__(2).fillna(0)

        self.df['space_box_candle'] = (self.df[self.high] - self.df[self.low]) / 5
        self.df['bottom_box_candle'] = self.df[self.low] - self.df['space_box_candle']
        self.df['top_box_candle'] = self.df[self.high] + self.df['space_box_candle']
        self.df['height_box_candle'] = self.df['top_box_candle'] - self.df['bottom_box_candle']
        if self.volume: self.df['max_box_volume'] = self.df[self.volume] * 1.15
        return

    def _set_lim(self, xmin, xmax, simpler=False, set_ma=True):
        super()._set_lim(xmin, xmax, simpler, set_ma)

        psub = (self.price_ymax - self.price_ymin)
        self.min_height_box_candle = psub / 8

        pydistance = psub / 20
        self.artist_text_date_price.set_y(self.price_ymin + pydistance)

        self.min_height_box_volume = self.volume_ymax / 4

        vxsub = self.vxmax - self.vxmin
        self.vmiddle = self.vxmax - int((vxsub) / 2)

        vxdistance = vxsub / 50
        self.v0, self.v1 = (self.vxmin + vxdistance, self.vxmax - vxdistance)
        self.vsixth = self.vxmin + int((vxsub) / 6)
        self.veighth = self.vxmin + int((vxsub) / 8)

        yvolume = self.volume_ymax * 0.85
        self.artist_text_date_volume.set_y(yvolume)

        # 정보 텍스트박스
        self.artist_text_price_info.set_y(self.price_ymax - pydistance)
        self.artist_text_volume_info.set_y(yvolume)
        return


class EventMixin(DataMixin):
    in_price_chart, in_volume_chart = (False, False)
    intx = None

    def _connect_event(self):
        super()._connect_event()
        self.figure.canvas.mpl_connect('motion_notify_event', lambda x: self._on_move(x))
        return

    def _on_move(self, e):
        self._on_move_action(e)
        return

    def _on_move_action(self, e: MouseEvent):
        self._check_ax(e)

        self.intx = None
        if self.in_price_chart or self.in_volume_chart: self._get_x(e)
        return

    def _check_ax(self, e: MouseEvent):
        ax = e.inaxes
        if not ax or e.xdata is None or e.ydata is None:
            self.in_price_chart, self.in_volume_chart = (False, False)
        else:
            if ax is self.ax_price:
                self.in_price_chart = True
                self.in_volume_chart = False
            elif ax is self.ax_volume:
                self.in_price_chart = False
                self.in_volume_chart = True
            else:
                self.in_price_chart = False
                self.in_volume_chart = False
        return

    def _get_x(self, e: MouseEvent):
        self.intx = e.xdata.__int__()
        if self.intx < 0: self.intx = None
        else:
            try: self.list_index[self.intx]
            except: self.intx = None
        return


class CrossLineMixin(EventMixin):
    digit_price, digit_volume = (0, 0)
    in_candle, in_volumebar = (False, False)

    def _on_move(self, e):
        super()._on_move(e)

        if self.in_price_chart or self.in_volume_chart:
            self._restore_region()
            self._draw_crossline(e, self.in_price_chart)
            self.figure.canvas.blit()
        else:
            if self._erase_crossline():
                self._restore_region()
                self.figure.canvas.blit()
        return

    def _erase_crossline(self):
        seg = self.collection_price_crossline.get_segments()
        if seg:
            self.collection_price_crossline.set_segments([])
            return True
        return False

    def _draw_crossline(self, e: MouseEvent, in_price_chart):
        x, y = (e.xdata, e.ydata)

        if in_price_chart:
            self.collection_price_crossline.set_segments([((x, self.price_ymin), (x, self.price_ymax)), ((self.vxmin, y), (self.vxmax, y))])
            self.collection_volume_crossline.set_segments([((x, 0), (x, self.volume_ymax))])
        else:
            self.collection_price_crossline.set_segments([((x, self.price_ymin), (x, self.price_ymax))])
            self.collection_volume_crossline.set_segments([((x, 0), (x, self.volume_ymax)), ((self.vxmin, y), (self.vxmax, y))])

        renderer = self.figure.canvas.renderer
        self.collection_price_crossline.draw(renderer)
        self.collection_volume_crossline.draw(renderer)

        self._draw_text_artist(e, in_price_chart)
        return

    def _draw_text_artist(self, e: MouseEvent, in_price_chart):
        x, y = (e.xdata, e.ydata)

        renderer = self.figure.canvas.renderer
        if in_price_chart:
            # 가격
            self.artist_text_price.set_text(f'{float_to_str(y, self.digit_price)}{self.unit_price}')
            self.artist_text_price.set_x(self.v0 if self.veighth < x else self.vsixth)
            self.artist_text_price.set_y(y)
            self.artist_text_price.draw(renderer)

            if self.intx is not None:
                # 기준시간 표시
                self.artist_text_date_volume.set_text(f'{self.df[self.date][self.intx]}')
                self.artist_text_date_volume.set_x(x)
                self.artist_text_date_volume.draw(renderer)
        else:
            # 거래량
            self.artist_text_volume.set_text(f'{float_to_str(y, self.digit_volume)}{self.unit_volume}')
            self.artist_text_volume.set_x(self.v0 if self.veighth < x else self.vsixth)
            self.artist_text_volume.set_y(y)
            self.artist_text_volume.draw(renderer)

            if self.intx is not None:
                # 기준시간 표시
                self.artist_text_date_price.set_text(f'{self.df[self.date][self.intx]}')
                self.artist_text_date_price.set_x(x)
                self.artist_text_date_price.draw(renderer)
        return


class BoxMixin(CrossLineMixin):
    def _draw_crossline(self, e, in_price_chart):
        super()._draw_crossline(e, in_price_chart)
        self._draw_box_artist(e, in_price_chart)
        return

    def _draw_box_artist(self, e: MouseEvent, in_price_chart):
        y = e.ydata

        renderer = self.figure.canvas.renderer
        if self.intx is not None:
            if in_price_chart:
                # 박스 크기
                high = self.df['top_box_candle'][self.intx]
                low = self.df['bottom_box_candle'][self.intx]
                height = self.df['height_box_candle'][self.intx]
                if height < self.min_height_box_candle:
                    sub = (self.min_height_box_candle - height) / 2
                    high, low = (high+sub, low-sub)

                # 커서가 캔들 사이에 있는지 확인
                if high < y or y < low: self.in_candle = False
                else:
                    # 캔들 강조
                    self.in_candle = True
                    x1, x2 = (self.intx-0.3, self.intx+1.3)
                    self.collection_price_box.set_segments([((x1, high), (x2, high), (x2, low), (x1, low), (x1, high))])
                    self.collection_price_box.draw(renderer)
            elif self.volume:
                # 거래량 강조
                high = self.df['max_box_volume'][self.intx]
                low = 0
                if high < self.min_height_box_volume: high = self.min_height_box_volume

                if high < y or y < low: self.in_volumebar = False
                else:
                    self.in_volumebar = True
                    x1, x2 = (self.intx-0.3, self.intx+1.3)
                    self.collection_volume_box.set_segments([((x1, high), (x2, high), (x2, low), (x1, low), (x1, high))])
                    self.collection_volume_box.draw(renderer)
        return


format_candleinfo_ko = """\
{dt}

종가:　 {close}
등락률: {rate}
대비:　 {compare}
시가:　 {open}({rate_open})
고가:　 {high}({rate_high})
저가:　 {low}({rate_low})
거래량: {volume}({rate_volume})\
"""
format_volumeinfo_ko = """\
{dt}

거래량:　　　 {volume}
거래량증가율: {rate_volume}
대비:　　　　 {compare}\
"""
format_candleinfo_en = """\
{dt}

close:      {close}
rate:        {rate}
compare: {compare}
open:      {open}({rate_open})
high:       {high}({rate_high})
low:        {low}({rate_low})
volume:  {volume}({rate_volume})\
"""
format_volumeinfo_en = """\
{dt}

volume:      {volume}
volume rate: {rate_volume}
compare:     {compare}\
"""

class InfoMixin(BoxMixin):
    fraction = False
    format_candleinfo = format_candleinfo_ko
    format_volumeinfo = format_volumeinfo_ko

    def set_data(self, df, sort_df=True, calc_ma=True, set_candlecolor=True, set_volumecolor=True, calc_info=True, *args, **kwargs):
        super().set_data(df, sort_df, calc_ma, set_candlecolor, set_volumecolor, calc_info, *args, **kwargs)

        self._set_length_text()
        return

    def _set_length_text(self):
        self._length_text = self.df[(self.volume if self.volume else self.high)].apply(lambda x: len(f'{x:,}')).max()
        lenth_high = self.df[self.high].apply(lambda x: len(f'{x:,}')).max()
        lenth_volume = 0 if not self.volume else self.df[self.volume].apply(lambda x: len(f'{x:,}')).max()
        self._length_text = lenth_high if lenth_volume < lenth_high else lenth_volume
        return

    def _draw_box_artist(self, e, in_price_chart):
        super()._draw_box_artist(e, in_price_chart)

        if self.intx is not None:
            if self.in_candle: self._draw_candle_info_artist(e)
            elif self.volume and self.in_volumebar: self._draw_volume_info_artist(e)
        return

    def _draw_candle_info_artist(self, e: MouseEvent):
        # 캔들 정보
        self.artist_text_price_info.set_text(self._get_info(self.intx))

        # 정보 텍스트를 중앙에 몰리게 설정할 수도 있지만,
        # 그런 경우 차트를 가리므로 좌우 끝단에 위치하도록 설정
        if self.vmiddle < e.xdata:
            self.artist_text_price_info.set_x(self.v0)
        else:
            # self.artist_text_price_info.set_x(self.vmax - self.x_distance)
            # self.artist_text_price_info.set_horizontalalignment('right')
            # 텍스트박스 크기 가져오기
            bbox = self.artist_text_price_info.get_window_extent().transformed(self.ax_price.transData.inverted())
            width = bbox.x1 - bbox.x0
            self.artist_text_price_info.set_x(self.v1 - width)

        self.artist_text_price_info.draw(self.figure.canvas.renderer)
        return

    def _draw_volume_info_artist(self, e: MouseEvent):
        # 거래량 정보
        self.artist_text_volume_info.set_text(self._get_info(self.intx, is_price=False))

        if self.vmiddle < e.xdata: self.artist_text_volume_info.set_x(self.v0)
        else:
            # self.artist_text_volume_info.set_x(self.vmax - self.x_distance)
            # self.artist_text_volume_info.set_horizontalalignment('right')
            # 텍스트박스 크기 가져오기
            bbox = self.artist_text_volume_info.get_window_extent().transformed(self.ax_price.transData.inverted())
            width = bbox.x1 - bbox.x0
            self.artist_text_volume_info.set_x(self.v1 - width)

        self.artist_text_volume_info.draw(self.figure.canvas.renderer)
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

    def _get_info(self, index, is_price=True):
        dt = self.df[self.date][index]
        if not self.volume: v, vr = ('-', '-')
        else:
            v = self.df[self.volume][index]
            v = float_to_str(v, self.digit_volume)
            # if not v % 1: v = int(v)
            vr = self.df['rate_volume'][index]
            vr = f'{vr:+06,.2f}'

        if is_price:
            o, h, l, c = (self.df[self.Open][index], self.df[self.high][index], self.df[self.low][index], self.df[self.close][index])
            rate, compare = (self.df['rate'][index], self.df['compare'][index])
            r = f'{rate:+06,.2f}'
            Or, hr, lr = (self.df['rate_open'][index], self.df['rate_high'][index], self.df['rate_low'][index])

            if self.fraction:
                c = c.__round__(self.digit_price)
                cd = divmod(c, 1)
                if cd[1]: c = f'{float_to_str(cd[0])} {Fraction((cd[1]))}'
                else: c = float_to_str(cd[0])
                comd = divmod(compare, 1)
                if comd[1]: com = f'{float_to_str(comd[0], plus=True)} {Fraction(comd[1])}'
                else: com = float_to_str(comd[0], plus=True)
                o = o.__round__(self.digit_price)
                od = divmod(o, 1)
                if od[1]: o = f'{float_to_str(od[0])} {Fraction(od[1])}'
                else: o = float_to_str(od[0])
                h = h.__round__(self.digit_price)
                hd = divmod(h, 1)
                if hd[1]: h = f'{float_to_str(hd[0])} {Fraction(hd[1])}'
                else: h = float_to_str(hd[0])
                l = l.__round__(self.digit_price)
                ld = divmod(l, 1)
                if ld[1]: l = f'{float_to_str(ld[0])} {Fraction(ld[1])}'
                else: l = float_to_str(ld[0])

                kwargs = self.get_info_kwargs(
                    is_price=is_price,
                    dt=dt,
                    close=f'{c:>{self._length_text}}{self.unit_price}',
                    rate=f'{r:>{self._length_text}}%',
                    compare=f'{com:>{self._length_text}}{self.unit_price}',
                    open=f'{o:>{self._length_text}}{self.unit_price}', rate_open=f'{Or:+06,.2f}%',
                    high=f'{h:>{self._length_text}}{self.unit_price}', rate_high=f'{hr:+06,.2f}%',
                    low=f'{l:>{self._length_text}}{self.unit_price}', rate_low=f'{lr:+06,.2f}%',
                    volume=f'{v:>{self._length_text}}{self.unit_volume}', rate_volume=f'{vr}%',
                )
                text = self.format_candleinfo.format(**kwargs)
            else:
                o, h, l, c = (float_to_str(o, self.digit_price), float_to_str(h, self.digit_price), float_to_str(l, self.digit_price), float_to_str(c, self.digit_price))
                com = float_to_str(compare, self.digit_price, plus=True)

                kwargs = self.get_info_kwargs(
                    is_price=is_price,
                    dt=dt,
                    close=f'{c:>{self._length_text}}{self.unit_price}',
                    rate=f'{r:>{self._length_text}}%',
                    compare=f'{com:>{self._length_text}}{self.unit_price}',
                    open=f'{o:>{self._length_text}}{self.unit_price}', rate_open=f'{Or:+06,.2f}%',
                    high=f'{h:>{self._length_text}}{self.unit_price}', rate_high=f'{hr:+06,.2f}%',
                    low=f'{l:>{self._length_text}}{self.unit_price}', rate_low=f'{lr:+06,.2f}%',
                    volume=f'{v:>{self._length_text}}{self.unit_volume}', rate_volume=f'{vr}%',
                )
                text = self.format_candleinfo.format(**kwargs)
        elif self.volume:
            compare = self.df['compare_volume'][index]
            com = float_to_str(compare, self.digit_volume, plus=True)
            kwargs = self.get_info_kwargs(
                is_price=is_price,
                dt=dt,
                volume=f'{v:>{self._length_text}}{self.unit_volume}',
                rate_volume=f'{vr:>{self._length_text}}%',
                compare=f'{com:>{self._length_text}}{self.unit_volume}',
            )
            text = self.format_volumeinfo.format(**kwargs)
        else: text = ''
        
        return text


class BaseMixin(InfoMixin):
    pass


class Chart(BaseMixin, Mixin):
    def _draw_artist(self):
        super()._draw_artist()
        return self.draw_artist()

    def _set_lim(self, xmin, xmax, simpler=False, set_ma=True):
        super()._set_lim(xmin, xmax, simpler, set_ma)
        return self.on_change_xlim(xmin, xmax, simpler, set_ma)

    def _on_draw(self, e):
        super()._on_draw(e)
        return self.on_draw(e)

    def _on_pick(self, e):
        self.on_pick(e)
        return super()._on_pick(e)

    def _on_move(self, e):
        super()._on_move(e)
        return self.on_move(e)

