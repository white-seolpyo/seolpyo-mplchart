import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.collections import LineCollection
from matplotlib.text import Text
from matplotlib.backend_bases import MouseEvent, MouseButton, cursors
import pandas as pd

from .base import convert_unit
from .cursor import BaseMixin as BM, Mixin as M


class Mixin(M):
    def on_click(self, e):
        "This function works if mouse button click event active."
        return
    def on_release(self, e):
        "This function works if mouse button release event active."
        return


class PlotMixin(BM):
    slider_top = True
    ratio_ax_slider = 3
    ratio_ax_none = 2

    def _get_plot(self):
        if self.slider_top:
            self.figure, axes = plt.subplots(
                4, # row 수
                figsize=self.figsize, # 기본 크기
                height_ratios=(self.ratio_ax_slider, self.ratio_ax_legend, self.ratio_ax_price, self.ratio_ax_volume) # row 크기 비율
            )
            axes: list[Axes]
            self.ax_slider, self.ax_legend, self.ax_price, self.ax_volume = axes
        else:
            self.figure, axes = plt.subplots(
                5, # row 수
                figsize=self.figsize, # 기본 크기
                height_ratios=(self.ratio_ax_legend, self.ratio_ax_price, self.ratio_ax_volume, self.ratio_ax_none, self.ratio_ax_slider) # row 크기 비율
            )
            axes: list[Axes]
            self.ax_legend, self.ax_price, self.ax_volume, ax_none, self.ax_slider = axes

            ax_none.set_axis_off()
            ax_none.xaxis.set_animated(True)
            ax_none.yaxis.set_animated(True)

        self.ax_slider.set_label('slider ax')
        self.ax_legend.set_label('legend ax')
        self.ax_price.set_label('price ax')
        self.ax_volume.set_label('volume ax')

        self.figure.canvas.manager.set_window_title(f'{self.title}')
        self.figure.set_facecolor(self.color_background)

        # 플롯간 간격 제거(Configure subplots)
        self.figure.subplots_adjust(**self.adjust)

        self.ax_legend.set_axis_off()

        # y ticklabel foramt 설정
        self.ax_slider.yaxis.set_major_formatter(lambda x, _: convert_unit(x, word=self.unit_price, digit=2))
        self.ax_price.yaxis.set_major_formatter(lambda x, _: convert_unit(x, word=self.unit_price, digit=2))
        self.ax_volume.yaxis.set_major_formatter(lambda x, _: convert_unit(x, word=self.unit_volume, digit=2))

        gridKwargs = {'visible': True, 'linewidth': 0.5, 'color': '#d0d0d0', 'linestyle': '-', 'dashes': (1, 0)}
        gridKwargs.update(self.gridKwargs)
        # 공통 설정
        for ax in (self.ax_slider, self.ax_price, self.ax_volume):
            ax.xaxis.set_animated(True)
            ax.yaxis.set_animated(True)

            # x tick 외부 눈금 표시하지 않기
            ax.xaxis.set_ticks_position('none')
            # x tick label 제거
            ax.set_xticklabels([])
            # y tick 우측으로 이동
            ax.tick_params(left=False, right=True, labelleft=False, labelright=True, colors=self.color_tick_label)
            # Axes 외곽선 색 변경
            for i in ['top', 'bottom', 'left', 'right']: ax.spines[i].set_color(self.color_tick)

            # 차트 영역 배경 색상
            ax.set_facecolor(self.color_background)

            # grid(구분선, 격자) 그리기
            # 어째서인지 grid의 zorder 값을 선언해도 1.6을 값으로 한다.
            ax.grid(**gridKwargs)
        return


