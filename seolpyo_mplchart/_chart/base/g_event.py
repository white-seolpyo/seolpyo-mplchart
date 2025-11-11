from matplotlib.axes import Axes
from matplotlib.backend_bases import PickEvent
from matplotlib.collections import LineCollection

from ..._config import ConfigData

from .a_canvas import Figure


class Base:
    figure: Figure

    _draw_canvas: callable
    _set_figure_ratios: callable

    def on_draw(self, e):
        self._background = None
        self._draw_canvas()
        return

    def on_resize(self, e):
        self._set_figure_ratios()
        return


class LegendMixin:
    CONFIG: ConfigData

    figure: Figure
    ax_legend: Axes
    collection_ma: LineCollection

    def on_pick(self, e):
        self._pick_legend_action(e)
        return

    def _pick_legend_action(self, e: PickEvent):
        handle = e.artist
        ax = handle.axes
        # print(f'{(ax is self.ax_legend)=}')
        if ax is not self.ax_legend:
            return

        visible = handle.get_alpha() == 0.2
        handle.set_alpha(1.0 if visible else 0.2)

        n = int(handle.get_label())
        if visible:
            self._visible_ma = {i for i in self.CONFIG.MA.ma_list if i in self._visible_ma or i == n}
        else:
            self._visible_ma = {i for i in self._visible_ma if i != n}

        alphas = [(1 if i in self._visible_ma else 0) for i in reversed(self.CONFIG.MA.ma_list)]
        self.collection_ma.set_alpha(alphas)

        self.figure.canvas.draw()
        return


class EventMixin(Base, LegendMixin):
    def connect_events(self):
        self.figure.canvas.mpl_connect('draw_event', lambda x: self.on_draw(x))
        self.figure.canvas.mpl_connect('pick_event', lambda x: self.on_pick(x))
        self.figure.canvas.mpl_connect('resize_event', lambda x: self.on_resize(x))
        return

