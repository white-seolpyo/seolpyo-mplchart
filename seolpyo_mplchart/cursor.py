from fractions import Fraction

from matplotlib.backend_bases import MouseEvent
from matplotlib.collections import LineCollection
from matplotlib.text import Text
import pandas as pd


from .draw import DrawMixin, Chart as CM
from .utils import float_to_str


class Mixin:
    def create_background(self):
        "This function works befor canvas.copy_from_bbox()."
        return
    def on_draw(self, e):
        "This function works if draw event active."
        return


class CollectionMixin(DrawMixin):
    lineKwargs = dict(edgecolor='k', linewidth=1, linestyle='-')
    textboxKwargs = dict(boxstyle='round', facecolor='w')

    def _add_collection(self):
        super()._add_collection()
        self.sliderline = LineCollection([], animated=True, **self.lineKwargs)
        self.ax_slider.add_artist(self.sliderline)
        self.slider_text = Text(animated=True, bbox=self.textboxKwargs, verticalalignment='top', horizontalalignment='center')
        self.ax_slider.add_artist(self.slider_text)

        self.price_vline = LineCollection([], animated=True, **self.lineKwargs)
        self.ax_price.add_artist(self.price_vline)
        self.text_date_price = Text(animated=True, bbox=self.textboxKwargs, verticalalignment='bottom', horizontalalignment='center')
        self.ax_price.add_artist(self.text_date_price)
        self.text_price = Text(animated=True, bbox=self.textboxKwargs, verticalalignment='center', horizontalalignment='left')
        self.ax_price.add_artist(self.text_price)

        self.volumeh_vline = LineCollection([], animated=True, **self.lineKwargs)
        self.ax_volume.add_artist(self.volumeh_vline)
        self.text_date_volume = Text(animated=True, bbox=self.textboxKwargs, verticalalignment='top', horizontalalignment='center')
        self.ax_volume.add_artist(self.text_date_volume)
        self.text_volume = Text(animated=True, bbox=self.textboxKwargs, verticalalignment='center', horizontalalignment='left')
        self.ax_volume.add_artist(self.text_volume)

        self.price_hline = LineCollection([], animated=True, **self.lineKwargs)
        self.ax_price.add_artist(self.price_hline)
        self.price_box = LineCollection([], animated=True, linewidth=1.2, edgecolor='k')
        self.ax_price.add_artist(self.price_box)
        self.text_price_info = Text(animated=True, bbox=self.textboxKwargs, verticalalignment='top', horizontalalignment='left')
        self.ax_price.add_artist(self.text_price_info)

        self.volume_hline = LineCollection([], animated=True, **self.lineKwargs)
        self.ax_volume.add_artist(self.volume_hline)
        self.volume_box = LineCollection([], animated=True, linewidth=1.2, edgecolor='k')
        self.ax_volume.add_artist(self.volume_box)
        self.text_volume_info = Text(animated=True, bbox=self.textboxKwargs, verticalalignment='top', horizontalalignment='left')
        self.ax_volume.add_artist(self.text_volume_info)

        return


_set_key = {'rate', 'compare', 'rate_open', 'rate_high', 'rate_low', 'rate_volume',}

class DataMixin(CollectionMixin):
    def _generate_data(self, df: pd.DataFrame):
        for i in ['date', 'Open', 'high', 'low', 'close', 'volume']:
            v = getattr(self, i)
            if v in _set_key: raise Exception(f'you can not set "self.{i}" value in {_set_key}.\nself.{i}={v!r}')

        super()._generate_data(df)

        df['rate'] = ((df[self.close] - df[self.close].shift(1)) / df[self.close] * 100).__round__(2).fillna(0)
        df['compare'] = (df[self.close] - df[self.close].shift(1)).fillna(0)
        df['rate_open'] = ((df[self.Open] - df[self.close].shift(1)) / df[self.close] * 100).__round__(2).fillna(0)
        df['rate_high'] = ((df[self.high] - df[self.close].shift(1)) / df[self.close] * 100).__round__(2).fillna(0)
        df['rate_low'] = ((df[self.low] - df[self.close].shift(1)) / df[self.close] * 100).__round__(2).fillna(0)
        df['rate_volume'] = ((df[self.volume] - df[self.volume].shift(1)) /  df[self.volume].shift(1) * 100).__round__(2).fillna(0)
        return


