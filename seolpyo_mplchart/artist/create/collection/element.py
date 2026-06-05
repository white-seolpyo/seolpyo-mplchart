from matplotlib.axes import Axes
from matplotlib.collections import LineCollection


class ChartMixin:
    def get_default_collection_kwargs(self):
        kwargs = dict(segments=[], animated=True)
        return kwargs

    def add_price_collection(self):
        ax: Axes = self.get_ax_price()

        kwargs = self.get_default_collection_kwargs()

        self.collection_price = LineCollection(**kwargs)
        ax.add_collection(self.collection_price)

        self.collection_ma = LineCollection(**kwargs)
        ax.add_collection(self.collection_ma)

        return

    def add_volume_collection(self):
        ax: Axes = self.get_ax_volume()

        kwargs = self.get_default_collection_kwargs()

        self.collection_volume = LineCollection(**kwargs)
        ax.add_collection(self.collection_volume)
        return


class SliderMixin:
    slider_top: bool

    @property
    def collection_slider(self):
        if self.slider_top:
            return self.collection_slider_top
        return self.collection_slider_bottom

    def _add_slider_collection(self, position):
        ax: Axes = getattr(self, f'get_ax_slider_{position}')()

        kwargs: dict = self.get_default_collection_kwargs()

        collection_slider = LineCollection(**kwargs)
        ax.add_collection(collection_slider)
        setattr(self, f'collection_slider_{position}', collection_slider)

        return

    def _add_slider_top_collection(self):
        self.collection_slider_top: LineCollection
        self._add_slider_collection('top')

        return

    def _add_slider_bottom_collection(self):
        self.collection_slider_bottom: LineCollection
        self._add_slider_collection('bottom')

        return

    def add_slider_collection(self):
        self._add_slider_top_collection()
        self._add_slider_bottom_collection()

        return

class ElementMixin(ChartMixin, SliderMixin):
    def _add_element(self):
        self.add_price_collection()
        self.add_volume_collection()
        self.add_slider_collection()

        return

