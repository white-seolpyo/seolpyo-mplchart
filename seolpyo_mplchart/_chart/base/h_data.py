from matplotlib.axes import Axes
import numpy as np
import pandas as pd

from ..._config import ConfigData


class Base:
    CONFIG: ConfigData
    df: pd.DataFrame

    key_date = 'date'
    key_open, key_high, key_low, key_close = ('open', 'high', 'low', 'close')
    key_volume = 'volume'

    ax_price: Axes
    index_list: list[int] = []

    set_segments: callable
    axis: callable

    def get_default_xlim(self):
        """
        get_default_xlim.

        space = int(self.index_list[-1] / 20)

        Returns:
            (int, int): (-space, self.index_list[-1]+space)
        """
        # print(f'{self.index_list[-1]=}')
        space = int(self.index_list[-1] / 20)
        return (-space, self.index_list[-1]+space)

    def set_variables(self):
        self.index_list.clear()
        self.index_list = self.df.index.tolist()
        self.xmin, self.xmax = (0, self.index_list[-1])

        self.chart_price_ymax = round(self.df['high'].max() * 1.3, self.CONFIG.UNIT.digit+2)
        if self.key_volume:
            self.chart_volume_ymax = round(self.df['volume'].max() * 1.3, self.CONFIG.UNIT.digit_volume+2)
        else:
            self.chart_volume_ymax = 10

        if not self.CONFIG.MA.ma_list:
            self.CONFIG.MA.ma_list = []
        else:
            self.CONFIG.MA.ma_list = sorted(self.CONFIG.MA.ma_list)

        return

    def set_data(self, df: pd.DataFrame, *, change_xlim=True):
        """
        `if change_xlim`: change xlim with `self.get_default_xlim()` value

        `if not change_xlim`: Keep the current xlim
        """
        self.df = self._convert_df(df)

        self._add_columns()
        # print(f'{self.df.columns=}')

        self.set_variables()

        self.set_segments()

        if change_xlim:
            xmin, xmax = self.get_default_xlim()
            self.axis(xmin, xmax=xmax)
        return
    
    def _convert_df(self, df: pd.DataFrame):
        keys = {
            self.key_date: 'date',
            self.key_open: 'open',
            self.key_high: 'high',
            self.key_low: 'low',
            self.key_close: 'close',
            self.key_volume: 'volume',
        }
        df.rename(columns=keys, inplace=True)

        # df column 추출
        if self.key_volume:
            df = df[['date', 'open', 'high', 'low', 'close', 'volume']].copy()
        else:
            df = df[['date', 'open', 'high', 'low', 'close',]].copy()
            df['volume'] = 0
        df.loc[:, 'ymax_volume'] = df['volume'] * 1.2

        # 오름차순 정렬
        df = df.sort_values(['date'])
        df = df.reset_index(drop=True)

        return df

    def _add_columns(self):
        # 전일 종가 추가
        self.df['pre_close'] = self.df['close'].shift(1).fillna(0)
        # 거래정지인 경우 전일종가 적용
        self.df.loc[self.df['close'] == 0, 'close'] = self.df['pre_close']
        # 종가만 유효한 경우 종가로 통일
        self.df.loc[(self.df['close'] != 0) & (self.df['open'] == 0), ['open', 'high', 'low']] = self.df['close']

        # 가격이동평균선 계산
        for ma in self.CONFIG.MA.ma_list:
            self.df[f'ma{ma}'] = self.df['close'].rolling(ma).mean()

        # 세그먼트 생성을 위한 column 추가
        self.df['x'] = self.df.index + 0.5
        self.df['left_candle'] = self.df['x'] - self.CONFIG.CANDLE.half_width
        self.df['right_candle'] = self.df['x'] + self.CONFIG.CANDLE.half_width
        self.df['left_volume'] = self.df['x'] - self.CONFIG.VOLUME.half_width
        self.df['right_volume'] = self.df['x'] + self.CONFIG.VOLUME.half_width
        self.df['zero'] = 0

        self.df['is_up'] = np.where(self.df['open'] < self.df['close'], True, False)
        self.df['top_candle'] = np.where(self.df['is_up'], self.df['close'], self.df['open'])
        self.df['bottom_candle'] = np.where(self.df['is_up'], self.df['open'], self.df['close'])

        return


class DataMixin(Base):
    key_date = 'date'
    key_open, key_high, key_low, key_close = ('open', 'high', 'low', 'close')
    key_volume = 'volume'

    index_list: list[int] = []

    df: pd.DataFrame

    chart_price_ymax: float
    chart_volume_ymax: float
    xmin: int
    xmax: int

