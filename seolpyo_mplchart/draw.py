from matplotlib.backend_bases import PickEvent
from matplotlib.collections import LineCollection
from matplotlib.lines import Line2D
import numpy as np
import pandas as pd


from .base import Base


class Mixin:
    def on_blit(self):
        "This function works after cavas.blit()."
        return
    def on_draw(self, e):
        "This function works if draw event active."
        return
    def on_move(self, e):
        "This function works if mouse move event active."
        return
    def on_pick(self, e):
        "This function works if pick event active."
        return


_set_key = {'zero', 'x', 'left', 'right', 'top', 'bottom',}

class DataMixin(Base):
    df: pd.DataFrame
    date = 'date'
    Open, high, low, close = ('open', 'high', 'low', 'close')
    volume = 'volume'

    _visible_ma = set()
    label_ma = '{}일선'
    list_ma = (5, 20, 60, 120, 240)
    # https://matplotlib.org/stable/gallery/color/named_colors.html
    list_macolor = ('darkred', 'fuchsia', 'olive', 'orange', 'navy', 'darkmagenta', 'limegreen', 'darkcyan',)

    color_up, color_down = ('#fe3032', '#0095ff')
    color_flat = 'k'
    color_up_down, color_down_up = ('w', 'w')
    colors_volume = '#1f77b4'

    candlewidth_half, volumewidth_half = (0.3, 0.36)

    def _generate_data(self, df: pd.DataFrame, sort_df=True, calc_ma=True, **_):
        for i in ('date', 'Open', 'high', 'low', 'close', 'volume'):
            k: str = getattr(self, i)
            if k in _set_key: raise Exception(f'you can not set "self.{i}" value in {_set_key}.\nself.{i}={k!r}')
            if i != 'date':
                dtype = df[k].dtype
                if not isinstance(dtype, (np.dtypes.Float64DType, np.dtypes.Int64DType, np.dtypes.Float32DType, np.dtypes.Int32DType)):
                    raise TypeError(f'column dtype must be one of "float64" or "int64" or "float32" or "int32".(excluding "date" column)\ndf[{k!r}].dtype={dtype!r}')

        # DataFrame 정렬
        if sort_df:
            df = df.sort_values([self.date]).reset_index()

        if not self.list_ma: self.list_ma = tuple()
        if calc_ma:
            for i in self.list_ma: df[f'ma{i}'] = df[self.close].rolling(i).mean()
        else:
            keys = set(df.keys())
            for i in self.list_ma:
                if f'ma{i}' not in keys:
                    raise Exception(f'"ma{i}" column not in DataFrame.\nadd column or set calc_ma=True.')

        df['x'] = df.index + 0.5
        df['left'] = df['x'] - self.candlewidth_half
        df['right'] = df['x'] + self.candlewidth_half
        df['vleft'] = df['x'] - self.volumewidth_half
        df['vright'] = df['x'] + self.volumewidth_half

        df['top'] = np.where(df[self.Open] <= df[self.close], df[self.close], df[self.Open])
        df['top'] = np.where(df[self.close] < df[self.Open], df[self.Open], df[self.close])
        df['bottom'] = np.where(df[self.Open] <= df[self.close], df[self.Open], df[self.close])
        df['bottom'] = np.where(df[self.close] < df[self.Open], df[self.close], df[self.Open])

        # 양봉
        df.loc[:, ['zero', 'facecolor', 'edgecolor']] = (0, self.color_up, self.color_up)
        if self.color_up != self.color_down:
            # 음봉
            df.loc[df[self.close] < df[self.Open], ['facecolor', 'edgecolor']] = (self.color_down, self.color_down)
        if self.color_up != self.color_flat:
            # 보합
            df.loc[df[self.close] == df[self.Open], ['facecolor', 'edgecolor']] = (self.color_flat, self.color_flat)
        if self.color_up != self.color_up_down:
            # 양봉(비우기)
            df.loc[(df['facecolor'] == self.color_up) & (df[self.close] < df[self.close].shift(1)), 'facecolor'] = self.color_up_down
        if self.color_down != self.color_down_up:
            # 음봉(비우기)
            df.loc[(df['facecolor'] == self.color_down) & (df[self.close].shift(1) < df[self.close]), ['facecolor']] = self.color_down_up

        self.df = df
        return

