from .draw import DrawMixin
from .resize import ResizeMixin
from .pick import PickMixin
from .mouse import MouseMixin, format_info_price, format_info_volume, format_info_price_en, format_info_volume_en


class EventMixn(DrawMixin, ResizeMixin, PickMixin, MouseMixin):
    def __init__(self):
        super().__init__()

        self.connect_events()

        return

    def connect_events(self):
        # print(f'{self.figure=}')
        # canvas = getattr(self.figure, 'canvas', None)
        # print(f'{canvas=}')
        self.figure.canvas.mpl_connect('draw_event', lambda x: self._on_draw(x))
        self.figure.canvas.mpl_connect('resize_event', lambda x: self._on_resize(x))
        self.figure.canvas.mpl_connect('pick_event', lambda x: self._on_pick(x))

        self.figure.canvas.mpl_connect('motion_notify_event', lambda x: self._on_move(x))

        self.figure.canvas.mpl_connect('button_press_event', lambda x: self._on_click(x))
        self.figure.canvas.mpl_connect('button_release_event', lambda x: self._on_release(x))
        return