class LineMixin(DataMixin):
    in_slider, in_price, in_volume = (False, False, False)

    intx, in_index = (None, False)
    _in_candle, _in_volumebar = (False, False)

    def _connect_event(self):
        super()._connect_event()
        self.canvas.mpl_connect('motion_notify_event', lambda x: self._on_move(x))
        return

    def _blit(self):
        self.canvas.blit()
        return

    def set_data(self, df):
        super().set_data(df)

        self.vmin, self.vmax = (self.xmin, self.xmax)
        return

    def _on_move(self, e):
        self._restore_region()

        self._on_move_action(e)

        if self.in_slider or self.in_price or self.in_volume:
            self._slider_move_action(e)
        if self.in_price or self.in_volume:
            self._chart_move_action(e)

        self._blit()
        return

    def _on_move_action(self, e: MouseEvent):
        if not e.inaxes:
            self.intx, self.in_index = (None, False)
        else:
            self._check_ax(e)
            x, y = (e.xdata, e.ydata)
            self.intx = x.__int__()
            if self.intx < 0: self.in_index = False
            else:
                try: self.df['x'][self.intx]
                except: self.in_index = False
                else: self.in_index = True
        return

    def _check_ax(self, e: MouseEvent):
        ax = e.inaxes

        self.in_slider = ax is self.ax_slider
        self.in_price = False if self.in_slider else ax is self.ax_price
        self.in_volume = False if (self.in_slider or self.in_price) else ax is self.ax_volume
        return

    def _slider_move_action(self, e: MouseEvent):
        x = e.xdata

        # 수직선
        self.sliderline.set_segments([((x, self._slider_ymin), (x, self._slider_ymax))])
        self.ax_slider.draw_artist(self.sliderline)
        return

    def _chart_move_action(self, e: MouseEvent):
        x, y = (e.xdata, e.ydata)
        if not y: return
        roundy = y.__round__()

        self.price_vline.set_segments([((x, self._price_ymin), (x, self._price_ymax))])
        self.volumeh_vline.set_segments([((x, 0), (x, self._vol_ymax))])
        self.ax_price.draw_artist(self.price_vline)
        self.ax_volume.draw_artist(self.volumeh_vline)

        if self.in_price: self._price_move_action(x, y, roundy)
        else: self._volume_move_action(x, y, roundy)
        return

    def _price_move_action(self, _, y, roundy):
        # 수평선
        self.price_hline.set_segments([((self.vmin, y), (self.vmax, y))])
        self.ax_price.draw_artist(self.price_hline)

        # 가격
        self.text_price.set_text(f'{roundy:,}{self.unit_price}')
        self.text_price.set_y(y)
        self.ax_price.draw_artist(self.text_price)

        # 캔들 강조
        if self.in_index:
            intx = self.intx
            
            high = self.df[self.high][intx] * 1.02
            low = self.df[self.low][intx] * 0.98
            if high < y or y < low: self._in_candle = False
            else:
                self._in_candle = True
                x1, x2 = (intx-0.3, intx+1.4)
                self.price_box.set_segments([((x1, high), (x2, high), (x2, low), (x1, low), (x1, high))])
                self.ax_price.draw_artist(self.price_box)
        return

    def _volume_move_action(self, _, y, roundy):
        # 수평선
        self.volume_hline.set_segments([((self.vmin, y), (self.vmax, y))])
        self.ax_volume.draw_artist(self.volume_hline)

        # 거래량
        self.text_volume.set_text(f'{roundy:,}{self.unit_volume}')
        self.text_volume.set_y(y)
        self.ax_volume.draw_artist(self.text_volume)

        # 거래량 강조
        if self.in_index:
            intx = self.intx

            high = self.df[self.volume][intx] * 1.1
            low = 0
            self._volumerange = (0, high)
            if high < y or y < low: self._in_volumebar: False
            else:
                self._in_volumebar = True
                x1, x2 = (intx-0.3, intx+1.4)
                self.volume_box.set_segments([((x1, high), (x2, high), (x2, low), (x1, low), (x1, high))])
                self.ax_volume.draw_artist(self.volume_box)
        return