class CollectionMixin(DataMixin):
    color_sliderline = 'k'

    _masegment, _macolors = ({}, {})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._connect_event()
        self._add_collection()
        return

    def _connect_event(self):
        self.canvas.mpl_connect('pick_event', lambda x: self._on_pick(x))
        return

    def _add_collection(self):
        self.macollection = LineCollection([], animated=True, antialiased=True, linewidth=1)
        self.ax_price.add_collection(self.macollection)

        self.slidercollection = LineCollection([], animated=True, antialiased=True)
        self.ax_slider.add_collection(self.slidercollection)

        # https://white.seolpyo.com/entry/145/
        self.candlecollection = LineCollection([], animated=True, antialiased=True, linewidths=1)
        self.ax_price.add_collection(self.candlecollection)

        # https://white.seolpyo.com/entry/145/
        self.volumecollection = LineCollection([], animated=True, antialiased=True, facecolors=self.colors_volume, linewidths=1, edgecolors='k')
        self.ax_volume.add_collection(self.volumecollection)

        return

    def _set_collection(self):
        candleseg = self.df[[
            'x', self.high,
            'x', 'top',
            'left', 'top',
            'left', 'bottom',
            'x', 'bottom',
            'x', self.low,
            'x', 'bottom',
            'right', 'bottom',
            'right', 'top',
            'x', 'top',
        ]].values
        candleseg = candleseg.reshape(candleseg.shape[0], 10, 2)

        self.candlecollection.set_segments(candleseg)
        self.candlecollection.set_facecolor(self.df['facecolor'].values)
        self.candlecollection.set_edgecolor(self.df['edgecolor'].values)

        volseg = self.df[[
            'left', 'zero',
            'left', self.volume,
            'right', self.volume,
            'right', 'zero',
        ]].values
        volseg = volseg.reshape(volseg.shape[0], 4, 2)

        self.volumecollection.set_segments(volseg)

        self._set_macollection()

        # 가격이동평균선
        maseg = reversed(self._masegment.values())
        colors, widths = ([], [])
        for i in reversed(self._macolors.values()): (colors.append(i), widths.append(1))
        self.macollection.set_segments(maseg)
        self.macollection.set_edgecolor(colors)

        # 슬라이더 선형차트
        keys = []
        for i in reversed(self.list_ma):
            keys.append('x')
            keys.append(f'ma{i}')
        sliderseg = self.df[keys + ['x', self.close]].values
        sliderseg = sliderseg.reshape(sliderseg.shape[0], self.list_ma.__len__()+1, 2).swapaxes(0, 1)
        (colors.append(self.color_sliderline), widths.append(1.8))
        self.slidercollection.set_segments(sliderseg)
        self.slidercollection.set_edgecolor(colors)
        self.slidercollection.set_linewidth(widths)
        return

    def _set_macollection(self):
        # 기존 legend 제거
        legends = self.ax_legend.get_legend()
        if legends: legends.remove()

        self._masegment.clear(), self._macolors.clear()
        handles, labels = ([], [])
        self._visible_ma.clear()
        for n, i in enumerate(self.list_ma):
            try: c = self.list_macolor[n]
            except: c = self.color_sliderline
            self._macolors[i] = c
            # seg = self.df['x', f'ma{i}'].values
            seg = self.df.loc[self.df[f'ma{i}'] != np.nan, ['x', f'ma{i}']].values
            # print(f'{seg[:5]=}')
            self._masegment[i] = seg

            handles.append(Line2D([0, 1], [0, 1], color=c, linewidth=5, label=i))
            labels.append(self.label_ma.format(i))

            self._visible_ma.add(i)

        # 가격이동평균선 legend 생성
        if handles:
            legends = self.ax_legend.legend(handles, labels, loc='lower left', ncol=10)

            for i in legends.legend_handles:
                i.set_picker(5)
        return

    def _on_pick(self, e):
        self._pick_ma_action(e)

        return self._draw()

    def _pick_ma_action(self, e: PickEvent):
        handle = e.artist
        if e.artist.get_alpha() == 0.2:
            visible = True
            handle.set_alpha(1.0)
        else:
            visible = False
            handle.set_alpha(0.2)

        n = int(handle.get_label())

        if visible: self._visible_ma = {i for i in self.list_ma if i in self._visible_ma or i == n}
        else: self._visible_ma = {i for i in self._visible_ma if i != n}

        self.macollection.set_segments([self._masegment[i] for i in reversed(self._masegment) if i in self._visible_ma])
        colors = [self._macolors[i] for i in reversed(self._macolors) if i in self._visible_ma]
        self.macollection.set_colors(colors)
        return

    def _draw(self):
        if self.fig.canvas is not self.canvas:
            self.canvas = self.fig.canvas
        self.canvas.draw()
        return


