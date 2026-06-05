from matplotlib.axes import Axes
from matplotlib.collections import LineCollection


class CanvasMixin:
    def add_price_grid_collection(self):
        ax: Axes = self.get_ax_price()

        kwargs: dict = self.get_default_collection_kwargs()

        self.collection_grid_price = LineCollection(**kwargs)
        ax.add_collection(self.collection_grid_price)

        return

    def add_volume_grid_collection(self):
        ax: Axes = self.get_ax_volume()

        kwargs: dict = self.get_default_collection_kwargs()

        self.collection_grid_volume = LineCollection(**kwargs)
        ax.add_collection(self.collection_grid_volume)

        return

    def _add_canvas_collection(self):
        self.add_price_grid_collection()
        self.add_volume_grid_collection()

        return

