from matplotlib.axes import Axes
from matplotlib.backend_bases import MouseEvent
from matplotlib.collections import LineCollection
import pandas as pd


class BoxMixin:
    key_volume: str

    df: pd.DataFrame

    collection_box_price: LineCollection
    collection_box_volume: LineCollection

    in_chart_price: bool
    in_chart_volume: bool

    min_height_box_price: float
    min_height_box_volume: float

    def get_ax_height(self, ax: Axes):
        y0, y1 = ax.get_ylim()
        height = y1 - y0
        return height

    def draw_box_artist(self, e: MouseEvent):
        self.in_box_price, self.in_box_volume = (False, False)
        xdata, ydata = (e.xdata, e.ydata)

        ind = int(xdata)
        # print(f'{ind=}')
        if ind < 0:
            return

        try:
            series = self.df.iloc[ind]
        except IndexError:
            return

        renderer = self.renderer

        if self.in_chart_price:
            # print(f'{series=}')
            # 박스 크기
            high = series['box_candle_top']
            low = series['box_candle_bottom']
            height = series['box_candle_height']
            # print(f'{(low, high)=}')
            # print(f'{height=}')

            # 박스 높이 보정
            ax: Axes = self.get_ax_price()
            ax_height = self.get_ax_height(ax)
            min_box_height = ax_height / 6
            if height < min_box_height:
                sub = (min_box_height - height) / 2
                high, low = (high+sub, low-sub)

            # 커서가 캔들 사이에 있는지 확인
            if low <= ydata and ydata <= high:
                self.in_box_price = True

                # 캔들 강조
                x0, x1 = (ind-0.3, ind+1.3)
                segment = [(
                    (x0, high),
                    (x1, high),
                    (x1, low),
                    (x0, low),
                    (x0, high)
                )]
                self.collection_box_price.set_segments(segment)
                self.collection_box_price.draw(renderer)

                return 1

        elif self.in_chart_volume and self.key_volume:
            # 박스 크기
            high = series['box_volume_top']
            low = 0

            ax: Axes = self.get_ax_volume()
            ax_height = self.get_ax_height(ax)
            min_box_height = ax_height / 4
            if high < min_box_height:
                high = min_box_height

            if low <= ydata and ydata <= high:
                # 거래량 강조
                self.in_box_volume = True

                x0, x1 = (ind-0.3, ind+1.3)
                segment = [(
                    (x0, high),
                    (x1, high),
                    (x1, low),
                    (x0, low),
                    (x0, high)
                )]
                self.collection_box_volume.set_segments(segment)
                self.collection_box_volume.draw(renderer)

                return 1

        return 1

