from matplotlib.axes import Axes
from matplotlib.text import Text
from matplotlib.lines import Line2D
from matplotlib.backend_bases import PickEvent
from matplotlib.collections import LineCollection

from ..._config import ConfigData

from .a_canvas import Figure


class Base:
    figure: Figure

    text_to_handle: dict[Text, Line2D] = {}

    _draw_canvas: callable
    _set_figure_ratios: callable

    def on_draw(self, e):
        self._background = None
        self._draw_canvas()
        return

    def on_resize(self, e):
        self._set_figure_ratios()
        return


class LegendMixin(Base):
    CONFIG: ConfigData

    figure: Figure
    ax_legend: Axes
    collection_ma: LineCollection

    def on_pick(self, e: PickEvent):
        artist = e.artist
        ax = artist.axes
        if ax is self.ax_legend:
            self._pick_legend_action(e)
        return

    def _pick_legend_action(self, e: PickEvent):
        artist = e.artist

        # ma label이 맞는지 검증
        if isinstance(artist, Line2D):
            text = artist.get_label()
        elif isinstance(artist, Text):
            text = artist.get_text()
        else:
            return
        # print(f'{text=}')

        for ma in self.CONFIG.MA.ma_list:
            label = self.CONFIG.MA.format.format(ma)
            # print(f'{label=}')
            if text == label:
                break
        else:
            return

        if not isinstance(artist, Text):
            handle = artist
        else:
            try:
                handle = self.text_to_handle[artist]
            except KeyError:
                return
        visible = handle.get_alpha() == 0.2
        handle.set_alpha(1.0 if visible else 0.2)

        if visible:
            self._visible_ma = {i for i in self.CONFIG.MA.ma_list if i in self._visible_ma or i == ma}
        else:
            self._visible_ma = {i for i in self._visible_ma if i != ma}

        alphas = [(1 if i in self._visible_ma else 0) for i in reversed(self.CONFIG.MA.ma_list)]
        self.collection_ma.set_alpha(alphas)

        self.draw()
        return


class EventMixin(LegendMixin):
    def connect_events(self):
        self.figure.canvas.mpl_connect('draw_event', lambda x: self.on_draw(x))
        self.figure.canvas.mpl_connect('pick_event', lambda x: self.on_pick(x))
        self.figure.canvas.mpl_connect('resize_event', lambda x: self.on_resize(x))
        return

