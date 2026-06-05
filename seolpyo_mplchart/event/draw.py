from matplotlib.backend_bases import DrawEvent


class DrawMixin:
    acting_draw = False

    def on_draw(self, e: DrawEvent):
        self.background = None
        self.restore_background()
        return

    def _on_draw(self, e: DrawEvent):
        if not self.acting_draw:
            self.acting_draw = True
            self.on_draw(e)
            self.acting_draw = False
        return

