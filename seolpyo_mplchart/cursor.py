from fractions import Fraction

import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseEvent
from matplotlib.collections import LineCollection
from matplotlib.text import Text
import pandas as pd

from .draw import BaseMixin as BM, Mixin as M
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

        self.price_crossline = LineCollection(**lineKwargs)
        self.ax_price.add_artist(self.price_crossline)
        self.text_date_price = Text(**textKwargs, horizontalalignment='center', verticalalignment='bottom')
        self.ax_price.add_artist(self.text_date_price)
        self.text_price = Text(**textKwargs, horizontalalignment='left', verticalalignment='center')
        self.ax_price.add_artist(self.text_price)

        self.volume_crossline = LineCollection(**lineKwargs)
        self.ax_volume.add_artist(self.volume_crossline)
        self.text_date_volume = Text(**textKwargs, horizontalalignment='center', verticalalignment='top')
        self.ax_volume.add_artist(self.text_date_volume)
        self.text_volume = Text(**textKwargs, horizontalalignment='left', verticalalignment='center')
        self.ax_volume.add_artist(self.text_volume)

        self.price_box = LineCollection([], animated=True, linewidth=1.2, edgecolor=self.color_box)
        self.ax_price.add_artist(self.price_box)
        self.text_price_info = Text(**textKwargs, horizontalalignment='left', verticalalignment='top')
        self.ax_price.add_artist(self.text_price_info)

        self.volume_box = LineCollection([], animated=True, linewidth=1.2, edgecolor=self.color_box)
        self.ax_volume.add_artist(self.volume_box)
        self.text_volume_info = Text(**textKwargs, horizontalalignment='left', verticalalignment='top')
        self.ax_volume.add_artist(self.text_volume_info)
        return

    def change_background_color(self, color):
        super().change_background_color(color)

        self.text_price.set_backgroundcolor(color)
        self.text_volume.set_backgroundcolor(color)

        self.text_date_price.set_backgroundcolor(color)
        self.text_date_volume.set_backgroundcolor(color)

        self.text_price_info.set_backgroundcolor(color)
        self.text_volume_info.set_backgroundcolor(color)
        return

    def change_text_color(self, color):
        super().change_text_color(color)

        self.text_price.set_color(color)
        self.text_volume.set_color(color)

        self.text_date_price.set_color(color)
        self.text_date_volume.set_color(color)

        self.text_price_info.set_color(color)
        self.text_volume_info.set_color(color)
        return

    def change_line_color(self, color):
        self.price_crossline.set_edgecolor(color)
        self.volume_crossline.set_edgecolor(color)

        self.price_box.set_edgecolor(color)
        self.volume_box.set_edgecolor(color)

        self.text_price.get_bbox_patch().set_edgecolor(color)
        self.text_volume.get_bbox_patch().set_edgecolor(color)

        self.text_date_price.get_bbox_patch().set_edgecolor(color)
        self.text_date_volume.get_bbox_patch().set_edgecolor(color)

        self.text_price_info.get_bbox_patch().set_edgecolor(color)
        self.text_volume_info.get_bbox_patch().set_edgecolor(color)
        return


_set_key = {'rate', 'compare', 'rate_open', 'rate_high', 'rate_low', 'rate_volume', '_boxheight', '_boxmin', '_boxmax', '_volumeboxmax',}

