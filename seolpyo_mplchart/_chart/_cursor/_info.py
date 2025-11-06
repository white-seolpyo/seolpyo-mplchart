from fractions import Fraction

from matplotlib.backend_bases import MouseEvent

from ._cursor import BaseMixin as Base
from ..._config.utils import float_to_str


class InfoMixin(Base):
    fraction = False

    def _set_data(self, df, *args, **kwargs):
        super()._set_data(df, *args, **kwargs)

        self._set_length_text()
        return

    def _set_length_text(self):
        func = lambda x: len(self.CONFIG.UNIT.func(x, digit=self.CONFIG.UNIT.digit, word=self.CONFIG.UNIT.price))
        self._length_text = self.df['high'].apply(func).max()

        if self.key_volume:
            func = lambda x: len(self.CONFIG.UNIT.func(x, digit=self.CONFIG.UNIT.digit_volume, word=self.CONFIG.UNIT.volume))
            lenth_volume = self.df['volume'].apply(func).max()
            # print(f'{self._length_text=}')
            # print(f'{lenth_volume=}')
            if self._length_text < lenth_volume:
                self._length_text = lenth_volume
        return

    def _draw_box_artist(self, e):
        super()._draw_box_artist(e)

        if self.intx is not None:
            if self.in_candle:
                self._draw_candle_info_artist(e)
            elif self.key_volume and self.in_volumebar:
                self._draw_volume_info_artist(e)
        return

    def _draw_candle_info_artist(self, e: MouseEvent):
        # 캔들 정보
        self.artist_info_candle.set_text(self._get_info(self.intx))

        # 정보 텍스트를 중앙에 몰리게 설정할 수도 있지만,
        # 그런 경우 차트를 가리므로 좌우 끝단에 위치하도록 설정
        if self.vmiddle < e.xdata:
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

    def _draw_volume_info_artist(self, e: MouseEvent):
        # 거래량 정보
        self.artist_info_volume.set_text(self._get_info(self.intx, is_price=False))

        if self.vmiddle < e.xdata:
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

    def _get_info(self, index, is_price=True):
        # print(f'{self._length_text=}')
        dt = self.df.loc[index, 'date']
        if not self.key_volume:
            v, vr = ('-', '-')
        else:
            v = self.df.loc[index, 'volume']
            # print(f'{self.CONFIG.UNIT.digit_volume=}')
            v = float_to_str(v, digit=self.CONFIG.UNIT.digit_volume)
            # if not v % 1:
            #     v = int(v)
            vr = self.df.loc[index, 'rate_volume']
            vr = f'{vr:+06,.2f}'

        if is_price:
            o, h, l, c = (self.df.loc[index, 'open'], self.df.loc[index, 'high'], self.df.loc[index, 'low'], self.df.loc[index, 'close'])
            rate, compare = (self.df.loc[index, 'rate'], self.df.loc[index, 'compare'])
            r = f'{rate:+06,.2f}'
            Or, hr, lr = (self.df.loc[index, 'rate_open'], self.df.loc[index, 'rate_high'], self.df.loc[index, 'rate_low'])

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
            compare = self.df.loc[index, 'compare_volume']
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


class BaseMixin(InfoMixin):
    pass


class Chart(BaseMixin):
    pass

