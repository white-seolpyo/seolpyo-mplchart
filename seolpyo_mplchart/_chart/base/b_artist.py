from matplotlib.axes import Axes
from matplotlib.collections import LineCollection
from matplotlib.lines import Line2D
from matplotlib.text import Text

from ..._config import ConfigData


class WatermarkMixin:
    CONFIG: ConfigData

    watermark = 'seolpyo mplchart'

    ax_price: Axes

    def _add_watermark(self):
        self.artist_watermark = Text(
            x=0.5, y=0.5, text='',
            animated=True,
            horizontalalignment='center', verticalalignment='center',
            transform=self.ax_price.transAxes
        )
        self.ax_price.add_artist(self.artist_watermark)
        return

    def _set_watermark(self):
        self.artist_watermark.set(animated=True, horizontalalignment='center', verticalalignment='center',)
        self.artist_watermark.set_text(self.watermark)
        self.artist_watermark.set_fontsize(self.CONFIG.FIGURE.WATERMARK.fontsize)
        self.artist_watermark.set_color(self.CONFIG.FIGURE.WATERMARK.color)
        self.artist_watermark.set_alpha(self.CONFIG.FIGURE.WATERMARK.alpha)
        return


class CollectionMixin:
    ax_price: Axes
    ax_volume: Axes
    ax_legend: Axes

    def _add_collections(self):
        self.collection_candle = LineCollection([], animated=True, linewidths=0.8)
        self.ax_price.add_collection(self.collection_candle)

        self.collection_ma = LineCollection([], animated=True, linewidths=1)
        self.ax_price.add_collection(self.collection_ma)

        self.collection_volume = LineCollection([], animated=True, linewidths=1)
        self.ax_volume.add_collection(self.collection_volume)
        return

    def set_collection_candle(self, segment, facecolors, edgecolors):
        self.collection_candle.set_segments(segment)
        self.collection_candle.set_facecolor(facecolors)
        self.collection_candle.set_edgecolor(edgecolors)
        self.collection_candle.set_transform(self.ax_price.transData)
        return

    def set_collection_volume(self, segment, facecolors, edgecolors):
        self.collection_volume.set_segments(segment)
        self.collection_volume.set_facecolor(facecolors)
        self.collection_volume.set_edgecolor(edgecolors)
        self.collection_volume.set_transform(self.ax_volume.transData)
        return


class MaMixin:
    CONFIG: ConfigData
    _visible_ma = set()

    ax_legend: Axes
    ax_price: Axes
    collection_ma: LineCollection
    _set_figure_ratios: callable

    def set_collection_ma(self, segment, edgecolors):
        self.collection_ma.set_segments(segment)
        self.collection_ma.set_facecolor([])
        self.collection_ma.set_edgecolor(edgecolors)
        # print(self.collection_ma.get_linewidth())
        self.collection_ma.set_linewidth(self.CONFIG.MA.linewidth)
        self.collection_ma.set_transform(self.ax_price.transData)
        return

    def _set_legends(self):
        legends = self.ax_legend.get_legend()
        if legends:
            legends.remove()

        self._visible_ma.clear()

        label_list, handle_list, edgecolor_list = ([], [], [])
        # Legend Ax에 표시하는 선 segment
        arr = [0, 1]
        for n, ma in enumerate(self.CONFIG.MA.ma_list):
            self._visible_ma.add(ma)
            label_list.append(self.CONFIG.MA.format.format(ma))
            try:
                color = self.CONFIG.MA.color_list[n]
            except:
                color = self.CONFIG.MA.color_default
            edgecolor_list.append(color)
            handle_list.append(Line2D(arr, ydata=arr, color=color, linewidth=5, label=ma))

        self.set_collection_ma([], edgecolors=edgecolor_list)

        # 가격이동평균선 legend 생성
        if handle_list:
            legends = self.ax_legend.legend(
                handle_list, label_list, loc='lower left', ncol=self.CONFIG.MA.ncol,
                borderpad=0.55,
                facecolor=self.CONFIG.AX.facecolor, edgecolor=self.CONFIG.AX.TICK.edgecolor,
                labelcolor=self.CONFIG.AX.TICK.fontcolor,
            )
            for handle in legends.legend_handles:
                # legend 클릭시 pick event가 발생할 수 있도록 설정
                handle.set_picker(5)

            # legend ax 크기 조정
            self._set_figure_ratios()
        return


class ArtistMixin(WatermarkMixin, CollectionMixin, MaMixin):
    artist_watermark: Text
    collection_candle: LineCollection
    collection_volume: LineCollection
    collection_ma: LineCollection

    _visible_ma: set[int] = set()

    def add_artists(self):
        self._add_watermark()
        self._set_watermark()
        self._add_collections()
        self._set_legends()
        return

    def set_artists(self):
        self._set_watermark()
        self._set_legends()
        return

