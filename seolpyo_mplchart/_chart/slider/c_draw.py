from matplotlib.axes import Axes
from matplotlib.collections import LineCollection
from matplotlib.text import Text

from .a_canvas import Figure


class Base:
    figure: Figure

    ax_slider: Axes

    collection_slider: LineCollection
    collection_nav: LineCollection
    collection_slider_vline: LineCollection
    artist_text_slider: Text


class SliderMixin(Base):
    def _draw_ax_slider(self):
        renderer = self.figure.canvas.renderer

        self.ax_slider.xaxis.draw(renderer)
        self.ax_slider.yaxis.draw(renderer)

        self.collection_slider.draw(renderer)
        c = self.collection_slider.get_edgecolor()
        # print(f'{c=}')
        s = self.collection_slider.get_segments()
        # print(f'{s=}')
        return

    def _draw_nav(self):
        renderer = self.figure.canvas.renderer

        self.collection_nav.draw(renderer)
        return

    def _draw_slider_vline(self):
        renderer = self.figure.canvas.renderer

        self.collection_slider_vline.draw(renderer)
        return

    def _draw_slider_text(self):
        renderer = self.figure.canvas.renderer

        self.artist_text_slider.draw(renderer)
        return


class DrawMixin(SliderMixin):
    pass

