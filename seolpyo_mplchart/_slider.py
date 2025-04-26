import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.collections import LineCollection
from matplotlib.text import Text
from matplotlib.backend_bases import MouseEvent, MouseButton, cursors

from ._base import convert_unit
from ._cursor import BaseMixin as BM, Mixin as M


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
    color_navigator_line = '#1E78FF'
    color_navigator_cover = 'k'

    def _add_collection(self):
        super()._add_collection()

        self.collection_slider = LineCollection([], animated=True)
        self.ax_slider.add_artist(self.collection_slider)

        # 슬라이더 네비게이터
        self.collection_navigator = LineCollection([], animated=True, edgecolors=[self.color_navigator_cover, self.color_navigator_line], alpha=(0.3, 1.0))
        self.ax_slider.add_artist(self.collection_navigator)

        lineKwargs = {'edgecolor': 'k', 'linewidth': 1, 'linestyle': '-'}
        lineKwargs.update(self.lineKwargs)
        lineKwargs.update({'segments': [], 'animated': True})

        self.collection_slider_vline = LineCollection(**lineKwargs)
        self.ax_slider.add_artist(self.collection_slider_vline)

        textboxKwargs = {'boxstyle': 'round', 'facecolor': 'w'}
        textboxKwargs.update(self.textboxKwargs)
        textKwargs = self.textKwargs
        textKwargs.update({'animated': True, 'bbox': textboxKwargs, 'horizontalalignment': '', 'verticalalignment': ''})
        (textKwargs.pop('horizontalalignment'), textKwargs.pop('verticalalignment'))

        self.artist_text_slider = Text(**textKwargs, horizontalalignment='center', verticalalignment='top')
        self.ax_slider.add_artist(self.artist_text_slider)
        return

    def _create_segments(self):
        super()._create_segments()

        self._create_slider_segment()
        return

    def _create_slider_segment(self):
        keys = []
        for i in reversed(self.list_ma):
            keys.append('x')
            keys.append(f'ma{i}')

        segment_slider = self.df[keys + ['x', self.close] ].values
        segment_slider = segment_slider.reshape(segment_slider.shape[0], len(self.list_ma)+1, 2).swapaxes(0, 1)
        self.collection_slider.set_segments(segment_slider)
        linewidth = [1 for _ in self.list_ma]
        self.collection_slider.set_linewidth(linewidth + [2.1])

        self._create_slider_color_segments()
        return

    def _create_slider_color_segments(self):
        self.collection_slider.set_edgecolor(self.edgecolor_ma + [self.color_priceline])
        return

    def change_background_color(self, color):
        super().change_background_color(color)

        self.ax_slider.set_facecolor(color)
        self.artist_text_slider.set_backgroundcolor(color)
        return

    def change_tick_color(self, color):
        super().change_tick_color(color)

        for i in ['top', 'bottom', 'left', 'right']: self.ax_slider.spines[i].set_color(self.color_tick)
        self.ax_slider.tick_params(colors=color)
        return

    def change_text_color(self, color):
        super().change_text_color(color)

        self.artist_text_slider.set_color(color)
        return

    def change_line_color(self, color):
        super().change_line_color(color)

        self.artist_text_slider.get_bbox_patch().set_edgecolor(color)
        self.collection_slider_vline.set_edgecolor(color)
        return


class NavigatorMixin(CollectionMixin):
    def _set_slider_lim(self):
        xmax = self.list_index[-1]
        # 슬라이더 xlim
        xdistance = xmax / 30
        self.slider_xmin, self.slider_xmax = (-xdistance, xmax+xdistance)
        self.ax_slider.set_xlim(self.slider_xmin, self.slider_xmax)

        # 슬라이더 ylim
        ymin, ymax = (self.df[self.low].min(), self.df[self.high].max())
        ysub = ymax - ymin
        self.sldier_ymiddle = ymin + (ysub / 2)
        ydistance = ysub / 5
        self.slider_ymin, self.slider_ymax = (ymin-ydistance, ymax+ydistance)
        self.ax_slider.set_ylim(self.slider_ymin, self.slider_ymax)

        # 슬라이더 텍스트 y
        self.artist_text_slider.set_y(ymax)

        self.collection_navigator.set_linewidth([ysub+ysub, 5])

        # 네비게이터 라인 선택 범위
        xsub = self.slider_xmax - self.slider_xmin
        self._navLineWidth = xsub * 8 / 1_000
        if self._navLineWidth < 1: self._navLineWidth = 1
        self._navLineWidth_half = self._navLineWidth / 2
        return

    def _set_navigator(self, navmin, navmax):
        seg = [
            (
                (self.slider_xmin, self.sldier_ymiddle),
                (navmin, self.sldier_ymiddle),
            ),
            (
                (navmin, self.slider_ymin),
                (navmin, self.slider_ymax),
            ),
            (
                (navmax, self.sldier_ymiddle),
                (self.slider_xmax, self.sldier_ymiddle),
            ),
            (
                (navmax, self.slider_ymin),
                (navmax, self.slider_ymax),
            ),
        ]

        self.collection_navigator.set_segments(seg)
        return


