from matplotlib.artist import Artist
from matplotlib.axes import Axes
from matplotlib.collections import LineCollection
from matplotlib.text import Text

import matplotlib.pyplot as plt
import pandas as pd

from ..utils.formatter import Formatter, FormatterEN

from ..models import Figure, AdjustData, AxData
from ..style import Style


class SliderAxMixin:
    STYLE: Style

    collection_slider: LineCollection
    collection_nav: LineCollection
    collection_slider_vline: LineCollection

    df: pd.DataFrame

    FORMATTER: Formatter

    def slider_formatter(self, x, pos):
        ax: Axes = self.get_ax_slider()
        y0, y1 = ax.get_ylim()
        if y0 <= x and x <= y1:
            # print('slider_formatter')
            # print(y0, y1)
            # print(x)
            return self.FORMATTER.price_formatter(x, pos)
        return ''

    def _set_ax_slider(self, position):
        ax: Axes = getattr(self, f'get_ax_slider_{position}')()

        # print(f'{self.slider_top=}')
        formatter = lambda x, pos: self.slider_formatter(x, pos)
        # 공통 설정
        for axis in (ax.xaxis, ax.yaxis):
            axis.set_major_locator(plt.AutoLocator())

        ax.xaxis.set_tick_params(which='minor', bottom=True, length=4)

        ax.yaxis.set_tick_params(which='major', right=True)
        ax.yaxis.set_major_formatter(formatter)

        # Axes grid(구분선, 격자) 그리기
        # 어째서인지 grid의 zorder 값을 선언해도 1.6을 값으로 한다.
        ax.grid(**self.STYLE.CHART.GRID.__dict__)

        # 슬라이더 x tick 위치
        ax.xaxis.set_ticks_position('bottom')

        return

    def set_ax_slider_top(self):
        self._set_ax_slider('top')

        return

    def set_ax_slider_bottom(self):
        self._set_ax_slider('bottom')

        return

    def set_ax_slider(self):
        self.set_ax_slider_top()
        self.set_ax_slider_bottom()

        return


class ChartAxMixin:
    STYLE: Style
    FORMATTER: Formatter

    def set_ax_legend(self):
        ax: Axes = self.get_ax_legend()

        # 이평선 라벨 Axes 배경색
        legend = ax.get_legend()
        if legend:
            legend.get_frame().set_facecolor(self.STYLE.CHART.facecolor)
            legend.get_frame().set_edgecolor(self.STYLE.CHART.edgecolor)

            # 이평선 라벨 폰트 색상
            fontcolor = self.STYLE.CHART.fontcolor
            legend_labels: list[Text] = legend.texts
            for i in legend_labels:
                i.set_color(fontcolor)
        return

    def price_formatter(self, x, pos):
        ax: Axes = self.get_ax_price()
        y0, y1 = ax.get_ylim()
        if y0 <= x and x <= y1:
            # print('price_formatter')
            # print(y0, y1)
            # print(x)
            return self.FORMATTER.price_formatter(x, pos)
        return ''

    def set_ax_price(self):
        ax: Axes = self.get_ax_price()

        for axis in (ax.yaxis,):
            axis.set_major_locator(plt.AutoLocator())

        ax.yaxis.set_tick_params(which='major', right=True)
        ax.yaxis.set_major_formatter(lambda x, pos: self.price_formatter(x, pos))

        return

    def volume_formatter(self, x, pos):
        ax: Axes = self.get_ax_volume()
        y0, y1 = ax.get_ylim()
        if y0 <= x and x <= y1:
            # print('volume_formatter')
            # print(y0, y1)
            # print(x)
            return self.FORMATTER.volume_formatter(x, pos)
        return ''

    def set_ax_volume(self):
        ax: Axes = self.get_ax_volume()

        for axis in (ax.yaxis,):
            axis.set_major_locator(plt.AutoLocator())
        # ax.xaxis.set_minor_locator(AutoMinorLocator())
        ax.xaxis.set_tick_params(which='minor', bottom=True, length=4)

        ax.yaxis.set_tick_params(which='major', right=True)
        ax.yaxis.set_major_formatter(lambda x, pos: self.volume_formatter(x, pos))

        return


