from matplotlib.axes import Axes
from matplotlib.backend_bases import MouseEvent, MouseButton, cursors
from matplotlib.collections import LineCollection
from matplotlib.text import Text
import numpy as np

from ..cursor.g_event import EventMixin as Base


class BaseMixin(Base):
    ax_slider: Axes

    slider_xmin: int
    slider_xmax: int
    slider_ymin: float
    slider_ymax: float

    in_slider = False
    is_click_slider = False
    is_click_chart = False
    is_move_chart = False

    click_nav_left = False
    click_nav_right = False

    min_distance = 5

    segment_nav: np.ndarray

    _set_slider_vline: callable
    _draw_slider_vline: callable
    _set_slider_text: callable
    _draw_slider_text: callable
    draw_chart: callable
    axis: callable
    _set_cursor: callable
    _move_chart: callable
    _draw_nav: callable
    _restore_region_background: callable

    collection_slider_vline: LineCollection
    artist_text_slider: Text
    collection_nav: LineCollection

    x_click: int
    _nav_width: float
    navcoordinate: tuple[int, int]
    vxmin: int
    vxmax: int

    def get_nav_xlim(self):
        seg = self.segment_nav
        # print(f'{seg=}')
        xmin = seg[-2][0][0]
        xmax = seg[-1][0][0]
        
        return (int(xmin), int(xmax))


class CursorMixin(BaseMixin):
    def _set_cursor(self, e: MouseEvent):
        # 마우스 커서 변경
        if self.is_click_slider:
            return
        elif not self.in_slider:
            self.figure.canvas.set_cursor(cursors.POINTER)
            return

        xmin, xmax = self.get_nav_xlim()
        if xmin == xmax:
            return

        x = e.xdata

        left0 = xmin - self._nav_width
        left1 = xmin

        if left0 <= x and x <= left1:
            # 커서가 좌경계선 위에 위치
            self.figure.canvas.set_cursor(cursors.RESIZE_HORIZONTAL)
            return

        right0 = xmax
        right1 = xmax + self._nav_width
        if right0 <= x and x <= right1:
            # 커서가 우경계선 위에 위치
            self.figure.canvas.set_cursor(cursors.RESIZE_HORIZONTAL)
            return

        if left1 < x and x < right0:
            # 커서가 조회영역 위에 위치
            self.figure.canvas.set_cursor(cursors.MOVE)
            return

        self.figure.canvas.set_cursor(cursors.POINTER)
        return


class AxMixin(BaseMixin):
    def _check_ax(self, e: MouseEvent):
        ax = e.inaxes
        # print(f'{ax=}')
        self.in_chart = False
        self.in_slider, self.in_chart_price, self.in_chart_volume = (False, False, False)

        if e.xdata is None or e.ydata is None:
            return

        if ax is self.ax_slider:
            if (
                (self.slider_xmin <= e.xdata and e.xdata <= self.slider_xmax)
                and (self.slider_ymin <= e.ydata and e.ydata <= self.slider_ymax)
            ):
                self.in_slider = True
        else:
            super()._check_ax(e)
        return


class ClickMixin(BaseMixin):
    is_click_slider = False
    is_click_chart = False

    click_nav_left = False
    click_nav_right = False

    def on_click(self, e: MouseEvent):
        if e.xdata is not None and e.ydata is not None:
            if self.in_chart and not self.is_click_chart:
                if e.button == MouseButton.LEFT:
                    self._on_click_chart(e)
            elif self.in_slider and not self.is_click_slider:
                if e.button == MouseButton.LEFT:
                    self._on_click_slider(e)
        return

    def _on_click_chart(self, e: MouseEvent):
        # 조회영역 이동 시작
        self.is_click_chart = True
        self.is_move_chart = True

        x = int(e.xdata)
        self.x_click = x

        xmin, xmax = self.get_nav_xlim()
        self.navcoordinate = (xmin, xmax)

        self.figure.canvas.set_cursor(cursors.RESIZE_HORIZONTAL)
        return

    def _on_click_slider(self, e: MouseEvent):
        self.is_click_slider = True
        self.figure.canvas.set_cursor(cursors.RESIZE_HORIZONTAL)

        xmin, xmax = self.get_nav_xlim()
        x = round(e.xdata)

        xmin0 = xmin - self._nav_width
        xmin1 = xmin
        if xmin0 <= x and x <= xmin1:
            # 좌경계선 이동 시작
            self.navcoordinate = (xmin, xmax)
            self.click_nav_left = True
            self.x_click = xmin
            return

        xmax0 = xmax
        if xmin1 < x and x < xmax0:
            # 조회영역 이동 시작
            self.navcoordinate = (xmin, xmax)
            self.is_move_chart = True
            self.x_click = x
            return

        if xmax0 <= x and x <= (xmax + self._nav_width):
            # 우경계선 이동 시작
            self.navcoordinate = (xmin, xmax)
            self.click_nav_right = True
            self.x_click = xmax
            return

        self.navcoordinate = (xmin, xmax)
        self.x_click = x
        return


