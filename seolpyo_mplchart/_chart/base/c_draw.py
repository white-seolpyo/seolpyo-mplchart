from matplotlib.axes import Axes
from matplotlib.collections import LineCollection
from matplotlib.text import Text

from .a_canvas import Figure


class Base:
    candle_on_ma = True

    watermark: str

    figure: Figure
    ax_legend: Axes
    ax_price: Axes
    ax_volume: Axes

    artist_watermark: Text
    collection_candle: LineCollection
    collection_volume: LineCollection
    collection_ma: LineCollection

    def draw_chart(self):
        self._draw_ax_price()
        self._draw_ax_volume()
        self._draw_chart_price()
        self._draw_chart_volume()
        return

    def _draw_chart_volume(self):
        renderer = self.figure.canvas.renderer

        self.collection_volume.draw(renderer)
        return

    def _draw_chart_price(self):
        renderer = self.figure.canvas.renderer
        # print(f'{renderer=}')

        # print(self.collection_candle.get_segments())
        if self.candle_on_ma:
            self.collection_ma.draw(renderer)
            self.collection_candle.draw(renderer)
        else:
            self.collection_candle.draw(renderer)
            self.collection_ma.draw(renderer)

        if self.watermark:
            if self.watermark != self.artist_watermark.get_text():
                self.artist_watermark.set_text(self.watermark)
            self.artist_watermark.draw(renderer)
        return

    def draw_artists(self):
        return

    def draw_background(self):
        self._draw_ax(self.ax_price)
        self._draw_ax(self.ax_volume)

        legend = self.ax_legend.get_legend()
        if legend:
            legend.draw(self.figure.canvas.renderer)
        return

    def _draw_ax(self, ax: Axes):
        renderer = self.figure.canvas.renderer

        # ax 배경
        ax.patch.draw(renderer)

        # ax 외곽선
        for spine in ax.spines.values():
            spine.draw(renderer)

        return

    def _draw_ax_volume(self):
        renderer = self.figure.canvas.renderer

        # grid, tick, ticklabel
        ax = self.ax_volume
        for axis in (ax.xaxis, ax.yaxis):
            axis.draw(renderer)
        return

    def _draw_ax_price(self):
        renderer = self.figure.canvas.renderer
        # print(f'{renderer=}')

        # grid, tick, ticklabel
        ax = self.ax_price
        for axis in (ax.xaxis, ax.yaxis):
            axis.draw(renderer)
        return


class DrawMixin(Base):
    candle_on_ma = True