class CollectionMixin(PlotMixin):
    min_distance = 30
    color_navigator_line = '#1e78ff'
    color_navigator_cover = 'k'

    def _add_collection(self):
        super()._add_collection()

        self.collection_slider = LineCollection([], animated=True)
        self.ax_slider.add_artist(self.collection_slider)

        # 슬라이더 네비게이터
        self.navigator = LineCollection([], animated=True, edgecolors=[self.color_navigator_cover, self.color_navigator_line], alpha=(0.3, 1.0))
        self.ax_slider.add_artist(self.navigator)

        lineKwargs = {'edgecolor': 'k', 'linewidth': 1, 'linestyle': '-'}
        lineKwargs.update(self.lineKwargs)
        lineKwargs.update({'segments': [], 'animated': True})

        self.slider_vline = LineCollection(**lineKwargs)
        self.ax_slider.add_artist(self.slider_vline)

        textboxKwargs = {'boxstyle': 'round', 'facecolor': 'w'}
        textboxKwargs.update(self.textboxKwargs)
        textKwargs = self.textKwargs
        textKwargs.update({'animated': True, 'bbox': textboxKwargs, 'horizontalalignment': '', 'verticalalignment': ''})
        (textKwargs.pop('horizontalalignment'), textKwargs.pop('verticalalignment'))

        self.text_slider = Text(**textKwargs, horizontalalignment='center', verticalalignment='top')
        self.ax_slider.add_artist(self.text_slider)
        return

    def _get_segments(self):
        super()._get_segments()

        keys = []
        for i in reversed(self.list_ma):
            keys.append('_x')
            keys.append(f'ma{i}')

        segment_slider = self.df[keys + ['_x', self.close] ].values
        segment_slider = segment_slider.reshape(segment_slider.shape[0], len(self.list_ma)+1, 2).swapaxes(0, 1)
        self.collection_slider.set_segments(segment_slider)
        return

    def _get_color_segment(self):
        super()._get_color_segment()

        self.collection_slider.set_edgecolor(self.edgecolor_ma + [self.color_priceline])
        return

    def change_background_color(self, color):
        super().change_background_color(color)

        self.ax_slider.set_facecolor(color)
        self.text_slider.set_backgroundcolor(color)
        return

    def change_tick_color(self, color):
        super().change_tick_color(color)

        for i in ['top', 'bottom', 'left', 'right']: self.ax_slider.spines[i].set_color(self.color_tick)
        self.ax_slider.tick_params(colors=color)
        return

    def change_text_color(self, color):
        super().change_text_color(color)

        self.text_slider.set_color(color)
        return

    def change_line_color(self, color):
        super().change_line_color(color)

        self.text_slider.get_bbox_patch().set_edgecolor(color)
        return


class NavigatorMixin(CollectionMixin):
    def _set_slider_lim(self):
        xmax = self.list_index[-1]
        # 슬라이더 xlim
        xdistance = xmax / 30
        self.slider_xmin, self.slider_xmax = (-xdistance, xmax + xdistance)
        self.ax_slider.set_xlim(self.slider_xmin, self.slider_xmax)

        # 슬라이더 ylim
        ymin, ymax = (self.df[self.low].min(), self.df[self.high].max())
        ysub = ymax - ymin
        self.sldier_ymiddle = ymin + (ysub / 2)
        ydistance = ysub / 5
        self.slider_ymin, self.slider_ymax = (ymin-ydistance, ymax+ydistance)
        self.ax_slider.set_ylim(self.slider_ymin, self.slider_ymax)

        # 슬라이더 텍스트 y
        self.text_slider.set_y(ymax)

        self.navigator.set_linewidth([ysub, 5])

        # 네비게이터 라인 선택 범위
        xsub = self.slider_xmax - self.slider_xmin
        self._navLineWidth = xsub * 8 / 1_000
        if self._navLineWidth < 1: self._navLineWidth = 1
        self._navLineWidth_half = self._navLineWidth / 2
        return

    def _set_navigator(self, navmin, navmax):
        navseg = [
            (
                (self.slider_xmin, self.sldier_ymiddle),
                (navmin, self.sldier_ymiddle)
            ),
            (
                (navmin, self.slider_ymin),
                (navmin, self.slider_ymax)
            ),
            (
                (navmax, self.sldier_ymiddle),
                (self.slider_xmax, self.sldier_ymiddle)
            ),
            (
                (navmax, self.slider_ymin),
                (navmax, self.slider_ymax)
            ),
        ]

        self.navigator.set_segments(navseg)
        return