class DataMixin(NavigatorMixin):
    navcoordinate: tuple[int, int] = (0, 0)

    def set_data(self, df, sort_df=True, calc_ma=True, set_candlecolor=True, set_volumecolor=True, calc_info=True, change_lim=True, *args, **kwargs):
        self._generate_data(df, sort_df, calc_ma, set_candlecolor, set_volumecolor, calc_info, *args, **kwargs)
        self._create_segments()
        
        vmin, vmax = self.navcoordinate
        if change_lim or (vmax-vmin) < self.min_distance:
            vmin, vmax = self.get_default_lim()
            self.navcoordinate = (vmin, vmax-1)
        else: vmax += 1

        self._set_lim(vmin, vmax)
        self._set_slider_lim()
        self._set_navigator(*self.navcoordinate)

        self._set_length_text()
        return

    def get_default_lim(self):
        xmax = self.list_index[-1] + 1
        xmin = xmax - 120
        if xmin < 0: xmin = 0
        return (xmin, xmax)


class BackgroundMixin(DataMixin):
    def _copy_bbox(self):
        renderer = self.figure.canvas.renderer

        self.ax_slider.xaxis.draw(renderer)
        self.ax_slider.yaxis.draw(renderer)
        self.collection_slider.draw(renderer)
        self.background_emtpy = renderer.copy_from_bbox(self.figure.bbox)

        self._draw_artist()
        self.background = renderer.copy_from_bbox(self.figure.bbox)

        self.collection_navigator.draw(self.figure.canvas.renderer)
        self.background_with_nav = renderer.copy_from_bbox(self.figure.bbox)
        return

    def _restore_region(self, is_empty=False, with_nav=True):
        if not self.background: self._create_background()

        restore_region = self.figure.canvas.renderer.restore_region
        if is_empty: restore_region(self.background_emtpy)
        elif with_nav: restore_region(self.background_with_nav)
        else: restore_region(self.background)
        return


class MouseMoveMixin(BackgroundMixin):
    in_slider = False
    is_click_slider = False

    def _erase_crossline(self):
        boolen = super()._erase_crossline()
        if boolen: return boolen

        seg = self.collection_slider_vline.get_segments()
        if seg:
            self.collection_slider_vline.set_segments([])
            return True
        return False

    def _on_move(self, e):
        self._on_move_action(e)

        if self.in_slider:
            self._restore_region(self.is_click_slider)
            self._on_move_slider(e)
            self.figure.canvas.blit()
        elif self.in_price_chart or self.in_volume_chart:
            self._restore_region()
            self._draw_crossline(e, self.in_price_chart)
            self.figure.canvas.blit()
        else:
            if self._erase_crossline():
                self._restore_region()
                self.figure.canvas.blit()
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

        x = e.xdata.__round__()

        leftmin = navleft - self._navLineWidth
        leftmax = navleft + self._navLineWidth_half
        rightmin = navright - self._navLineWidth_half
        rightmax = navright + self._navLineWidth
        if x < leftmin: self.figure.canvas.set_cursor(cursors.POINTER)
        elif x <= leftmax: self.figure.canvas.set_cursor(cursors.RESIZE_HORIZONTAL)
        elif x < rightmin: self.figure.canvas.set_cursor(cursors.MOVE)
        elif x <= rightmax: self.figure.canvas.set_cursor(cursors.RESIZE_HORIZONTAL)
        else: self.figure.canvas.set_cursor(cursors.POINTER)
        return

    def _check_ax(self, e: MouseEvent):
        ax = e.inaxes
        if not ax or e.xdata is None or e.ydata is None:
            self.in_slider, self.in_price_chart, self.in_volume_chart = (False, False, False)
        else:
            if ax is self.ax_slider:
                self.in_slider = True
                self.in_price_chart = False
                self.in_volume_chart = False
            elif ax is self.ax_price:
                self.in_slider = False
                self.in_price_chart = True
                self.in_volume_chart = False
            elif ax is self.ax_volume:
                self.in_slider = False
                self.in_price_chart = False
                self.in_volume_chart = True
            else:
                self.in_slider = False
                self.in_price_chart = False
                self.in_volume_chart = False
        return

    def _on_move_slider(self, e: MouseEvent):
        x = e.xdata
        if self.intx is not None:
            renderer = self.figure.canvas.renderer
            self.collection_slider_vline.set_segments([((x, self.slider_ymin), (x, self.slider_ymax))])
            self.collection_slider_vline.draw(renderer)

            if self.in_slider:
                self.artist_text_slider.set_text(f'{self.df[self.date][self.intx]}')
                self.artist_text_slider.set_x(x)
                self.artist_text_slider.draw(renderer)
        return

    def _draw_crossline(self, e: MouseEvent, in_price_chart):
        self.collection_slider_vline.set_segments([((e.xdata, self.slider_ymin), (e.xdata, self.slider_ymax))])
        self.collection_slider_vline.draw(self.figure.canvas.renderer)
        return super()._draw_crossline(e, in_price_chart)


