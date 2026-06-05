from matplotlib.axes import Axes
from matplotlib.backend_bases import MouseEvent
from matplotlib.text import Text
import pandas as pd

from ....models import Figure
from ....utils.formatter import Formatter, FormatterEN


class LabelMixin:
    figure: Figure

    df: pd.DataFrame

    FORMATTER: Formatter

    in_chart: bool

    artist_label_chart_x: Text
    artist_label_chart_y: Text
    artist_label_slider: Text

    slider_top: bool
    show_slider: bool

    in_chart_price: bool
    in_chart_volume: bool

    digit_price = 0
    digit_volume = 0

    def draw_label(self, e: MouseEvent):
        if self.in_chart:
            self.draw_chart_label_x(e)
            self.draw_chart_label_y(e)

        if self.show_slider and self.in_slider:
            self.draw_slider_label(e)

        return 1

    def draw_chart_label_x(self, e: MouseEvent):
        xdata = e.xdata
        if xdata is None or xdata < 0:
            return

        idx = int(xdata)
        if idx < 0:
            return

        try:
            text = self.df.iloc[idx]['date']
        except IndexError:
            return

        renderer = self.renderer
        artist = self.artist_label_chart_x

        artist.set_text(text)

        display_coords = e.inaxes.transData.transform((xdata, e.ydata))
        figure_coords = self.figure.transFigure.inverted()\
            .transform(display_coords)
        # print(f'{figure_coords=}')

        artist.set_position([-0.5, 0.5])
        # bbox 크기를 가져와야하기 때문에 draw
        artist.draw(renderer)

        artist.set_x(figure_coords[0])
        y = self.set_chart_label_x_position(artist)
        artist.set_y(y)

        # print(f'{self.artist_label_x.get_position()=}')
        artist.draw(renderer)

        return 1

    def set_chart_label_x_position(self, artist: Text):
        ax: Axes = self.get_ax_volume()

        renderer = self.renderer

        # Axes 하단 경계 좌표
        boundary = ax.get_position()\
            .y0
        # print(f'{boundary=}')

        # print(f'{artist=}')
        # print(f'{artist.get_bbox_patch()=}')
        # Text bbox 너비
        bbox = artist.get_bbox_patch()\
            .get_window_extent(renderer)
        bbox_size = bbox.height
        # 밀어야 하는 값
        fig_size = self.figure.bbox.height
        offset = (bbox_size + 10) / fig_size
        # print(f'{bbox_size=}')
        # print(f'{fig_size=}')
        # print(f'{offset=}')

        # x축 값(가격 또는 거래량)
        # self.artist_label_y.set_x(x1)
        y = boundary - (offset / 2)
        # print(f'{(x1, x)=}')
        # artist.set_y(y)
        return y

    def draw_chart_label_y(self, e: MouseEvent):
        xdata, ydata = (e.xdata, e.ydata)
        artist = self.artist_label_chart_y
        renderer = self.renderer

        if self.in_chart_price:
            # text = self.CONFIG.FORMAT.yFormatter(ydata, word=self.CONFIG.UNIT.price)
            text = self.price_formatter(round(ydata, self.digit_price), None)
        elif self.in_chart_volume:
            # text = self.CONFIG.FORMAT.yFormatter(ydata, word=self.CONFIG.UNIT.volume)
            text = self.volume_formatter(round(ydata, self.digit_volume), None)
        # print(f'{text=}')
        artist.set_text(text)
        artist.set_position([-0.5, -0.5])
        # bbox 크기를 가져와야하기 때문에 draw
        artist.draw(renderer)

        display_coords = e.inaxes.transData.transform((xdata, ydata))
        figure_coords = self.figure.transFigure.inverted()\
            .transform(display_coords)

        artist.set_y(figure_coords[1])
        self.set_chart_label_y_position(artist)

        artist.draw(renderer)

        return 1

    def set_chart_label_y_position(self, artist: Text):
        renderer = self.figure.canvas.renderer

        # Axes 우측 경계 좌표
        ax: Axes = self.get_ax_volume()
        boundary = ax.get_position()\
            .x1
        # print(f'{boundary=}')

        # Text bbox 너비
        bbox = artist.get_bbox_patch()\
            .get_window_extent(renderer)
        bbox_size = bbox.width
        # 밀어야 하는 값
        fig_size = self.figure.bbox.width
        offset = (bbox_size + 8) / fig_size
        # print(f'{fig_size=}')

        # x축 값(가격 또는 거래량)
        # artist.set_x(x1)
        x = boundary + (offset / 2)
        # print(f'{(x1, x)=}')
        artist.set_x(x)

        return

    def draw_slider_label(self, e: MouseEvent):
        xdata = e.xdata
        if xdata is None:
            return

        idx = round(xdata)
        if idx < 0:
            return

        try:
            text = self.df.iloc[idx]['date']
        except IndexError:
            return

        if self.slider_top:
            self.set_slider_label_top()
        else:
            self.set_slider_label_bottom()

        label_slider = self.artist_label_slider
        label_slider.set_text(text)
        label_slider.set_x(round(xdata, 2))

        label_slider.draw(self.renderer)

        return 1

