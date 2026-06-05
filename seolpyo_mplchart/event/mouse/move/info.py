from fractions import Fraction
from typing import TypedDict

from matplotlib.axes import Axes
from matplotlib.text import Text
import pandas as pd

from ....utils.formatter import Formatter, FormatterEN


format_info_price = """\
{dt}

종가:　 {close}
등락률: {rate}
대비:　 {change}
시가:　 {open}({rate_open})
고가:　 {high}({rate_high})
저가:　 {low}({rate_low})
거래량: {volume}({rate_volume})\
"""
format_info_volume = """\
{dt}

거래량:　　　 {volume}
거래량증가율: {rate_volume}
대비:　　　　 {change}\
"""


format_info_price_en = """\
{dt}

close:      {close}
rate:        {rate}
change: {change}
open:      {open}({rate_open})
high:       {high}({rate_high})
low:        {low}({rate_low})
volume:  {volume}({rate_volume})\
"""
format_info_volume_en = """\
{dt}

volume:      {volume}
volume rate: {rate_volume}
change:     {change}\
"""


class InfoPriceData(TypedDict):
    dt: any
    close: str
    rate: str
    change: str
    open: str
    high: str
    low: str
    volume: str


class InfoVolumeData(TypedDict):
    dt: any
    volume: str
    rate_volume: str
    change: str


class KwargMixin:
    key_volume: str

    FORMATTER: Formatter
    df: pd.DataFrame

    digit_price: int
    digit_volume: int
    _length_text: int

    fraction: bool

    def get_info_kwargs(self, idx, *, is_price: bool) -> InfoPriceData|InfoVolumeData:
        """
        get text info kwargs

        Args:
            is_price (bool): is price chart info or not

        Returns:
            dict[str, any]: text info kwargs
        """
        kwargs = self._get_info_kwargs(idx, is_price=is_price)
        # print(f'{kwargs=}')
        return kwargs

    def num_to_fraction(self, value):
        if not value:
            return '0'

        if 9_999 < value:
            return self.FORMATTER.price_formatter(round(value, self.digit_price), None)

        str_value = str(value)
        if '.' not in str_value:
            return self.FORMATTER.price_formatter(value, None)

        int_value, deci_value = str_value.split('.')
        if deci_value == '0':
            return self.FORMATTER.price_formatter(value, None)

        int_value = int(int_value)
        frac = Fraction(f'0.{deci_value}')
        # print(f'{value=}')
        # print(f'{deci_value=}')
        # print(f'{(frac.numerator, frac.denominator)=}')
        # print(f'{(9 < frac.denominator)=}')

        if 9 < frac.denominator:
            return self.FORMATTER.price_formatter(round(value, self.digit_price), None)

        if int_value:
            return f"{int_value:,} {frac}{self.FORMATTER.price_word}"

        return f'　 {frac}{self.FORMATTER.price_word}'

    def _get_info_kwargs(self, idx: int, *, is_price=True):
        # print(f'{self._length_text=}')
        try:
            series = self.df.iloc[idx]
        except IndexError:
            return {}
        # print(series)

        dt = series['date']
        if not self.key_volume:
            v, vr = ('-', '-')
        else:
            v, vr = series.loc[['volume', 'rate_volume']]
            v = self.FORMATTER.volume_formatter(round(v, self.digit_volume), None)
            # print(f'{v=}')
            # if not v % 1:
            #     v = int(v)
            vr = f'{vr:+06,.2f}'

        if is_price:
            o, h, l, c = (series['open'], series['high'], series['low'], series['close'])
            rate, change = (series['rate'], series['change'])
            r = f'{rate:+06,.2f}'
            Or, hr, lr = (series['rate_open'], series['rate_high'], series['rate_low'])
            # print(f'{(rate, change)=}')

            if self.fraction:
                data = {}
                for value, key in [
                    [c, 'close'],
                    [change, 'change'],
                    [o, 'open'],
                    [h, 'high'],
                    [l, 'low'],
                ]:
                    v = self.num_to_fraction(value)
                    if key == 'change' and 0 <= value:
                        if v.startswith('　'):
                            v = v.replace('　 ', '　 +',)
                        else:
                            v = f'+{v}'
                    data[key] = v
                # print(f'{data=}')

                kwargs = dict(
                    is_price=is_price,
                    dt=dt,
                    close=f'{data["close"]:>{self._length_text}}',
                    rate=f'{r:>{self._length_text}}%',
                    change=f'{data["change"]:>{self._length_text}}',
                    open=f'{data["open"]:>{self._length_text}}', rate_open=f'{Or:+06,.2f}%',
                    high=f'{data["high"]:>{self._length_text}}', rate_high=f'{hr:+06,.2f}%',
                    low=f'{data["low"]:>{self._length_text}}', rate_low=f'{lr:+06,.2f}%',
                    volume=f'{v:>{self._length_text}}', rate_volume=f'{vr}%',
                )
            else:
                o, h, l, c = (
                    self.FORMATTER.price_formatter(round(o, self.digit_price), None),
                    self.FORMATTER.price_formatter(round(h, self.digit_price), None),
                    self.FORMATTER.price_formatter(round(l, self.digit_price), None),
                    self.FORMATTER.price_formatter(round(c, self.digit_price), None),
                )
                ch = self.FORMATTER.price_formatter(round(change, self.digit_price), None)
                if 0 <= change:
                    ch = f'+{ch}'
                # print(f'{change=}')

                kwargs = dict(
                    is_price=is_price,
                    dt=dt,
                    close=f'{c:>{self._length_text}}',
                    rate=f'{r:>{self._length_text}}%',
                    change=f'{ch:>{self._length_text}}',
                    open=f'{o:>{self._length_text}}', rate_open=f'{Or:+06,.2f}%',
                    high=f'{h:>{self._length_text}}', rate_high=f'{hr:+06,.2f}%',
                    low=f'{l:>{self._length_text}}', rate_low=f'{lr:+06,.2f}%',
                    volume=f'{v:>{self._length_text}}', rate_volume=f'{vr}%',
                )
        elif self.key_volume:
            change = self.df.loc[idx, 'change_volume']
            ch = self.FORMATTER.volume_formatter(round(change, self.digit_volume), None)
            if 0 <= change:
                ch = f'+{ch}'
            kwargs = dict(
                is_price=is_price,
                dt=dt,
                volume=f'{v:>{self._length_text}}',
                rate_volume=f'{vr:>{self._length_text}}%',
                change=f'{ch:>{self._length_text}}',
            )
        else:
            kwargs = {}

        return kwargs


