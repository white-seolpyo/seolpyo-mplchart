from matplotlib.collections import LineCollection
from matplotlib.backend_bases import MouseEvent, MouseButton, cursors
import pandas as pd


from .cursor import CursorMixin, Chart as CM


def get_wickline(x: pd.Series):
    v = x.values
    return ((v[0], v[1]), (v[0], v[2]))
def get_volumeline(x: pd.Series):
    v = x.values
    return ((v[0], 0), (v[0], v[1]))


class Mixin(CursorMixin):
    def on_click(self, e):
        "This function works if mouse button click event active."
        return
    def on_release(self, e):
        "This function works if mouse button release event active."
        return

class NavgatorMixin(Mixin):
    min_distance = 30
    color_navigatorline = '#1e78ff'
    color_navigator = 'k'

    _x_click, _x_release = (0, 0)
    is_click, is_move = (False, False)
    _navcoordinate = (0, 0)

    def _add_collection(self):
        super()._add_collection()

        # 슬라이더 네비게이터
        self.navigator = LineCollection([], animated=True, edgecolors=[self.color_navigator, self.color_navigatorline], alpha=(0.2, 1.0))
        self.ax_slider.add_artist(self.navigator)
        return

    def set_data(self, df):
        super().set_data(df)

        # 네비게이터 라인 선택 영역
        xsub = self.xmax - self.xmin
        self._navLineWidth = xsub * 0.008
        if self._navLineWidth < 1: self._navLineWidth = 1
        self._navLineWidth_half = self._navLineWidth / 2
        return

    def _connect_event(self):
        super()._connect_event()
        self.canvas.mpl_connect('axes_leave_event', lambda x: self._leave_axes(x))
        self.canvas.mpl_connect('button_press_event', lambda x: self._on_click(x))
        self.canvas.mpl_connect('button_release_event', lambda x: self._on_release(x))
        return

    def _leave_axes(self, e: MouseEvent):
        if not self.is_click and e.inaxes is self.ax_slider:
            self.canvas.set_cursor(cursors.POINTER)
        return

    def _on_click(self, e: MouseEvent):
        if self.is_click or e.button != MouseButton.LEFT or e.inaxes is not self.ax_slider: return

        self.is_click = True

        x = e.xdata.__int__()
        left, right = self._navcoordinate
        lmin, lmax = (left-self._navLineWidth, left+self._navLineWidth_half)
        rmin, rmax = (right-self._navLineWidth_half, right+self._navLineWidth)

        gtl, ltr = (lmax < x, x < rmin)
        if gtl and ltr:
            self._x_click = x
            self.is_move = True
            self.canvas.set_cursor(cursors.MOVE)
        else:
            self.canvas.set_cursor(cursors.RESIZE_HORIZONTAL)
            if not gtl and lmin <= x:
                self._x_click = right
            elif not ltr and x <= rmax:
                self._x_click = left
            else:
                self._x_click = x

        # 그리기 후 최초 클릭이면 좌표 수정
        if left == right:
            self._navcoordinate = (x, x)
        return

    def _on_release(self, e: MouseEvent):
        if e.inaxes is not self.ax_slider: return
        self.is_click, self.is_move = (False, False)

        if self._navcoordinate[0] == self._navcoordinate[1]:
            self._navcoordinate = (self._navcoordinate[0], self._navcoordinate[1]+self.min_distance)

        self.background = None
        self._draw()
        return


class BackgroundMixin(NavgatorMixin):
    def _on_draw(self, e):
        self.background = None
        self._restore_region()
        return

    def _restore_region(self, with_nav=True):
        if not self.background: self._create_background()

        if with_nav: self.canvas.restore_region(self.background_with_nav)
        else: self.canvas.renderer.restore_region(self.background)
        return

    def _copy_bbox(self):
        self.ax_slider.xaxis.draw(self.canvas.renderer)
        self.ax_slider.yaxis.draw(self.canvas.renderer)
        self.slidercollection.draw(self.canvas.renderer)

        super()._copy_bbox()

        self.navigator.draw(self.canvas.renderer)
        self.background_with_nav = self.canvas.renderer.copy_from_bbox(self.fig.bbox)
        return

    def _draw_artist(self):
        renderer = self.canvas.renderer

        self.ax_price.xaxis.draw(renderer)
        self.ax_price.yaxis.draw(renderer)

        if self.candle_on_ma:
            self.macollection.draw(renderer)
            self.candlecollection.draw(renderer)
        else:
            self.candlecollection.draw(renderer)
            self.macollection.draw(renderer)

        self.ax_volume.xaxis.draw(renderer)
        self.ax_volume.yaxis.draw(renderer)

        self.volumecollection.draw(renderer)
        return