class ClickMixin(MouseMoveMixin):
    x_click = None
    is_move = False
    click_navleft, click_navright = (False, False)

    def _connect_event(self):
        super()._connect_event()

        self.figure.canvas.mpl_connect('button_press_event', lambda x: self._on_click(x))
        return

    def _on_click(self, e: MouseEvent):
        if self.in_slider and not self.is_click_slider and e.button == MouseButton.LEFT: self._on_click_slider(e)
        return

    def _on_click_slider(self, e: MouseEvent):
        self.background_with_nav_pre = self.background_with_nav

        self.is_click_slider = True
        self.figure.canvas.set_cursor(cursors.RESIZE_HORIZONTAL)

        navleft, navright = self.navcoordinate
        x = e.xdata.__round__()
        
        leftmax = navleft + self._navLineWidth_half
        rightmin = navright - self._navLineWidth_half

        grater_than_left = leftmax < x
        less_then_right = x < rightmin
        if grater_than_left and less_then_right:
            self.is_move = True
            self.x_click = x
        else:
            leftmin = navleft - self._navLineWidth
            rightmax = navright + self._navLineWidth
            if not grater_than_left and leftmin <= x:
                self.click_navleft = True
                self.x_click = navright
            elif not less_then_right and x <= rightmax:
                self.click_navright = True
                self.x_click = navleft
            else:
                self.x_click = x
        return


class SliderSelectMixin(ClickMixin):
    limit_ma = 8_000

    def _on_move_slider(self, e):
        if self.is_click_slider: self._set_navcoordinate(e)
        return super()._on_move_slider(e)

    def _set_navcoordinate(self, e: MouseEvent):
        navmin, navmax = self.navcoordinate

        x = e.xdata.__int__()
        if self.is_move:
            xsub = self.x_click - x
            navmin, navmax = (navmin-xsub, navmax-xsub)

            # 값 보정
            if navmax < 0: navmin, navmax = (navmin-navmax, 0)
            if self.list_index[-1] < navmin: navmin, navmax = (self.list_index[-1], self.list_index[-1] + (navmax-navmin))

            self.navcoordinate = (navmin, navmax)
            self.x_click = x

            self._set_lim(navmin, navmax+1, simpler=True, set_ma=(navmax-navmin < self.limit_ma))

            self._set_navigator(navmin, navmax)
            self.collection_navigator.draw(self.figure.canvas.renderer)

            self._draw_artist()
            self.background_with_nav = self.figure.canvas.renderer.copy_from_bbox(self.figure.bbox)
            self._restore_region()
        else:
            navmin, navmax = (x, self.x_click) if x < self.x_click else (self.x_click, x)

            # 슬라이더가 차트를 벗어나지 않도록 선택 영역 제한
            if navmax < 0 or self.list_index[-1] < navmin:
                seg = self.collection_navigator.get_segments()
                navmin, navmax = (int(seg[1][0][0]), int(seg[3][0][0]))

            nsub = navmax - navmin
            if nsub < self.min_distance:
                self._restore_region(False, False)
                self._set_navigator(navmin, navmax)
                self.collection_navigator.draw(self.figure.canvas.renderer)
            else:
                self._set_lim(navmin, navmax+1, simpler=True, set_ma=(nsub < self.limit_ma))
                self._set_navigator(navmin, navmax)

                self.collection_navigator.draw(self.figure.canvas.renderer)

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
        if self.in_slider and self.is_click_slider and e.button == MouseButton.LEFT: self._on_release_slider(e)
        return

    def _on_release_slider(self, e: MouseEvent):
        if not self.is_move:
            seg = self.collection_navigator.get_segments()
            navmin, navmax = (int(seg[1][0][0]), int(seg[3][0][0]))
            nsub = navmax - navmin
            if self.min_distance <= nsub: self.navcoordinate = (navmin, navmax)
            else:
                self.background_with_nav = self.background_with_nav_pre
                navmin, navmax = self.navcoordinate
                self._set_lim(navmin, navmax+1, simpler=True, set_ma=(nsub < self.limit_ma))
                self._restore_region(False, True)
                self.figure.canvas.blit()
            self._set_navigator(*self.navcoordinate)

        self.is_click_slider = False
        self.is_move = False
        self.click_navleft, self.click_navright = (False, False)

        self.figure.canvas.draw()
        return


