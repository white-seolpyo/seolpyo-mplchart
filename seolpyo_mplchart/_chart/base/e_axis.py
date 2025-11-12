from matplotlib.axes import Axes
from matplotlib.collections import LineCollection
from matplotlib.text import Text
import numpy as np
import pandas as pd

from ..._config import ConfigData


class Base:
    CONFIG: ConfigData

    key_volume: str
    df: pd.DataFrame

    index_list: list[int]

    collection_candle: LineCollection
    collection_volume: LineCollection
    collection_ma: LineCollection

    segment_candle: np.ndarray
    segment_candle_wick: np.ndarray
    segment_priceline: np.ndarray
    facecolor_candle: np.ndarray
    edgecolor_candle: np.ndarray

    segment_volume: np.ndarray
    segment_volume_wick: np.ndarray
    facecolor_volume: np.ndarray
    edgecolor_volume: np.ndarray

    segment_ma: np.ndarray
    edgecolor_ma: np.ndarray


class LimMixin(Base):
    def _get_indices(self, ind_start, *, ind_end):
        "조회 영역에 해당하는 index 가져오기"
        if ind_start < 0:
            ind_start = 0
        if ind_end < 1:
            ind_end = 1

        if ind_end < ind_start:
            msg = 'ind_end < ind_start'
            msg += f'  {ind_start=:,}'
            msg += f'  {ind_end=:,}'
            raise Exception(msg)
        return (ind_start, ind_end)

    def _get_price_ylim(self, ind_start, *, ind_end):
        ymin, ymax = (self.df['low'][ind_start:ind_end].min(), self.df['high'][ind_start:ind_end].max())

        if ymin == ymax:
            if ymax:
                ymin, ymax = (round(ymax * 0.9, self.CONFIG.UNIT.digit+2), round(ymax * 1.1, self.CONFIG.UNIT.digit+2))
            else:
                ymin, ymax = (-5, 10)
        else:
            height = ymax - ymin
            if height < 15:
                height = 15

            ymin = ymin - round(height / 20, self.CONFIG.UNIT.digit+2)
            ymax = ymax + round(height / 10, self.CONFIG.UNIT.digit+2)

        return (ymin, ymax)

    def _get_volume_ylim(self, ind_start, *, ind_end):
        if not self.key_volume:
            ymax = 1
        else:
            series = self.df['volume'][ind_start:ind_end]
            # print(f'{series=}')
            ymax = series.max()
            height = ymax
            ymax = ymax + round(height / 5, self.CONFIG.UNIT.digit_volume+2)
            if ymax < 1:
                ymax = 1
        # print(f'{ymax=}')
        return (0, ymax)


class MaMixin(Base):
    def _set_ma_collection_segments(self, ind_start, ind_end):
        self.collection_ma.set_segments(self.segment_ma[:, ind_start:ind_end])
        self.collection_ma.set_edgecolor(self.edgecolor_ma)
        return


class VolumeMixin(Base):
    def _set_volume_collection_segments(self, ind_start, ind_end):
        if not self.key_volume:
            self.collection_volume.set_segments([])
            return

        self.collection_volume.set_segments(self.segment_volume[ind_start:ind_end])
        self.collection_volume.set_linewidth(self.CONFIG.VOLUME.linewidth)
        self.collection_volume.set_facecolor(self.facecolor_volume[ind_start:ind_end])
        self.collection_volume.set_edgecolor(self.edgecolor_volume[ind_start:ind_end])
        return

    def _set_volume_collection_wick_segments(self, ind_start, ind_end):
        # print(f'{(ind_start, ind_end)=}')
        if not self.key_volume:
            self.collection_volume.set_segments([])
            return

        seg_volume = self.segment_volume_wick[ind_start:ind_end]
        seg_edgecolor_volume = self.edgecolor_volume[ind_start:ind_end]

        self.collection_volume.set_segments(seg_volume)
        self.collection_volume.set_linewidth(1.3)
        self.collection_volume.set_facecolor([])
        self.collection_volume.set_edgecolor(seg_edgecolor_volume)
        return


class CandleMixin(Base):
    def _set_candle_collection_segments(self, ind_start, ind_end):
        # print(f'{self.edgecolor_candle[ind_start:ind_end]=}')
        self.collection_candle.set_segments(self.segment_candle[ind_start:ind_end])
        self.collection_candle.set_facecolor(self.facecolor_candle[ind_start:ind_end])
        self.collection_candle.set_edgecolor(self.edgecolor_candle[ind_start:ind_end])
        self.collection_candle.set_linewidth(self.CONFIG.CANDLE.linewidth)
        return

    def _set_candle_collection_wick_segments(self, ind_start, ind_end):
        # print(f'{self.edgecolor_candle[ind_start:ind_end]=}')
        self.collection_candle.set_segments(self.segment_candle_wick[ind_start:ind_end])
        self.collection_candle.set_facecolor([])
        self.collection_candle.set_edgecolor(self.edgecolor_candle[ind_start:ind_end])
        self.collection_candle.set_linewidth(self.CONFIG.CANDLE.linewidth * 1.5)
        return

    def set_candle_collection_priceline_segments(self, ind_start, ind_end):
        self.collection_candle.set_segments(self.segment_priceline[:, ind_start:ind_end])
        self.collection_candle.set_facecolor([])
        self.collection_candle.set_edgecolor(self.CONFIG.CANDLE.line_color)
        self.collection_candle.set_linewidth(2)
        return


