import numpy as np
import pandas as pd

from .utils.formatter import Formatter, FormatterEN

from .style import Style


class ColumnMixin:
    STYLE: Style

    key_volume: str

    def add_columns(self, df: pd.DataFrame):
        N = len(df)

        idx = np.arange(N, dtype=np.float64)
        x = idx + 0.5
        candle_left = x - self.STYLE.CHART.PRICE.half_width
        candle_right = x + self.STYLE.CHART.PRICE.half_width

        zeros = np.zeros_like(idx)
        volume_left = x - self.STYLE.CHART.VOLUME.half_width
        volume_right = x + self.STYLE.CHART.VOLUME.half_width
        columns = ['idx', 'x', 'candle_left', 'candle_right', 'zeros', 'volume_left', 'volume_right']
        df[columns] = np.column_stack([idx, x, candle_left, candle_right, zeros, volume_left, volume_right])

        df['pre_close'] = df['close'].shift(1).fillna(0)

        Open = df['open'].to_numpy()
        high = df['high'].to_numpy()
        low = df['low'].to_numpy()
        close = df['close'].to_numpy()
        volume = df['volume'].to_numpy()

        pre_close = df['pre_close'].to_numpy()

        is_up = Open < close
        is_rise = pre_close < close
        is_flat = Open == close
        unchanged = pre_close == close
        columns = ['is_up','is_rise', 'is_flat', 'unchanged']
        df[columns] = np.column_stack([is_up, is_rise, is_flat, unchanged])

        # top / bottom 배열
        candle_top = np.where(is_up, close, Open)
        candle_bottom = np.where(is_up, Open, close)
        columns = ['candle_top','candle_bottom']
        df[columns] = np.column_stack([candle_top, candle_bottom])

        df['pre_volume'] = df['volume'].shift(1).fillna(0)
        pre_close = df['pre_close'].to_numpy()
        pre_volume = df['pre_volume'].to_numpy()
        change = close - pre_close
        change[0] = 0
        change_volume = volume - pre_volume
        change_volume[0] = 0

        mask = pre_close != 0
        safe_pre_close = np.where(mask, pre_close, np.nan)
        rate = np.where(mask, np.round(change / safe_pre_close * 100, 2), 0)
        rate_open = np.where(mask, np.round((Open - safe_pre_close) / safe_pre_close * 100, 2), 0)
        rate_high = np.where(mask, np.round((high - safe_pre_close) / safe_pre_close * 100, 2), 0)
        rate_low = np.where(mask, np.round((low - safe_pre_close) / safe_pre_close * 100, 2), 0)

        mask = pre_volume != 0
        safe_pre_volume = np.where(mask, pre_volume, np.nan)
        rate_volume = np.where(mask, np.round(change_volume / safe_pre_volume * 100, 2), 0)
        columns = ['change', 'change_volume', 'rate', 'rate_open', 'rate_high', 'rate_low', 'rate_volume']
        df[columns] = np.column_stack([change, change_volume, rate, rate_open, rate_high, rate_low, rate_volume])

        candle_space = np.round((high - low) / 5, 6)
        box_candle_top = high + candle_space
        box_candle_bottom = low - candle_space
        box_candle_height = box_candle_top - box_candle_bottom
        columns = ['box_candle_top', 'box_candle_bottom', 'box_candle_height']
        df[columns] = np.column_stack([box_candle_top, box_candle_bottom, box_candle_height])

        if self.key_volume:
            df['box_volume_top'] = df['volume'] * 1.15
        else:
            df['box_volume_top'] = 5

        return

class DataFrameMixin(ColumnMixin):
    key_date = 'date'

    key_open = 'open'
    key_high = 'high'
    key_low = 'low'
    key_close = 'close'
    key_volume = 'volume'

    STYLE: Style

    def get_df(self, df: pd.DataFrame):
        # print(f'{df.keys()=}')
        keys = {
            self.key_date: 'date',
            self.key_open: 'open',
            self.key_high: 'high',
            self.key_low: 'low',
            self.key_close: 'close',
            self.key_volume: 'volume',
        }
        # print(f'{keys=}')
        df.rename(columns=keys, inplace=True)
        # print(f'{df.columns=}')

        # df column 추출
        if self.key_volume:
            df = df[['date', 'open', 'high', 'low', 'close', 'volume']].copy()
        else:
            df = df[['date', 'open', 'high', 'low', 'close',]].copy()
            df['volume'] = 0
        # axis에서 volume chart ymax에 사용하기 위한 값
        # df.loc[:, 'ymax_volume'] = df['volume'] * 1.2

        # 오름차순 정렬
        df = df.sort_values(['date'])\
            .reset_index(drop=True)

        # 종가 정보가 없으면 전일 종가로 고정
        close = df['close'].to_numpy()
        mask = close == 0
        if np.any(mask):
            idx = np.flatnonzero(mask)
            idx = idx[idx > 0]
            close[idx] = close[idx - 1]
            df['close'] = close

        # 종가 정보만 있으면 종가로 고정
        Open = df['open'].to_numpy()
        mask = Open == 0
        if np.any(mask):
            high = df['high'].to_numpy()
            low = df['low'].to_numpy()
            # 주가 정보가 0인 날짜 덮어쓰기
            close_select = close[mask]
            Open[mask] = close_select
            high[mask] = close_select
            low[mask] = close_select
            columns = ['open', 'high', 'low']
            df[columns] = np.column_stack([Open, high, low])

        self.add_columns(df)

        return df


class DataMixin(DataFrameMixin):
    segment_slider: np.ma.MaskedArray
    slider_edgecolors: np.ma.MaskedArray
    slider_linewidths: list[float]

    digit_price: int
    digit_volume: int
    FORMATTER: Formatter

    def list_to_df(self, data: list[dict]):
        return pd.DataFrame(data)

    def set_data(self, df: pd.DataFrame, *, change_xlim=True):
        """
        `if change_xlim`: change xlim with `self.get_default_xlim()` value

        `if not change_xlim`: Keep the current xlim
        """
        self.df = self.get_df(df)
        # print(self.df.keys())

        self.refresh(change_xlim)

        return

