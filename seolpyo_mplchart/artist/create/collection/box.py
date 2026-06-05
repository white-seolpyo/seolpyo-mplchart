from matplotlib.axes import Axes
from matplotlib.collections import LineCollection


class ChartMixin:
    def add_price_box_collection(self):
        ax: Axes = self.get_ax_price()

        kwargs: dict = self.get_default_collection_kwargs()

        self.collection_box_price = LineCollection(**kwargs)
        ax.add_collection(self.collection_box_price)
        return

    def add_volume_box_collection(self):
        ax: Axes = self.get_ax_volume()

        kwargs: dict = self.get_default_collection_kwargs()

        self.collection_box_volume = LineCollection(**kwargs)
        ax.add_collection(self.collection_box_volume)
        return


class BoxMixin(ChartMixin):
    def _add_box(self):
        self.add_price_box_collection()
        self.add_volume_box_collection()

        return
