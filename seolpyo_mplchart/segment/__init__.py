from numpy.ma import MaskedArray

from .price import PriceMixin
from .volume import VolumeMixin
from .ma import MaMixin
from .slider import SliderMixin


class SegmentMixin(PriceMixin, VolumeMixin, MaMixin, SliderMixin):
    segment_candle: MaskedArray = []
    segment_wick: MaskedArray = []
    segment_priceline: MaskedArray = []

    segment_volume: MaskedArray = []
    segment_volume_wick: MaskedArray = []

    segment_ma: MaskedArray = []

    segment_slider: MaskedArray = []
    segment_nav: MaskedArray = []

    def set_segment(self):
        self.set_price_segment()
        self.set_volume_segment()
        self.set_ma_segment()
        self.set_slider_segment()
        return

