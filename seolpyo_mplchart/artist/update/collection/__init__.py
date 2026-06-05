from .canvas import CanvasMixin
from .crossline import CrossLineMixin
from .box import BoxMixin
from .slider import SliderMixin


class CollectionMixin(CanvasMixin, CrossLineMixin, BoxMixin, SliderMixin):
    def set_collection(self):
        self.set_canvas_artist()

        self.set_collection_crossline()
        self.set_collection_box()

        self.set_slider_nav_collection()

        return