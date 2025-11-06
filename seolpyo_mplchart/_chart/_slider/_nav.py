from matplotlib.backend_bases import MouseEvent, MouseButton, cursors

from ._mouse import BaseMixin as Base


class SliderSelectMixin(Base):
    limit_ma = 8_000

    def _on_move_slider(self, e):
        if self.is_click_slider:
            self._set_navcoordinate(e)
        return super()._on_move_slider(e)

    def _set_navcoordinate(self, e: MouseEvent):
        navmin, navmax = self.navcoordinate

        x = e.xdata.__int__()
        if self.is_move:
            xsub = self.x_click - x
            navmin, navmax = (navmin-xsub, navmax-xsub)

            # 값 보정
            if navmax < 0:
                navmin, navmax = (navmin-navmax, 0)
            if self.index_list[-1] < navmin:
                navmin, navmax = (self.index_list[-1], self.index_list[-1] + (navmax-navmin))

            self.navcoordinate = (navmin, navmax)
            self.x_click = x

            self.axis(navmin, xmax=navmax+1, simpler=True, draw_ma=(navmax-navmin < self.limit_ma))

            self._axis_navigator(navmin, navmax)
            self.collection_navigator.draw(self.figure.canvas.renderer)

            self.draw_artists()
            self.background_with_nav = self.figure.canvas.renderer.copy_from_bbox(self.figure.bbox)
            self._restore_region()
        else:
            navmin, navmax = (x, self.x_click) if x < self.x_click else (self.x_click, x)

            # 슬라이더가 차트를 벗어나지 않도록 선택 영역 제한
            if navmax < 0 or self.index_list[-1] < navmin:
                seg = self.collection_navigator.get_segments()
                navmin, navmax = (int(seg[1][0][0]), int(seg[3][0][0]))

            nsub = navmax - navmin
            min_distance = 5 if not self.min_distance or self.min_distance < 5 else self.min_distance
            if nsub < min_distance:
                self._restore_region(False, False)
                self._axis_navigator(navmin, navmax)
                self.collection_navigator.draw(self.figure.canvas.renderer)
            else:
                self.axis(navmin, xmax=navmax+1, simpler=True, draw_ma=(nsub < self.limit_ma))
                self._axis_navigator(navmin, navmax)

                self.collection_navigator.draw(self.figure.canvas.renderer)

                self.draw_artists()
                self.background_with_nav = self.figure.canvas.renderer.copy_from_bbox(self.figure.bbox)
                self._restore_region(False, True)
        return


class ReleaseMixin(SliderSelectMixin):
    def _connect_events(self):
        super()._connect_events()

        self.figure.canvas.mpl_connect('button_release_event', lambda x: self.on_release(x))
        return

    def on_release(self, e: MouseEvent):
        self._on_release(e)
        return

    def _on_release(self, e: MouseEvent):
        if self.in_slider and self.is_click_slider:
            if e.button == MouseButton.LEFT:
                self._on_release_slider(e)
                self.axis(self.vxmin, xmax=self.vxmax, simpler=False, draw_ma=True)
                self.figure.canvas.draw()
        return

    def _on_release_slider(self, e: MouseEvent):
        if not self.is_move:
            seg = self.collection_navigator.get_segments()
            navmin, navmax = (int(seg[1][0][0]), int(seg[3][0][0]))
            nsub = navmax - navmin
            min_distance = 5 if not self.min_distance or self.min_distance < 5 else self.min_distance
            if min_distance <= nsub:
                self.navcoordinate = (navmin, navmax)
            else:
                self.background_with_nav = self.background_with_nav_pre
                navmin, navmax = self.navcoordinate
                self.axis(navmin, xmax=navmax+1, simpler=False, draw_ma=True)
                self._restore_region(False, True)
                self.figure.canvas.blit()
            self._axis_navigator(*self.navcoordinate)

        self.is_click_slider = False
        self.is_move = False
        self.click_navleft, self.click_navright = (False, False)

        # self.figure.canvas.draw()
        return


class ChartClickMixin(ReleaseMixin):
    is_click_chart = False

    def _on_click(self, e: MouseEvent):
        if e.button == MouseButton.LEFT:
            if (
                not self.is_click_chart
                and (self.in_price_chart or self.in_volume_chart)
            ):
                self._on_click_chart(e)
            elif not self.is_click_slider and self.in_slider:
                self._on_click_slider(e)
        return

    def _on_click_chart(self, e: MouseEvent):
        self.is_click_chart = True
        x = e.xdata.__int__()
        self.x_click = x - self.navcoordinate[0]
        self.figure.canvas.set_cursor(cursors.RESIZE_HORIZONTAL)
        return

    def _on_release(self, e):
        if e.button ==  MouseButton.LEFT:
            if (
                self.is_click_chart
                and (self.in_price_chart or self.in_volume_chart)
            ):
                self._on_release_chart(e)
                self.axis(self.vxmin, xmax=self.vxmax, simpler=False, draw_ma=True)
                self.figure.canvas.draw()
            elif self.is_click_slider and self.in_slider:
                self._on_release_slider(e)
                self.axis(self.vxmin, xmax=self.vxmax, simpler=False, draw_ma=True)
                self.figure.canvas.draw()
        return

    def _on_release_chart(self, e):
        self.is_click_chart = False
        self.figure.canvas.set_cursor(cursors.POINTER)
        return

    def _set_cursor(self, e):
        if self.is_click_chart:
            return
        return super()._set_cursor(e)

    def _on_move_action(self, e):
        super()._on_move_action(e)

        if self.in_slider:
            self._restore_region(self.is_click_slider)
            self._on_move_slider(e)
            self.figure.canvas.blit()
        elif self.in_price_chart or self.in_volume_chart:
            self._restore_region(self.is_click_chart)
            if not self.is_click_chart:
                self._draw_crossline(e)
            else:
                self._move_chart(e)
            self.figure.canvas.blit()
        else:
            if self._erase_crossline():
                self._restore_region()
                self.figure.canvas.blit()
        return

    def _move_chart(self, e: MouseEvent):
        left, right = self.navcoordinate
        x = e.xdata.__int__() - left
        xsub = x - self.x_click
        if not xsub:
            self.collection_navigator.draw(self.figure.canvas.renderer)
            self.draw_artists()
        else:
            left, right = (left-xsub, right-xsub)
            if right < 0 or self.df.index[-1] < left:
                self._restore_region()
            else:
                self.x_click = x
                self.navcoordinate = (left, right)
                self.axis(left, xmax=right+1, simpler=True, draw_ma=(right-left < self.limit_ma))
                self._axis_navigator(left, right)
                self.collection_navigator.draw(self.figure.canvas.renderer)

                self.draw_artists()
                self.background_with_nav = self.figure.canvas.renderer.copy_from_bbox(self.figure.bbox)
                self._restore_region()
        return


class BaseMixin(ChartClickMixin):
    pass


class Chart(BaseMixin):
    pass