class DrawMixin(BackgroundMixin):
    def set_data(self, df):
        super().set_data(df)

        # 네비게이터 높이 설정
        if 0 < self._slider_ymin: ysub = self._slider_ymax
        else: ysub = self._slider_ymax - self._slider_ymin
        self._ymiddle = ysub / 2
        self.navigator.set_linewidth((ysub, 5))
        return

    def _on_release(self, e: MouseEvent):
        if e.inaxes is not self.ax_slider: return
        self.is_click, self.is_move = (False, False)

        if self._navcoordinate[0] == self._navcoordinate[1]:
            self._navcoordinate = (self._navcoordinate[0], self._navcoordinate[1]+self.min_distance)
        self._set_navigator(*self._navcoordinate)

        self.background = None
        self._draw()
        return

    def _on_move(self, e: MouseEvent):
        self._restore_region((not self.is_click))

        self._on_move_action(e)

        if self.in_slider:
            self._change_coordinate()
            if self.is_click:
                if self.is_move: self._set_navigator(*self._navcoordinate)
                elif self.intx is not None: self._set_navigator(self._x_click, self.intx)
                self.navigator.draw(self.canvas.renderer)
            self._slider_move_action(e)
        elif self.is_click:
            self.navigator.draw(self.canvas.renderer)
        else:
            if self.in_slider or self.in_price or self.in_volume:
                self._slider_move_action(e)
            if self.in_price or self.in_volume:
                self._chart_move_action(e)

        self._blit()
        return

    def _change_coordinate(self):
        if self.intx is None: return
        x = self.intx
        left, right = self._navcoordinate

        if not self.is_click:
            lmin, lmax = (left-self._navLineWidth, left+self._navLineWidth_half)
            rmin, rmax = (right-self._navLineWidth_half, right+self._navLineWidth)
            ltel, gter = (x <= lmax, rmin <= x)
            if ltel and lmin <= x:
                self.canvas.set_cursor(cursors.RESIZE_HORIZONTAL)
            elif gter and x <= rmax:
                self.canvas.set_cursor(cursors.RESIZE_HORIZONTAL)
            elif not ltel and not gter: self.canvas.set_cursor(cursors.MOVE)
            else: self.canvas.set_cursor(cursors.POINTER)
        else:
            # 네비게이터 좌표 수정
            intx = x.__int__()
            if self.is_move:
                xsub = self._x_click - intx
                left, right = (left-xsub, right-xsub)
                self._x_click = intx
            else:
                if intx == left: left = intx
                elif intx == right: right = intx
                else:
                    if self._x_click < intx: left, right = (self._x_click, intx)
                    else: left, right = (intx, self._x_click)

            nsub = right - left
            if right < 0 or self.df.index[-1] < left or nsub < self.min_distance: left, right = self._navcoordinate
            self._navcoordinate = (left, right)
        return

    def _set_navigator(self, x1, x2):
        xmin, xmax = (x1, x2) if x1 < x2 else (x2, x1)

        left = ((self.xmin, self._ymiddle), (xmin, self._ymiddle))
        right = ((xmax, self._ymiddle), (self.xmax, self._ymiddle))
        leftline = ((xmin, self._slider_ymin), (xmin, self._slider_ymax))
        rightline = ((xmax, self._slider_ymin), (xmax, self._slider_ymax))
        self.navigator.set_segments((left, leftline, right, rightline))
        return