class DataMixin(NavigatorMixin):
    navcoordinate = (0, 0)

    def set_data(self, df, sort_df=True, calc_ma=True, set_candlecolor=True, set_volumecolor=True, calc_info=True, change_lim=True, *args, **kwargs):
        self._generate_data(df, sort_df, calc_ma, set_candlecolor, set_volumecolor, calc_info, *args, **kwargs)
        self._get_segments()

        vmin, vmax = self.navcoordinate
        if change_lim or (vmax-vmin) < self.min_distance:
            vmin, vmax = self.get_default_lim()
            self.navcoordinate = (vmin, vmax)

        self._set_lim(vmin, vmax)
        self._set_slider_lim()
        self._set_navigator(vmin, vmax)

        self._length_text = self.df[(self.volume if self.volume else self.high)].apply(lambda x: len(str(x))).max()
        return

    def get_default_lim(self):
        xmax = self.list_index[-1]
        return (xmax-120, xmax)


class BackgroundMixin(DataMixin):
    def _copy_bbox(self):
        renderer = self.figure.canvas.renderer

        self.ax_slider.xaxis.draw(renderer)
        self.ax_slider.yaxis.draw(renderer)
        self.collection_slider.draw(renderer)
        self.background_emtpy = renderer.copy_from_bbox(self.figure.bbox)

        self._draw_artist()
        self.background = renderer.copy_from_bbox(self.figure.bbox)

        self.navigator.draw(self.figure.canvas.renderer)
        self.background_with_nav = renderer.copy_from_bbox(self.figure.bbox)
        return

    def _restore_region(self, is_empty=False, with_nav=True):
        if not self.background: self._create_background()

        if is_empty: self.figure.canvas.renderer.restore_region(self.background_emtpy)
        elif with_nav: self.figure.canvas.renderer.restore_region(self.background_with_nav)
        else: self.figure.canvas.renderer.restore_region(self.background)
        return


class MouseMoveMixin(BackgroundMixin):
    in_slider = False
    is_click_slider = False

    def _on_move(self, e):
        self._on_move_action(e)

        self._restore_region((self.is_click_slider and self.in_slider))

        if self.in_slider:
            self._on_move_slider(e)
        elif self.in_price_chart:
            self._on_move_price_chart(e)
        elif self.in_volume_chart:
            self._on_move_volume_chart(e)

        self._blit()
        return

    def _on_move_action(self, e: MouseEvent):
        self._check_ax(e)

        self.intx = None
        if self.in_slider or self.in_price_chart or self.in_volume_chart: self._get_x(e)

        self._change_cursor(e)
        return

    def _change_cursor(self, e: MouseEvent):
        # 마우스 커서 변경
        if self.is_click_slider: return
        elif not self.in_slider:
            self.figure.canvas.set_cursor(cursors.POINTER)
            return

        navleft, navright = self.navcoordinate
        if navleft == navright: return

        x = e.xdata
        leftmin, leftmax = (navleft-self._navLineWidth, navleft+self._navLineWidth_half)
        rightmin, rightmax = (navright-self._navLineWidth_half, navright+self._navLineWidth)
        if x < leftmin: self.figure.canvas.set_cursor(cursors.POINTER)
        elif x < leftmax: self.figure.canvas.set_cursor(cursors.RESIZE_HORIZONTAL)
        elif x < rightmin: self.figure.canvas.set_cursor(cursors.MOVE)
        elif x < rightmax: self.figure.canvas.set_cursor(cursors.RESIZE_HORIZONTAL)
        else: self.figure.canvas.set_cursor(cursors.POINTER)
        return

    def _check_ax(self, e: MouseEvent):
        ax = e.inaxes
        if not ax or e.xdata is None or e.ydata is None:
            self.in_slider, self.in_price_chart, self.in_volume_chart = (False, False, False)
        else:
            self.in_slider = ax is self.ax_slider
            self.in_price_chart = False if self.in_slider else ax is self.ax_price
            self.in_volume_chart = False if (self.in_slider or self.in_price_chart) else ax is self.ax_volume
        return

    def _on_move_slider(self, e: MouseEvent):
        x = e.xdata

        if self.intx is not None:
            renderer = self.figure.canvas.renderer
            self.slider_vline.set_segments([((x, self.slider_ymin), (x, self.slider_ymax))])
            self.slider_vline.draw(renderer)

            if self.in_slider:
                self.text_slider.set_text(f'{self.df[self.date][self.intx]}')
                self.text_slider.set_x(x)
                self.text_slider.draw(renderer)
        return


