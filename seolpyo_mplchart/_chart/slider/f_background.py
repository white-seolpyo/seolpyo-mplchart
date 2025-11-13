from matplotlib.axes import Axes


class Base:
    _background = None
    _background_background = None

    _creating_background = False

    draw_background: callable
    _draw_ax: callable
    _draw_ax_slider: callable
    draw_artists: callable
    _draw_nav: callable


class SliderMixin(Base):
    ax_slider: Axes

    def draw_background(self):
        self._draw_ax(self.ax_slider)
        self._draw_ax_slider()

        super().draw_background()
        return

    def draw_artists(self):
        super().draw_artists()

        self._draw_nav()
        return


class BackgroundMixin(SliderMixin):
    _background = None
    _creating_background = False