class LimMixin(DrawMixin):
    def _restore_region(self, with_nav=True, empty=False):
        if not self.background: self._create_background()

        if empty: self.canvas.restore_region(self.background_empty)
        elif with_nav: self.canvas.restore_region(self.background_with_nav)
        else: self.canvas.renderer.restore_region(self.background)
        return

    def _copy_bbox(self):
        self.ax_slider.xaxis.draw(self.canvas.renderer)
        self.ax_slider.yaxis.draw(self.canvas.renderer)
        self.slidercollection.draw(self.canvas.renderer)
        self.background_empty = self.canvas.renderer.copy_from_bbox(self.fig.bbox)

        self._draw_artist()
        self.background = self.canvas.renderer.copy_from_bbox(self.fig.bbox)

        self.navigator.draw(self.canvas.renderer)
        self.background_with_nav = self.canvas.renderer.copy_from_bbox(self.fig.bbox)
        return

    def _on_release(self, e: MouseEvent):
        if e.inaxes is not self.ax_slider: return
        self.is_click, self.is_move = (False, False)

        if self._navcoordinate[0] == self._navcoordinate[1]:
            self._navcoordinate = (self._navcoordinate[0], self._navcoordinate[1]+self.min_distance)
        self._set_navigator(*self._navcoordinate)
        self._lim()

        self.background = None
        self._draw()
        return

    def _on_move(self, e):
        self._restore_region(with_nav=(not self.is_click), empty=self.is_click)

        self._on_move_action(e)

        if self.in_slider:
            self._change_coordinate()
            if self.is_click:
                nsub = self._navcoordinate[1] - self._navcoordinate[0]
                if self.min_distance <= nsub: self._lim()
                if self.is_move: self._set_navigator(*self._navcoordinate)
                elif self.intx is not None: self._set_navigator(self._x_click, self.intx)
                self.navigator.draw(self.canvas.renderer)
                self._draw_blit_artist()
            self._slider_move_action(e)
        elif self.is_click:
            self.navigator.draw(self.canvas.renderer)
            self._draw_blit_artist()
        else:
            if self.in_slider or self.in_price or self.in_volume:
                self._slider_move_action(e)
            if self.in_price or self.in_volume:
                self._chart_move_action(e)

        self._blit()
        return

    def _draw_blit_artist(self):
        return self._draw_artist()

    def _lim(self):
        xmin, xmax = self._navcoordinate

        xmax += 1
        self.ax_price.set_xlim(xmin, xmax)
        self.ax_volume.set_xlim(xmin, xmax)

        indmin, indmax = (xmin, xmax)
        if xmin < 0: indmin = 0
        if indmax < 1: indmax = 1
        if indmin == indmax: indmax += 1
        ymin, ymax = (self.df[self.low][indmin:indmax].min(), self.df[self.high][indmin:indmax].max())
        ysub = (ymax - ymin) / 15
        pmin, pmax = (ymin-ysub, ymax+ysub)
        self.ax_price.set_ylim(pmin, pmax)
    
        ymax = self.df[self.volume][indmin:indmax].max()
        # self._vol_ymax = ymax*1.2
        volmax = ymax * 1.2
        self.ax_volume.set_ylim(0, volmax)

        self.set_text_coordante(xmin, xmax, pmin, pmax, volmax)
        return


class SimpleMixin(LimMixin):
    simpler = False
    limit_volume = 2_000

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # 영역 이동시 주가 collection
        self.blitcandle = LineCollection([], animated=True)
        self.ax_price.add_collection(self.blitcandle)
        self.priceline = LineCollection([], animated=True, edgecolors='k')
        self.ax_price.add_artist(self.priceline)

        # 영역 이동시 거래량 collection
        self.blitvolume = LineCollection([], animated=True, edgecolors=self.colors_volume)
        self.ax_volume.add_collection(self.blitvolume)
        return

    def set_data(self, df):
        super().set_data(df)

        seg = self.df[['x', self.high, self.low]].agg(get_wickline, axis=1)
        self.blitcandle.set_segments(seg)
        self.blitcandle.set_edgecolor(self.df['edgecolor'])
        self.priceline.set_verts([self.df[['x', self.close]].apply(tuple, axis=1).tolist()])

        volmax = self.df[self.volume].max()
        l = self.df.__len__()
        if l < self.limit_volume:
            volseg = self.df.loc[:, ['x', self.volume]].agg(get_volumeline, axis=1)
        else:
            n, step = (1, 1 / self.limit_volume)
            for _ in range(self.limit_volume):
                n -= step
                volmin = volmax * n
                length = self.df.loc[volmin < self.df[self.volume]].__len__()
                if self.limit_volume < length: break
            
            volseg = self.df.loc[volmin < self.df[self.volume], ['x', self.volume]].agg(get_volumeline, axis=1)
        self.blitvolume.set_segments(volseg)

        index = self.df.index[-1]
        if index < 120: self._navcoordinate = (int(self.xmin)-1, int(self.xmax)+1)
        else: self._navcoordinate = (index-80, index+10)
        self._set_navigator(*self._navcoordinate)
        self._lim()
        return self._draw()

    def _draw_blit_artist(self):
        renderer = self.canvas.renderer

        self.ax_price.xaxis.draw(renderer)
        self.ax_price.yaxis.draw(renderer)

        if self.simpler: self.blitcandle.draw(renderer)
        elif self.candle_on_ma:
            self.macollection.draw(renderer)
            self.candlecollection.draw(renderer)
        else:
            self.candlecollection.draw(renderer)
            self.macollection.draw(renderer)

        self.ax_volume.xaxis.draw(renderer)
        self.ax_volume.yaxis.draw(renderer)

        self.blitvolume.draw(renderer)
        return


