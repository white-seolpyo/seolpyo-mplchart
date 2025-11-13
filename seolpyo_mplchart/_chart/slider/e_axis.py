from matplotlib.collections import LineCollection
import numpy as np


class Base:
    limit_volume = 200
    limit_ma = 8_000

    x_click: int
    vxmin: int
    vxmax: int

    axis: callable
    _set_nav_segment: callable
    set_collections: callable

    key_volume: str
    segment_volume_wick: np.ndarray
    _set_volume_collection_wick_segments: callable
    _set_ma_collection_segments: callable
    facecolor_volume: np.ndarray
    edgecolor_volume: np.ndarray
    collection_volume: LineCollection
    collection_ma: LineCollection


class Mixin(Base):
    def axis(self, xmin, *, xmax):
        super().axis(xmin, xmax=xmax)
        self._set_nav_segment(self.vxmin, xmax=self.vxmax-1)
        return

    def _set_volume_collection_wick_segments(self, ind_start, ind_end):
        if not self.key_volume or not self.x_click:
            super()._set_volume_collection_wick_segments(ind_start, ind_end=ind_end)
        else:
            indsub = ind_end - ind_start
            if indsub <= self.limit_volume:
                super()._set_volume_collection_wick_segments(ind_start, ind_end=ind_end)
            else:
                # 일부 거래량만 그리기
                seg_volume = self.segment_volume_wick[ind_start:ind_end]
                values = seg_volume[:, 1, 1]
                top_index = np.argsort(-values)[:self.limit_volume]
                seg = seg_volume[top_index]
                facecolors = self.facecolor_volume[ind_start:ind_end][top_index]
                edgecolors = self.edgecolor_volume[ind_start:ind_end][top_index]
                self.collection_volume.set_segments(seg)
                self.collection_volume.set_linewidth(1.3)
                self.collection_volume.set_facecolor(facecolors)
                self.collection_volume.set_edgecolor(edgecolors)
        return

    def _set_ma_collection_segments(self, ind_start, ind_end):
        if not self.x_click:
            super()._set_ma_collection_segments(ind_start, ind_end=ind_end)
        else:
            indsub = ind_end - ind_start
            if indsub <= self.limit_ma:
                super()._set_ma_collection_segments(ind_start, ind_end=ind_end)
            else:
                # 이평선 그리지 않기
                self.collection_ma.set_segments([])
        return


class AxisMixin(Mixin):
    limit_volume = 200
    limit_ma = 8_000

