import numpy as np

from ..style import Style


class SliderMixin:
    STYLE: Style

    ma_list: list[int]
    ma_colors: list[any]

    segment_priceline: np.ma.MaskedArray
    segment_ma: np.ma.MaskedArray

    def set_slider_segment(self):
        if not self.ma_list:
            self.segment_slider = self.segment_priceline
            self.slider_edgecolors = [self.STYLE.CHART.PRICE.line_color]
            self.slider_linewidths = [2.4]
        else:
            seg_priceline = self.segment_priceline
            seg_ma = self.segment_ma
            seg = np.concatenate([seg_ma, seg_priceline], axis=0)

            self.segment_slider = seg

            linewidth = []
            ma_colors = self.ma_colors

            self.slider_edgecolors = ma_colors + [self.STYLE.CHART.PRICE.line_color]
            self.slider_linewidths = linewidth + [2.4]

        # print(f'{self.segment_slider=}')

        return

