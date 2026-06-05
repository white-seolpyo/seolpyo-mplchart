from .ma import Mamixin


class LegendMixin(Mamixin):
    def set_legend(self):
        self.set_ma_legend()
        return

