from ._lim import BaseMixin as Base


class DrawMixin(Base):
    candle_on_ma = True

    def _connect_events(self):
        super()._connect_events()
        self.figure.canvas.mpl_connect('draw_event', lambda x: self.on_draw(x))
        return

    def on_draw(self, e):
        self._on_draw(e)
        return

    def _on_draw(self, e):
        self.draw_artists()
        self.figure.canvas.blit()
        return

    def draw_artists(self):
        self._draw_artists()
        return

    def _draw_artists(self):
        self._draw_ax_price()
        self._draw_ax_volume()
        return

    def _draw_ax_price(self):
        renderer = self.figure.canvas.renderer
        # print(f'{renderer=}')

        self.ax_price.xaxis.draw(renderer)
        self.ax_price.yaxis.draw(renderer)

        if self.candle_on_ma:
            self.collection_ma.draw(renderer)
            self.collection_candle.draw(renderer)
        else:
            self.collection_candle.draw(renderer)
            self.collection_ma.draw(renderer)

        if self.watermark:
            if self.watermark != self.artist_watermark.get_text():
                self.artist_watermark.set_text(self.watermark)
            self.artist_watermark.draw(renderer)
        return

    def _draw_ax_volume(self):
        renderer = self.figure.canvas.renderer

        self.ax_volume.xaxis.draw(renderer)
        self.ax_volume.yaxis.draw(renderer)

        self.collection_volume.draw(renderer)
        return


class BackgroundMixin(DrawMixin):
    background = None

    _creating_background = False

    def _create_background(self):
        if self._creating_background:
            return

        self._creating_background = True
        self._copy_bbox()
        self._creating_background = False
        return

    def _copy_bbox(self):
        self.draw_artists()

        renderer = self.figure.canvas.renderer
        self.background = renderer.copy_from_bbox(self.figure.bbox)
        return

    def _on_draw(self, e):
        self.background = None
        self._restore_region()
        return

    def _restore_region(self):
        if not self.background:
            self._create_background()

        self.figure.canvas.renderer.restore_region(self.background)
        return


class BaseMixin(BackgroundMixin):
    def _refresh(self):
        self.set_segments()
        self.set_collections(self.vxmin, xmax=self.vxmax)
        return super()._refresh()


class Chart(BaseMixin):
    pass

