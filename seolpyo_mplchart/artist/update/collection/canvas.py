from matplotlib.collections import LineCollection

from ....style import Style


class CanvasMixin:
    STYLE: Style

    collection_grid_price: LineCollection
    collection_grid_volume: LineCollection

    def set_artist_grid_price(self):
        self.collection_grid_price.set_linewidth(self.STYLE.CHART.GRID.linewidth)
        self.collection_grid_price.set_linestyle(self.STYLE.CHART.GRID.linestyle)
        self.collection_grid_price.set_edgecolor(self.STYLE.CHART.GRID.color)
        return

    def set_artist_grid_volume(self):
        self.collection_grid_volume.set_linewidth(self.STYLE.CHART.GRID.linewidth)
        self.collection_grid_volume.set_linestyle(self.STYLE.CHART.GRID.linestyle)
        self.collection_grid_volume.set_edgecolor(self.STYLE.CHART.GRID.color)
        return

    def set_artist_grid(self):
        self.set_artist_grid_price()
        self.set_artist_grid_volume()

        return

    def set_canvas_artist(self):
        self.set_artist_grid()

        return

