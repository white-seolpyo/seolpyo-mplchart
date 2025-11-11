import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.collections import LineCollection
from matplotlib.text import Text

from ..._config import SLIDERCONFIG, SliderConfigData
from ..base.a_canvas import CanvasMixin as BaseMixin, Figure


class Base(BaseMixin):
    CONFIG: SliderConfigData

    def add_axes(self):
        if not self.figure:
            self.figure, *_ = plt.subplots(
                7, # row 수
                figsize=self.CONFIG.FIGURE.figsize, # 기본 크기
                height_ratios=(
                    0,
                    0,
                    0,
                    self.CONFIG.FIGURE.RATIO.price,
                    self.CONFIG.FIGURE.RATIO.volume,
                    0,
                    0,
                ) # row 크기 비율
            )

        self._ax_slider_top, self.ax_none_top, self.ax_legend, self.ax_price, self.ax_volume, self.ax_none_bottom, self._ax_slider_bottom = self.figure.axes

        return


class FigureMixin(Base):
    key_volume: str
    ax_legend: Axes

    slider_top = True

    def _set_figure_ratios(self):
        gs = self.figure.axes[0].get_subplotspec().get_gridspec()

        ratio_volume = self.CONFIG.FIGURE.RATIO.volume
        if not self.key_volume:
            ratio_volume = 0

        legend = self.ax_legend.get_legend()
        if not legend:
            if self.slider_top:
                ratios = [
                    self.CONFIG.FIGURE.RATIO.slider,
                    0,
                    0,
                    self.CONFIG.FIGURE.RATIO.price, ratio_volume,
                    0,
                    0,
                ]
            else:
                ratios = [
                    0,
                    0,
                    0,
                    self.CONFIG.FIGURE.RATIO.price, ratio_volume,
                    self.CONFIG.FIGURE.RATIO.none,
                    self.CONFIG.FIGURE.RATIO.slider,
                ]
        else:
            fig_heihgt = self.figure.get_figheight()
            fig_px = fig_heihgt * (1-self.CONFIG.FIGURE.ADJUST.hspace*2) * self.figure.dpi
            # print(f'{(fig_heihgt, fig_px)=}')

            # Legend에 Axes 높이 맞추기
            bbox = legend.get_window_extent().transformed(self.figure.transFigure.inverted())
            ax_pos = self.ax_legend.get_position()
            self.ax_legend.set_position([ax_pos.x0, ax_pos.y0, ax_pos.width, bbox.height])

            legend_height = bbox.height
            legend_px = legend.get_window_extent().height
            # print(f'{(legend_height, legend_px)=}')

            chart_px = fig_px - legend_height
            chart_ratio = self.CONFIG.FIGURE.RATIO.price + ratio_volume

            # print(f'{self.CONFIG.FIGURE.RATIO.__dict__=}')
            ratio_none = 0 if self.slider_top else self.CONFIG.FIGURE.RATIO.none
            chart_ratio += self.CONFIG.FIGURE.RATIO.slider
            div_chart = chart_px / chart_ratio
            price_px = div_chart * self.CONFIG.FIGURE.RATIO.price
            volume_px = div_chart * ratio_volume
            slider_px = div_chart * self.CONFIG.FIGURE.RATIO.slider
            none_px = div_chart * ratio_none
            # print(f'{none_px=}')

            if self.slider_top:
                # 차트 비율
                ratios = [
                    slider_px,
                    0,
                    legend_px * 3,
                    price_px, volume_px,
                    0,
                    0,
                ]
            else:
                ratios = [
                    0,
                    0,
                    legend_px * 1.2,
                    price_px, volume_px,
                    none_px,
                    slider_px,
                ]

        # print(f'{ratios=}')
        gs.set_height_ratios(ratios)

        self.figure.tight_layout()

        # 플롯간 간격 설정(Configure subplots)
        self.figure.subplots_adjust(**self.CONFIG.FIGURE.ADJUST.__dict__)

        return

    def _set_figure(self):
        self.figure.canvas.manager.set_window_title('Seolpyo MPLChart')

        # print(f'{self.CONFIG.FIGURE.RATIO.volume=}')
        # print(f'{gs.get_height_ratios()=}')

        self._set_figure_ratios()

        self.figure.set_facecolor(self.CONFIG.FIGURE.facecolor)
        return


