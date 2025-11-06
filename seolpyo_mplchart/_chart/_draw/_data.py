from matplotlib.lines import Line2D
import numpy as np
import pandas as pd

from ._artist import BaseMixin as Base


class DataMixin(Base):
    df: pd.DataFrame

    key_date = 'date'
    key_open, key_high, key_low, key_close = ('open', 'high', 'low', 'close')
    key_volume = 'volume'

    def set_data(self, df: pd.DataFrame, *args, **kwargs):
        self._set_data(df, *args, **kwargs)
        self.figure.canvas.draw_idle()
        return

    def _set_data(self, df: pd.DataFrame, *args, **kwargs):
        keys = {
            self.key_date: 'date',
            self.key_open: 'open',
            self.key_high: 'high',
            self.key_low: 'low',
            self.key_close: 'close',
            self.key_volume: 'volume',
        }
        df.rename(columns=keys, inplace=True)

        # 오름차순 정렬
        df = df.sort_values(['date'])
        df = df.reset_index(drop=True)

        if self.key_volume:
            df = df[['date', 'open', 'high', 'low', 'close', 'volume']]
        else:
            df = df[['date', 'open', 'high', 'low', 'close',]]
            df['volume'] = 0

        # 전일 종가
        df['pre_close'] = df['close'].shift(1).fillna(0)
        # 거래정지인 경우 전일종가 적용
        df.loc[df['close'] == 0, 'close'] = df['pre_close']
        # 종가만 유효한 경우 종가로 통일
        df.loc[(df['close'] != 0) & (df['open'] == 0), ['open', 'high', 'low']] = df['close']

        self.chart_price_ymax = df['high'].max() * 1.3
        if self.key_volume:
            self.chart_volume_ymax = df['volume'].max() * 1.3
        else:
            self.chart_volume_ymax = 10
            # 거래량 차트 영역 최소화
            self.CONFIG.FIGURE.RATIO.volume = 0
            # tick 그리지 않기
            self.ax_volume.set_yticklabels([])
            self.ax_volume.set_yticks([])
            self._set_figure()

        self.index_list = df.index.tolist()
        self.xmin, self.xmax = (0, self.index_list[-1])

        if not self.CONFIG.MA.ma_list:
            self.CONFIG.MA.ma_list = tuple()
        else:
            self.CONFIG.MA.ma_list = sorted(self.CONFIG.MA.ma_list)
            # 가격이동평균선 계산
            for i in self.CONFIG.MA.ma_list:
                df[f'ma{i}'] = df['close'].rolling(i).mean()

        df['x'] = df.index + 0.5
        df['left_candle'] = df['x'] - self.CONFIG.CANDLE.half_width
        df['right_candle'] = df['x'] + self.CONFIG.CANDLE.half_width
        df['left_volume'] = df['x'] - self.CONFIG.VOLUME.half_width
        df['right_volume'] = df['x'] + self.CONFIG.VOLUME.half_width
        df['zero'] = 0

        df['is_up'] = np.where(df['open'] < df['close'], True, False)
        df['top_candle'] = np.where(df['is_up'], df['close'], df['open'])
        df['bottom_candle'] = np.where(df['is_up'], df['open'], df['close'])

        if self.key_volume:
            df['ymax_volume'] = df['volume'] * 1.2

        self.df = df

        return


class CandleSegmentMixin(DataMixin):
    def set_segments(self):
        self.set_candle_segments()
        self.set_candle_color_segments()
        return

    def set_color_segments(self):
        self.set_candle_color_segments()
        return

    def set_candle_segments(self):
        # 캔들 세그먼트
        segment_candle = []
        segment_wick = []
        segment_priceline = []
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

    def set_candle_color_segments(self):
        self.add_candle_color_column()

        self.facecolor_candle = self.df['facecolor'].values
        self.edgecolor_candle = self.df['edgecolor'].values
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


class MaSegmentMixin(CandleSegmentMixin):
    _visible_ma = set()

    def set_segments(self):
        super().set_segments()

        self.set_ma_segments()
        self._set_ma_color_segments()
        return

    def set_color_segments(self):
        self._set_ma_color_segments()

        super().set_color_segments()
        return

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
        # 기존 legend 제거
        legends = self.ax_legend.get_legend()
        if legends:
            legends.remove()

        self._visible_ma.clear()

        # 이평선 색상 가져오기
        handle_list, label_list, list_color = ([], [], [])
        arr = [0, 1]
        for n, i in enumerate(self.CONFIG.MA.ma_list):
            try:
                c = self.CONFIG.MA.color_list[n]
            except:
                c = self.CONFIG.MA.color_default
            list_color.append(c)

            handle_list.append(Line2D(arr, arr, color=c, linewidth=5, label=i))
            label_list.append(self.CONFIG.MA.format.format(i))

            self._visible_ma.add(i)
        self.edgecolor_ma = list(reversed(list_color))

        # 가격이동평균선 legend 생성
        if handle_list:
            legends = self.ax_legend.legend(
                handle_list, label_list, loc='lower left', ncol=10,
                facecolor=self.CONFIG.AX.facecolor, edgecolor=self.CONFIG.AX.TICK.edgecolor,
                labelcolor=self.CONFIG.AX.TICK.fontcolor,
            )
            for i in legends.legend_handles:
                # legend 클릭시 pick event가 발생할 수 있도록 설정
                i.set_picker(5)
        return


class VolumeSegmentMixin(MaSegmentMixin):
    def set_segments(self):
        super().set_segments()

        if self.key_volume:
            self.set_volume_segments()
            self.set_volume_color_segments()
        return

    def set_color_segments(self):
        super().set_color_segments()

        self.set_volume_color_segments()
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

        # segment_volume = []
        # for x, left, right, top in zip(
        #     self.df['x'].to_numpy().tolist(),
        #     self.df['left_volume'].to_numpy().tolist(), self.df['right_volume'].to_numpy().tolist(),
        #     self.df[self.key_volume].to_numpy().tolist(),
        # ):
        #     segment_volume.append(
        #         self.get_volume_segment(x=x, left=left, right=right, top=top)
        #     )
        # self.segment_volume = np.array(segment_volume)

        # 거래량 심지 세그먼트
        segment_volume_wick = self.df[[
            'x', 'zero',
            'x', 'volume',
        ]].values
        self.segment_volume_wick = segment_volume_wick.reshape(segment_volume_wick.shape[0], 2, 2)

        return

    def _add_volume_color_column(self):
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

    def set_volume_color_segments(self):
        self._add_volume_color_column()

        self.facecolor_volume = self.df['facecolor_volume'].values
        self.edgecolor_volume = self.df['edgecolor_volume'].values
        return


class BaseMixin(VolumeSegmentMixin):
    pass