class ReleaseMixin(BaseMixin):
    def on_release(self, e: MouseEvent):
        if e.button ==  MouseButton.LEFT:
            if (
                self.is_click_chart
                and self.in_chart
            ):
                self._on_release_chart(e)
            elif self.is_click_slider and self.in_slider:
                self._on_release_slider(e)
        return

    def _on_release_chart(self, e):
        self.x_click = None
        self.is_click_chart = False
        self.is_move_chart = False
        self.figure.canvas.set_cursor(cursors.POINTER)

        xmin, xmax = self.navcoordinate
        self.axis(xmin, xmax=xmax)
        self.figure.canvas.draw()
        return

    def _on_release_slider(self, e: MouseEvent):
        if self.x_click:
            xmin, xmax = self.get_nav_xlim()
            xsub = xmax - xmin
            min_distance = 5 if not self.min_distance or self.min_distance < 5 else self.min_distance
            # print(f'{xsub=}')
            # print(f'{min_distance=}')
            if min_distance <= xsub:
                self.navcoordinate = (xmin, xmax)
            else:
                xmin, xmax = self.navcoordinate

            self.x_click = None
            self.is_click_slider = False
            self.is_move_chart = False
            self.click_nav_left, self.click_nav_right = (False, False)
            self.axis(xmin, xmax=xmax)

            self.figure.canvas.draw()
        return


class ChartMixin(BaseMixin):
    def _move_chart(self, e: MouseEvent):
        if self.is_click_chart and self.in_chart:
            xdata = int(e.xdata)
            # print(f'{(self.x_click, xdata)=}')
            xsub = self.x_click - xdata
            if xsub:
                pre_xmin, pre_xmax = self.navcoordinate
                xmin, xmax = (pre_xmin+xsub, pre_xmax+xsub)
                # print(f'{(xmin, xmax)=}')
                if 0 <= xmax and xmin <= self.index_list[-1] and xmin != xmax:
                    self.axis(xmin, xmax=xmax)
                    self.navcoordinate = (xmin, xmax)
        elif self.is_click_slider and self.in_slider:
            xdata = round(e.xdata)
            pre_xmin, pre_xmax = self.navcoordinate
            if self.click_nav_left:
                if xdata < pre_xmax:
                    xmin, xmax = (xdata, pre_xmax)
                else:
                    xmin, xmax = (pre_xmax, xdata)
            elif self.click_nav_right:
                if xdata < pre_xmin:
                    xmin, xmax = (xdata, pre_xmin)
                else:
                    xmin, xmax = (pre_xmin, xdata)
            else:
                if self.is_move_chart:
                    xsub = self.x_click - xdata
                    xmax = -1
                    if xsub:
                        pre_xmin, pre_xmax = self.navcoordinate
                        xmin, xmax = (pre_xmin-xsub, pre_xmax-xsub)
                else:
                    if xdata == self.x_click:
                        xmax = -1
                    elif xdata < self.x_click:
                        xmin, xmax = (xdata, self.x_click)
                    else:
                        xmin, xmax = (self.x_click, xdata)
    
            if 0 <= xmax and xmin <= self.index_list[-1] and xmin != xmax:
                self.axis(xmin, xmax=xmax)
        return


class MoveMixin(BaseMixin):
    def _set_and_draw_vline(self, e: MouseEvent):
        self._set_slider_vline(e)
        self._draw_slider_vline()
        if self.in_slider and self._set_slider_text(e):
            self._draw_slider_text()
        return
 
    def _set_and_draw_crossline(self, e: MouseEvent):
        self._set_and_draw_vline(e)

        super()._set_and_draw_crossline(e)
        return
 
    def _on_move_action(self, e: MouseEvent):
        if e.xdata is not None:
            if self.x_click is not None:
                self._restore_region_background()

                self._move_chart(e)
                self.draw_chart()
                self._draw_nav()
                if self.in_slider:
                    self._set_and_draw_vline(e)

                self.figure.canvas.blit()
                self.figure.canvas.flush_events()
            else:
                self._set_cursor(e)

                if self.in_slider:
                    self._restore_region()

                    self._set_and_draw_vline(e)

                    self.figure.canvas.blit()
                    self.figure.canvas.flush_events()
                else:
                    super()._on_move_action(e)
        else:
            super()._on_move_action(e)
        return

    def need_restore(self):
        if not super().need_restore():
            if self.collection_slider_vline.get_segments():
                self.collection_slider_vline.set_segments([])
                return True
        return


class EventMixin(AxMixin, CursorMixin, ClickMixin, ReleaseMixin, ChartMixin, MoveMixin,):
    x_click = None
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

    min_distance = 5

    navcoordinate: tuple[int, int]

    def connect_events(self):
        super().connect_events()

        self.figure.canvas.mpl_connect('button_press_event', lambda x: self.on_click(x))
        self.figure.canvas.mpl_connect('button_release_event', lambda x: self.on_release(x))
        return
