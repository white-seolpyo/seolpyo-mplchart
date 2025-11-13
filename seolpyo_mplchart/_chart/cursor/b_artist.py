from matplotlib.axes import Axes
from matplotlib.collections import LineCollection
from matplotlib.text import Text

from ..._config import ConfigData
from ..base.a_canvas import Figure


class Base:
    CONFIG: ConfigData

    figure: Figure
    ax_price: Axes
    ax_volume: Axes

    add_artists: callable
    set_artists: callable


class CrossLineMixin(Base):
    def _add_crosslines(self):
        kwargs = {'segments': [], 'animated': True}

        self.collection_price_crossline = LineCollection(**kwargs)
        self.ax_price.add_artist(self.collection_price_crossline)

        self.collection_volume_crossline = LineCollection(**kwargs)
        self.ax_volume.add_artist(self.collection_volume_crossline)
        return

    def _set_crosslines(self):
        kwargs = self.CONFIG.CURSOR.CROSSLINE.__dict__
        kwargs.update({'segments': [], 'animated': True})

        self.collection_price_crossline.set(**kwargs)
        self.collection_volume_crossline.set(**kwargs)
        return


class LabelMixin(Base):
    def _add_artist_labels(self):
        kwargs = {'text': '', 'animated': True,}

        self.artist_label_x = Text(**kwargs)
        self.figure.add_artist(self.artist_label_x)

        self.artist_label_y = Text(**kwargs)
        self.figure.add_artist(self.artist_label_y)
        return

    def _set_artist_labels(self):
        kwargs = self.CONFIG.CURSOR.TEXT.to_dict()
        kwargs.update({'text': ' ', 'animated': True, 'horizontalalignment': 'center', 'verticalalignment': 'center', 'clip_on':True})

        self.artist_label_x.set(**kwargs)
        self.artist_label_y.set(**kwargs)
        return


class BoxMixin(Base):
    def _add_box_collections(self):
        kwargs = {'segments': [], 'animated': True,}

        self.collection_box_price = LineCollection(**kwargs)
        self.ax_price.add_artist(self.collection_box_price)
        self.collection_box_volume = LineCollection(**kwargs)
        self.ax_volume.add_artist(self.collection_box_volume)
        return

    def _set_box_collections(self):
        kwargs = self.CONFIG.CURSOR.BOX.__dict__
        kwargs.update({'segments': [], 'animated': True,})

        self.collection_box_price.set(**kwargs)
        self.collection_box_volume.set(**kwargs)
        return


class InfoMixin(Base):
    def _add_info_texts(self):
        kwargs = {'text': '', 'animated': True, 'horizontalalignment': 'left', 'verticalalignment': 'top',}

        self.artist_info_candle = Text(**kwargs)
        self.ax_price.add_artist(self.artist_info_candle)
        self.artist_info_volume = Text(**kwargs)
        self.ax_volume.add_artist(self.artist_info_volume)
        return

    def _set_info_texts(self):
        kwargs = self.CONFIG.CURSOR.TEXT.to_dict()
        kwargs.update({'text': '', 'animated': True, 'horizontalalignment': 'left', 'verticalalignment': 'top',})

        self.artist_info_candle.set(**kwargs)
        self.artist_info_volume.set(**kwargs)
        return


class ArtistMixin(CrossLineMixin, LabelMixin, BoxMixin, InfoMixin):
    collection_price_crossline: LineCollection
    collection_volume_crossline: LineCollection

    artist_label_x: Text = None
    artist_label_y: Text = None

    collection_box_price: LineCollection
    collection_box_volume: LineCollection

    artist_info_candle: Text
    artist_info_volume: Text

    def add_artists(self):
        super().add_artists()

        self._add_crosslines()
        self._add_artist_labels()
        self._add_box_collections()
        self._add_info_texts()

        self.set_artists()
        return

    def set_artists(self):
        super().set_artists()

        self._set_crosslines()
        self._set_artist_labels()
        self._set_box_collections()
        self._set_info_texts()
        return

