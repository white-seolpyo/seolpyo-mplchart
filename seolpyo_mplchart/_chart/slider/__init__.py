from matplotlib.axes import Axes
from matplotlib.collections import LineCollection
from matplotlib.text import Text
from matplotlib.axes import Axes
import numpy as np
import pandas as pd

from ..._config import SLIDERCONFIG, SliderConfigData
from ..base import Chart as BaseChart
from ..cursor import CursorMixin

from .a_canvas import CanvasMixin, Figure
from .b_artist import ArtistMixin
from .c_draw import DrawMixin
from .d_segment import SegmentMixin
from .e_axis import AxisMixin
from .f_background import BackgroundMixin
from .g_event import EventMixin
from .h_data import DataMixin


class SliderMixin(
    CanvasMixin,
    ArtistMixin,
    DrawMixin,
    SegmentMixin,
    AxisMixin,
    BackgroundMixin,
    EventMixin,
    DataMixin,
):
    pass


class Chart(SliderMixin, CursorMixin, BaseChart):
    candle_on_ma = True
    slider_top = True
    fraction = False

    limit_candle = 400
    limit_wick = 2_000
    limit_volume = 200
    limit_ma = 8_000

    min_distance = 5

    key_date = 'date'
    key_open, key_high, key_low, key_close = ('open', 'high', 'low', 'close')
    key_volume = 'volume'

    index_list: list[int] = []

    df: pd.DataFrame

    CONFIG: SliderConfigData

    figure: Figure
    ax_legend: Axes
    ax_price: Axes
    ax_volume: Axes

    ax_slider: Axes
    ax_none: Axes
    _ax_slider_top: Axes
    _ax_slider_bottom: Axes

    artist_watermark: Text
    collection_candle: LineCollection
    collection_volume: LineCollection
    collection_ma: LineCollection

    collection_slider: LineCollection
    collection_nav: LineCollection
    collection_slider_vline: LineCollection
    artist_text_slider: Text

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

    v0: int
    v1: int
    vmiddle: int

    min_height_box_candle: float
    min_height_box_volume: float

    _length_text: int

    _in_mouse_move = False

    ###

    segment_nav: np.ndarray
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

    _nav_width: float

    slider_xmin: int
    slider_xmax: int
    slider_ymin: float
    slider_ymax: float

    in_chart = False
    in_slider = False
    in_chart_price = False
    in_chart_volume = False

    is_move_chart = False
    is_click_slider = False
    is_click_chart = False
    x_click: float

    click_nav_left = False
    click_nav_right = False

    navcoordinate: tuple[int, int]

    ###

    _visible_ma: set[int] = set()
    _edgecolor_ma = []

    _background = None
    _creating_background = False

    def __init__(self, config=SLIDERCONFIG):
        self.CONFIG = config
        super().__init__()
        return

    def refresh(self):
        self._set_slider_artists()
        super().refresh()
        return