class InfoMixin(LineMixin):
    fraction = False
    candleformat = '{}\n\n종가:　 {}\n등락률: {}\n대비:　 {}\n시가:　 {}({})\n고가:　 {}({})\n저가:　 {}({})\n거래량: {}({})'
    volumeformat = '{}\n\n거래량　　　: {}\n거래량증가율: {}'
    digit_price, digit_volume = (0, 0)

    def set_data(self, df):
        super().set_data(df)

        # 슬라이더 날짜 텍스트 y 위치
        y = self._slider_ymax - (self._slider_ymax - self._slider_ymin) / 6
        self.slider_text.set_y(y)

        v = self.df[self.volume].max()
        self._length_text = len(f'{v:,}')
        self.set_text_coordante(self.xmin, self.xmax, self._price_ymin, self._price_ymax, self._vol_ymax)

        return

    def set_text_coordante(self, vmin, vmax, pmin, pmax, volmax):
        # 주가, 거래량 텍스트 x 위치
        x_distance = (vmax - vmin) / 30
        self.v0, self.v1 = (vmin + x_distance, vmax - x_distance)
        self.text_price.set_x(self.v0)
        self.text_volume.set_x(self.v0)

        self.vmin, self.vmax = (vmin, vmax)
        self.vmiddle = vmax - int((vmax - vmin) / 2)

        # 주가 날짜 텍스트 y 위치
        y = (pmax - pmin) / 20 + pmin
        self.text_date_price.set_y(y)
        # 주가 정보 y 위치
        y = pmax - (pmax - pmin) / 20
        self.text_price_info.set_y(y)

        # 거래량 날짜 텍스트 y 위치
        y = volmax * 0.85
        self.text_date_volume.set_y(y)
        # 거래량 정보 y 위치
        self.text_volume_info.set_y(y)

        return

    def _slider_move_action(self, e):
        super()._slider_move_action(e)

        intx = self.intx

        if self.in_slider and self.in_index:
            self.slider_text.set_text(f'{self.df[self.date][intx]}')
            self.slider_text.set_x(e.xdata)
            self.ax_slider.draw_artist(self.slider_text)
        return

    def _price_move_action(self, x, y, roundy):
        super()._price_move_action(x, y, roundy)
        if not self.in_index: return
        intx = self.intx

        # 텍스트
        text = f'{self.df[self.date][intx]}'
        self.text_date_volume.set_text(text)
        self.text_date_volume.set_x(x)
        self.ax_volume.draw_artist(self.text_date_volume)

        # 캔들 강조
        if self.in_price and self._in_candle:
            # 캔들 정보
            self.text_price_info.set_text(self._get_info(intx))
            if x < self.vmiddle:
                # 텍스트박스 크기 가져오기
                bbox = self.text_price_info.get_window_extent().transformed(self.ax_price.transData.inverted())
                width = bbox.x1 - bbox.x0
                self.text_price_info.set_x(self.v1 - width)
            else:
                self.text_price_info.set_x(self.v0)
                self.text_price_info.set_horizontalalignment('left')
            self.ax_price.draw_artist(self.text_price_info)
        return

    def _volume_move_action(self, x, y, roundy):
        super()._volume_move_action(x, y, roundy)
        if not self.in_index: return
        intx = self.intx

        text = f'{self.df[self.date][intx]}'
        self.text_date_price.set_text(text)
        self.text_date_price.set_x(x)
        self.ax_price.draw_artist(self.text_date_price)

        # 거래량 강조
        if self.in_volume and self._in_volumebar:
            # 거래량 정보
            if x < self.vmiddle:
                bbox = self.text_volume_info.get_window_extent().transformed(self.ax_price.transData.inverted())
                width = bbox.x1 - bbox.x0
                self.text_volume_info.set_x(self.v1 - width)
            else:
                self.text_volume_info.set_x(self.v0)
                self.text_volume_info.set_horizontalalignment('left')
            self.text_volume_info.set_text(self._get_info(intx, False))
            self.ax_volume.draw_artist(self.text_volume_info)
        return

    def _get_info(self, index, is_price=True):
        dt = self.df[self.date][index]
        v = self.df[self.volume][index]
        v = float_to_str(v, self.digit_volume)
        vr = self.df['rate_volume'][index]
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

                text = self.candleformat.format(
                    dt,
                    f'{c:>{self._length_text}}{self.unit_price}',
                    f'{r:>{self._length_text}}%',
                    f'{com:>{self._length_text}}{self.unit_price}',
                    f'{o:>{self._length_text}}{self.unit_price}', f'{Or:+06,.2f}%',
                    f'{h:>{self._length_text}}{self.unit_price}', f'{hr:+06,.2f}%',
                    f'{l:>{self._length_text}}{self.unit_price}', f'{lr:+06,.2f}%',
                    f'{v:>{self._length_text}}{self.unit_volume}', f'{vr:+06,.2f}%',
                )
            else:
                o, h, l, c = (float_to_str(o, self.digit_price), float_to_str(h, self.digit_price), float_to_str(l, self.digit_price), float_to_str(c, self.digit_price))
                com = float_to_str(compare, self.digit_price, plus=True)

                text = self.candleformat.format(
                    dt,
                    f'{c:>{self._length_text}}{self.unit_price}',
                    f'{r:>{self._length_text}}%',
                    f'{com:>{self._length_text}}{self.unit_price}',
                    f'{o:>{self._length_text}}{self.unit_price}', f'{Or:+06,.2f}%',
                    f'{h:>{self._length_text}}{self.unit_price}', f'{hr:+06,.2f}%',
                    f'{l:>{self._length_text}}{self.unit_price}', f'{lr:+06,.2f}%',
                    f'{v:>{self._length_text}}{self.unit_volume}', f'{vr:+06,.2f}%',
                )
        else:
            vrate = f'{vr:+06,.2f}'
            text = self.volumeformat.format(
                dt,
                f'{v:>{self._length_text}}{self.unit_volume}',
                f'{vrate:>{self._length_text}}%',
            )
        return text


class CursorMixin(InfoMixin):
    pass


class Chart(CursorMixin, CM, Mixin):
    def _generate_data(self, df):
        super()._generate_data(df)
        return self.generate_data(df)

    def _on_draw(self, e):
        super()._on_draw(e)
        return self.on_draw(e)

    def _on_pick(self, e):
        self.on_pick(e)
        return super()._on_pick(e)

    def _draw_artist(self):
        super()._draw_artist()
        return self.create_background()

    def _blit(self):
        super()._blit()
        return self.on_blit()

    def _on_move(self, e):
        super()._on_move(e)
        return self.on_move(e)


if __name__ == '__main__':
    import json
    from time import time

    import matplotlib.pyplot as plt
    from pathlib import Path

    file = Path(__file__).parent / 'data/samsung.txt'
    file = Path(__file__).parent / 'data/apple.txt'
    with open(file, 'r', encoding='utf-8') as txt:
        data = json.load(txt)
    data = data[:100]
    df = pd.DataFrame(data)

    t = time()
    c = CursorMixin()
    c.unit_price = '$'
    # c.fraction = True
    c.set_data(df=df)
    t2 = time() - t
    print(f'{t2=}')
    plt.show()


