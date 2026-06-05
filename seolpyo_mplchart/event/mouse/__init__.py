from matplotlib.backend_bases import MouseEvent, cursors

from .move import MoveMixin, format_info_price, format_info_volume, format_info_price_en, format_info_volume_en
from .click import ClickMixin
from .release import ReleaseMixin


class MouseMixin(MoveMixin, ClickMixin, ReleaseMixin):
    def set_cursor(self, e: MouseEvent):
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

        xmin += 0.5
        xmax += 0.5

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

