from matplotlib.axes import Axes
from matplotlib.collections import LineCollection
from matplotlib.text import Text

from ..._config import SliderConfigData


class Base:
    CONFIG: SliderConfigData

    ax_slider: Axes
    ax_price: Axes
    ax_volume: Axes
    ax_legend: Axes

    add_artists: callable
    set_artists: callable


class CollectionMixin(Base):
    def add_artists(self):
        super().add_artists()

        self.collection_slider = LineCollection([])
        self.collection_nav = LineCollection([])
        self.collection_slider_vline = LineCollection([])
        self.artist_text_slider = Text('')

        for artist in [
            self.collection_slider,
            self.collection_nav,
            self.collection_slider_vline,
            self.artist_text_slider
        ]:
            self.ax_slider.add_artist(artist)
        return

    def set_artists(self):
        super().set_artists()

        self._set_slider_artists()
        self._set_slider_test()
        return

    def _set_slider_artists(self):
        self.collection_slider.set_animated(True)
        self.collection_slider.set_transform(self.ax_slider.transData)

        color_overay = self.CONFIG.SLIDER.NAV.facecolor
        color_line = self.CONFIG.SLIDER.NAV.edgecolor
        colors = [color_overay, color_overay, color_line, color_line]
        # print(f'{colors=}')
        self.collection_nav.set_linewidth(0.1)
        self.collection_nav.set_facecolor(colors)

        # facecolor alpha값 제거
        colors = []
        for c in self.collection_nav.get_facecolor():
            # print(c)
            colors.append(c[:3])
        self.collection_nav.set_facecolor(colors)

        alpha = self.CONFIG.SLIDER.NAV.alpha
        self.collection_nav.set_alpha([alpha, alpha, 1, 1])

        self.collection_nav.set_edgecolor([(0, 0, 0, 0) for _ in colors])
        self.collection_nav.set_animated(True)
        self.collection_nav.set_transform(self.ax_slider.transData)

        kwargs = self.CONFIG.CURSOR.CROSSLINE.__dict__
        kwargs.update({'segments': [], 'animated': True})
        self.collection_slider_vline.set(**kwargs)

        kwargs = self.CONFIG.CURSOR.TEXT.to_dict()
        kwargs.update({'text': ' ', 'animated': True})
        self.artist_text_slider.set(**kwargs)
        return

    def _set_slider_test(self):
        kwargs = self.CONFIG.CURSOR.TEXT.to_dict()
        kwargs.update(animated=True, verticalalignment='top', horizontalalignment='center')
        self.artist_text_slider.set(**kwargs)
        return


class ArtistMixin(CollectionMixin):
    collection_slider: LineCollection
    collection_nav: LineCollection
    collection_slider_vline: LineCollection
    artist_text_slider: Text