class DataMixin(CollectionMixin):
    def _validate_column_key(self):
        super()._validate_column_key()
        for i in ['date', 'Open', 'high', 'low', 'close', 'volume']:
            v = getattr(self, i)
            if v in _set_key: raise Exception(f'you can not set "{i}" to column key.\nself.{i}={v!r}')
        return

    def _generate_data(self, df, sort_df, calc_ma, set_candlecolor, set_volumecolor, calc_info, *_, **__):
        super()._generate_data(df, sort_df, calc_ma, set_candlecolor, set_volumecolor, *_, **__)

        if not calc_info:
            keys = set(df.keys())
            list_key = ['rate', 'compare', 'rate_open', 'rate_high', 'rate_low',]
            if self.volume: list_key.append('rate_volume')
            for i in list_key:
                if i not in keys:
                    raise Exception(f'"{i}" column not in DataFrame.\nadd column or set calc_info=True.')
        else:
            self.df['compare'] = (self.df[self.close] - self.df['_pre']).fillna(0)
            self.df['rate'] = (self.df['compare'] / self.df[self.close] * 100).__round__(2).fillna(0)
            self.df['rate_open'] = ((self.df[self.Open] - self.df['_pre']) / self.df[self.close] * 100).__round__(2).fillna(0)
            self.df['rate_high'] = ((self.df[self.high] - self.df['_pre']) / self.df[self.close] * 100).__round__(2).fillna(0)
            self.df['rate_low'] = ((self.df[self.low] - self.df['_pre']) / self.df[self.close] * 100).__round__(2).fillna(0)
            if self.volume:
                self.df['compare_volume'] = (self.df[self.volume] - self.df[self.volume].shift(1)).fillna(0)
                self.df['rate_volume'] = (self.df['compare_volume'] / self.df[self.volume].shift(1) * 100).__round__(2).fillna(0)

        self.df['_boxheight'] = (self.df[self.high] - self.df[self.low]) / 5
        self.df['_boxmin'] = self.df[self.low] - self.df['_boxheight']
        self.df['_boxmax'] = self.df[self.high] + self.df['_boxheight']
        if self.volume: self.df['_volumeboxmax'] = self.df[self.volume] * 1.13
        return

    def _set_lim(self, xmin, xmax, simpler=False, set_ma=True):
        super()._set_lim(xmin, xmax, simpler, set_ma)

        psub = (self.price_ymax - self.price_ymin)
        self.min_candleboxheight = psub / 8

        pydistance = psub / 20
        self.text_date_price.set_y(self.price_ymin + pydistance)

        self.min_volumeboxheight = self.volume_ymax / 4

        vxsub = self.vxmax - self.vxmin
        self.vmiddle = self.vxmax - int((vxsub) / 2)

        vxdistance = vxsub / 50
        self.v0, self.v1 = (self.vxmin + vxdistance, self.vxmax - vxdistance)
        self.vsixth = self.vxmin + int((vxsub) / 6)
        self.veighth = self.vxmin + int((vxsub) / 8)

        yvolume = self.volume_ymax * 0.85
        self.text_date_volume.set_y(yvolume)

        # 정보 텍스트박스
        self.text_price_info.set_y(self.price_ymax - pydistance)
        self.text_volume_info.set_y(yvolume)
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
            self.in_price_chart = ax is self.ax_price
            self.in_volume_chart = False if self.in_price_chart else ax is self.ax_volume

        return

    def _get_x(self, e: MouseEvent):
        self.intx = e.xdata.__int__()
        if self.intx < 0: self.intx = None
        else:
            try: self.list_index[self.intx]
            except: self.intx = None
        return


