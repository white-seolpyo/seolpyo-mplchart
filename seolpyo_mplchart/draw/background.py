from matplotlib.axes import Axes
from matplotlib.collections import LineCollection
from matplotlib.text import Text

from ..models import Figure


class SldierMixin:
    slider_top: bool

    def draw_ax_slider(self):
        ax: Axes = self.get_ax_slider()

        self._draw_ax(ax)

        collection_slider: LineCollection = self.collection_slider
        collection_slider.draw(self.renderer)

        return

    def draw_slider(self):
        if self.show_slider:
            self.draw_ax_slider()
        return


class ChartMixin:
    candle_on_ma: bool

    collection_price: LineCollection
    collection_volume: LineCollection
    collection_ma: LineCollection

    collection_grid_price: LineCollection
    collection_grid_volume: LineCollection

    artist_watermark: Text

    def draw_price_chart(self):
        self.draw_price_chart_background()

        self.draw_watermark()
        self.draw_price_chart_element()
        return

    def draw_price_chart_background(self):
        ax: Axes = self.get_ax_price()
        self._draw_ax(ax, grid=False, xtick=False)

        self.collection_grid_price.draw(self.renderer)

        self.draw_watermark()
        return

    def draw_watermark(self):
        watermark = self.artist_watermark.get_text()
        # print(f'{watermark=}')
        if not watermark:
            return
        
        # if self.watermark != self.artist_watermark.get_text():
        #     self.artist_watermark.set_text(self.watermark)
        self.artist_watermark.draw(self.renderer)

        # print('watermark')
        # print(f'{self.watermark=}')
        # print(f'{self.artist_watermark.get_position()=}')
        # print(f'{self.artist_watermark.get_text()=}')
        # print(f'{self.artist_watermark.get_fontweight()=}')
        return

    def draw_price_chart_element(self):
        renderer = self.renderer

        if self.candle_on_ma:
            self.collection_ma.draw(renderer)
            self.collection_price.draw(renderer)
        else:
            self.collection_price.draw(renderer)
            self.collection_ma.draw(renderer)
        # print(f'{self.collection_price.get_linewidth()=}')

        return

    def draw_volume_chart(self):
        self.draw_volume_chart_background()
        self.draw_volume_chart_element()
        return

    def draw_volume_chart_background(self):
        ax: Axes = self.get_ax_volume()
        self._draw_ax(ax, grid=False)

        self.collection_grid_volume.draw(self.renderer)
        return

    def draw_chart_canvas(self):
        self.draw_price_chart()
        self.draw_volume_chart()
        return

    def draw_volume_chart_element(self):
        self.collection_volume.draw(self.renderer)
        return

    def draw_chart_element(self):
        self.draw_price_chart_element()
        self.draw_volume_chart_element()
        return

    def draw_chart(self):
        self.draw_chart_canvas()
        self.draw_watermark()
        self.draw_chart_element()
        return


class ArtistMixin:
    slider_top: bool

    def draw_slider_nav(self):
        collection_nav: LineCollection = self.collection_slider_nav

        collection_nav.draw(self.renderer)
        return

    def draw_slider_artist(self):
        self.draw_slider_nav()
        return

    def draw_artist(self):
        self.draw_slider_artist()
        return


class BackgroundMixin(SldierMixin, ChartMixin, ArtistMixin):
    figure: Figure

    creating_background = False

    background_canvas = None
    background_sldier = None
    background_chart = None
    background_artist = None

    @property
    def renderer(self):
        return self.figure.canvas.renderer

    def _draw_ax(self, ax: Axes, *, grid=True, xtick=True):
        renderer = self.renderer

        # grid, tick, ticklabel
        for axis in (ax.xaxis, ax.yaxis):
            axis.draw(renderer)

        if grid:
            # grid
            for axis in (ax.xaxis, ax.yaxis):
                for tick in axis.get_major_ticks():
                    tick.gridline.draw(renderer)
        # spine
        for spine in ax.spines.values():
            spine.draw(renderer)
        # tick
        for tick in ax.yaxis.get_major_ticks():
            tick.tick1line.draw(renderer)
            tick.label1.draw(renderer)
            tick.label2.draw(renderer)
        if xtick:
            for tick in ax.xaxis.get_minor_ticks():
                tick.tick1line.draw(renderer)
                tick.label1.draw(renderer)
                tick.label2.draw(renderer)

        return

    def restore_region(self, background):
        self.renderer.restore_region(background)
        return

    def copy_bbox(self):
        renderer = self.renderer
        return renderer.copy_from_bbox(self.figure.bbox)

    def set_background_slider(self):
        self.draw_slider()
        self.background_sldier = self.copy_bbox()
        return

    def set_background_chart(self):
        self.draw_chart()
        self.background_chart = self.copy_bbox()
        return

    def set_background_artist(self):
        self.draw_artist()
        self.background_artist = self.background = self.copy_bbox()
        return

    def _set_background(self):
        self.background_canvas = self.copy_bbox()

        self.set_background_slider()

        self.set_background_chart()

        self.set_background_artist()

        return

    def set_background(self):
        if not self.creating_background:
            self.creating_background = True
            self._set_background()
            self.creating_background = False
        return

    def restore_canvas(self):
        if not self.background_canvas:
            self.set_background()
        self.restore_region(self.background_canvas)
        return

    def restore_slider(self):
        if not self.background_sldier:
            self.set_background()
        self.restore_region(self.background_sldier)
        return

    def restore_chart(self):
        if not self.background_chart:
            self.set_background()
        self.restore_region(self.background_chart)
        return

    def restore_artist(self):
        if not self.background_artist:
            self.set_background()
        self.restore_region(self.background_artist)
        return

    def restore_background(self):
        if not self.background:
            self.set_background()
        self.restore_region(self.background)
        return

