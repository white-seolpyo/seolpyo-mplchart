from matplotlib.artist import Artist
from matplotlib.axes import Axes
from matplotlib.backend_bases import PickEvent
from matplotlib.collections import LineCollection
from matplotlib.lines import Line2D
from matplotlib.text import Text
import pandas as pd

from ..style import Style


class Mamixin:
    STYLE: Style

    df: pd.DataFrame

    collection_ma: LineCollection

    ma_list: list[int]
    ma_colors: list[any]
    ma_format = '{}일선'
    ma_format_en = 'ma {}'

    _visible_ma = set()
    legends_dict: dict[Artist, tuple[Line2D, Text]] = {}

    def get_ma_legend_handles(self):
        item_list: list[Line2D] = []
        # Legend Ax에 표시하는 선 segment
        arr = [0, 1]
        for ma, color in zip(reversed(self.ma_list), reversed(self.ma_colors)):
            self._visible_ma.add(ma)
            label = self.ma_format.format(ma)
            # print(f'{label=}')
            item_list.append(Line2D(arr, ydata=arr, color=color, linewidth=5, label=label))

        return item_list

    def set_ma_legend(self):
        ax: Axes = self.get_ax_legend()
        legend = ax.get_legend()
        if legend:
            # 기존 lenend 제거
            legend.remove()

        self._visible_ma.clear()

        # 핸들 생성
        handles = self.get_ma_legend_handles()

        # 가격이동평균선 legend 생성
        self.legends_dict.clear()
        if handles:
            # 핸들에서 라벨 꺼내기
            labels = [handle.get_label() for handle in handles]
            legend = ax.legend(
                handles, labels, loc='lower left', ncol=self.STYLE.CHART.MA.ncol,
                borderpad=0.55,
                facecolor=self.STYLE.CHART.facecolor, edgecolor=self.STYLE.CHART.edgecolor,
                labelcolor=self.STYLE.CHART.fontcolor,
            )
            for handle, text in zip(legend.legend_handles, legend.get_texts()):
                self.legends_dict[handle] = (handle, text)
                self.legends_dict[text] = (handle, text)

                # set pick event
                handle.set_picker(5)
                text.set_picker(5)

                # set pick action
                pick_action = lambda x: self._ma_pick_action(x)
                setattr(handle, 'pick_action', pick_action)
                setattr(text, 'pick_action', pick_action)

        self.collection_ma.set_alpha([1 for _ in self.ma_list])

        return

    def _ma_pick_action(self, e: PickEvent):
        handle, text = self.legends_dict[e.artist]
        label = handle.get_label()
        for ma in self.ma_list:
            ma_label = self.ma_format.format(ma)
            # print(f'{label=}')
            if ma_label == label:
                break
        else:
            return
        # print(f'{label=}')

        legend_alpha = handle.get_alpha()
        visible = legend_alpha and legend_alpha < 0.9
        handle.set_alpha((1.0 if visible else 0.2))
        text.set_alpha(alpha = (1.0 if visible else 0.5))

        if visible:
            self._visible_ma = {i for i in self.ma_list if i in self._visible_ma or i == ma}
        else:
            self._visible_ma = {i for i in self._visible_ma if i != ma}

        alphas = [(1 if i in self._visible_ma else 0) for i in self.ma_list]
        self.collection_ma.set_alpha(alphas)

        self.draw()

        return

