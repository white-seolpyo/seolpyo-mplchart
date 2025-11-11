import pandas as pd
import numpy as np

from ..._config import ConfigData


class DataMixin:
    df: pd.DataFrame
    CONFIG: ConfigData

    def add_volume_color_column(self):
        columns = ['facecolor_volume', 'edgecolor_volume']
        face_rise = self.CONFIG.VOLUME.FACECOLOR.rise
        face_fall = self.CONFIG.VOLUME.FACECOLOR.fall
        edge_rise = self.CONFIG.VOLUME.EDGECOLOR.rise
        edge_fall = self.CONFIG.VOLUME.EDGECOLOR.fall
        face_doji = self.CONFIG.VOLUME.FACECOLOR.doji
        edge_doji = self.CONFIG.VOLUME.EDGECOLOR.doji

        # 주가 상승
        self.df.loc[:, columns] = (face_rise, edge_rise)
        if face_rise != face_fall or edge_rise != edge_fall:
            # 주가 하락
            condition = self.df['close'] < self.df['pre_close']
            self.df.loc[condition, columns] = (face_fall, edge_fall)
        if face_rise != face_doji or edge_rise != edge_doji:
            # 보합
            condition = self.df['close'] == self.df['pre_close']
            self.df.loc[condition, columns] = (edge_doji, edge_doji)
        return

    def add_candle_color_column(self):
        columns = ['facecolor', 'edgecolor']
        face_bull_rise = self.CONFIG.CANDLE.FACECOLOR.bull_rise
        face_bull_fall = self.CONFIG.CANDLE.FACECOLOR.bull_fall
        face_bear_rise = self.CONFIG.CANDLE.FACECOLOR.bear_rise
        face_bear_fall = self.CONFIG.CANDLE.FACECOLOR.bear_fall
        edge_bull_rise = self.CONFIG.CANDLE.EDGECOLOR.bull_rise
        edge_bull_fall = self.CONFIG.CANDLE.EDGECOLOR.bull_fall
        edge_bear_rise = self.CONFIG.CANDLE.EDGECOLOR.bear_rise
        edge_bear_fall = self.CONFIG.CANDLE.EDGECOLOR.bear_fall
        doji = self.CONFIG.CANDLE.EDGECOLOR.doji

        # 상승양봉
        self.df.loc[:, columns] = (face_bull_rise, edge_bull_rise)
        if face_bull_rise != face_bear_fall or edge_bull_rise != edge_bear_fall:
            # 하락음봉
            self.df.loc[self.df['close'] < self.df['open'], columns] = (face_bear_fall, edge_bear_fall)
        if face_bull_rise != doji or face_bear_fall != doji or edge_bull_rise != doji or edge_bear_fall != doji:
            # 보합
            self.df.loc[self.df['close'] == self.df['open'], columns] = (doji, doji)

        if face_bull_rise != face_bull_fall or edge_bull_rise != edge_bull_fall:
            # 하락양봉(비우기)
            self.df.loc[(self.df['facecolor'] == face_bull_rise) & (self.df['close'] <= self.df['pre_close']), columns] = (face_bull_fall, edge_bull_fall)
        if face_bear_fall != face_bear_rise or edge_bear_fall != edge_bear_rise:
            # 상승음봉(비우기)
            self.df.loc[(self.df['facecolor'] == face_bear_fall) & (self.df['pre_close'] <= self.df['close']), columns] = (face_bear_rise, edge_bear_rise)
        return


class VolumeSegmentMixin(DataMixin):
    key_volume: str

    segment_volume: np.ndarray
    segment_volume_wick: np.ndarray
    facecolor_volume: np.ndarray
    edgecolor_volume: np.ndarray

    def set_volume_color_segments(self):
        self.add_volume_color_column()

        self.facecolor_volume = self.df['facecolor_volume'].values
        self.edgecolor_volume = self.df['edgecolor_volume'].values
        return

    def set_volume_segments(self):
        # 거래량 바 세그먼트
        segment_volume_wick = self.df[[
            'left_volume', 'zero',
            'left_volume', 'volume',
            'right_volume', 'volume',
            'right_volume', 'zero',
        ]].values

        self.segment_volume = segment_volume_wick.reshape(segment_volume_wick.shape[0], 4, 2)

        # 거래량 심지 세그먼트
        segment_volume_wick = self.df[[
            'x', 'zero',
            'x', 'volume',
        ]].values
        self.segment_volume_wick = segment_volume_wick.reshape(segment_volume_wick.shape[0], 2, 2)

        return


