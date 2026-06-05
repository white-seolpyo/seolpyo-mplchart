from matplotlib.axes import Axes
from matplotlib.text import Text
import pandas as pd

from ...models import Figure


class WatermarkMixin:
    figure: Figure

    def get_default_text_kwargs(self):
        kwargs = dict(text='', animated=True)
        return kwargs

    def add_artist_watermark(self):
        kwargs: dict = self.get_default_text_kwargs()

        self.artist_watermark = Text(**kwargs)
        self.figure.add_artist(self.artist_watermark)
        return


class ChartMixin:
    figure = Figure

    def get_default_label_kwargs(self):
        kwargs = dict(
            text='', animated=True,
            horizontalalignment='center', verticalalignment='center',
            clip_on=True,
        )
        return kwargs

    def add_chart_label(self):
        kwargs = self.get_default_label_kwargs()

        self.artist_label_chart_x = Text(**kwargs)
        self.figure.add_artist(self.artist_label_chart_x)
        self.artist_label_chart_y = Text(**kwargs)
        self.figure.add_artist(self.artist_label_chart_y)

        ax_price: Axes = self.get_ax_price()

        kwargs = self.get_default_label_kwargs()
        kwargs['horizontalalignment'] = 'left'
        kwargs['verticalalignment'] = 'top'

        self.artist_info_price = Text(**kwargs)
        ax_price.add_artist(self.artist_info_price)

        ax_volume: Axes = self.get_ax_volume()

        self.artist_info_volume = Text(**kwargs)
        ax_volume.add_artist(self.artist_info_volume)

        return


class SliderMixin:
    slider_top: bool

    df: pd.DataFrame

    @property
    def artist_label_slider(self):
        if self.slider_top:
            label = self.artist_label_slider_top
            if not label:
                self.add_slider_top_label()
                label = self.artist_label_slider_top
            return label
        label = self.artist_label_slider_bottom
        if not label:
            self.add_slider_bottom_label()
            label = self.artist_label_slider_bottom
        return label

    def _add_slider_label(self, position):
        ax: Axes = getattr(self, f'get_ax_slider_{position}')()

        artist_label = Text('')
        ax.add_artist(artist_label)
        setattr(self, f'artist_label_slider_{position}', artist_label)

        return

    def add_slider_top_label(self):
        self.artist_label_slider_top: Text
        self._add_slider_label('top')

        return

    def add_slider_bottom_label(self):
        self.artist_label_slider_bottom: Text
        self._add_slider_label('bottom')

        return

    def add_slider_label(self):
        self.add_slider_top_label()
        self.add_slider_bottom_label()

        return


class TextMixin(WatermarkMixin, ChartMixin, SliderMixin):
    def _add_text(self):
        self.add_artist_watermark()

        self.add_chart_label()
        self.add_slider_label()
        return
