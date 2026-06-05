from .canvas import CanvasMixin
from .element import ElementMixin
from .crossline import CrossLineMixin
from .box import BoxMixin
from .slider import SliderMixin


class CollectionMixin(CanvasMixin, ElementMixin, CrossLineMixin, BoxMixin, SliderMixin):
    def _add_collection(self):
        self._add_canvas_collection()

        self._add_element()

        self._add_cross_line()

        self._add_box()

        self.add_slider_nav_collection()

        return

