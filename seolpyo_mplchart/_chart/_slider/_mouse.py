from matplotlib.backend_bases import MouseEvent, MouseButton, cursors

from ._data import BaseMixin as Base


class MouseMoveMixin(Base):
    in_slider = False
    is_click_slider = False

    def _erase_crossline(self):
        boolen = super()._erase_crossline()
        if boolen:
            return boolen

        seg = self.collection_slider_vline.get_segments()
        if seg:
            self.collection_slider_vline.set_segments([])
            return True
        return False

    def _on_move_action(self, e):
        super()._on_move_action(e)

        if self.in_slider:
            self._restore_region(self.is_click_slider)
            self._on_move_slider(e)
            self.figure.canvas.blit()
        elif self.in_price_chart or self.in_volume_chart:
            self._restore_region()
            self._draw_crossline(e)
            self.figure.canvas.blit()
        else:
            if self._erase_crossline():
                self._restore_region()
                self.figure.canvas.blit()
        return

    def _on_move_action(self, e: MouseEvent):
        self._check_ax(e)

        self.intx = None
        if self.in_slider or self.in_price_chart or self.in_volume_chart:
            self._get_x(e)

        self._set_cursor(e)
        return

    def _set_cursor(self, e: MouseEvent):
        # 마우스 커서 변경
        if self.is_click_slider:
            return
        elif not self.in_slider:
            self.figure.canvas.set_cursor(cursors.POINTER)
            return

        navleft, navright = self.navcoordinate
        if navleft == navright:
            return

        x = e.xdata.__round__()

        leftmin = navleft - self._navLineWidth
        leftmax = navleft + self._navLineWidth_half
        rightmin = navright - self._navLineWidth_half
        rightmax = navright + self._navLineWidth
        if x < leftmin:
            self.figure.canvas.set_cursor(cursors.POINTER)
        elif x <= leftmax:
            self.figure.canvas.set_cursor(cursors.RESIZE_HORIZONTAL)
        elif x < rightmin:
            self.figure.canvas.set_cursor(cursors.MOVE)
        elif x <= rightmax:
            self.figure.canvas.set_cursor(cursors.RESIZE_HORIZONTAL)
        else:
            self.figure.canvas.set_cursor(cursors.POINTER)
        return

    def _check_ax(self, e: MouseEvent):
        ax = e.inaxes
        if not ax or e.xdata is None or e.ydata is None:
            self.in_slider, self.in_price_chart, self.in_volume_chart = (False, False, False)
        else:
            if ax is self.ax_slider:
                self.in_slider = True
                self.in_price_chart = False
                self.in_volume_chart = False
            elif ax is self.ax_price:
                self.in_slider = False
                self.in_price_chart = True
                self.in_volume_chart = False
            elif ax is self.ax_volume:
                self.in_slider = False
                self.in_price_chart = False
                self.in_volume_chart = True
            else:
                self.in_slider = False
                self.in_price_chart = False
                self.in_volume_chart = False
        return

    def _on_move_slider(self, e: MouseEvent):
        x = e.xdata
        if self.intx is not None:
            renderer = self.figure.canvas.renderer
            seg = [((x, self.slider_ymin), (x, self.slider_ymax))]
            self.collection_slider_vline.set_segments(seg)
            self.collection_slider_vline.draw(renderer)

            if self.in_slider:
                self.artist_text_slider.set_text(f'{self.df["date"][self.intx]}')
                self.artist_text_slider.set_x(x)
                self.artist_text_slider.draw(renderer)
        return

    def _draw_crossline(self, e: MouseEvent):
        x = e.xdata
        self.collection_slider_vline.set_segments([((x-0.5, self.slider_ymin), (x-0.5, self.slider_ymax))])
        self.collection_slider_vline.draw(self.figure.canvas.renderer)
        return super()._draw_crossline(e)


class ClickMixin(MouseMoveMixin):
    x_click = None
    is_move = False
    click_navleft, click_navright = (False, False)

    def _connect_events(self):
        super()._connect_events()

        self.figure.canvas.mpl_connect('button_press_event', lambda x: self.on_click(x))
        return

    def on_click(self, e: MouseEvent):
        self._on_click(e)
        return

    def _on_click(self, e: MouseEvent):
        if self.in_slider and not self.is_click_slider:
            if e.button == MouseButton.LEFT:
                self._on_click_slider(e)
        return

    def _on_click_slider(self, e: MouseEvent):
        self.background_with_nav_pre = self.background_with_nav

        self.is_click_slider = True
        self.figure.canvas.set_cursor(cursors.RESIZE_HORIZONTAL)

        navleft, navright = self.navcoordinate
        x = e.xdata.__round__()

        leftmax = navleft + self._navLineWidth_half
        rightmin = navright - self._navLineWidth_half

        grater_than_left = leftmax < x
        less_then_right = x < rightmin
        if grater_than_left and less_then_right:
            self.is_move = True
            self.x_click = x
        else:
            leftmin = navleft - self._navLineWidth
            rightmax = navright + self._navLineWidth
            if not grater_than_left and leftmin <= x:
                self.click_navleft = True
                self.x_click = navright
            elif not less_then_right and x <= rightmax:
                self.click_navright = True
                self.x_click = navleft
            else:
                self.x_click = x
        return


class BaseMixin(ClickMixin):
    pass

