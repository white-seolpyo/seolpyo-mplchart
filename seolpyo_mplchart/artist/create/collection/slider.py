from matplotlib.axes import Axes
from matplotlib.collections import LineCollection


class SliderMixin:
    slider_top: bool

    @property
    def collection_slider_nav(self):
        if self.slider_top:
            return self.collection_slider_top_nav
        return self.collection_slider_bottom_nav

    def _add_slider_nav_collection(self, position):
        ax: Axes = getattr(self, f'get_ax_slider_{position}')()

        kwargs: dict = self.get_default_collection_kwargs()

        collection_slider_nav = LineCollection(**kwargs)
        ax.add_collection(collection_slider_nav)
        setattr(self, f'collection_slider_{position}_nav', collection_slider_nav)

        return

    def _add_slider_top_nav_collection(self):
        self.collection_slider_top_nav: LineCollection
        self._add_slider_nav_collection('top')

        return

    def _add_slider_bottom_nav_collection(self):
        self.collection_slider_bottom_nav: LineCollection
        self._add_slider_nav_collection('bottom')

        return

    def add_slider_nav_collection(self):
        self._add_slider_top_nav_collection()
        self._add_slider_bottom_nav_collection()

        return

