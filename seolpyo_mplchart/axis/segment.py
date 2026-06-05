from matplotlib.axes import Axes
from matplotlib.collections import LineCollection
import numpy as np
from numpy.ma import MaskedArray

from ..style import Style


class MaMixin:
    STYLE: Style

    collection_ma: LineCollection

    segment_ma: MaskedArray

    ma_colors: list

    limit_ma = None

    def set_ma_collection_segment(self, ind_start, ind_end, /, *, step=1):
        ind_sub = ind_end - ind_start
        if self.limit_ma and self.limit_ma < ind_sub:
            self.collection_ma.set_segments([])
            return

        if step == 1:
            self.collection_ma.set_segments(self.segment_ma[:, ind_start:ind_end])
        else:
            self.collection_ma.set_segments(self.segment_ma[:, ind_start:ind_end:step])
        self.collection_ma.set_edgecolor(self.ma_colors)
        self.collection_ma.set_linewidth(self.STYLE.CHART.MA.linewidth)
        return


class PriceMixin:
    STYLE: Style

    collection_price: LineCollection

    segment_candle: MaskedArray
    segment_wick: MaskedArray
    segment_priceline: MaskedArray

    price_facecolors: MaskedArray
    price_edgecolors: MaskedArray

    def _set_price_candle_segment(self, ind_start, ind_end, /):
        # print(f'{(ind_start, ind_end)=}')
        self.collection_price.set_segments(self.segment_candle[ind_start:ind_end])
        self.collection_price.set_facecolor(self.price_facecolors[ind_start:ind_end])
        self.collection_price.set_edgecolor(self.price_edgecolors[ind_start:ind_end])
        self.collection_price.set_linewidth(self.STYLE.CHART.PRICE.linewidth)
        # print('candle')
        return

    def _set_price_wick_segment(self, ind_start, ind_end, /):
        seg = self.segment_wick[ind_start:ind_end]
        # print(f'{seg=}')
        self.collection_price.set_segments(seg)
        self.collection_price.set_facecolor([])
        self.collection_price.set_edgecolor(self.price_edgecolors[ind_start:ind_end])
        self.collection_price.set_linewidth(1.5)
        # print('wick')
        return

    def _set_price_line_segment(self, ind_start, ind_end, /, *, step=1):
        if step == 1:
            seg = self.segment_priceline[:, ind_start:ind_end]
        else:
            seg = self.segment_priceline[:, ind_start:ind_end:step]
        # print(f'{seg=}')
        self.collection_price.set_segments(seg)
        self.collection_price.set_facecolor([])
        self.collection_price.set_edgecolor(self.STYLE.CHART.PRICE.line_color)
        self.collection_price.set_linewidth(2)
        # print('priceline')
        return


class VolumeMixin:
    STYLE: Style

    key_volume: str

    collection_volume: LineCollection
    collection_volume: LineCollection

    segment_volume: MaskedArray
    segment_volume_wick: MaskedArray
    segment_volume_line: MaskedArray

    volume_facecolors: MaskedArray
    volume_edgecolors: MaskedArray

    def _set_volume_bar_segment(self, ind_start, ind_end, /):
        if not self.key_volume:
            return

        self.collection_volume.set_segments(self.segment_volume[ind_start:ind_end])
        self.collection_volume.set_facecolor(self.volume_facecolors[ind_start:ind_end])
        self.collection_volume.set_edgecolor(self.volume_edgecolors[ind_start:ind_end])
        self.collection_volume.set_linewidth(self.STYLE.CHART.VOLUME.linewidth)
        return

    def _set_volume_wick_segment(self, ind_start, ind_end, /):
        if not self.key_volume:
            return

        self.collection_volume.set_segments(self.segment_volume_wick[ind_start:ind_end])
        self.collection_volume.set_facecolor([])
        self.collection_volume.set_edgecolor(self.volume_edgecolors[ind_start:ind_end])
        self.collection_volume.set_linewidth(1.5)
        return


