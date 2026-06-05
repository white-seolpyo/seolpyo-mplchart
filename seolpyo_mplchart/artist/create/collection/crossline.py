from matplotlib.axes import Axes
from matplotlib.collections import LineCollection


class ChartLineMixin:
    def add_price_crossline_collection(self):
        ax: Axes = self.get_ax_price()

        kwargs: dict = self.get_default_collection_kwargs()

        self.collection_crossline_price = LineCollection(**kwargs)
        ax.add_collection(self.collection_crossline_price)
        return

    def add_volume_crossline_collection(self):
        ax: Axes = self.get_ax_volume()

        kwargs: dict = self.get_default_collection_kwargs()

        kwargs['transform'] = ax.transData
        self.collection_crossline_volume = LineCollection(**kwargs)
        ax.add_collection(self.collection_crossline_volume)
        return


class SliderMixin:
    slider_top: bool

    @property
    def collection_slider_vline(self):
        if self.slider_top:
            return self.collection_slider_top_vline
        return self.collection_slider_bottom_vline

    def _add_slider_vline_collection(self, position):
        ax: Axes = getattr(self, f'get_ax_slider_{position}')()

        kwargs: dict = self.get_default_collection_kwargs()

        collection_slider_vline = LineCollection(**kwargs)
        ax.add_collection(collection_slider_vline)
        setattr(self, f'collection_slider_{position}_vline', collection_slider_vline)

        return

    def add_slider_top_vline_collection(self):
        self.collection_slider_top_vline: LineCollection
        self._add_slider_vline_collection('top')

        return

    def add_slider_bottom_vline_collection(self):
        self.collection_slider_bottom_vline: LineCollection
        self._add_slider_vline_collection('bottom')

        return

    def add_slider_vline_collection(self):
        self.add_slider_top_vline_collection()
        self.add_slider_bottom_vline_collection()

        return


class CrossLineMixin(ChartLineMixin, SliderMixin):
    def _add_cross_line(self):
        self.add_price_crossline_collection()
        self.add_volume_crossline_collection()
        self.add_slider_vline_collection()

        return

