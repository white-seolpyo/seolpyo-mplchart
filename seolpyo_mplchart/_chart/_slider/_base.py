import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.collections import LineCollection
from matplotlib.text import Text

from ..._config import SLIDERCONFIG, SliderConfigData
from .._cursor import BaseMixin as Base


class PlotMixin(Base):
    slider_top = True
    CONFIG: SliderConfigData

    def __init__(self, config=SLIDERCONFIG, *args, **kwargs):
        super().__init__(config=config, *args, **kwargs)
        return

    def add_axes(self):
        if self.slider_top:
            self.figure, axes = plt.subplots(
                4, # row 수
                figsize=self.CONFIG.FIGURE.figsize, # 기본 크기
                height_ratios=(
                    self.CONFIG.FIGURE.RATIO.slider,
                    self.CONFIG.FIGURE.RATIO.legend,
                    self.CONFIG.FIGURE.RATIO.price, self.CONFIG.FIGURE.RATIO.volume
                ) # row 크기 비율
            )
            axes: list[Axes]
            self.ax_slider, self.ax_legend, self.ax_price, self.ax_volume = axes
        else:
            self.figure, axes = plt.subplots(
                5, # row 수
                figsize=self.CONFIG.FIGURE.figsize, # 기본 크기
                height_ratios=(
                    self.CONFIG.FIGURE.RATIO.legend,
                    self.CONFIG.FIGURE.RATIO.price, self.CONFIG.FIGURE.RATIO.volume,
                    self.CONFIG.FIGURE.RATIO.none,
                    self.CONFIG.FIGURE.RATIO.slider
                ) # row 크기 비율
            )
            axes: list[Axes]
            self.ax_legend, self.ax_price, self.ax_volume, ax_none, self.ax_slider = axes

            ax_none.set_axis_off()
            ax_none.xaxis.set_animated(True)
            ax_none.yaxis.set_animated(True)

        self.ax_slider.set_label('slider ax')
        self.ax_legend.set_label('legend ax')
        self.ax_price.set_label('price ax')
        self.ax_volume.set_label('volume ax')
        self.ax_legend.set_axis_off()

        # y ticklabel foramt 설정
        self.ax_slider.yaxis.set_major_formatter(lambda x, _: self.CONFIG.UNIT.func(x, word=self.CONFIG.UNIT.price, digit=self.CONFIG.UNIT.digit))
        self.ax_price.yaxis.set_major_formatter(lambda x, _: self.CONFIG.UNIT.func(x, word=self.CONFIG.UNIT.price, digit=self.CONFIG.UNIT.digit))
        self.ax_volume.yaxis.set_major_formatter(lambda x, _: self.CONFIG.UNIT.func(x, word=self.CONFIG.UNIT.volume, digit=self.CONFIG.UNIT.digit))

        # 공통 설정
        for ax in (self.ax_slider, self.ax_price, self.ax_volume):
            ax.xaxis.set_animated(True)
            ax.yaxis.set_animated(True)

            # x tick 외부 눈금 표시하지 않기
            ax.xaxis.set_ticks_position('none')
            # x tick label 제거
            ax.set_xticklabels([])
            # y tick 우측으로 이동
            ax.tick_params(
                left=False, right=True, labelleft=False, labelright=True,
                colors=self.CONFIG.AX.TICK.edgecolor
            )
        return

    def _set_axes(self):
        super()._set_axes()

        self.ax_slider.set_facecolor(self.CONFIG.AX.facecolor)
        self.ax_slider.grid(**self.CONFIG.AX.GRID.__dict__)

        # 틱 색상
        self.ax_slider.tick_params('both', colors=self.CONFIG.AX.TICK.edgecolor)
        # 틱 라벨 색상
        ticklabels: list[Text] = self.ax_slider.get_xticklabels() + self.ax_slider.get_yticklabels()
        for ticklabel in ticklabels:
            ticklabel.set_color(self.CONFIG.AX.TICK.fontcolor)
        return

    def _set_figure(self):
        self.figure.canvas.manager.set_window_title('Seolpyo MPLChart')

        # 차트 비율 변경
        # print(f'{self.CONFIG.FIGURE.RATIO.volume=}')
        gs = self.ax_price.get_subplotspec().get_gridspec()
        if len(self.figure.axes) == 4:
            gs.set_height_ratios([
                self.CONFIG.FIGURE.RATIO.slider,
                self.CONFIG.FIGURE.RATIO.legend,
                self.CONFIG.FIGURE.RATIO.price, self.CONFIG.FIGURE.RATIO.volume,
            ])
        else:
            gs.set_height_ratios([
                self.CONFIG.FIGURE.RATIO.legend,
                self.CONFIG.FIGURE.RATIO.price, self.CONFIG.FIGURE.RATIO.volume,
                self.CONFIG.FIGURE.RATIO.none,
                self.CONFIG.FIGURE.RATIO.slider,
            ])
        self.figure.tight_layout()

        # 플롯간 간격 설정(Configure subplots)
        self.figure.subplots_adjust(**self.CONFIG.FIGURE.ADJUST.__dict__)

        self.figure.set_facecolor(self.CONFIG.FIGURE.facecolor)
        return