class AxesMixin(Base):
    slider_top = True

    ax_slider: Axes = None

    collection_slider: LineCollection
    collection_nav: LineCollection
    collection_slider_vline: LineCollection
    artist_text_slider: Text

    def _set_axes(self):
        super()._set_axes()

        if self.slider_top:
            ax_slider = self._ax_slider_top
        else:
            ax_slider = self._ax_slider_bottom

        if self.ax_slider and ax_slider is not self.ax_slider:
            # print('move artist')
            # ax_slider 위치가 변경된 경우 artist 이동하기
            artists: list[LineCollection|Text] = [
                self.collection_slider,
                self.collection_nav,
                self.collection_slider_vline,
                self.artist_text_slider,
            ]
            for artist in artists:
                artist.remove()
                artist.set_transform(ax_slider.transData)
                ax_slider.add_artist(artist)
            # axis
            ax_slider.set_xlim(*self.ax_slider.get_xlim())
            ax_slider.set_ylim(*self.ax_slider.get_ylim())
            # tick label
            ax_slider.set_xticks(self.ax_slider.get_xticks(minor=True), minor=True)
            ax_slider.set_xticklabels(self.ax_slider.get_xticklabels(minor=True), minor=True)

        self.ax_slider = ax_slider

        self._ax_slider_top.set_label('top slider ax')
        self._ax_slider_bottom.set_label('bottom slider ax')
        self.ax_none_top.set_label('top none ax')
        self.ax_none_bottom.set_label('bottom none ax')

        self.ax_slider.set_label('slider ax')

        for ax in (self.ax_none_top, self.ax_none_bottom):
            ax.set_animated(True)
            ax.set_axis_off()

        self._set_axes_slider()

        return

    def _set_axes_slider(self):
        # print(f'{self.slider_top=}')
        formatter = lambda x, _: self.CONFIG.UNIT.func(
            x,
            word=self.CONFIG.UNIT.price,
            digit=self.CONFIG.UNIT.digit+2
        )
        # 공통 설정
        for ax in (self._ax_slider_top, self._ax_slider_bottom):
            ax.yaxis.set_major_formatter(formatter)
            # x tick 외부 눈금 표시하지 않기
            ax.xaxis.set_ticks_position('none')
            # x tick label 제거
            ax.set_xticklabels([])
            # y tick 눈금 표시하지 않기
            ax.yaxis.set_ticks_position('none')

            # 차트 영역 배경 색상
            ax.set_facecolor(self.CONFIG.AX.facecolor)

            # Axes 외곽선 색 변경(틱 색과 일치)
            for i in ['top', 'bottom', 'left', 'right']:
                ax.spines[i].set_color(self.CONFIG.AX.TICK.edgecolor)
            # 틱 색상
            ax.tick_params('both', colors=self.CONFIG.AX.TICK.edgecolor)
            # 틱 라벨 색상
            ticklabels: list[Text] = ax.get_xticklabels() + ax.get_yticklabels()
            for ticklabel in ticklabels:
                ticklabel.set_color(self.CONFIG.AX.TICK.fontcolor)

            # Axes grid(구분선, 격자) 그리기
            # 어째서인지 grid의 zorder 값을 선언해도 1.6을 값으로 한다.
            ax.grid(**self.CONFIG.AX.GRID.__dict__)

            # major tick mark 길이를 0으로 만들어 튀어나오지 않게 하기
            ax.tick_params('x', which='major', length=0)
            # minor tick mark 색상 변경
            ax.tick_params('x', which='minor', colors=self.CONFIG.AX.TICK.edgecolor)
            # 틱 라벨 색상
            ticklabels: list[Text] = ax.get_xticklabels(minor=True) + ax.get_yticklabels()
            for ticklabel in ticklabels:
                ticklabel.set_color(self.CONFIG.AX.TICK.fontcolor)

            ax.yaxis.set_ticks_position('right')
        # 상단 슬라이더의 x tick 하단 설정
        self._ax_slider_top.xaxis.set_ticks_position('bottom')
        # 하단 슬라이더의 x tick 상단 설정
        self._ax_slider_bottom.xaxis.set_ticks_position('top')

        return


class CanvasMixin(FigureMixin, AxesMixin):
    slider_top = True

    figure: Figure

    ax_legend: Axes
    ax_price: Axes
    ax_volume: Axes
    ax_slider: Axes
    ax_none: Axes
    _ax_slider_top: Axes
    _ax_slider_bottom: Axes

    def __init__(self, config=SLIDERCONFIG):
        super().__init__(config=config)
        return


