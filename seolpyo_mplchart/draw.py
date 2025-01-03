from matplotlib.backend_bases import PickEvent
from matplotlib.collections import LineCollection
from matplotlib.lines import Line2D
import numpy as np
import pandas as pd


from .base import Base


class Mixin:
    def generate_data(self, df):
        "This function works after data generate process is done."
        return

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


_set_key = {'x', 'left', 'right', 'top', 'bottom',}

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

    color_up = '#fe3032'
    color_down = '#0095ff'
    color_flat = 'k'
    color_up_down = 'w'
    color_down_up = 'w'
    colors_volume = '#1f77b4'

    def _generate_data(self, df: pd.DataFrame):
        for i in ['date', 'Open', 'high', 'low', 'close', 'volume']:
            k: str = getattr(self, i)
            if k in _set_key: raise Exception(f'you can not set "self.{i}" value in {_set_key}.\nself.{i}={k!r}')
            if i != 'date':
                dtype = df[k].dtype
                if not isinstance(dtype, np.dtypes.Float64DType): raise TypeError(f'Data column type must be "float64".(excluding "date" column)\ndf[{k!r}].dtype={dtype!r}')

        for i in self.list_ma: df[f'ma{i}'] = df[self.close].rolling(i).mean()

        candlewidth_half = 0.3
        volumewidth_half = 0.36
        df['x'] = df.index + 0.5
        df['left'] = df['x'] - candlewidth_half
        df['right'] = df['x'] + candlewidth_half
        df['vleft'] = df['x'] - volumewidth_half
        df['vright'] = df['x'] + volumewidth_half

        df['top'] = np.where(df['open'] <= df['close'], df['close'], df['open'])
        df['top'] = np.where(df['close'] < df['open'], df['open'], df['close'])
        df['bottom'] = np.where(df['open'] <= df['close'], df['open'], df['close'])
        df['bottom'] = np.where(df['close'] < df['open'], df['close'], df['open'])

        # 양봉
        df.loc[:, ['facecolor', 'edgecolor']] = (self.color_up, self.color_up)
        if self.color_up != self.color_down:
            # 음봉
            df.loc[df['close'] < df['open'], ['facecolor', 'edgecolor']] = (self.color_down, self.color_down)
        if self.color_up != self.color_flat:
            # 보합
            df.loc[df['close'] == df['open'], ['facecolor', 'edgecolor']] = (self.color_flat, self.color_flat)
        if self.color_up != self.color_up_down:
            # 양봉(비우기)
            df.loc[(df['facecolor'] == self.color_up) & (df['close'] < df['close'].shift(1)), 'facecolor'] = self.color_up_down
        if self.color_down != self.color_down_up:
            # 음봉(비우기)
            df.loc[(df['facecolor'] == self.color_down) & (df['close'].shift(1) < df['close']), ['facecolor']] = self.color_down_up

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

    def _get_candlesegment(self, s: pd.Series):
        v = s.values
        segment = (
            (v[0], v[3]), # 심지 상단
            (v[0], v[5]), # 몸통 상단
            (v[1], v[5]), # 몸통 상단 좌측
            (v[1], v[6]), # 몸통 하단 좌측
            (v[0], v[6]), # 몸통 하단
            (v[0], v[4]), # 심지 하단
            (v[0], v[6]), # 몸통 하단
            (v[2], v[6]), # 몸통 하단 우측
            (v[2], v[5]), # 몸통 상단 우측
            (v[0], v[5]), # 몸통 상단
        )
        return segment

    def _get_volumesegment(self, s: pd.Series):
        v = s.values
        segment = (
            (v[0], 0), # 몸통 하단 좌측
            (v[0], v[2]), # 몸통 상단 좌측
            (v[1], v[2]), # 몸통 상단 우측
            (v[1], 0), # 몸통 하단 우측
        )
        return segment

    def _set_collection(self):
        self.df.loc[:, ['candlesegment']] = self.df[['x', 'left', 'right', self.high, self.low, 'top', 'bottom']].agg(self._get_candlesegment, axis=1)
        self.df.loc[:, ['volumesegment']] = self.df[['vleft', 'vright', self.volume]].agg(self._get_volumesegment, axis=1)

        self._set_macollection()

        # 가격이동평균선
        segments = list(reversed(self._masegment.values()))
        colors, widths = ([], [])
        for i in reversed(self._macolors.values()): (colors.append(i), widths.append(1))
        self.macollection.set_segments(segments)
        self.macollection.set_edgecolor(colors)

        # 슬라이더 선형차트
        segments.append(self.df[['x', self.close]].apply(tuple, axis=1).tolist())
        (colors.append(self.color_sliderline), widths.append(1.8))
        self.slidercollection.set_segments(segments)
        self.slidercollection.set_edgecolor(colors)
        self.slidercollection.set_linewidth(widths)

        self.candlecollection.set_segments(self.df['candlesegment'])
        self.candlecollection.set_facecolor(self.df['facecolor'].values)
        self.candlecollection.set_edgecolor(self.df['edgecolor'].values)

        self.volumecollection.set_segments(self.df['volumesegment'])
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
            self._masegment[i] = self.df[['x', f'ma{i}']].apply(tuple, axis=1).tolist()

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
    def set_data(self, df: pd.DataFrame):
        self._generate_data(df)
        self._set_collection()
        self._draw_collection()
        return

    def _draw_collection(self):
        xmax = self.df['x'].values[-1] + 1

        xspace = xmax / 40
        self.xmin, self.xmax = (-xspace, xmax+xspace)
        # 슬라이더 xlim
        self.ax_slider.set_xlim(self.xmin, self.xmax)
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
        self.ax_price.set_ylim(self._price_ymin, self._price_ymax)

        # 거래량 ylim
        self._vol_ymax = self.df[self.volume].max() * 1.2
        self.ax_volume.set_ylim(0, self._vol_ymax)
        return


class Chart(DrawMixin, Mixin):
    def _generate_data(self, df):
        super()._generate_data(df)
        return self.generate_data(self.df)

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
