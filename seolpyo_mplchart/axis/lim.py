from matplotlib.axes import Axes
from matplotlib.collections import LineCollection
from matplotlib.text import Text
import numpy as np
from numpy.ma import MaskedArray
import pandas as pd

from ..style import Style


class PriceMixin:
    df: pd.DataFrame

    digit_price: int

    def _calc_price_ylim(self, ind_start, ind_end, /):
        if ind_start < 0:
            ind_start = 0
        ind_end += 1
        low = self.df['low'].to_numpy()[ind_start:ind_end].min()
        high = self.df['high'].to_numpy()[ind_start:ind_end].max()
        return (low, high)

    def calc_price_ylim(self, ind_start, ind_end, /):
        low, high = self._calc_price_ylim(ind_start, ind_end)

        if low == high:
            if low:
                ymin, ymax = (round(high * 0.9, self.digit_price+2), round(high * 1.1, self.digit_price+2))
            else:
                ymin, ymax = (-5, 10)
        else:
            height = high - low

            ymin = low - round(height / 10, self.digit_price+2)
            ymax = high + round(height / 10, self.digit_price+2)

        return (ymin, ymax)


class VolumeMixin:
    df: pd.DataFrame
    digit_volume: int

    def _calc_volume_ymax(self, ind_start, ind_end, /):
        if ind_start < 0:
            ind_start = 0
        ind_end += 1
        high = self.df['volume'].to_numpy()[ind_start:ind_end].max()
        return high

    def calc_volume_ymax(self, ind_start, ind_end, /):
        high = self._calc_volume_ymax(ind_start, ind_end)

        if not high:
            ymax = 10
        else:
            ymax = high + round(high / 5, self.digit_volume+2)
            if ymax <= 0:
                ymax = 10
        # print(f'{(high, ymax)=}')

        return (0, ymax)


