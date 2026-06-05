import pandas as pd
import numpy as np

from ..style import Style


class CandleMixin:
    df: pd.DataFrame

    def get_candle_segment(self):
        x = self.df['x'].to_numpy()
        low = self.df['low'].to_numpy()
        high = self.df['high'].to_numpy()
        left = self.df['candle_left'].to_numpy()
        right = self.df['candle_right'].to_numpy()
        top = self.df['candle_top'].to_numpy()
        bottom = self.df['candle_bottom'].to_numpy()

        N = len(x)
        arr = np.empty((N, 10, 2), dtype=np.float64)

        arr[:, :, 1] = np.column_stack([
            top,    # 0
            top,    # 1
            bottom, # 2
            bottom, # 3
            low,    # 4
            bottom, # 5
            bottom, # 6
            top,    # 7
            top,    # 8
            high,   # 9
        ])

        arr[:, :, 0] = np.column_stack([
            x,     # 0
            left,  # 1
            left,  # 2
            x,     # 3
            x,     # 4
            x,     # 5
            right, # 6
            right, # 7
            x,     # 8
            x,     # 9
        ])

        segment = np.ma.MaskedArray(arr)
        return segment


class BarMixin:
    df: pd.DataFrame

    def get_bar_segment(self):
        x = self.df['x'].to_numpy()
        low = self.df['low'].to_numpy()
        high = self.df['high'].to_numpy()
        left = self.df['candle_left'].to_numpy()
        right = self.df['candle_right'].to_numpy()
        top = self.df['candle_top'].to_numpy()
        bottom = self.df['candle_bottom'].to_numpy()
        is_up = self.df['is_up'].to_numpy()

        N = int(self.df.index[-1]) + 1

        # 결과 배열 생성
        arr = np.empty((N, 8, 2), dtype=np.float64)

        arr[:, :, 1] = np.column_stack([
            top,    # 0
            top,    # 1
            top,    # 2
            low,    # 3
            bottom, # 4
            bottom, # 5
            bottom, # 6
            high    # 7
        ])

        arr[:, :, 0] = np.column_stack([
            x,     # 0
            left,  # 1
            x,     # 2
            x,     # 3
            x,     # 4
            right, # 5
            x,     # 6
            x      # 7
        ])

        # 좌우 교체
        dn = is_up
        arr[dn, 1, 0] = right[dn]  # 1
        arr[dn, 5, 0] = left[dn]   # 5

        segment = np.ma.MaskedArray(arr)
        return segment


class PriceMixin(CandleMixin, BarMixin):
    STYLE: Style

    df: pd.DataFrame

    def set_price_segment(self):
        # candle
        self.segment_candle = self.get_candle_segment()
        # print(f'{self.segment_candle[:2]=}')

        arr = self.get_price_wick_segemnt()
        self.segment_wick = arr

        # priceline
        arr = self.get_price_line_segment()
        # print(f'{arr.shape=}')
        self.segment_priceline = arr

        self.price_facecolors, self.price_edgecolors = self.get_price_colors()
        return

    def get_price_wick_segemnt(self):
        x = self.df['x'].to_numpy()
        high = self.df['high'].to_numpy()
        low = self.df['low'].to_numpy()
        # wick
        arr = np.stack([
            np.column_stack([x, low]),
            np.column_stack([x, high])
        ], axis=1)
        segment = np.ma.MaskedArray(arr)
        return segment

    def get_price_line_segment(self):
        x = self.df['x'].to_numpy()
        close = self.df['close'].to_numpy()

        arr = np.stack((x, close), axis=1)[np.newaxis, :, :]
        # print(f'{arr.shape=}')
        segment = np.ma.MaskedArray(arr)
        return segment

    def get_price_hl_line_segment(self):
        x = self.df['x'].to_numpy()
        high = self.df['high'].to_numpy()
        low = self.df['low'].to_numpy()

        arr = np.stack((x, low), axis=1)[np.newaxis, :, :]

        is_rise = self.df['is_rise'].to_numpy()
        arr[0, is_rise, 1] = high[is_rise]

        segment = np.ma.MaskedArray(arr)
        return segment

    def get_price_colors(self):
        cfg = self.STYLE.CHART.PRICE

        # 상승양봉
        face_up_rise = cfg.FACECOLOR.up_rise
        edge_up_rise = cfg.EDGECOLOR.up_rise
        # 하락음봉
        face_down_fall = cfg.FACECOLOR.down_fall
        edge_down_fall = cfg.EDGECOLOR.down_fall
        # 하락양봉
        face_up_fall = cfg.FACECOLOR.up_fall
        edge_up_fall = cfg.EDGECOLOR.up_fall
        # 상승음봉
        face_down_rise = cfg.FACECOLOR.down_rise
        edge_down_rise = cfg.EDGECOLOR.down_rise
        # 시가=종가
        flat = cfg.EDGECOLOR.flat

        is_up = self.df['is_up'].to_numpy()
        is_flat = self.df['is_flat'].to_numpy()
        is_rise = self.df['is_rise'].to_numpy()

        mask = [
            is_flat,           # 시가=종가
            is_rise & is_up,   # 상승양봉
            ~is_rise & ~is_up, # 하락음봉
            ~is_rise & is_up,  # 하락양봉
        ]

        face_choices = [flat, face_up_rise, face_down_fall, face_up_fall]
        edge_choices = [flat, edge_up_rise, edge_down_fall, edge_up_fall]

        facecolors = np.select(mask, face_choices, default=face_down_rise)
        edgecolors = np.select(mask, edge_choices, default=edge_down_rise)
        # print(f'{self.df[["close", "pre_close", "is_flat"]][:50]=}')
        # print(f'{facecolors[:50]=}')
        # print(f'{edgecolors[:50]=}')
        # print(f'{len(is_flat)=}')
        # print(f'{len(facecolors)=}')
        # print(f'{len(edgecolors)=}')

        return (facecolors, edgecolors)

