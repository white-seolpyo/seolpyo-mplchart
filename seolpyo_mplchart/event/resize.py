from matplotlib.backend_bases import ResizeEvent


class ResizeMixin:
    acting_resize = False

    def on_resize(self, e: ResizeEvent):
        self.set_figure_ratios()
        return

    def _on_resize(self, e: ResizeEvent):
        if not self.acting_resize:
            self.acting_resize = True
            self.on_resize(e)
            self.acting_resize = False
        return