class CollectionMixin(CandleMixin, VolumeMixin, MaMixin):
    limit_candle = 400
    limit_wick = 2_000

    def set_collections(self, ind_start, *, ind_end):
        if ind_start < 0:
            ind_start = 0
        indsub = ind_end - ind_start
        # print(f'{indsub=:,}')

        if not self.limit_candle or indsub < self.limit_candle:
            # print('candle')
            self._set_candle_collection_segments(ind_start, ind_end=ind_end)
            self._set_volume_collection_segments(ind_start, ind_end=ind_end)
        else:
            self._set_volume_collection_wick_segments(ind_start, ind_end=ind_end)

            if not self.limit_wick or indsub < self.limit_wick:
                # print('wick')
                self._set_candle_collection_wick_segments(ind_start, ind_end=ind_end)
            else:
                # print('line')
                self.set_candle_collection_priceline_segments(ind_start, ind_end=ind_end)

        self._set_ma_collection_segments(ind_start, ind_end=ind_end)
        return


class AxisMixin(LimMixin, CollectionMixin):
    limit_candle = 400
    limit_wick = 2_000

    ax_price: Axes
    ax_volume: Axes

    vxmin: int
    vxmax: int
    price_ymin: int
    price_ymax: int
    volume_ymax: int

    def axis(self, xmin, *, xmax):
        "조회 영역 변경"
        # print('base axis')
        self.set_collections(xmin, ind_end=xmax+1)

        self.vxmin, self.vxmax = (xmin, xmax+1)
        ind_start, ind_end = self._get_indices(xmin, ind_end=xmax)

        self.price_ymin, self.price_ymax = self._get_price_ylim(ind_start, ind_end=ind_end)

        # 주가 차트 xlim
        self.ax_price.set_xlim(self.vxmin, self.vxmax)
        # 주가 차트 ylim
        self.ax_price.set_ylim(self.price_ymin, self.price_ymax)

        # 거래량 차트 xlim
        self.ax_volume.set_xlim(self.vxmin, self.vxmax)
        self.volume_ymax = 1
        if self.key_volume:
            _, self.volume_ymax = self._get_volume_ylim(ind_start, ind_end=ind_end)
            # 거래량 차트 ylim
            self.ax_volume.set_ylim(0, self.volume_ymax)

        self.set_xtick_labels(xmin, xmax=xmax)
        return

    def set_xtick_labels(self, xmin, *, xmax):
        # x축에 일부 date 표시하기
        xsub = xmax - xmin
        xmiddle = xmin + (xsub // 2)
        indices = [idx for idx in (xmin, xmiddle, xmax) if 0 <= idx and idx <= self.index_list[-1]]
        # print(f'{xmiddle=}')
        # print(f'{indices=}')

        m = (xmiddle - xmin) // 2
        ind_end = self.index_list[-1]
        aligns = ['left', 'center', 'center']
        if len(indices) < 2:
            if xmin < 0 and self.index_list[-1] < xmax:
                indices = [0, xmiddle, ind_end]
            else:
                if xmin <= 0:
                    if m <= xmax:
                        aligns = aligns[-2:]
                        indices = [0, xmax]
                    else:
                        aligns = aligns[-1:]
                        indices = [0]
                else:
                    if xmin+m <= ind_end:
                        aligns = aligns[:2]
                        indices = [xmin, ind_end]
                    else:
                        aligns = aligns[:1]
                        indices = [ind_end]
        elif len(indices) < 3:
            if xmin < 0:
                if 0 <= (xmiddle - m):
                    indices = [0] + indices
                else:
                    aligns = aligns[-2:]
                    indices[0] = 0
            else:
                if (xmiddle + m) <= ind_end:
                    indices.append(ind_end)
                else:
                    aligns = aligns[:2]
                    indices[-1] = ind_end

        date_list = [self.df.iloc[idx]['date'] for idx in indices]
        # 라벨을 노출할 틱 위치, major tick과 겹쳐서 무시되는 것 방지
        self.ax_volume.set_xticks([idx+0.501 for idx in indices], minor=True)
        # 라벨
        self.ax_volume.set_xticklabels(date_list, minor=True)
        labels: list[Text] = self.ax_volume.get_xticklabels(minor=True)
        for label, align in zip(labels, aligns):
            # 라벨 텍스트 정렬
            label.set_horizontalalignment(align)
        return

