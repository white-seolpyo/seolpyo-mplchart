import pandas as pd
import numpy as np

from ..style import Style


class MaMixin:
    STYLE: Style

    df: pd.DataFrame

    ma_list = [5, 20, 50, 120, 240,]

    def set_ma_segment(self):
        self.segment_ma = self.get_ma_segment()
        # print(f'{self.segment_ma.shape=}')
        self.ma_colors = self.get_ma_colors()
        self.ma_alphas = [1 for _ in self.ma_colors]

        return

    def get_ma_segment(self):
        if not self.ma_list:
            return []

        self.ma_list = sorted(self.ma_list, reverse=True)

        close = self.df['close'].to_numpy()
        x = self.df['x'].to_numpy()
        N = int(self.df.index[-1]) + 1

        segment = np.empty((len(self.ma_list), N, 2), dtype=np.float64)

        # z-index 5 > 120
        for n, period in enumerate(self.ma_list):
            ma = np.full(N, np.nan, dtype=np.float64)
            if period <= N:
                cumsum = np.cumsum(np.insert(close, 0, 0))
                ma[period-1:] = (cumsum[period:] - cumsum[:-period]) / period

            # 배열 채우기
            segment[n, :, 0] = x   # x값
            segment[n, :, 1] = ma  # ma값

        # 예: ma_arrays[5] → shape (N, 2), 열: [x, ma5]
        return segment

    def get_ma_colors(self):
        item_list = []
        for n, _ in enumerate(self.ma_list, 1):
            try:
                color = self.STYLE.CHART.MA.color_list[-n]
            except IndexError:
                color = self.STYLE.CHART.MA.color_default
            item_list.append(color)
        return item_list