class ChartClickMixin(ReleaseMixin):
    is_click_chart = False

    def _on_click(self, e: MouseEvent):
        if e.button == MouseButton.LEFT:
            if (
                not self.is_click_chart
                and (self.in_price_chart or self.in_volume_chart)
            ): self._on_click_chart(e)
            elif not self.is_click_slider and self.in_slider:
                self._on_click_slider(e)
        return

    def _on_click_chart(self, e: MouseEvent):
        self.is_click_chart = True
        x = e.xdata.__int__()
        self.x_click = x - self.navcoordinate[0]
        self.figure.canvas.set_cursor(cursors.RESIZE_HORIZONTAL)
        return

    def _on_release(self, e):
        if e.button ==  MouseButton.LEFT:
            if (
                self.is_click_chart
                and (self.in_price_chart or self.in_volume_chart)
            ): self._on_release_chart(e)
            elif self.is_click_slider and self.in_slider:
                self._on_release_slider(e)
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

        if self.in_slider:
            self._restore_region(self.is_click_slider)
            self._on_move_slider(e)
            self.figure.canvas.blit()
        elif self.in_price_chart or self.in_volume_chart:
            self._restore_region(self.is_click_chart)
            if not self.is_click_chart:
                self._draw_crossline(e, self.in_price_chart)
            else: self._move_chart(e)
            self.figure.canvas.blit()
        else:
            if self._erase_crossline():
                self._restore_region()
                self.figure.canvas.blit()
        return

    def _move_chart(self, e: MouseEvent):
        left, right = self.navcoordinate
        x = e.xdata.__int__() - left
        xsub = x - self.x_click
        if not xsub:
            self.collection_navigator.draw(self.figure.canvas.renderer)
            self._draw_artist()
        else:
            left, right = (left-xsub, right-xsub)
            if right < 0 or self.df.index[-1] < left: self._restore_region()
            else:
                self.x_click = x
                self.navcoordinate = (left, right)
                self._set_lim(left, right+1, simpler=True, set_ma=((right-left) < self.limit_ma))
                self._set_navigator(left, right)
                self.collection_navigator.draw(self.figure.canvas.renderer)

                self._draw_artist()
                self.background_with_nav = self.figure.canvas.renderer.copy_from_bbox(self.figure.bbox)
                self._restore_region()
        return


class BaseMixin(ChartClickMixin):
    pass


class Chart(BaseMixin, Mixin):
    def _draw_artist(self):
        super()._draw_artist()
        return self.draw_artist()

    def _set_lim(self, xmin, xmax, simpler=False, set_ma=True):
        super()._set_lim(xmin, xmax, simpler, set_ma)
        return self.on_change_xlim(xmin, xmax, simpler, set_ma)

    def _on_draw(self, e):
        super()._on_draw(e)
        return self.on_draw(e)

    def _on_pick(self, e):
        self.on_pick(e)
        return super()._on_pick(e)

    def _on_move(self, e):
        super()._on_move(e)
        return self.on_move(e)

    def _on_click(self, e):
        super()._on_click(e)
        return self.on_click(e)

    def on_release(self, e):
        super().on_release(e)
        return self.on_release(e)

