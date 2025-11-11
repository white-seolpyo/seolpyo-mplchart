from matplotlib.axes import Axes
from matplotlib.collections import LineCollection
from matplotlib.text import Text
from matplotlib.axes import Axes
import numpy as np
import pandas as pd

from ..._config import DEFAULTCONFIG, ConfigData

from .a_canvas import CanvasMixin, Figure
from .b_artist import ArtistMixin
from .c_draw import DrawMixin
from .d_segment import SegmentMixin
from .e_axis import AxisMixin
from .f_background import BackgroundMixin
from .g_event import EventMixin
from .h_data import DataMixin


class Chart(
    CanvasMixin,
    ArtistMixin,
    DrawMixin,
    SegmentMixin,
    AxisMixin,
    BackgroundMixin,
    EventMixin,
    DataMixin,
):
    limit_candle = 400
    limit_wick = 2_000
    candle_on_ma = True

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

    ###

    _visible_ma: set[int] = set()

    _background = None
    _background_background = None
    _creating_background = False

    def __init__(self, config=DEFAULTCONFIG):
        self.CONFIG = config
        super().__init__()

        self.add_artists()
        self.connect_events()
        return

    def refresh(self):
        self.set_artists()

        self.set_candle_segments()
        self.set_color_segments()
        ma_alpha = self.collection_ma.get_alpha()
        # print(f'{ma_alpha=}')
        if ma_alpha is not None:
            self.collection_ma.set_alpha([1 for _ in ma_alpha])

        self.axis(self.vxmin, xmax=self.vxmax-1)

        self.set_canvas()
        self.figure.canvas.draw()
        return

