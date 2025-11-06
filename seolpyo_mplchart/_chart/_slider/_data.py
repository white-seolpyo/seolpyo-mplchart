from ._base import BaseMixin as Base


class DataMixin(Base):
    navcoordinate: tuple[int, int] = (0, 0)

    def set_data(self, df, chane_lim=True, *args, **kwargs):
        return super().set_data(df, chane_lim=chane_lim, *args, **kwargs)

    def _set_data(self, df, change_lim=True, *args, **kwargs):
        # print(f'{change_lim=}')
        super()._set_data(df, *args, **kwargs)

        vmin, vmax = self.navcoordinate
        min_distance = 5 if not self.min_distance or self.min_distance < 5 else self.min_distance
        if not change_lim and min_distance <= (vmax-vmin):
            vmax += 1
        else:
            vmin, vmax = self.get_default_lim()
            self.navcoordinate = (vmin, vmax-1)

        self._set_slider_collection()

        self.axis(vmin, xmax=vmax)

        self._set_navigator_artists()
        self._set_slider_xtick()

        self._axis_navigator(*self.navcoordinate)

        self._set_length_text()
        return

    def _set_slider_xtick(self):
        if self.slider_top:
            self.ax_slider.xaxis.set_ticks_position('top')
        else:
            self.ax_slider.xaxis.set_ticks_position('bottom')
        self.ax_slider.get_yticks()

        # grid가 xtick에 영향을 받기 때문에 구간별 tick을 설정해주어야 한다.
        step = len(self.index_list) // 6
        indices = []
        for idx in self.index_list[::step]:
            indices.append(idx)
        if indices[-1] + 1 < self.index_list[-1]:
            indices += [self.index_list[-1]]
        else:
            indices[-1] = self.index_list[-1]
        # print(f'{indices=}')
        # tick label은 0과 -1 구간에만 설정
        date_list = ['' for _ in indices]
        date_list[0] = self.df.iloc[0]['date']
        date_list[-1] = self.df.iloc[-1]['date']
        # xtick 설정
        self.ax_slider.set_xticks(indices)
        self.ax_slider.set_xticklabels(date_list)
        labels = self.ax_slider.get_xticklabels()
        for label, align in zip(labels, ['center', 'center']):
            # 라벨 텍스트 정렬
            label.set_horizontalalignment(align)
        return

    def get_default_lim(self):
        xmax = self.index_list[-1] + 1
        xmin = xmax - 120
        if xmin < 0:
            xmin = 0
        return (xmin, xmax)


class BackgroundMixin(DataMixin):
    def _copy_bbox(self):
        renderer = self.figure.canvas.renderer

        self.ax_slider.xaxis.draw(renderer)
        self.ax_slider.yaxis.draw(renderer)
        self.collection_slider.draw(renderer)
        self.background_emtpy = renderer.copy_from_bbox(self.figure.bbox)

        self.draw_artists()
        self.background = renderer.copy_from_bbox(self.figure.bbox)

        self.collection_navigator.draw(renderer)
        self.background_with_nav = renderer.copy_from_bbox(self.figure.bbox)
        return

    def _restore_region(self, is_empty=False, with_nav=True):
        if not self.background:
            self._create_background()

        func = self.figure.canvas.renderer.restore_region
        if is_empty:
            func(self.background_emtpy)
        elif with_nav:
            func(self.background_with_nav)
        else:
            func(self.background)
        return


class BaseMixin(BackgroundMixin):
    pass

