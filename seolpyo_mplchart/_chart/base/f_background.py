from .a_canvas import Figure


class Base:
    _background = None
    _background_background = None

    _creating_background = False

    figure: Figure

    draw_chart: callable
    draw_artists: callable
    draw_background: callable

    def _draw_canvas(self):
        self._background = None
        self._restore_region()
        return

    def _restore_region(self):
        # print(f'{self._background=}')
        if not self._background:
            self._create_background()

        self.figure.canvas.renderer.restore_region(self._background)
        return

    def _restore_region_background(self):
        if not self._background:
            self._create_background()

        self.figure.canvas.renderer.restore_region(self._background_background)
        return

    def _create_background(self):
        if self._creating_background:
            return

        self._creating_background = True
        self._copy_bbox()
        self._creating_background = False
        return

    def _copy_bbox(self):
        renderer = self.figure.canvas.renderer

        self.draw_background()
        self._background_background = renderer.copy_from_bbox(self.figure.bbox)

        self.draw_chart()
        self.draw_artists()
        self._background = renderer.copy_from_bbox(self.figure.bbox)

        return


class BackgroundMixin(Base):
    _background = None
    _background_background = None
    _creating_background = False