class ChartMixin(PriceMixin, VolumeMixin):
    STYLE: Style

    max_xticks = 8
    periods = np.array([
        5,         # 1 week
        10,        # 2 week
        20,        # 1 month
        60,        # 3 month
        120,       # 6 month
        240,       # 1 year
        5 * 240,   # 5 year
        10 * 240,  # 10 year
        20 * 240,  # 20 year
        60 * 240,  # 60 year
        120 * 240, # 120 year
        240 * 240, # 240 year
    ])

    collection_grid_price: LineCollection
    collection_grid_volume: LineCollection

    def axis_price_chart(self, x0, x1, xticks, /):
        """
        주가 차트 xlim
        """
        ax: Axes = self.get_ax_price()

        ax.set_xlim(x0, x1+1)

        # 주가 차트 ylim
        y0, y1 = self.calc_price_ylim(x0, x1)
        ax.set_ylim(y0, y1)

        ax.set_xticks(xticks)
        # grid segment
        grid_x = grid_y = []
        if self.STYLE.CHART.GRID.axis in {'both', 'x'}:
            grid_x = [[(x, y0), (x, y1)] for x in xticks]
        if self.STYLE.CHART.GRID.axis in {'both', 'y'}:
            grid_y = [[(x0, y), (x1+1, y)] for y in ax.get_yticks()]
        self.collection_grid_price.set_segments(MaskedArray(grid_x + grid_y))

        return

    def axis_volume_chart(self, x0, x1, xticks, /):
        """
        거래량 차트 xlim
        """
        ax: Axes = self.get_ax_volume()

        ax.set_xlim(x0, x1+1)

        # 거래량 차트 ylim
        y0, y1 = self.calc_volume_ymax(x0, x1)
        ax.set_ylim(y0, y1)

        ax.set_xticks(xticks)
        # grid segment
        grid_x = grid_y = []
        if self.STYLE.CHART.GRID.axis in {'both', 'x'}:
            grid_x = [[(x, y0), (x, y1)] for x in xticks]
        if self.STYLE.CHART.GRID.axis in {'both', 'y'}:
            grid_y = [[(x0, y), (x1+1, y)] for y in ax.get_yticks()]
        self.collection_grid_volume.set_segments(MaskedArray(grid_x + grid_y))

        return

    def calc_xticks(self, xmin, xmax, /):
        item_list: list[int] = []

        periods = self.periods
        sub: int = xmax - xmin
        if sub < periods.min():
            return item_list

        max_ticks = self.max_xticks
        arr_div = sub / periods
        mask = arr_div <= max_ticks
        # print(f'{mask=}')
        if np.any(mask):
            period: int = periods[mask].min()  # 가장 작은 단위 중 조건 만족
        else:
            period = periods.max()
        # print(f'{period=}')

        ind_end = int(self.df.index[-1]) + 1

        ticks = np.arange(0, ind_end * period, period)
        mask = (xmin <= ticks) & (ticks <= xmax)
        item_list += ticks[mask].tolist()

        return item_list

    def axis_chart(self, x0, x1, /):
        xticks = self.calc_xticks(x0, x1)

        self.axis_price_chart(x0, x1, xticks)
        self.axis_volume_chart(x0, x1, xticks)

        self.set_xtick_labels()

        return

    def set_xtick_labels(self):
        ax: Axes = self.get_ax_volume()

        xmin, xmax = ax.get_xlim()
        xmin = int(xmin)
        xmax = int(xmax) - 1

        # x축에 일부 date 표시하기
        xsub = xmax - xmin
        xmiddle = xmin + (xsub // 2)
        ind_end = int(self.df.index[-1])
        indices = [idx for idx in (xmin, xmiddle, xmax) if 0 <= idx and idx <= ind_end]
        len_indices = len(indices)
        # print(f'{xmiddle=}')
        # print(f'{indices=}')
        # print(f'{len_indices=}')

        aligns = ['left', 'center', 'center']
        m = (xmiddle - xmin) // 2
        x0 = xmin + m    # 1/4
        x1 = xmiddle + m # 3/4
        if not indices:
            indices.append(ind_end)
            if ind_end < x0:
                aligns = aligns[:1]
            else:
                aligns = aligns[-1:]
        elif len_indices == 1:
            x = indices[0]
            if x == xmin:
                if ind_end < x0:
                    indices[0] = ind_end
                    aligns = aligns[:1]
                else:
                    indices.append(ind_end)
                    aligns = aligns[:2]
            elif x == xmiddle:
                # print('x == xmiddle')
                # print(f'{(xmin, xmax)=}')
                # print(f'{(ind_end)=}')
                if xmin <= 0 and ind_end <= xmax:
                    if ind_end < m:
                        # print('ind_end < m')
                        indices[0] = ind_end
                        if ind_end <= x0:
                            aligns = aligns[:1]
                        else:
                            aligns = aligns[-1:]
                    else:
                        # print('not ind_end < m')
                        indices = [0, ind_end]
                        aligns = aligns[:2]
            else:
                if 0 < x1:
                    indices = [0, x]
                    aligns = aligns[-2:]
                else:
                    indices[0] = 0
                    aligns = aligns[-1:]
        elif len_indices == 2:
            if xmin < 0:
                if 0 <= x0:
                    indices = [0] + indices
                else:
                    aligns = aligns[-2:]
                    indices[0] = 0
            else:
                if x1 < ind_end:
                    indices.append(ind_end)
                else:
                    aligns = aligns[:2]
                    indices[-1] = ind_end

        # print(f'{indices=}')
        date_list = [self.df.iloc[idx]['date'] for idx in indices]
        # print(f'{date_list=}')
        # 라벨을 노출할 틱 위치, major tick과 겹쳐서 무시되는 것 방지
        ax.set_xticks([idx+0.501 for idx in indices], minor=True)
        # 라벨
        ax.set_xticklabels(date_list, minor=True)
        labels: list[Text] = ax.get_xticklabels(minor=True)
        for label, align in zip(labels, aligns):
            # 라벨 텍스트 정렬
            label.set_horizontalalignment(align)

        return


class SliderMixin:
    df: pd.DataFrame

    digit_price: int

    def axis_slider(self):
        self._axis_slider('top')
        self._axis_slider('bottom')
        return

    def _axis_slider(self, position):
        # print('_set_slider')
        ax: Axes = getattr(self, f'get_ax_slider_{position}')()

        self._set_slider_xtick(ax)

        ind_end = int(self.df.index[-1]) + 1

        xmax = ind_end + 1
        # 슬라이더 xlim
        xdistance = round(xmax / 30)
        x0, x1 = (-xdistance, xmax+xdistance)
        ax.set_xlim(x0, x1)

        # 네비게이터 경계선 두께
        self._nav_width = round((x1 - x0) / 200, 2)

        # 슬라이더 ylim
        ymin, ymax = (self.df['low'].min(), self.df['high'].max())
        ysub = ymax - ymin
        ydistance = round(ysub / 5, self.digit_price+2)
        y0, y1 = (ymin-ydistance, ymax+ydistance)
        ax.set_ylim(y0, y1)

        # 네비게이터 경계선 두께
        self._nav_width = round((x1 - x0) / 200, 2)

        return

    def _set_slider_xtick(self, ax: Axes):
        ind_end = int(self.df.index[-1])
        if not ind_end:
            return

        # print(self.df.index[:5])
        # print(self.df.index[-5:])

        indices = [0, ind_end]
        # print(f'{indices=}')

        date_list = [self.df.iloc[idx]['date'] for idx in indices]
        # print(f'{date_list=}')
        # xtick 설정, major tick과 겹쳐서 무시되는 것 방지
        ax.set_xticks([idx+0.51 for idx in indices], labels=date_list, minor=True)

        labels = ax.get_xticklabels(minor=True)
        # print(f'{labels=}')
        for label, align in zip(labels, ['center', 'center']):
            # 라벨 텍스트 정렬
            label.set_horizontalalignment(align)
        return


class LimMixin(ChartMixin, SliderMixin):
    pass

