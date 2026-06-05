from matplotlib.backend_bases import MouseEvent, MouseButton, cursors


class ChartMixin:
    def _on_click_chart(self, e: MouseEvent):
        self.is_click_chart = True
        # 조회영역 이동 시작
        self.is_move_chart = True

        self.set_cursor(cursors.RESIZE_HORIZONTAL)

        x = int(e.xdata)
        self._click_x_coord = x

        x0, x1 = self.get_nav_xlim()
        self._nav_x_coords = (x0, x1)

        return


class SliderMixin:
    _nav_width: float

    def _on_click_slider(self, e: MouseEvent):
        self.is_click_slider = True
        self.set_cursor(cursors.RESIZE_HORIZONTAL)

        x0, x1 = self.get_nav_xlim()
        x = int(e.xdata)

        left0 = x0 - self._nav_width
        left1 = x0
        if left0 <= x and x <= left1:
            # 좌경계선 이동 시작
            self._nav_x_coords = (x0, x1)
            self._click_nav_side = 'left'
            self._click_x_coord = x0
            return

        right0 = x1
        if left1 < x and x < right0:
            # 조회영역 이동 시작
            self._nav_x_coords = (x0, x1)
            self.is_move_chart = True
            self._click_x_coord = x
            return

        if right0 <= x and x <= (x1 + self._nav_width):
            # 우경계선 이동 시작
            self._nav_x_coords = (x0, x1)
            self._click_nav_side = 'right'
            self._click_x_coord = x1
            return

        # 위 조건들에 해당하는 사항이 없으면 조회영역 변경
        self._nav_x_coords = (x0, x1)
        self._click_x_coord = x

        return


class ClickMixin(ChartMixin, SliderMixin):
    in_chart: bool
    in_slider: bool

    acting_click = False

    is_click_slider = False
    is_click_chart = False

    _click_x_coord = None

    is_move_chart = False
    
    _click_nav_side = None

    def _on_click(self, e: MouseEvent):
        if not self.acting_click:
            self.acting_click = True
            self.on_click(e)
            self.acting_click = False
        return

    def on_click(self, e: MouseEvent):
        if e.button != MouseButton.LEFT:
            return

        if not self._click_x_coord:
            if not self.is_click_chart and self.in_chart:
                self._on_click_chart(e)
            elif not self.is_click_slider and self.in_slider:
                self._on_click_slider(e)

        return

