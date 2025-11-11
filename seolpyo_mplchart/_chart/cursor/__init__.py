from matplotlib.axes import Axes
from matplotlib.collections import LineCollection
from matplotlib.text import Text
from matplotlib.axes import Axes
import numpy as np
import pandas as pd

from ..base import Chart as BaseChart, Figure, ConfigData

from .b_artist import ArtistMixin
from .c_draw import DrawMixin
from .d_segment import SegmentMixin
from .e_axis import AxisMixin
from .g_event import EventMixin
from .h_data import DataMixin


class CursorMixin(
    ArtistMixin,
    DrawMixin,
    SegmentMixin,
    AxisMixin,
    EventMixin,
    DataMixin
):
    pass


class Chart(CursorMixin, BaseChart):
    limit_candle = 400
    limit_wick = 2_000
    candle_on_ma = True
    fraction = False

    key_date = 'date'
    key_open, key_high, key_low, key_close = ('open', 'high', 'low', 'close')
    key_volume = 'volume'

    index_list: list[int] = []

    df: pd.DataFrame

    CONFIG: ConfigData

    figure: Figure
    ax_legend: Axes
    ax_price: Axes
    ax_volume: Axes

    artist_watermark: Text
    collection_candle: LineCollection
    collection_volume: LineCollection
    collection_ma: LineCollection

    in_chart = False
    in_chart_price = False
    in_chart_volume = False

    in_candle = False
    in_volume = False

    collection_price_crossline: LineCollection
    collection_volume_crossline: LineCollection

    artist_label_x: Text = None
    artist_label_y: Text = None

    collection_box_price: LineCollection
    collection_box_volume: LineCollection

    artist_info_candle: Text
    artist_info_volume: Text

    ###

    segment_volume: np.ndarray
    segment_volume_wick: np.ndarray
    facecolor_volume: np.ndarray
    edgecolor_volume: np.ndarray

    segment_candle: np.ndarray
    segment_candle_wick: np.ndarray
    segment_priceline: np.ndarray
    facecolor_candle: np.ndarray
    edgecolor_candle: np.ndarray

    segment_ma: np.ndarray
    edgecolor_ma: np.ndarray

    price_ymin: int
    price_ymax: int
    volume_ymax: int

    chart_price_ymax: float
    chart_volume_ymax: float

    vxmin: int
    vxmax: int

    v0: int
    v1: int
    vmiddle: int

    min_height_box_candle: float
    min_height_box_volume: float

    ###

    _visible_ma: set[int] = set()
    _edgecolor_ma = []

    _background = None
    _background_background = None
    _creating_background = False

    _length_text: int

    _in_mouse_move = False

    def refresh(self):
        super().refresh()

        self._set_length_text()
        return

