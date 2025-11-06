import matplotlib.pyplot as plt
import matplotlib.style as mplstyle
from matplotlib.axes import Axes
from matplotlib.backends.backend_agg import FigureCanvasAgg, RendererAgg
from matplotlib.backend_bases import FigureManagerBase
from matplotlib.figure import Figure as Fig
from matplotlib.text import Text

from .._config import DEFAULTCONFIG

try: plt.switch_backend('TkAgg')
except: pass

# 한글 깨짐 문제 방지
try: plt.rcParams['font.family'] ='Malgun Gothic'
except: pass

mplstyle.use('fast')


class Canvas(FigureCanvasAgg):
    manager: FigureManagerBase
    renderer = RendererAgg

class Figure(Fig):
    canvas: Canvas


class Base:
    watermark = 'seolpyo mplchart'

    figure: Figure

    def __init__(self, config=DEFAULTCONFIG):
        # 기본 툴바 비활성화
        plt.rcParams['toolbar'] = 'None'
        # plt.rcParams['figure.dpi'] = 600

        self.CONFIG = config
        self.add_axes()
        self.set_window()
        return

    def add_axes(self):
        self.figure, axes = plt.subplots(
            3, # row 수
            figsize=self.CONFIG.FIGURE.figsize, # 기본 크기
            height_ratios=(
                self.CONFIG.FIGURE.RATIO.legend,
                self.CONFIG.FIGURE.RATIO.price,
                self.CONFIG.FIGURE.RATIO.volume,
            ) # row 크기 비율
        )

        axes: list[Axes]
        self.ax_legend, self.ax_price, self.ax_volume = axes
        self.ax_legend.set_label('legend ax')
        self.ax_price.set_label('price ax')
        self.ax_volume.set_label('volume ax')

        # 이평선 라벨 axis 그리지 않기
        self.ax_legend.set_axis_off()

        # y ticklabel foramt 설정
        self.ax_price.yaxis.set_major_formatter(
            lambda x, _: self.CONFIG.UNIT.func(
                x,
                word=self.CONFIG.UNIT.price,
                digit=self.CONFIG.UNIT.digit
            )
        )
        self.ax_volume.yaxis.set_major_formatter(
            lambda x, _: self.CONFIG.UNIT.func(
                x,
                word=self.CONFIG.UNIT.volume,
                digit=self.CONFIG.UNIT.digit
            )
        )

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
        return


    def set_window(self):
        self._set_figure()
        self._set_axes()
        return

    def _set_figure(self):
        self.figure.canvas.manager.set_window_title('Seolpyo MPLChart')

        # 차트 비율 변경
        # print(f'{self.CONFIG.FIGURE.RATIO.volume=}')
        gs = self.ax_price.get_subplotspec().get_gridspec()
        gs.set_height_ratios([
            self.CONFIG.FIGURE.RATIO.legend,
            self.CONFIG.FIGURE.RATIO.price,
            self.CONFIG.FIGURE.RATIO.volume,
        ])
        # print(f'{gs.get_height_ratios()=}')
        self.figure.tight_layout()

        # 플롯간 간격 설정(Configure subplots)
        self.figure.subplots_adjust(**self.CONFIG.FIGURE.ADJUST.__dict__)

        self.figure.set_facecolor(self.CONFIG.FIGURE.facecolor)
        return

    def _set_axes(self):
        self._set_axes_legend()

        # 공통 설정
        for ax in (self.ax_price, self.ax_volume):
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
        return

    def _set_axes_legend(self):
        color = self.CONFIG.AX.facecolor

        # 이평선 라벨 Axes 배경색
        legends = self.ax_legend.get_legend()
        if legends:
            legends.get_frame().set_facecolor(color)

        # 이평선 라벨 Axes 테두리색
        color = self.CONFIG.AX.TICK.edgecolor
        legends = self.ax_legend.get_legend()
        if legends:
            legends.get_frame().set_edgecolor(color)

        # 이평선 라벨 폰트 색상
        color = self.CONFIG.AX.TICK.fontcolor
        legends = self.ax_legend.get_legend()
        if legends:
            legend_labels: list[Text] = legends.texts
            for i in legend_labels:
                i.set_color(color)
        return


class ArtistMixin(Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.add_artists()
        return

    def add_artists(self):
        self._add_artists()
        return

    def _add_artists(self):
        self._add_watermark()
        self._set_wartermark()
        return

    def set_artists(self):
        self._set_artists()
        return

    def _set_artists(self):
        self._set_wartermark()
        return

    def _add_watermark(self):
        self.artist_watermark = Text(
            x=0.5, y=0.5, text='',
            animated=True,
            horizontalalignment='center', verticalalignment='center',
            transform=self.ax_price.transAxes
        )
        self.ax_price.add_artist(self.artist_watermark)
        return

    def _set_wartermark(self):
        self.artist_watermark.set_text(self.watermark)
        self.artist_watermark.set_fontsize(self.CONFIG.FIGURE.WATERMARK.fontsize)
        self.artist_watermark.set_color(self.CONFIG.FIGURE.WATERMARK.color)
        self.artist_watermark.set_alpha(self.CONFIG.FIGURE.WATERMARK.alpha)
        return


class BaseMixin(ArtistMixin):
    def refresh(self):
        self._refresh()
        self.figure.canvas.draw()
        return

    def _refresh(self):
        self.set_window()
        self.set_artists()
        return
