import pandas as pd
import numpy as np

from ..style import Style


class VolumeMixin:
    STYLE: Style

    df: pd.DataFrame

    def set_volume_segment(self):
        # volume bar
        self.segment_volume = self.get_volumebar_segment()

        # wick
        arr = self.get_volume_wick_segment()
        self.segment_volume_wick = arr

        # volumeline
        self.segment_volume_line = self.get_sement_volume_line()

        self.volume_facecolors, self.volume_edgecolors = self.get_volume_colors()

        return

    def get_volumebar_segment(self):
        left = self.df['volume_left'].to_numpy()
        right = self.df['volume_right'].to_numpy()
        top = self.df['volume'].to_numpy()
        bottom = self.df['zeros'].to_numpy()

        arr = np.stack([
            np.stack([left, bottom], axis=1), # [left, 0]
            np.stack([left, top], axis=1),    # [left, top]
            np.stack([right, top], axis=1),   # [right, top]
            np.stack([right, bottom], axis=1) # [right, 0]
        ], axis=1)

        segment = np.ma.MaskedArray(arr)

        return segment

    def get_volume_wick_segment(self):
        x = self.df['x'].to_numpy()
        high = self.df['volume'].to_numpy()
        low = self.df['zeros'].to_numpy()
        # wick
        arr = np.stack([
            np.column_stack([x, low]),
            np.column_stack([x, high])
        ], axis=1)
        segment = np.ma.MaskedArray(arr)

        return segment

    def get_sement_volume_line(self):
        x = self.df['x'].to_numpy()
        high = self.df['volume'].to_numpy()

        N = int(self.df.index[-1]) + 1
        arr = np.empty((1, N, 2, 2), dtype=np.float64)
        arr[0, :, :, 0] = x[:, None]
        # arr[0, :, [0, 2], 1] = 0
        arr[0, :, 1, 1] = high
        # arr = np.stack([
        #     np.column_stack([x, low]),
        #     np.column_stack([x, high]),
        #     np.column_stack([x, low]),
        # ], axis=1)
        # arr = np.empty((1, self.N*3, 2))
        # arr = np.empty((1, self.N*3, 2))
        # arr[0, 0::3, 0] = x
        # arr[:, [0, 2], 1] = low
        # arr[0, 0::3, 1] = high
        return arr

    def get_volume_colors(self):
        cfg = self.STYLE.CHART.VOLUME

        # 전일대비 상승
        face_rise = cfg.FACECOLOR.rise
        edge_rise = cfg.EDGECOLOR.rise
        # 전일대비 하락
        face_fall = cfg.FACECOLOR.fall
        edge_fall = cfg.EDGECOLOR.fall
        # 전일과 동일
        face_unchange = cfg.EDGECOLOR.unchange
        edge_unchange = cfg.EDGECOLOR.unchange

        unchanged = self.df['unchanged'].to_numpy()
        is_rise = self.df['is_rise'].to_numpy()

        mask = [
            unchanged, # 보합
            is_rise, # 전일대비 상승
        ]

        face_choices = [face_unchange, face_rise]
        edge_choices = [edge_unchange, edge_rise]

        facecolors = np.select(mask, face_choices, default=face_fall)
        edgecolors = np.select(mask, edge_choices, default=edge_fall)
        # print(f'{self.df[["close", "pre_close", "is_doji"]][:50]=}')
        # print(f'{facecolors[:50]=}')
        # print(f'{edgecolors[:50]=}')
        # print(f'{len(is_doji)=}')
        # print(f'{len(facecolors)=}')
        # print(f'{len(edgecolors)=}')

        return (facecolors, edgecolors)

