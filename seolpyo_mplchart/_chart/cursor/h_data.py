import pandas as pd

from ..._config import ConfigData


class Base:
    CONFIG: ConfigData

    key_volume: str
    df: pd.DataFrame

    _add_columns: callable
    set_variables: callable


class Mixin(Base):
    def _add_columns(self):
        super()._add_columns()

        self.df['compare'] = (self.df['close'] - self.df['pre_close']).fillna(0)
        self.df['rate'] = (self.df['compare'] * 100 / self.df['pre_close']).__round__(2).fillna(0)
        self.df['rate_open'] = ((self.df['open'] - self.df['pre_close']) * 100 / self.df['pre_close']).__round__(2).fillna(0)
        self.df['rate_high'] = ((self.df['high'] - self.df['pre_close']) * 100 / self.df['pre_close']).__round__(2).fillna(0)
        self.df['rate_low'] = ((self.df['low'] - self.df['pre_close']) * 100 / self.df['pre_close']).__round__(2).fillna(0)
        if self.key_volume:
            self.df['pre_volume'] = self.df['volume'].shift(1)
            self.df['compare_volume'] = (self.df['volume'] - self.df['pre_volume']).fillna(0)
            self.df['rate_volume'] = (self.df['compare_volume'] * 100 / self.df['pre_volume']).__round__(2).fillna(0)

        self.df['space_box_candle'] = (self.df['high'] - self.df['low']) / 5
        self.df['box_candle_top'] = self.df['high'] + self.df['space_box_candle']
        self.df['box_candle_bottom'] = self.df['low'] - self.df['space_box_candle']
        self.df['box_candle_height'] = self.df['box_candle_top'] - self.df['box_candle_bottom']

        if self.key_volume:
            self.df['box_volume_top'] = self.df['volume'] * 1.15

        return

    def set_variables(self):
        super().set_variables()

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


class DataMixin(Mixin):
    _length_text: int