class BackgroundMixin(CollectionMixin):
    background = None
    candle_on_ma = True

    _creating_background = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        return

    def _connect_event(self):
        super()._connect_event()
        self.canvas.mpl_connect('draw_event', lambda x: self._on_draw(x))
        return

    def _create_background(self):
        if self._creating_background: return

        if self.fig.canvas is not self.canvas:
            self.canvas = self.fig.canvas

        self._creating_background = True
        self._copy_bbox()
        self._creating_background = False
        return

    def _copy_bbox(self):
        self._draw_artist()
        self.background = self.canvas.renderer.copy_from_bbox(self.fig.bbox)
        return

    def _draw_artist(self):
        renderer = self.canvas.renderer

        self.ax_slider.xaxis.draw(renderer)
        self.ax_slider.yaxis.draw(renderer)

        self.slidercollection.draw(renderer)

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

    def _on_draw(self, e):
        self.background = None
        self._restore_region()
        return

    def _restore_region(self):
        if not self.background: self._create_background()

        self.canvas.renderer.restore_region(self.background)
        return

class DrawMixin(BackgroundMixin):
    def set_data(self, df: pd.DataFrame, sort_df=True, calc_ma=True, change_lim=True, *_, **kwargs):
        self._set_data(df, sort_df, calc_ma, change_lim, **kwargs)
        return self.df

    def _set_data(self, df: pd.DataFrame, sort_df=True, calc_ma=True, change_lim=True, *_, **kwargs):
        self._generate_data(df, sort_df, calc_ma, **kwargs)
        self._set_collection()
        self._draw_collection(change_lim)
        return

    def _draw_collection(self, change_lim=True):
        xmax = self.df['x'].values[-1] + 1

        xspace = xmax / 40
        self.xmin, self.xmax = (-xspace, xmax+xspace)
        # 슬라이더 xlim
        self.ax_slider.set_xlim(self.xmin, self.xmax)
        if change_lim:
            # 주가 xlim
            self.ax_price.set_xlim(self.xmin, self.xmax)
            # 거래량 xlim
            self.ax_volume.set_xlim(self.xmin, self.xmax)

        ymin, ymax = (self.df[self.low].min(), self.df[self.high].max())
        ysub = (ymax - ymin) / 15

        # 슬라이더 ylim
        self._slider_ymin, self._slider_ymax = (ymin-ysub, ymax+ysub)
        self.ax_slider.set_ylim(self._slider_ymin, self._slider_ymax)

        # 주가 ylim
        self._price_ymin, self._price_ymax = (ymin-ysub, ymax+ysub)
        if change_lim: self.ax_price.set_ylim(self._price_ymin, self._price_ymax)

        # 거래량 ylim
        self._vol_ymax = self.df[self.volume].max() * 1.2
        if change_lim: self.ax_volume.set_ylim(0, self._vol_ymax)
        return


class Chart(DrawMixin, Mixin):
    def _on_draw(self, e):
        super()._on_draw(e)
        return self.on_draw(e)

    def _on_pick(self, e):
        self.on_pick(e)
        return super()._on_pick(e)


if __name__ == '__main__':
    import json
    from time import time

    import matplotlib.pyplot as plt
    from pathlib import Path

    with open(Path(__file__).parent / 'data/samsung.txt', 'r', encoding='utf-8') as txt:
        data = json.load(txt)
    print(f'{len(data)=}')
    # data = data[:200]
    df = pd.DataFrame(data)

    t = time()
    DrawMixin().set_data(df)
    t2 = time() - t
    print(f'{t2=}')
    plt.show()