class CollectionMixin(PlotMixin):
    def add_artists(self):
        super().add_artists()

        # 슬라이더에 그려질 주가 선형 차트
        self.collection_slider = LineCollection([], animated=True)
        self.ax_slider.add_artist(self.collection_slider)

        # 슬라이더 네비게이터
        self.collection_navigator = LineCollection([], animated=True, alpha=(0.3, 1.0))
        self.ax_slider.add_artist(self.collection_navigator)

        # 현재 위치 표시용 line
        self.collection_slider_vline = LineCollection(segments=[], animated=True)
        self.ax_slider.add_artist(self.collection_slider_vline)

        # 현대 위치에 해당하는 date 출력용 text
        self.artist_text_slider = Text(text='', animated=True, horizontalalignment='center', verticalalignment='top')
        self.ax_slider.add_artist(self.artist_text_slider)

        self._set_slider_artists()
        return

    def _set_slider_artists(self):
        edgecolors = [self.CONFIG.SLIDER.NAVIGATOR.facecolor, self.CONFIG.SLIDER.NAVIGATOR.edgecolor]
        self.collection_navigator.set_edgecolor(edgecolors)

        kwargs = self.CONFIG.CURSOR.CROSSLINE.__dict__
        kwargs.update({'segments': [], 'animated': True})
        self.collection_slider_vline.set(**kwargs)

        kwargs = self.CONFIG.CURSOR.TEXT.to_dict()
        kwargs.update({'text': ' ', 'animated': True})
        self.artist_text_slider.set(**kwargs)
        return

    def _set_artists(self):
        super()._set_artists()

        self._set_slider_artists()
        self._set_slider_collection()
        return

    def _set_slider_collection(self):
        keys = []
        for i in reversed(self.CONFIG.MA.ma_list):
            keys.append('x')
            keys.append(f'ma{i}')

        series = self.df[keys + ['x', 'close']]
        series['x'] = series['x'] - 0.5
        segment_slider = series.values
        sizes = [segment_slider.shape[0], len(self.CONFIG.MA.ma_list)+1, 2]
        segment_slider = segment_slider.reshape(*sizes).swapaxes(0, 1)
        self.collection_slider.set_segments(segment_slider)

        linewidth = []
        ma_colors = []
        for n, _ in enumerate(self.CONFIG.MA.ma_list):
            linewidth.append(0.9)
            try:
                ma_colors.append(self.CONFIG.MA.color_list[n])
            except:
                ma_colors.append(self.CONFIG.MA.color_default)

        self.collection_slider.set_linewidth(linewidth + [2.4])
        self.collection_slider.set_edgecolor(ma_colors + [self.CONFIG.CANDLE.line_color])
        return


class NavigatorMixin(CollectionMixin):
    def _connect_events(self):
        super()._connect_events()

        self.figure.canvas.mpl_connect('resize_event', lambda x: self.on_resize(x))
        return

    def on_resize(self, e):
        self._on_resize(e)
        return

    def _on_resize(self, e):
        self._set_navigator_artists()
        return

    def _refresh(self):
        super()._refresh()
        self._set_navigator_artists()
        return

    def _set_navigator_artists(self):
        if not getattr(self, 'index_list', False):
            return
        xmax = self.index_list[-1]
        # 슬라이더 xlim
        xdistance = xmax / 30
        self.slider_xmin, self.slider_xmax = (-xdistance, xmax+xdistance)
        self.ax_slider.set_xlim(self.slider_xmin, self.slider_xmax)

        # 슬라이더 ylim
        ymin, ymax = (self.df['low'].min(), self.df['high'].max())
        ysub = ymax - ymin
        self.sldier_ymiddle = ymin + (ysub / 2)
        ydistance = ysub / 5
        self.slider_ymin, self.slider_ymax = (ymin-ydistance, ymax+ydistance)
        self.ax_slider.set_ylim(self.slider_ymin, self.slider_ymax)

        # 슬라이더 텍스트 y
        self.artist_text_slider.set_y(ymax)

        self.collection_navigator.set_linewidth([self.ax_slider.bbox.height, 5])

        # 슬라이더 라인 선택 범위
        xsub = self.slider_xmax - self.slider_xmin
        self._navLineWidth = xsub * 8 / 1_000
        if self._navLineWidth < 1:
            self._navLineWidth = 1
        self._navLineWidth_half = self._navLineWidth / 2
        return

    def _axis_navigator(self, navmin, navmax):
        seg = [
            # 좌측 오버레이
            (
                (self.slider_xmin, self.sldier_ymiddle),
                (navmin, self.sldier_ymiddle),
            ),
            # 좌측 네비게이터
            (
                (navmin, self.slider_ymin),
                (navmin, self.slider_ymax),
            ),
            # 우측 네비게이터
            (
                (navmax, self.sldier_ymiddle),
                (self.slider_xmax, self.sldier_ymiddle),
            ),
            # 우측 오버레이
            (
                (navmax, self.slider_ymin),
                (navmax, self.slider_ymax),
            ),
        ]

        self.collection_navigator.set_segments(seg)
        return


class BaseMixin(NavigatorMixin):
    min_distance = 5

