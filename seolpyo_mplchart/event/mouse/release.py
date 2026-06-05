from matplotlib.backend_bases import MouseEvent, MouseButton, cursors
from matplotlib.collections import LineCollection

from ...models import Figure


class ChartMixin:
    def _on_release_chart(self, e: MouseEvent):
        self._click_x_coord = None
        self.is_click_chart = False
        self.is_move_chart = False

        self.axis(*self._nav_x_coords)

        self._on_release_action()

        return

class SliderMixin:
    min_distance = 3

    collection_slider_nav: LineCollection

    def _on_release_slider(self, e: MouseEvent):
        self._click_x_coord = None
        self.is_click_slider = False
        self.is_move_chart = False
        self._click_nav_side = ''

        xmin, xmax = self.get_nav_xlim()
        xsub = xmax - xmin

        min_distance = 3 if not self.min_distance or self.min_distance < 3 else self.min_distance
        # print(f'{xsub=}')
        # print(f'{min_distance=}')

        if xsub < min_distance:
            xmin, xmax = self._nav_x_coords
        self.axis(xmin, xmax)
        self.segment_nav = self.collection_slider_nav.get_segments()

        self._on_release_action()

        return


class ReleaseMixin(ChartMixin, SliderMixin):
    figure: Figure

    in_chart: bool
    in_slider: bool

    acting_release = False

    def _on_release_action(self):
        self.figure.canvas.set_cursor(cursors.POINTER)

        # self.draw()
        self.restore_slider()
        self.set_background_chart()
        self.set_background_artist()
        self.restore_background()

        self.blit()
        return

    def _on_release(self, e: MouseEvent):
        if not self.acting_release:
            self.acting_release = True
            self.on_release(e)
            self.acting_release = False
        return

    def on_release(self, e: MouseEvent):
        if self._click_x_coord is not None and e.button == MouseButton.LEFT:
            if self.is_click_chart and self.in_chart:
                self._on_release_chart(e)
            elif self.is_click_slider and self.in_slider:
                self._on_release_slider(e)
        return