class InfoMixin(KwargMixin):
    key_volume: str

    fraction = False

    price_info_format = format_info_price
    volume_info_format = format_info_volume

    artist_info_price: Text
    artist_info_volume: Text

    in_box_price: bool
    in_box_volume: bool

    def draw_info(self, idx):
        if self.in_box_price:
            self.draw_info_price(idx)
        elif self.in_box_volume:
            self.draw_info_volume(idx)
        return

    def draw_info_price(self, idx):
        kwargs = self.get_info_kwargs(idx, is_price=True)
        text = self.price_info_format.format(**kwargs)
        self.artist_info_price.set_text(text)

        ax: Axes = self.get_ax_price()

        # 정보 텍스트박스 y축 설정
        ymin, ymax = ax.get_ylim()
        ysub = ymax - ymin
        ydistance = ysub / 20
        self.artist_info_price.set_y(ymax - ydistance)

        xmin, xmax = ax.get_xlim()
        xsub = xmax - xmin
        middle = xmax - (xsub / 2)
        xdistance = xsub / 50

        # 정보 텍스트를 중앙에 몰리게 설정할 수도 있지만,
        # 그런 경우 차트를 가리므로 좌우 끝단에 위치하도록 설정
        if middle < idx:
            x = xmin + xdistance
            self.artist_info_price.set_x(x)
        else:
            # self.artist_info_price.set_x(self.vmax - self.x_distance)
            # self.artist_info_price.set_horizontalalignment('right')
            # 텍스트박스 크기 가져오기
            bbox = self.artist_info_price.get_window_extent()\
                .transformed(ax.transData.inverted())
            width = bbox.x1 - bbox.x0

            x = (xmax - xdistance) - width
            self.artist_info_price.set_x(x)

        self.artist_info_price.draw(self.renderer)
        return 1

    def draw_info_volume(self, idx):
        text = ''
        if self.key_volume:
            kwargs = self.get_info_kwargs(idx, is_price=False)
            text = self.volume_info_format.format(**kwargs)
            # print(f'{kwargs=}')
            # print('volume_format')
            # print(self.volume_format)
            # print('text')
            # print(text)
        self.artist_info_volume.set_text(text)

        ax: Axes = self.get_ax_volume()

        # 정보 텍스트박스 y축 설정
        ymin, ymax = ax.get_ylim()
        ysub = ymax - ymin
        ydistance = ysub / 10
        self.artist_info_volume.set_y(ymax - ydistance)

        xmin, xmax = ax.get_xlim()
        xsub = xmax - xmin
        middle = xmax - (xsub / 2)
        xdistance = xsub / 50

        if middle < idx:
            x = xmin + xdistance
            self.artist_info_volume.set_x(x)
        else:
            # self.artist_info_volume.set_x(self.vmax - self.x_distance)
            # self.artist_info_volume.set_horizontalalignment('right')
            # 텍스트박스 크기 가져오기
            bbox = self.artist_info_volume.get_window_extent()\
                .transformed(ax.transData.inverted())
            width = bbox.x1 - bbox.x0

            x = xmax - xdistance - width
            self.artist_info_volume.set_x(x)

        self.artist_info_volume.draw(self.renderer)
        return 1

