from matplotlib.axes import Axes
from matplotlib.text import Text

from ...style import Style


class WatermarkMixin:
    watermark: str

    artist_watermark: Text

    STYLE: Style

    def set_artist_watermark(self):
        self.artist_watermark.set_text(self.watermark)
        self.artist_watermark.set_fontsize(self.STYLE.ARTIST.WATERMARK.fontsize)
        self.artist_watermark.set_color(self.STYLE.ARTIST.WATERMARK.color)
        self.artist_watermark.set_alpha(self.STYLE.ARTIST.WATERMARK.alpha)
        self.artist_watermark.set_fontweight(self.STYLE.ARTIST.WATERMARK.fontweight)

        self.artist_watermark.set_horizontalalignment('center')
        self.artist_watermark.set_verticalalignment('center')
        self.artist_watermark.set_animated(True)

        ax_price: Axes = self.get_ax_price()

        pos = ax_price.get_position()
        x = (pos.x0 + pos.x1) / 2
        y = (pos.y0 + pos.y1) / 2

        # ax_volume: Axes = self.get_ax_volume()
        # volume_y0, volume_y1 = ax_volume.get_ylim()
        # y = (volume_y0 + pos.y1) / 5 * 3

        self.artist_watermark.set_position([x, y])

        return


class ChartMixin:
    artist_label_chart_x: Text
    artist_label_chart_y: Text

    artist_info_price: Text
    artist_info_volume: Text

    STYLE: Style

    def get_artist_label_kwargs(self):
        kwargs = self.STYLE.ARTIST.TEXT.to_dict()
        kwargs.update({'text': ' ', 'animated': True, 'horizontalalignment': 'center', 'verticalalignment': 'center', 'clip_on':True})
        return kwargs

    def set_artist_label_chart(self):
        kwargs = self.get_artist_label_kwargs()

        self.artist_label_chart_x.set(**kwargs)
        self.artist_label_chart_y.set(**kwargs)
        return

    def get_artist_info_kwargs(self):
        kwargs = self.get_artist_label_kwargs()
        kwargs['horizontalalignment'] = 'left'
        kwargs['verticalalignment'] = 'top'

        return kwargs

    def set_artist_label_info_price(self):
        kwargs = self.get_artist_info_kwargs()

        self.artist_info_price.set(**kwargs)

        return

    def set_artist_label_info_volume(self):
        kwargs = self.get_artist_info_kwargs()

        self.artist_info_volume.set(**kwargs)

        return

    def set_artist_label_info(self):
        self.set_artist_label_info_price()
        self.set_artist_label_info_volume()

        return


class SliderMixin:
    artist_label_slider_top: Text
    artist_label_slider_bottom: Text

    STYLE: Style

    def _set_slider_label(self, position):
        artist_label_slider: Text = getattr(self, f'artist_label_slider_{position}', None)
        if not artist_label_slider:
            getattr(self, f'add_slider_{position}_label')()

        artist_label_slider: Text = getattr(self, f'artist_label_slider_{position}')

        kwargs: dict = self.get_artist_label_kwargs()
        kwargs['verticalalignment'] = 'top'

        artist_label_slider.set_y(self.df['high'].max())

        artist_label_slider.set(**kwargs)

        return

    def set_slider_label_top(self):
        self._set_slider_label('top')
        return

    def set_slider_label_bottom(self):
        self._set_slider_label('bottom')
        return

    def set_slider_label(self):
        self.set_slider_label_top()
        self.set_slider_label_bottom()

        return


class TextMixin(WatermarkMixin, ChartMixin, SliderMixin):
    def set_text(self):
        self.set_artist_watermark()

        self.set_artist_label_chart()
        self.set_artist_label_info()

        self.set_slider_label()

        return
