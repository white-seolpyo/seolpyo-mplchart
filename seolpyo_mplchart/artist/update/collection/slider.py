from matplotlib.collections import LineCollection

from ....style import Style


class SliderMixin:
    STYLE: Style

    collection_slider_top_nav: LineCollection
    collection_slider_bottom_nav: LineCollection

    slider_xmin: int
    slider_xmax: int

    def _set_slider_nav_collection(self, position):
        collection_slider_nav: LineCollection = getattr(self, f'collection_slider_{position}_nav')

        facecolor = self.STYLE.SLIDER.NAV.facecolor
        edgecolor = self.STYLE.SLIDER.NAV.edgecolor
        facecolors = [facecolor, facecolor, edgecolor, edgecolor]
        collection_slider_nav.set_linewidth(0.1)
        collection_slider_nav.set_facecolor(facecolors)

        # facecolor alpha값 제거
        edgecolors = []
        for c in collection_slider_nav.get_facecolor():
            # print(c)
            edgecolors.append(c[:3])
        collection_slider_nav.set_facecolor(edgecolors)

        alpha = self.STYLE.SLIDER.NAV.alpha
        collection_slider_nav.set_alpha([alpha, alpha, 1, 1])

        collection_slider_nav.set_edgecolor([(0, 0, 0, 0) for _ in edgecolors])
        collection_slider_nav.set_animated(True)

        return

    def _set_slider_top_nav_collection(self):
        self.collection_slider_top_nav: LineCollection
        self._set_slider_nav_collection('top')

        return

    def _set_slider_bottom_nav_collection(self):
        self.collection_slider_bottom_nav: LineCollection
        self._set_slider_nav_collection('bottom')

        return

    def set_slider_nav_collection(self):
        self._set_slider_top_nav_collection()
        self._set_slider_bottom_nav_collection()

        return