class LineMixin(EventMixin):
    digit_price, digit_volume = (0, 0)
    in_candle, in_volumebar = (False, False)

    def _on_move(self, e):
        super()._on_move(e)

        self._restore_region()

        if self.in_price_chart: self._on_move_price_chart(e)
        elif self.in_volume_chart: self._on_move_volume_chart(e)

        self._blit()
        return

    def _on_move_price_chart(self, e: MouseEvent):
        x, y = (e.xdata, e.ydata)

        self.price_crossline.set_segments([((x, self.price_ymin), (x, self.price_ymax)), ((self.vxmin, y), (self.vxmax, y))])
        self.volume_crossline.set_segments([((x, 0), (x, self.volume_ymax))])
        self._draw_crossline()

        renderer = self.figure.canvas.renderer

        # 가격
        self.text_price.set_text(f'{float_to_str(y, self.digit_price)}{self.unit_price}')
        self.text_price.set_x(self.v0 if self.veighth < x else self.vsixth)
        self.text_price.set_y(y)
        self.text_price.draw(renderer)

        index = self.intx
        if index is None: self.in_candle = False
        else:
            # 기준시간 표시
            self.text_date_volume.set_text(f'{self.df[self.date][index]}')
            self.text_date_volume.set_x(x)
            self.text_date_volume.draw(renderer)

            # 캔들 강조
            low = self.df['_boxmin'][index]
            high = self.df['_boxmax'][index]
            sub = high - low
            if sub < self.min_candleboxheight:
                sub = (self.min_candleboxheight - sub) / 2
                low -= sub
                high += sub

            if high < y or y < low: self.in_candle = False
            else:
                self.in_candle = True
                x1, x2 = (index-0.3, index+1.4)
                self.price_box.set_segments([((x1, high), (x2, high), (x2, low), (x1, low), (x1, high))])
                self.price_box.draw(renderer)
        return

    def _draw_crossline(self):
        renderer = self.figure.canvas.renderer
        self.price_crossline.draw(renderer)
        self.volume_crossline.draw(renderer)
        return

    def _on_move_volume_chart(self, e: MouseEvent):
        x, y = (e.xdata, e.ydata)

        self.price_crossline.set_segments([((x, self.price_ymin), (x, self.price_ymax))])
        self.volume_crossline.set_segments([((x, 0), (x, self.volume_ymax)), ((self.vxmin, y), (self.vxmax, y))])
        self._draw_crossline()

        if not self.volume: return

        renderer = self.figure.canvas.renderer

        # 거래량
        self.text_volume.set_text(f'{float_to_str(y, self.digit_volume)}{self.unit_volume}')
        self.text_volume.set_x(self.v0 if self.veighth < x else self.vsixth)
        self.text_volume.set_y(y)
        self.text_volume.draw(renderer)

        index = self.intx
        if index is None: self.in_volumebar = False
        else:
            # 기준시간 표시
            self.text_date_price.set_text(f'{self.df[self.date][index]}')
            self.text_date_price.set_x(x)
            self.text_date_price.draw(renderer)

            # 거래량 강조
            high = self.df[self.volume][index] * 1.15
            low = 0
            if high < self.min_volumeboxheight: high = self.min_volumeboxheight

            if high < y or y < low: self.in_volumebar = False
            else:
                self.in_volumebar = True
                x1, x2 = (index-0.3, index+1.4)
                self.volume_box.set_segments([((x1, high), (x2, high), (x2, low), (x1, low), (x1, high))])
                self.volume_box.draw(renderer)
        return


format_candleinfo_ko = '{dt}\n\n종가:　 {close}\n등락률: {rate}\n대비:　 {compare}\n시가:　 {open}({rate_open})\n고가:　 {high}({rate_high})\n저가:　 {low}({rate_low})\n거래량: {volume}({rate_volume})'
format_volumeinfo_ko = '{dt}\n\n거래량:　　　 {volume}\n거래량증가율: {rate_volume}\n대비:　　　　 {compare}'
format_candleinfo_en = '{dt}\n\nclose:   {close}\nrate:    {rate}\ncompare: {compare}\nopen:    {open}({rate_open})\nhigh:    {high}({rate_high})\nlow:     {low}({rate_low})\nvolume:  {volume}({rate_volume})'
format_volumeinfo_en = '{dt}\n\nvolume:      {volume}\nvolume rate: {rate_volume}\ncompare:     {compare}'

