from matplotlib.axes import Axes
from matplotlib.backend_bases import MouseEvent

from ....models import Figure

from .crossline import CrosslineMixin
from .label import LabelMixin
from .box import BoxMixin
from .info import InfoMixin, format_info_price, format_info_volume, format_info_price_en, format_info_volume_en
from .move import ChartMoveMixin


class AxMixin:
    def check_ax(self, e: MouseEvent):
        ax = e.inaxes
        # print(f'{ax=}')

        self.in_chart_price = False
        self.in_chart_volume = False

        self.in_chart = False
        self.in_slider = False

        xdata, ydata = (e.xdata, e.ydata)
        if xdata is None or ydata is None:
            return

        ax_price: Axes = self.get_ax_price()
        ax_volume: Axes = self.get_ax_volume()
        ax_slider: Axes = self.get_ax_slider()

        if ax is ax_slider:
            xmin, xmax = ax_slider.get_xlim()
            ymin, ymax = ax_slider.get_ylim()
            if (
                (xmin <= xdata and xdata <= xmax)
                and (ymin <= ydata and ydata <= ymax)
            ):
                self.in_slider = True
        elif ax is ax_price:
            xmin, xmax = ax_price.get_xlim()
            ymin, ymax = ax_price.get_ylim()
            if (
                (xmin <= xdata and xdata <= xmax)
                and (ymin <= ydata and ydata <= ymax)
            ):
                self.in_chart_price = True
                self.in_chart = True
        elif ax is ax_volume:
            xmin, xmax = ax_volume.get_xlim()
            ymin, ymax = ax_volume.get_ylim()
            if (
                (xmin <= xdata and xdata <= xmax)
                and (ymin <= ydata and ydata <= ymax)
            ):
                self.in_chart_volume = True
                self.in_chart = True
        return


class MoveMixin(
    CrosslineMixin, LabelMixin,
    BoxMixin, InfoMixin,
    ChartMoveMixin,

    AxMixin,
):
    figure: Figure

    _click_x_coord: int

    segment_nav: list

    acting_mouse_move = False

    in_chart = False
    in_chart_price = False
    in_chart_volume = False
    in_slider  = False

    @property
    def renderer(self):
        return self.figure.canvas.renderer

    def need_restore(self):
        if self.collection_crossline_price.get_segments() or self._click_x_coord is None:
            self.collection_crossline_price.set_segments([])
            self.collection_slider_vline.set_segments([])
            return True
        return

    def get_nav_xlim(self):
        seg = self.segment_nav
        # print(f'{seg=}')
        x0 = int(seg[-2][0][0])
        x1 = int(seg[-1][0][0])

        if x0 < 0:
            x0 -= 1

        return (x0, x1)

    def _on_move_mouse(self, e: MouseEvent):
        if self.in_chart:
            self.restore_artist()

            self.draw_crossline(e)
            self.draw_label(e)
            if self.draw_label(e):
                self.draw_box_artist(e)
                if self.in_box_price or self.in_box_volume:
                    self.draw_info(int(e.xdata))

            self.blit()

        elif self.in_slider:
            self.restore_artist()

            self.draw_crossline(e)
            self.draw_label(e)

            self.blit()

        return

    def _on_move_chart(self, e: MouseEvent):
        if e.xdata is not None:
            if self._click_x_coord is not None:
                self.restore_slider()

                self._move_chart(e)

                self.draw_chart()
                self.draw_artist()

                if self.in_slider:
                    self.draw_slider_vline(e)
                    self.draw_slider_label(e)

                self.blit()
            else:
                self.set_cursor(e)

                if self.in_slider:
                    self.restore_chart()

                    self.draw_slider_vline(e)
                    self.draw_slider_label(e)

                    self.blit()
        return

    def _on_move(self, e: MouseEvent):
        if not self.acting_mouse_move:
            self.acting_mouse_move = True
            self.on_move(e)
            self.acting_mouse_move = False
        return

    def on_move(self, e: MouseEvent):
        self.check_ax(e)

        self.set_cursor(e)

        if self.in_chart or self.in_slider:
            if self.is_move_chart or self.is_click_slider:
                self._on_move_chart(e)
            else:
                self._on_move_mouse(e)

        elif self.need_restore():
            self.restore_artist()
            self.blit()

        return

