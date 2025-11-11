from matplotlib.axes import Axes
from matplotlib.text import Text

from ..base.a_canvas import Figure


class Base:
    figure: Figure
    ax_price: Axes
    ax_volume: Axes

    key_volume: str

    vxmin: int
    vxmax: int
    price_ymin: int
    price_ymax: int
    volume_ymax: int

    artist_info_candle: Text
    artist_info_volume: Text
    artist_label_x: Text
    artist_label_y: Text

    axis: callable


class Mixin(Base):
    def axis(self, xmin, *, xmax):
        super().axis(xmin, xmax=xmax)
        # print('cursor axis')

        psub = (self.price_ymax - self.price_ymin)
        self.min_height_box_candle = psub / 8

        pydistance = psub / 20

        self.min_height_box_volume = 10
        if self.key_volume:
            self.min_height_box_volume = self.volume_ymax / 4

        vxsub = self.vxmax - self.vxmin
        self.vmiddle = self.vxmax - int((vxsub) / 2)

        vxdistance = vxsub / 50
        self.v0, self.v1 = (self.vxmin + vxdistance, self.vxmax - vxdistance)

        yvolume = self.volume_ymax * 0.85

        # 정보 텍스트박스 y축 설정
        self.artist_info_candle.set_y(self.price_ymax - pydistance)
        self.artist_info_volume.set_y(yvolume)

        return


class AxisMixin(Mixin):
    v0: int
    v1: int
    vmiddle: int

    min_height_box_candle: float
    min_height_box_volume: float