class ChartMixin(PriceMixin, MaMixin, VolumeMixin):
    limit_candle = 400
    limit_wick = 2_000

    def _set_candle_segment(self, *indices):
        self._set_price_candle_segment(*indices)
        self._set_volume_bar_segment(*indices)
        return

    def _set_wick_segment(self, *indices):
        self._set_price_wick_segment(*indices)
        self._set_volume_wick_segment(*indices)
        return

    def _set_priceline_segment(self, *indices):
        self._set_price_line_segment(*indices)
        self._set_volume_wick_segment(*indices)
        return

    def set_collection_segment(self, ind_start, ind_end, /):
        indices = (ind_start, ind_end)

        if ind_start < 0:
            ind_start = 0
        indsub = ind_end - ind_start
        # print(f'{indsub=:,}')

        step = 1
        if not self.limit_candle or indsub < self.limit_candle:
            # print('candle')
            self._set_candle_segment(*indices)
        else:
            if not self.limit_wick or indsub < self.limit_wick:
                # print('wick')
                self._set_wick_segment(*indices)
            else:
                # print('line')
                step = self.get_step(indsub)
                if not step:
                    step = 1
                self._set_priceline_segment(*indices)

        self.set_ma_collection_segment(*indices, step=step)
        return

    def get_step(self, indsub: float):
        return int(indsub // 1_500)


class SliderMixin:
    _nav_width: float

    collection_slider_top_nav: LineCollection
    collection_slider_bottom_nav: LineCollection

    def set_collection_nav_segment(self, xmin, xmax, /):
        ax: Axes = self.get_ax_slider()
        x0, y0, x1, y1 = ax.viewLim.extents

        xmin += 0.5
        xmax += 0.5
        left0 = xmin - self._nav_width
        left1 = xmin
        right0 = xmax
        right1 = xmax + self._nav_width
        seg = [
            # 좌측 오버레이
            (
                (x0, y1),
                (left0, y1),
                (left0, y0),
                (x0, y0),
            ),
            # 우측 오버레이
            (
                (right1, y1),
                (x1, y1),
                (x1, y0),
                (right1, y0),
            ),
            # 좌측 네비게이터
            (
                (left1, y1),
                (left1, y0),
                (left0, y0),
                (left0, y1),
            ),
            # 우측 네비게이터
            (
                (right0, y0),
                (right0, y1),
                (right1, y1),
                (right1, y0),
            ),
        ]
        self.segment_nav = MaskedArray(seg)

        self.collection_slider_top_nav.set_segments(self.segment_nav)
        self.collection_slider_bottom_nav.set_segments(self.segment_nav)
        return


class SegmentMixin(ChartMixin, SliderMixin):
    key_volume: str

    segment_volume_wick: MaskedArray
    volume_facecolors: MaskedArray
    volume_edgecolors: MaskedArray

    _click_x_coord: int

    limit_volume = 2000
    limit_ma = 8_000

    # def set_ma_collection_segment(self, ind_start, ind_end, /, step=1):
    #     if not self._click_x_coord:
    #         super().set_ma_collection_segment(ind_start, ind_end, step=step)
    #     else:
    #         indsub = ind_end - ind_start
    #         if indsub <= self.limit_ma:
    #             super().set_ma_collection_segment(ind_start, ind_end, step=step)
    #         else:
    #             # 이평선 그리지 않기
    #             self.collection_ma.set_segments([])
    #     return

    # def _set_volume_wick_segment(self, ind_start, ind_end, /):
    #     if not self.key_volume or not self._click_x_coord:
    #         super()._set_volume_wick_segment(ind_start, ind_end)
    #     else:
    #         indsub = ind_end - ind_start
    #         if indsub <= self.limit_volume:
    #             super()._set_volume_wick_segment(ind_start, ind_end)
    #         else:
    #             # 일부 거래량만 그리기
    #             seg_volume = self.segment_volume_wick[ind_start:ind_end]
    #             values = seg_volume[:, 1, 1]
    #             top_index = np.argsort(-values)[:self.limit_volume]
    #             seg = seg_volume[top_index]

    #             facecolors = self.volume_facecolors[ind_start:ind_end][top_index]
    #             edgecolors = self.volume_edgecolors[ind_start:ind_end][top_index]

    #             self.collection_volume.set_segments(seg)
    #             self.collection_volume.set_linewidth(1.3)
    #             self.collection_volume.set_facecolor(facecolors)
    #             self.collection_volume.set_edgecolor(edgecolors)
    #     return

    def _set_volume_wick_segment(self, ind_start, ind_end, /):
        if not self.key_volume:
            return

        indsub = ind_end - ind_start
        if indsub <= self.limit_volume:
            super()._set_volume_wick_segment(ind_start, ind_end)
        else:
            # 일부 거래량만 그리기
            seg_volume = self.segment_volume_wick[ind_start:ind_end]
            values = seg_volume[:, 1, 1]
            top_index = np.argsort(-values)[:self.limit_volume]
            seg = seg_volume[top_index]
            # seg = self.segment_volume_line[0, ind_start:ind_end]
            # print(f'{self.segment_volume_line=}')
            # print(f'{seg=}')

            # facecolors = self.volume_facecolors[ind_start:ind_end][top_index]
            # edgecolors = self.volume_edgecolors[ind_start:ind_end][top_index]
            facecolors = []
            edgecolors = self.STYLE.CHART.VOLUME.EDGECOLOR.unchange

            self.collection_volume.set_segments(seg)
            self.collection_volume.set_linewidth(1.3)
            self.collection_volume.set_facecolor(facecolors)
            self.collection_volume.set_edgecolor(edgecolors)

        return

