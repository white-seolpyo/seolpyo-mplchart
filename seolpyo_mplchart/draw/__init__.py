from .background import BackgroundMixin


class DrawMixin(BackgroundMixin):
    def draw(self):
        if self.figure and getattr(self.figure, 'canvas', None):
            self.figure.canvas.draw()
        return

    def blit(self):
        self.figure.canvas.blit()
        self.figure.canvas.flush_events()
        return

