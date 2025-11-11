from matplotlib.axes import Axes
from matplotlib.collections import LineCollection
from matplotlib.text import Text
import pandas as pd

from ..._config import ConfigData
from ..._chart.base.a_canvas import Figure


class Base:
    CONFIG: ConfigData

    df: pd.DataFrame

    watermark: str

    figure: Figure
    ax_legend: Axes
    ax_price: Axes
    ax_volume: Axes
    artist_watermark: Text
    collection_candle: LineCollection
    collection_volume: LineCollection
    collection_ma: LineCollection

    collection_price_crossline: LineCollection
    collection_volume_crossline: LineCollection

    artist_label_x: Text
    artist_label_y: Text

    collection_box_price: LineCollection
    collection_box_volume: LineCollection

    artist_info_candle: Text
    artist_info_volume: Text

    in_chart_price: bool
    in_chart_volume: bool


class CrosslineMixin(Base):
    def _draw_crossline(self):
        renderer = self.figure.canvas.renderer
        for artist in [
            self.collection_price_crossline,
            self.collection_volume_crossline,
        ]:
            artist.draw(renderer)
        return


class LabelMixin(Base):
    def _draw_label_x(self):
        artist = self.artist_label_x
        renderer = self.figure.canvas.renderer

        artist.draw(renderer)
        # print(f'{artist.get_position()=}')
        return

    def _draw_label_y(self):
        artist = self.artist_label_y
        renderer = self.figure.canvas.renderer

        artist.draw(renderer)
        return


class BoxMixin(Base):
    def _draw_box_candle(self):
        renderer = self.figure.canvas.renderer
        self.collection_box_price.draw(renderer)
        return

    def _draw_box_volume(self):
        renderer = self.figure.canvas.renderer
        self.collection_box_volume.draw(renderer)
        return


class InfoMixin(Base):
    def _draw_info_candle(self):
        renderer = self.figure.canvas.renderer
        self.artist_info_candle.draw(renderer)
        return

    def _draw_info_volume(self):
        renderer = self.figure.canvas.renderer
        self.artist_info_volume.draw(renderer)
        return


class DrawMixin(CrosslineMixin, LabelMixin, BoxMixin, InfoMixin):
    pass

