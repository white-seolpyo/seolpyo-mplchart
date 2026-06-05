from .create import CreateMixin
from .update import UpdateMixin


class CanvasMixin(CreateMixin, UpdateMixin):
    slider_top = True
    show_slider = True

    def __init__(self):
        self.create_figure()

        manager = self.figure.canvas.manager
        backend_window = manager.window
        # print(f'{backend_window=}')
        if hasattr(backend_window, 'setMinimumSize'):
            backend_window.setMinimumSize(800, 500)
        elif hasattr(backend_window, 'minsize'):
            backend_window.minsize(800, 500)

        super().__init__()

        return