class ClickMixin(MouseMoveMixin):
    x_click = None
    is_move = False
    click_navleft, click_navright = (False, False)

    def _connect_event(self):
        super()._connect_event()

        self.figure.canvas.mpl_connect('button_press_event', lambda x: self._on_click(x))
        return

    def _on_click(self, e: MouseEvent):
        if self.in_slider: self._on_click_slider(e)
        return

    def _on_click_slider(self, e: MouseEvent):
        if self.is_click_slider or e.button != MouseButton.LEFT: return

        self.background_with_nav_pre = self.background_with_nav

        self.is_click_slider = True
        self.figure.canvas.set_cursor(cursors.RESIZE_HORIZONTAL)

        x = e.xdata.__int__()
        navmin, navmax = self.navcoordinate
        
        leftmin, leftmax = (navmin-self._navLineWidth, navmin+self._navLineWidth_half)
        rightmin, rightmax = (navmax-self._navLineWidth_half, navmax+self._navLineWidth)

        grater_than_left, less_then_right = (leftmax < x, x < rightmin)
        if grater_than_left and less_then_right:
            self.is_move = True
            self.x_click = x
        else:
            if not grater_than_left and leftmin <= x:
                self.click_navleft = True
                self.x_click = navmax
            elif not less_then_right and x <= rightmax:
                self.click_navright = True
                self.x_click = navmin
            else:
                self.x_click = x
        return


class SliderSelectMixin(ClickMixin):
    limit_ma = 8_000

    def _on_move_slider(self, e):
        if self.is_click_slider: self._set_navcoordinate(e)
        return super()._on_move_slider(e)

    def _set_navcoordinate(self, e: MouseEvent):
        x = e.xdata.__int__()
        navmin, navmax = self.navcoordinate

        if self.is_move:
            xsub = self.x_click - x
            navmin, navmax = (navmin-xsub, navmax-xsub)

            # 값 보정
            if navmax < 0: navmin, navmax = (navmin-navmax, 0)
            if self.list_index[-1] < navmin: navmin, navmax = (self.list_index[-1], self.list_index[-1] + (navmax-navmin))

            self.navcoordinate = (navmin, navmax)
            self.x_click = x

            self._set_lim(navmin, navmax, simpler=True, set_ma=(navmax-navmin < self.limit_ma))

            self._set_navigator(navmin, navmax)
            self.navigator.draw(self.figure.canvas.renderer)

            self._draw_artist()
            self.background_with_nav = self.figure.canvas.renderer.copy_from_bbox(self.figure.bbox)
            self._restore_region(False, True)
        else:
            navmin, navmax = (x, self.x_click) if x < self.x_click else (self.x_click, x)

            # 슬라이더가 차트를 벗어나지 않도록 선택 영역 제한
            if navmax < 0 or self.list_index[-1] < navmin:
                seg = self.navigator.get_segments()
                navmin, navmax = (int(seg[1][0][0]), int(seg[3][0][0]))

            nsub = navmax - navmin
            if nsub < self.min_distance:
                self._restore_region(False, False)
                self._set_navigator(navmin, navmax)
                self.navigator.draw(self.figure.canvas.renderer)
            else:
                self._set_lim(navmin, navmax, simpler=True, set_ma=(nsub < self.limit_ma))
                self._set_navigator(navmin, navmax)

                self.navigator.draw(self.figure.canvas.renderer)

                self._draw_artist()
                self.background_with_nav = self.figure.canvas.renderer.copy_from_bbox(self.figure.bbox)
                self._restore_region(False, True)
        return


class ReleaseMixin(SliderSelectMixin):
    def _connect_event(self):
        super()._connect_event()

        self.figure.canvas.mpl_connect('button_release_event', lambda x: self._on_release(x))
        return

    def _on_release(self, e: MouseEvent):
        if self.in_slider and self.is_click_slider: self._on_release_slider(e)
        return

    def _on_release_slider(self, e: MouseEvent):
        if not self.is_move:
            seg = self.navigator.get_segments()
            navmin, navmax = (int(seg[1][0][0]), int(seg[3][0][0]))
            nsub = navmax - navmin
            if self.min_distance <= nsub: self.navcoordinate = (navmin, navmax)
            else:
                self.background_with_nav = self.background_with_nav_pre
                navmin, navmax = self.navcoordinate
                self._set_lim(navmin, navmax, simpler=True, set_ma=(nsub < self.limit_ma))
                self._restore_region(False, True)
                self._blit()
            self._set_navigator(*self.navcoordinate)

        self.is_click_slider = False
        self.is_move = False
        self.click_navleft, self.click_navright = (False, False)
        return


