import matplotlib.pyplot as plt
import matplotlib.style as mplstyle
from matplotlib.artist import Artist
from matplotlib.axes import Axes
from matplotlib.backends.backend_agg import FigureCanvasAgg, RendererAgg
from matplotlib.backend_bases import FigureManagerBase
from matplotlib.figure import Figure as Fig
from matplotlib.text import Text

try: plt.switch_backend('TkAgg')
except: pass

# 한글 깨짐 문제 방지
try: plt.rcParams['font.family'] ='Malgun Gothic'
except: pass

from ..._config import DEFAULTCONFIG, ConfigData


mplstyle.use('fast')


class Canvas(FigureCanvasAgg):
    manager: FigureManagerBase
    renderer = RendererAgg

class Figure(Fig):
    canvas: Canvas


class Base:
    CONFIG: ConfigData
    figure: Figure = None

    def add_axes(self):
        if not self.figure:
            self.figure, *_ = plt.subplots(
                3, # row 수
                figsize=self.CONFIG.FIGURE.figsize, # 기본 크기
                height_ratios=(
                    1,
                    self.CONFIG.FIGURE.RATIO.price,
                    self.CONFIG.FIGURE.RATIO.volume,
                ) # row 크기 비율
            )

        self.ax_legend, self.ax_price, self.ax_volume = self.figure.axes
        self.ax_legend.set_label('legend ax')
        self.ax_price.set_label('price ax')
        self.ax_volume.set_label('volume ax')

        return


class FigureMixin(Base):
    key_volume: str
    ax_legend: Axes

    def _set_figure_ratios(self):
        gs = self.figure.axes[0].get_subplotspec().get_gridspec()

        ratio_volume = self.CONFIG.FIGURE.RATIO.volume
        if not self.key_volume:
            ratio_volume = 0

        legend = self.ax_legend.get_legend()
        if not legend:
            ratios = [
                0,
                self.CONFIG.FIGURE.RATIO.price, ratio_volume
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
            div_chart = chart_px / chart_ratio
            price_px = div_chart * self.CONFIG.FIGURE.RATIO.price
            volume_px = div_chart * ratio_volume

            # 차트 비율 변경
            ratios = [
                legend_px * 1.2,
                price_px, volume_px
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


class AxesMixin(FigureMixin):
    def _set_axes(self):
        # ax 요소 animated 처리
        for ax in self.figure.axes:
            ax.patch.set_animated(True)

            # ax 경계선
            for spine in ax.spines.values():
                spine.set_animated(True)

            for axis in (ax.xaxis, ax.yaxis):
                axis.set_animated(True)
                axis.label.set_animated(True)
                for tick in axis.get_major_ticks() + axis.get_minor_ticks():
                    artists: list[Artist] = [
                        tick.tick1line, tick.tick2line,
                        tick.gridline,
                        tick.label1, tick.label2
                    ]
                    for artist in artists:
                        if artist is not None:
                            artist.set_animated(True)

        # y ticklabel foramt 설정
        self.ax_price.yaxis.set_major_formatter(
            lambda x, _: self.CONFIG.UNIT.func(
                x,
                word=self.CONFIG.UNIT.price,
                digit=self.CONFIG.UNIT.digit+(0 if self.CONFIG.UNIT.digit % 1 else 2)
            )
        )
        self.ax_volume.yaxis.set_major_formatter(
            lambda x, _: self.CONFIG.UNIT.func(
                x,
                word=self.CONFIG.UNIT.volume,
                digit=self.CONFIG.UNIT.digit_volume
            )
        )

        if not self.key_volume:
            # tick 그리지 않기
            self.ax_volume.set_yticklabels([])
            self.ax_volume.set_yticks([])

        # 공통 설정
        for ax in (self.ax_price, self.ax_volume):
            ax.xaxis.set_animated(True)
            ax.yaxis.set_animated(True)

            # x tick 외부 눈금 표시하지 않기
            ax.xaxis.set_ticks_position('none')
            # x tick label 제거
            ax.set_xticklabels([])
            # y tick 위치를 우측으로 이동
            ax.tick_params(left=False, right=True, labelleft=False, labelright=True)

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
        
        # 거래량 차트의 x tick 외부 눈금 표시하기
        self.ax_volume.xaxis.set_ticks_position('bottom')
        # major tick mark 길이를 0으로 만들어 튀어나오지 않게 하기
        self.ax_volume.tick_params('x', which='major', length=0)
        # minor tick mark 색상 변경
        self.ax_volume.tick_params('x', which='minor', colors=self.CONFIG.AX.TICK.edgecolor)
        return


class LegendMixin(AxesMixin):
    def _set_axes_legend(self):
        # 이평선 라벨 axis 그리지 않기
        self.ax_legend.set_axis_off()
        self.ax_legend.xaxis.set_animated(True)
        self.ax_legend.yaxis.set_animated(True)
        self.ax_legend.set_animated(True)

        # 이평선 라벨 Axes 배경색
        legends = self.ax_legend.get_legend()
        if legends:
            legends.get_frame().set_facecolor(self.CONFIG.AX.facecolor)

        # 이평선 라벨 Axes 테두리색
        legends = self.ax_legend.get_legend()
        if legends:
            legends.get_frame().set_edgecolor(self.CONFIG.AX.TICK.edgecolor)

        # 이평선 라벨 폰트 색상
        fontcolor = self.CONFIG.AX.TICK.fontcolor
        legends = self.ax_legend.get_legend()
        if legends:
            legend_labels: list[Text] = legends.texts
            for i in legend_labels:
                i.set_color(fontcolor)
        return


class CanvasMixin(LegendMixin):
    figure: Figure
    ax_legend: Axes
    ax_price: Axes
    ax_volume: Axes

    def __init__(self, config=DEFAULTCONFIG):
        # 기본 툴바 비활성화
        plt.rcParams['toolbar'] = 'None'
        # plt.rcParams['figure.dpi'] = 600

        self.CONFIG = config
        self.add_axes()
        self.set_canvas()
        return

    def set_canvas(self):
        self._set_axes()
        self._set_axes_legend()
        self._set_figure()
        return

