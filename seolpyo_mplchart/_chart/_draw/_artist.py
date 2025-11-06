from matplotlib.collections import LineCollection

from .._base import BaseMixin as Base


class CollectionMixin(Base):
    def _add_artists(self):
        super()._add_artists()

        self.collection_candle = LineCollection([], animated=True, linewidths=0.8)
        self.ax_price.add_collection(self.collection_candle)

        self.collection_ma = LineCollection([], animated=True, linewidths=1)
        self.ax_price.add_collection(self.collection_ma)

        self.collection_volume = LineCollection([], animated=True, linewidths=1)
        self.ax_volume.add_collection(self.collection_volume)
        return


class SegmentMixin(CollectionMixin):
    def get_candle_segment(self, *, is_up, x, left, right, top, bottom, high, low):
        """
        get candle segment

        Args:
            is_up (bool): (True if open < close else False)
            x (float): center of candle
            left (float): left of candle
            right (float): right of candle
            top (float): top of candle(close if `is_up` else open)
            bottom (float): bottom of candle(open if `is_up` else close)
            high (float): top of candle wick
            low (float): bottom of candle wick

        Returns:
            tuple[tuple[float, float]]: candle segment
        """
        return (
            (x, top),
            (left, top), (left, bottom),
            (x, bottom), (x, low), (x, bottom),
            (right, bottom), (right, top),
            (x, top), (x, high)
        )


class BaseMixin(SegmentMixin):
    pass