class ChartClickMixin(ReleaseMixin):
    is_click_chart = False

    def _on_click(self, e: MouseEvent):
        if self.in_price_chart or self.in_volume_chart: self._on_click_chart(e)
        elif self.in_slider: self._on_click_slider(e)
        return

    def _on_click_chart(self, e: MouseEvent):
        if self.is_click_chart: return

        self.is_click_chart = True
        self._x_click = e.x.__round__(2)
        self.figure.canvas.set_cursor(cursors.RESIZE_HORIZONTAL)
        return

    def _on_release(self, e):
        if self.is_click_chart and (self.in_price_chart or self.in_volume_chart): self._on_release_chart(e)
        elif self.is_click_slider and self.in_slider: self._on_release_slider(e)
        return

    def _on_release_chart(self, e):
        self.is_click_chart = False
        self.figure.canvas.set_cursor(cursors.POINTER)
        return

    def _change_cursor(self, e):
        if self.is_click_chart: return
        return super()._change_cursor(e)

    def _on_move(self, e):
        self._on_move_action(e)

        need_slider_action = self.is_click_slider and self.in_slider
        need_chart_action = False if need_slider_action else self.is_click_chart and (self.in_price_chart or self.in_volume_chart)
        self._restore_region((need_slider_action or need_chart_action))

        if self.in_slider:
            self._on_move_slider(e)
        elif self.in_price_chart:
            self._on_move_price_chart(e)
        elif self.in_volume_chart:
            self._on_move_volume_chart(e)

        self._blit()
        return

    def _on_move_price_chart(self, e):
        if self.is_click_chart: self._move_chart(e)
        return super()._on_move_price_chart(e)

    def _on_move_volume_chart(self, e):
        if self.is_click_chart: self._move_chart(e)
        return super()._on_move_volume_chart(e)

    def _move_chart(self, e: MouseEvent):
        x = e.x.__round__(2)
        left, right = self.navcoordinate
        nsub = right - left
        xsub = x - self._x_click
        xdiv = (xsub / (1200 / nsub)).__int__()
        if not xdiv:
            self.navigator.draw(self.figure.canvas.renderer)
            self._draw_artist()
        else:
            left, right = (left-xdiv, right-xdiv)
            if right < 0 or self.df.index[-1] < left: self._restore_region(False, True)
            else:
                self.navcoordinate = (left, right)
                self._set_lim(left, right, simpler=True, set_ma=((right-left) < self.limit_ma))
                self._set_navigator(left, right)
                self.navigator.draw(self.figure.canvas.renderer)

                self._draw_artist()
                self.background_with_nav = self.figure.canvas.renderer.copy_from_bbox(self.figure.bbox)
                self._restore_region(False, True)
            self._x_click = x
        return


class BaseMixin(ChartClickMixin):
    pass


class Chart(BaseMixin, Mixin):
    def _add_collection(self):
        super()._add_collection()
        return self.add_artist()

    def _draw_artist(self):
        super()._draw_artist()
        return self.draw_artist()

    def _get_segments(self):
        self.generate_data()
        return super()._get_segments()

    def _on_draw(self, e):
        super()._on_draw(e)
        return self.on_draw(e)

    def _on_pick(self, e):
        self.on_pick(e)
        return super()._on_pick(e)

    def _set_candle_segments(self, index_start, index_end):
        super()._set_candle_segments(index_start, index_end)
        self.set_segment(index_start, index_end)
        return

    def _set_wick_segments(self, index_start, index_end, simpler=False):
        super()._set_wick_segments(index_start, index_end, simpler)
        self.set_segment(index_start, index_end, simpler)
        return

    def _set_line_segments(self, index_start, index_end, simpler=False, set_ma=True):
        super()._set_line_segments(index_start, index_end, simpler, set_ma)
        self.set_segment(index_start, index_end, simpler, set_ma)
        return

    def _on_move(self, e):
        super()._on_move(e)
        return self.on_move(e)

    def _on_click(self, e):
        super()._on_click(e)
        return self.on_click(e)

    def on_release(self, e):
        super().on_release(e)
        return self.on_release(e)