class ClickMixin(SimpleMixin):
    is_click_chart = False

    def _on_click(self, e: MouseEvent):
        if not self.is_click and e.button == MouseButton.LEFT:
            if e.inaxes is self.ax_slider: pass
            elif e.inaxes is self.ax_price or e.inaxes is self.ax_volume: return self._on_chart_click(e)
            else: return
        else: return

        self.is_click = True

        x = e.xdata.__int__()
        left, right = self._navcoordinate
        lmin, lmax = (left-self._navLineWidth, left+self._navLineWidth_half)
        rmin, rmax = (right-self._navLineWidth_half, right+self._navLineWidth)

        gtl, ltr = (lmax < x, x < rmin)
        if gtl and ltr:
            self._x_click = x
            self.is_move = True
            self.canvas.set_cursor(cursors.MOVE)
        else:
            self.canvas.set_cursor(cursors.RESIZE_HORIZONTAL)
            if not gtl and lmin <= x:
                self._x_click = right
            elif not ltr and x <= rmax:
                self._x_click = left
            else:
                self._x_click = x

        # 그리기 후 최초 클릭이면 좌표 수정
        if left == right:
            self._navcoordinate = (x, x)
        return

    def _on_release(self, e: MouseEvent):
        if not self.is_click: return
        elif e.inaxes is self.ax_slider: return super()._on_release(e)
        elif not self.in_price and not self.in_volume and not self.is_click_chart: return
        self.canvas.set_cursor(cursors.POINTER)
        self.is_click, self.is_move = (False, False)
        self.is_click_chart = False

        self._draw()
        return self._restore_region()

    def _on_chart_click(self, e: MouseEvent):
        self.is_click = True
        self.is_click_chart = True
        self._x_click = e.x.__int__()
        self.canvas.set_cursor(cursors.RESIZE_HORIZONTAL)
        return

    def _change_coordinate(self):
        if self.is_click_chart: self._change_coordinate_chart()
        else: super()._change_coordinate()
        return

    def _change_coordinate_chart(self, e: MouseEvent):
        x = e.x.__int__()
        left, right = self._navcoordinate
        nsub = right - left
        xsub = x - self._x_click
        xdiv = (xsub / (1200 / nsub)).__int__()
        if xdiv:
            left, right = (left-xdiv, right-xdiv)
            if -1 < right and left < self.df.index[-1]:
                self._navcoordinate = (left, right)
            self._x_click = x
        return

    def _on_move(self, e):
        self._restore_region(with_nav=(not self.is_click), empty=self.is_click)

        self._on_move_action(e)

        if self.in_slider and not self.is_click_chart:
            self._change_coordinate()
            if self.is_click:
                nsub = self._navcoordinate[1] - self._navcoordinate[0]
                if self.min_distance <= nsub: self._lim()
                if self.is_move: self._set_navigator(*self._navcoordinate)
                elif self.intx is not None: self._set_navigator(self._x_click, self.intx)
                self.navigator.draw(self.canvas.renderer)
                self._draw_blit_artist()
            self._slider_move_action(e)
        elif self.is_click:
            if self.is_click_chart and (self.in_price or self.in_volume):
                if (self.vmin, self.vmax) != self._navcoordinate:
                    self._change_coordinate_chart(e)
                    self._lim()
                    self._set_navigator(*self._navcoordinate)
            self.navigator.draw(self.canvas.renderer)
            self._draw_blit_artist()
        else:
            if self.in_slider or self.in_price or self.in_volume:
                self._slider_move_action(e)
            if self.in_price or self.in_volume:
                self._chart_move_action(e)

        self._blit()
        return


