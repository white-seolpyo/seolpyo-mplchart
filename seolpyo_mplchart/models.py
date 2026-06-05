from typing import TypedDict

from matplotlib.backends.backend_agg import FigureCanvasAgg, RendererAgg
from matplotlib.backend_bases import FigureManagerBase
from matplotlib.figure import Figure as Fig


class Canvas(FigureCanvasAgg):
    manager: FigureManagerBase
    renderer = RendererAgg


class Figure(Fig):
    canvas: Canvas


class AxData(TypedDict):
    name: str
    is_px: bool
    size: int


class AdjustData(TypedDict):
    "https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.subplots_adjust.html"
    # 여백
    top: float
    bottom: float
    left: float
    right: float
    # 플롯간 간격
    wspace: float
    hspace: float