class MethodMixin:
    def get_candle_segment(self, *, is_up, x, left, right, top, bottom, high, low):
        """
        get candle segment

        Args:
            is_up (bool): (True if open < close else False)
            x (float): center of candle
            left (float): left of candle
            right (float): right of candle
            top (float): top of candle(close if `is_up` else open)
            bottom (float): bottom of candle(open if `is_up` else close)
            high (float): top of candle wick
            low (float): bottom of candle wick

        Returns:
            tuple[tuple[float, float]]: candle segment
        """
        return (
            (x, top),
            (left, top), (left, bottom),
            (x, bottom), (x, low), (x, bottom),
            (right, bottom), (right, top),
            (x, top), (x, high)
        )

    def get_bar_segment(self, *, is_up, x, left, right, top, bottom, high, low):
        if is_up:
            return (
                (x, top),
                (x, high),
                (x, top),
                (right, top),
                (x, top),
                (x, low),
                (x, bottom),
                (left, bottom),
                (x, bottom),
            )
        return (
            (x, top),
            (x, high),
            (x, top),
            (left, top),
            (x, top),
            (x, low),
            (x, bottom),
            (right, bottom),
            (x, bottom),
        )


class CandleSegmentMixin(MethodMixin, DataMixin):
    segment_candle: np.ndarray
    segment_candle_wick: np.ndarray
    segment_priceline: np.ndarray
    facecolor_candle: np.ndarray
    edgecolor_candle: np.ndarray

    def set_candle_color_segments(self):
        self.add_candle_color_column()

        self.facecolor_candle = self.df['facecolor'].values
        self.edgecolor_candle = self.df['edgecolor'].values
        return

    def set_candle_segments(self):
        # 캔들 세그먼트
        segment_candle = []
        for x, left, right, top, bottom, is_up, high, low in zip(
            self.df['x'].to_numpy().tolist(),
            self.df['left_candle'].to_numpy().tolist(), self.df['right_candle'].to_numpy().tolist(),
            self.df['top_candle'].to_numpy().tolist(), self.df['bottom_candle'].to_numpy().tolist(),
            self.df['is_up'].to_numpy().tolist(),
            self.df['high'].to_numpy().tolist(), self.df['low'].to_numpy().tolist(),
        ):
            segment_candle.append(
                self.get_candle_segment(
                    is_up=is_up,
                    x=x, left=left, right=right,
                    top=top, bottom=bottom,
                    high=high, low=low,
                )
            )

        self.segment_candle = np.array(segment_candle)
        return

    def _set_candle_segments(self):
        # 심지 세그먼트
        segment_wick = self.df[[
            'x', 'high',
            'x', 'low',
        ]].values
        self.segment_candle_wick = segment_wick.reshape(segment_wick.shape[0], 2, 2)
        # 종가 세그먼트
        segment_priceline = segment_wick = self.df[['x', 'close']].values
        self.segment_priceline = segment_priceline.reshape(1, *segment_wick.shape)
        return


class MaSegmentMixin(DataMixin):
    _visible_ma: set

    segment_ma: np.ndarray
    edgecolor_ma: np.ndarray

    def set_ma_segments(self):
        # 주가 차트 가격이동평균선
        key_ma = []
        for i in reversed(self.CONFIG.MA.ma_list):
            key_ma.append('x')
            key_ma.append(f'ma{i}')
        if key_ma:
            segment_ma = self.df[key_ma].values
            self.segment_ma = segment_ma.reshape(
                segment_ma.shape[0], len(self.CONFIG.MA.ma_list), 2
            ).swapaxes(0, 1)
        return

    def _set_ma_color_segments(self):
        # 이평선 색상 가져오기
        edgecolors = []
        for n, _ in enumerate(self.CONFIG.MA.ma_list):
            try:
                c = self.CONFIG.MA.color_list[n]
            except:
                c = self.CONFIG.MA.color_default
            edgecolors.append(c)

        self.edgecolor_ma = list(reversed(edgecolors))

        return


class SegmentMixin(CandleSegmentMixin, VolumeSegmentMixin, MaSegmentMixin):
    segment_volume: np.ndarray
    segment_volume_wick: np.ndarray
    facecolor_volume: np.ndarray
    edgecolor_volume: np.ndarray

    segment_candle: np.ndarray
    segment_candle_wick: np.ndarray
    segment_priceline: np.ndarray
    facecolor_candle: np.ndarray
    edgecolor_candle: np.ndarray

    segment_ma: np.ndarray
    edgecolor_ma: np.ndarray

    def set_segments(self):
        self.set_candle_segments()
        self._set_candle_segments()
        self.set_volume_segments()
        self.set_ma_segments()

        self.set_color_segments()
        return

    def set_color_segments(self):
        self.set_candle_color_segments()
        self.set_volume_color_segments()
        self._set_ma_color_segments()
        return

