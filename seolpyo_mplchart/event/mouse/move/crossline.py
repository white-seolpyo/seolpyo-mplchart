from matplotlib.axes import Axes
from matplotlib.backend_bases import MouseEvent
from matplotlib.collections import LineCollection


class CrosslineMixin:
    in_chart_price: bool
    in_chart_volume: bool
    in_chart: bool

    collection_crossline_price: LineCollection
    collection_crossline_volume: LineCollection
    collection_slider_vline: LineCollection

    slider_top: bool
    show_slider: bool

    def draw_crossline(self, e: MouseEvent):
        self.draw_chart_crossline(e)

        if self.show_slider:
            self.draw_slider_vline(e)

        return 1

    def draw_chart_crossline(self, e: MouseEvent):
        xdata, ydata = (e.xdata, e.ydata)

        renderer = self.renderer

        ax_price: Axes = self.get_ax_price()
        ax_volume: Axes = self.get_ax_volume()
        # print(f'{ax_price=}')
        # print(f'{ax_volume=}')

        price_y0, price_y1 = ax_price.get_ylim()
        volume_y0, volume_y1 = ax_volume.get_ylim()

        price_seg = []
        volume_seg = []
        if self.in_chart:
            x0, x1 = ax_price.get_xlim()
            if self.in_chart_price:
                price_seg = [
                    [[x0, ydata], [x1, ydata]],
                    [[xdata, price_y0], [xdata, price_y1]]
                ]
                volume_seg = [
                    [[xdata, volume_y0], [xdata, volume_y1]]
                ]
            elif self.in_chart_volume:
                price_seg = [
                    [[xdata, price_y0], [xdata, price_y1]]
                ]
                volume_seg = [
                    [[x0, ydata], [x1, ydata]],
                    [[xdata, volume_y0], [xdata, volume_y1]]
                ]
        else:
            price_seg = [
                [[xdata, price_y0], [xdata, price_y1]]
            ]
            volume_seg = [
                [[xdata, volume_y0], [xdata, volume_y1]]
            ]

        # print(f'{price_seg=}')
        # print(f'{volume_seg=}')

        self.collection_crossline_price.set_segments(price_seg)
        self.collection_crossline_volume.set_segments(volume_seg)

        self.collection_crossline_price.draw(renderer)
        self.collection_crossline_volume.draw(renderer)

        return 1

    def draw_slider_vline(self, e: MouseEvent):
        xdata = e.xdata

        renderer = self.renderer
    
        ax_slider: Axes = self.get_ax_slider()
        collection_slider_vline = self.collection_slider_vline

        slider_y0, slider_y1 = ax_slider.get_ylim()

        seg = [((xdata, slider_y0), (xdata, slider_y1))]
        # print(f'{seg=}')
        collection_slider_vline.set_segments(seg)

        collection_slider_vline.draw(renderer)

        return 1