class SliderMixin(ClickMixin):
    pass


class Chart(SliderMixin, CM, Mixin):
    r"""
    You can see the guidance document:
        Korean: https://white.seolpyo.com/entry/147/
        English: https://white.seolpyo.com/entry/148/

    Variables:
        unit_price, unit_volume: unit for price and volume. default ('원', '주').

        figsize: figure size if you use plt.show(). default (12, 6).
        ratio_ax_slider, ratio_ax_legend, ratio_ax_price, ratio_ax_volume: Axes ratio. default (3, 2, 18, 5).
        adjust: figure adjust. default dict(top=0.95, bottom=0.05, left=0.01, right=0.93, wspace=0, hspace=0).
        slider_top: ax_slider is located at the top or bottom. default True.
        color_background: color of background. default '#fafafa'.
        color_grid: color of grid. default '#d0d0d0'.

        df: stock data.
        date: date column key. default 'date'
        Open, high, low, close: price column key. default ('open', 'high', 'low', 'close')
        volume: volume column key. default 'volume'

        label_ma: moving average legend label format. default '{}일선'
        list_ma: Decide how many days to draw the moving average line. default (5, 20, 60, 120, 240)
        list_macolor: Color the moving average line. If the number of colors is greater than the moving average line, black is applied. default ('darkred', 'fuchsia', 'olive', 'orange', 'navy', 'darkmagenta', 'limegreen', 'darkcyan',)

        candle_on_ma: Decide whether to draw candles on the moving average line. default True
        color_sliderline: Color of closing price line in ax_slider. default 'k'
        color_navigatorline: Color of left and right dividing lines in selected area. default '#1e78ff'
        color_navigator: Color of unselected area. default 'k'

        color_up: The color of the candle. When the closing price is greater than the opening price. default '#fe3032'
        color_down: The color of the candle. When the opening price is greater than the opening price. default '#0095ff'
        color_flat: The color of the candle. WWhen the closing price is the same as the opening price. default 'k'
        color_up_down: The color of the candle. If the closing price is greater than the opening price, but is lower than the previous day's closing price. default 'w'
        color_down_up: The color of the candle. If the opening price is greater than the closing price, but is higher than the closing price of the previous day. default 'w'
        colors_volume: The color of the volume bar. default '#1f77b4'

        lineKwargs: Options applied to horizontal and vertical lines drawn along the mouse position. default dict(edgecolor='k', linewidth=1, linestyle='-')
        textboxKwargs: Options that apply to the information text box. dufault dict(boxstyle='round', facecolor='w')

        fraction: Decide whether to express information as a fraction. default False
        candleformat: Candle information text format. default '{}\n\n종가:　 {}\n등락률: {}\n대비:　 {}\n시가:　 {}({})\n고가:　 {}({})\n저가:　 {}({})\n거래량: {}({})'
        volumeformat: Volume information text format. default '{}\n\n거래량　　　: {}\n거래량증가율: {}'
        digit_price, digit_volume: Number of decimal places expressed in informational text. default (0, 0)

        min_distance: Minimum number of candles that can be selected with the slider. default 30
        simpler: Decide whether to display candles simply when moving the chart. default False
        limit_volume: Maximum number of volume bars drawn when moving the chart. default 2_000
    """
    def _generate_data(self, df):
        super()._generate_data(df)
        return self.generate_data(self.df)

    def _on_draw(self, e):
        super()._on_draw(e)
        return self.on_draw(e)

    def _on_pick(self, e):
        self.on_pick(e)
        return super()._on_pick(e)

    def _draw_artist(self):
        super()._draw_artist()
        return self.create_background()

    def _blit(self):
        super()._blit()
        return self.on_blit()

    def _on_move(self, e):
        super()._on_move(e)
        return self.on_move(e)


if __name__ == '__main__':
    import json
    from time import time

    import matplotlib.pyplot as plt
    from pathlib import Path

    file = Path(__file__).parent / 'data/samsung.txt'
    # file = Path(__file__).parent / 'data/apple.txt'
    with open(file, 'r', encoding='utf-8') as txt:
        data = json.load(txt)
    data = data
    df = pd.DataFrame(data)

    t = time()
    c = SliderMixin()
    c.set_data(df)
    t2 = time() - t
    print(f'{t2=}')
    plt.show()