class RatioMixin:
    key_volume: str

    show_slider: bool
    slider_top: bool

    artist_label_slider_top: Artist
    artist_label_slider_bottom: Artist

    figure: Figure

    STYLE: Style

    def get_adjust(self) -> AdjustData:
        "https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.subplots_adjust.html"
        adjust: AdjustData = {
            'top': 0.98,
            'bottom': 0.05,
            'left': 0.01,
            'right': 0.93,
            'wspace': 0,
            'hspace': 0,
        }

        return adjust

    def set_figure_ratios(self):
        """
        min size: 400px * 600px
        """
        # figure 내부 높이
        fig_height = float(self.figure.get_figheight() * self.figure.dpi)
        # print(f'{fig_height=}')
        if fig_height < 400:
            # print('height < 400')
            return
        fig_width = float(self.figure.get_figwidth() * self.figure.dpi)
        # print(f'{fig_width=}')
        if fig_width < 600:
            # print('width < 600')
            return

        # 다음 에러를 방지하기 위해 Text Artist는 제거한다.
        # matplotlib.units.ConversionError: Failed to convert value(s) to axis units: ''
        for position in ['top', 'bottom']:
            artist_label = getattr(self, f'artist_label_slider_{position}')
            if artist_label:
                artist_label.remove()
                del artist_label
                setattr(self, f'artist_label_slider_{position}', None)

        ax_config_list: list[AxData] = self._get_ax_config_list()
        if (len(ax_config_list) + 2) != len(self.figure.axes):
            msg = 'ax_config_list length+2 does not match len(self.figure.axes)\n  If you want add Axes, override Chart.get_ax_config_list() and Create New Chart Instance.'
            raise Exception(msg)

        adjust = self.get_adjust()
        max_height = fig_height * (adjust['top'] - adjust['bottom'])

        show_volume = bool(self.key_volume)

        ratio_height = max_height
        ratios = []
        for config in ax_config_list:
            # print(f'{ax_config=}')
            label = config['name']
            if not self.show_slider and label in {'slider', 'none'}:
                pass
            elif not show_volume and label == 'volume':
                pass
            else:
                if not config['is_px']:
                    ratios.append(config['size'])
                else:
                    ax_height = config['size']
                    if label == 'none' and self.slider_top:
                        ax_height = ax_height / 2
                    ratio_height -= ax_height

        sum_ratios = sum(ratios)

        ratio_list = []
        for config in ax_config_list:
            # print(f'{ax_config=}')
            label = config['name']
            if not self.show_slider and label in {'slider', 'none'}:
                ratio_list.append(0)
            elif not show_volume and label == 'volume':
                ratio_list.append(0)
            else:
                if config['is_px']:
                    ax_height = config['size']
                    if label == 'none' and self.slider_top:
                        ax_height = ax_height / 2
                else:
                    ax_height = ratio_height * (config['size'] / sum_ratios)
                    ax_height = round(ax_height, 2)
                ratio = ax_height / fig_height
                ratio_list.append(ratio)

        if self.slider_top:
            ratio_list += [0, 0]
        else:
            ratio_slider, ratio_none, *ratio_list = ratio_list
            ratio_list = [0, 0] + ratio_list + [ratio_none, ratio_slider]

        # print(f'{ratio_list=}')

        gs = self.figure.axes[0].get_subplotspec().get_gridspec()
        gs.set_height_ratios(ratio_list)

        self.figure.tight_layout()

        # 플롯간 간격 설정(Configure subplots)
        self.figure.subplots_adjust(**adjust)

        return

    def get_window_title(self):
        return 'Seolpyo MPLChart'

    def set_figure(self):
        if (
            getattr(self.figure, 'canvas', None)
            and self.figure.canvas.manager
            and hasattr(self.figure.canvas.manager, 'set_window_title')
        ):
            self.figure.canvas.manager.set_window_title(self.get_window_title())

        self.set_figure_ratios()

        self.figure.set_facecolor(self.STYLE.CHART.facecolor)
        return


class AxesMixin(SliderAxMixin, ChartAxMixin):
    slider_top: bool

    figure: Figure

    STYLE: Style

    def _set_axes(self):
        for ax in self.figure.axes:
            # print(f'{ax.get_label()=}')
            # 차트 영역 배경 색상
            ax.set_facecolor(self.STYLE.CHART.facecolor)

            # xlim 변경시 ylim, ylim 변경시 xlim 자동계산하지 않도록 설정
            # ax.autoscale(False, axis='both')

            # ax 요소 animated 처리
            ax.patch.set_animated(True)

            # ax 경계선
            for spine in ax.spines.values():
                spine.set_animated(True)
                # Axes 외곽선 색 변경(틱 색과 일치)
                spine.set_color(self.STYLE.CHART.edgecolor)

            # x tick 외부 눈금 표시하지 않기, # y tick 위치를 우측으로 이동
            ax.tick_params(axis='x', which='major', length=0)
            # tick 공통설정
            ax.tick_params(
                which='both',
                left=False, labelleft=False,
                right=True, labelright=True,
                color=self.STYLE.CHART.edgecolor, labelcolor=self.STYLE.CHART.fontcolor,
            )

            null_locator = plt.NullLocator()
            null_formatter = plt.NullFormatter()
            for axis in (ax.xaxis, ax.yaxis):
                axis.set_animated(True)
                axis.label.set_animated(True)

                # 로케이터 off
                axis.set_major_locator(null_locator)
                axis.set_minor_locator(null_locator)

                # 포매터 단순화
                axis.set_major_formatter(null_formatter)
                axis.set_minor_formatter(null_formatter)

                # 틱 눈금 표시하지 않기
                axis.set_ticks_position('none')

                # tick 요소 animated
                for tick in axis.get_major_ticks() + axis.get_minor_ticks():
                    artists: list[Artist] = [
                        tick.tick1line, tick.tick2line,
                        tick.gridline,
                        tick.label1, tick.label2
                    ]
                    for artist in artists:
                        if artist is not None:
                            artist.set_animated(True)

        return


class UpdateMixin(AxesMixin, RatioMixin):
    def set_axes(self):
        self._set_axes()

        self.set_ax_legend()
        self.set_ax_price()
        self.set_ax_volume()

        self.set_ax_slider()

        return

    def set_canvas(self):
        # 항상 마지막에 실행
        self.set_figure()

        self.set_axes()

        return