class InfoMixin(LineMixin):
    fraction = False
    format_candleinfo = format_candleinfo_ko
    format_volumeinfo = format_volumeinfo_ko

    def set_data(self, df, sort_df=True, calc_ma=True, set_candlecolor=True, set_volumecolor=True, calc_info=True, *args, **kwargs):
        super().set_data(df, sort_df, calc_ma, set_candlecolor, set_volumecolor, calc_info, *args, **kwargs)

        self._length_text = self.df[(self.volume if self.volume else self.high)].apply(lambda x: len(f'{x:,}')).max()
        return

    def _on_move_price_chart(self, e):
        super()._on_move_price_chart(e)

        # 캔들 강조 확인
        if not self.in_candle: return

        # 캔들 정보
        self.text_price_info.set_text(self._get_info(self.intx))

        if self.vmiddle < e.xdata: self.text_price_info.set_x(self.v0)
        else:
            # self.text_price_info.set_x(self.vmax - self.x_distance)
            # self.text_price_info.set_horizontalalignment('right')
            # 텍스트박스 크기 가져오기
            bbox = self.text_price_info.get_window_extent().transformed(self.ax_price.transData.inverted())
            width = bbox.x1 - bbox.x0
            self.text_price_info.set_x(self.v1 - width)

        self.text_price_info.draw(self.figure.canvas.renderer)
        return

    def _on_move_volume_chart(self, e):
        super()._on_move_volume_chart(e)

        # 거래량 강조 확인
        if not self.in_volumebar: return

        # 거래량 정보
        self.text_volume_info.set_text(self._get_info(self.intx, is_price=False))

        if self.vmiddle < e.xdata: self.text_volume_info.set_x(self.v0)
        else:
            # self.text_volume_info.set_x(self.vmax - self.x_distance)
            # self.text_volume_info.set_horizontalalignment('right')
            # 텍스트박스 크기 가져오기
            bbox = self.text_volume_info.get_window_extent().transformed(self.ax_price.transData.inverted())
            width = bbox.x1 - bbox.x0
            self.text_volume_info.set_x(self.v1 - width)

        self.text_volume_info.draw(self.figure.canvas.renderer)
        return

    def _get_info(self, index, is_price=True):
        dt = self.df[self.date][index]
        if not self.volume:
            v, vr = ('-', '-%')
        else:
            v = self.df[self.volume][index]
            v = float_to_str(v, self.digit_volume)
            # if not v % 1: v = int(v)
            vr = self.df['rate_volume'][index]
            vr = f'{vr:+06,.2f}%'

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

                text = self.format_candleinfo.format(
                    dt=dt,
                    close=f'{c:>{self._length_text}}{self.unit_price}',
                    rate=f'{r:>{self._length_text}}%',
                    compare=f'{com:>{self._length_text}}{self.unit_price}',
                    open=f'{o:>{self._length_text}}{self.unit_price}', rate_open=f'{Or:+06,.2f}%',
                    high=f'{h:>{self._length_text}}{self.unit_price}', rate_high=f'{hr:+06,.2f}%',
                    low=f'{l:>{self._length_text}}{self.unit_price}', rate_low=f'{lr:+06,.2f}%',
                    volume=f'{v:>{self._length_text}}{self.unit_volume}', rate_volume=vr,
                )
            else:
                o, h, l, c = (float_to_str(o, self.digit_price), float_to_str(h, self.digit_price), float_to_str(l, self.digit_price), float_to_str(c, self.digit_price))
                com = float_to_str(compare, self.digit_price, plus=True)

                text = self.format_candleinfo.format(
                    dt=dt,
                    close=f'{c:>{self._length_text}}{self.unit_price}',
                    rate=f'{r:>{self._length_text}}%',
                    compare=f'{com:>{self._length_text}}{self.unit_price}',
                    open=f'{o:>{self._length_text}}{self.unit_price}', rate_open=f'{Or:+06,.2f}%',
                    high=f'{h:>{self._length_text}}{self.unit_price}', rate_high=f'{hr:+06,.2f}%',
                    low=f'{l:>{self._length_text}}{self.unit_price}', rate_low=f'{lr:+06,.2f}%',
                    volume=f'{v:>{self._length_text}}{self.unit_volume}', rate_volume=vr,
                )
        elif self.volume:
            compare = self.df['compare_volume'][index]
            com = float_to_str(compare, self.digit_volume, plus=True)
            text = self.format_volumeinfo.format(
                dt=dt,
                volume=f'{v:>{self._length_text}}{self.unit_volume}',
                rate_volume=f'{vr:>{self._length_text}}%',
                compare=f'{com:>{self._length_text}}{self.unit_volume}',
            )
        else: text = ''
        return text


class BaseMixin(InfoMixin):
    pass


class Chart(BaseMixin, Mixin):
    def _add_collection(self):
        super()._add_collection()
        return self.add_artist()

    def _draw_artist(self):
        super()._draw_artist()
        return self.draw_artist()

    def _get_segments(self):
        self.generate_data()
        return super()._get_segments()

    def _on_draw(self, e):
        super()._on_draw(e)
        return self.on_draw(e)

    def _on_pick(self, e):
        self.on_pick(e)
        return super()._on_pick(e)

    def _set_candle_segments(self, index_start, index_end):
        super()._set_candle_segments(index_start, index_end)
        self.set_segment(index_start, index_end)
        return

    def _set_wick_segments(self, index_start, index_end, simpler=False):
        super()._set_wick_segments(index_start, index_end, simpler)
        self.set_segment(index_start, index_end, simpler)
        return

    def _set_line_segments(self, index_start, index_end, simpler=False, set_ma=True):
        super()._set_line_segments(index_start, index_end, simpler, set_ma)
        self.set_segment(index_start, index_end, simpler, set_ma)
        return

    def _on_move(self, e):
        super()._on_move(e)
        return self.on_move(e)

