from matplotlib.backend_bases import MouseEvent

from ._artist import BaseMixin as Base
from ..._config.utils import float_to_str


class EventMixin(Base):
    in_price_chart, in_volume_chart = (False, False)
    intx = None

    def _connect_events(self):
        super()._connect_events()

        self.figure.canvas.mpl_connect('motion_notify_event', lambda x: self.on_move(x))
        return

    def on_move(self, e):
        self._on_move_action(e)
        return

    def _on_move_action(self, e: MouseEvent):
        self._check_ax(e)

        self.intx = None
        if self.in_price_chart or self.in_volume_chart: self._get_x(e)
        return

    def _get_x(self, e: MouseEvent):
        self.intx = e.xdata.__int__()
        if self.intx < 0: self.intx = None
        else:
            try: self.index_list[self.intx]
            except: self.intx = None
        return

    def _check_ax(self, e: MouseEvent):
        ax = e.inaxes
        if not ax or e.xdata is None or e.ydata is None:
            self.in_price_chart, self.in_volume_chart = (False, False)
        else:
            if ax is self.ax_price:
                self.in_price_chart = True
                self.in_volume_chart = False
            elif ax is self.ax_volume:
                self.in_price_chart = False
                self.in_volume_chart = True
            else:
                self.in_price_chart = False
                self.in_volume_chart = False
        return


class CrossLineMixin(EventMixin):
    in_candle, in_volumebar = (False, False)

    def _on_move_action(self, e):
        super()._on_move_action(e)

        if self.in_price_chart or self.in_volume_chart:
            self._restore_region()
            self._draw_crossline(e)
            self.figure.canvas.blit()
        else:
            if self._erase_crossline():
                self._restore_region()
                self.figure.canvas.blit()
        return

    def _erase_crossline(self):
        seg = self.collection_price_crossline.get_segments()
        if seg:
            self.collection_price_crossline.set_segments([])
            return True
        return False

    def _draw_crossline(self, e: MouseEvent):
        x, y = (e.xdata, e.ydata)

        if self.in_price_chart:
            self.collection_price_crossline.set_segments([((x, self.price_ymin), (x, self.price_ymax)), ((self.vxmin, y), (self.vxmax, y))])
            self.collection_volume_crossline.set_segments([((x, 0), (x, self.key_volume_ymax))])
        else:
            self.collection_price_crossline.set_segments([((x, self.price_ymin), (x, self.price_ymax))])
            self.collection_volume_crossline.set_segments([((x, 0), (x, self.key_volume_ymax)), ((self.vxmin, y), (self.vxmax, y))])

        renderer = self.figure.canvas.renderer
        self.collection_price_crossline.draw(renderer)
        self.collection_volume_crossline.draw(renderer)

        self._draw_text_artist(e)
        return

    def _draw_text_artist(self, e: MouseEvent):
        x, y = (e.xdata, e.ydata)

        display_coords = e.inaxes.transData.transform((e.xdata, e.ydata))
        figure_coords = self.figure.transFigure.inverted().transform(display_coords)
        # print(f'{figure_coords=}')

        renderer = self.figure.canvas.renderer
        if self.in_price_chart:
            text = f'{float_to_str(y, digit=self.CONFIG.UNIT.digit)}{self.CONFIG.UNIT.price}'
        else:
            text = f'{float_to_str(y, digit=self.CONFIG.UNIT.digit_volume)}{self.CONFIG.UNIT.volume}'

        # y축 값(가격 또는 거래량)
        self.artist_text_y.set_text(text)
        self.artist_text_y.set_y(figure_coords[1])
        self.artist_text_y.draw(renderer)

        if self.intx is not None:
            # x축 값(날짜)
            self.artist_text_x.set_text(f'{self.df['date'][self.intx]}')
            self.artist_text_x.set_x(figure_coords[0])
            self.artist_text_x.draw(renderer)
        return


class BoxMixin(CrossLineMixin):
    def _draw_crossline(self, e):
        super()._draw_crossline(e)
        self._draw_box_artist(e)
        return

    def _draw_box_artist(self, e: MouseEvent):
        y = e.ydata

        renderer = self.figure.canvas.renderer

        self.in_candle = False
        self.in_volumebar = False
        if self.intx is not None:
            if self.in_price_chart:
                # 박스 크기
                high = self.df['top_box_candle'][self.intx]
                low = self.df['bottom_box_candle'][self.intx]
                height = self.df['height_box_candle'][self.intx]
                if height < self.min_height_box_candle:
                    sub = (self.min_height_box_candle - height) / 2
                    high, low = (high+sub, low-sub)

                # 커서가 캔들 사이에 있는지 확인
                if low <= y and y <= high:
                    # 캔들 강조
                    self.in_candle = True
                    x1, x2 = (self.intx-0.3, self.intx+1.3)
                    self.collection_box_price.set_segments([((x1, high), (x2, high), (x2, low), (x1, low), (x1, high))])
                    self.collection_box_price.draw(renderer)
            elif self.in_volume_chart and self.key_volume:
                # 거래량 강조
                high = self.df['max_box_volume'][self.intx]
                low = 0
                if high < self.min_height_box_volume: high = self.min_height_box_volume

                if low <= y and y <= high:
                    self.in_volumebar = True
                    x1, x2 = (self.intx-0.3, self.intx+1.3)
                    self.collection_box_volume.set_segments([((x1, high), (x2, high), (x2, low), (x1, low), (x1, high))])
                    self.collection_box_volume.draw(renderer)
        return


class BaseMixin(BoxMixin):
    pass

