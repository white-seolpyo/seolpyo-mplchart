from matplotlib.backend_bases import PickEvent
from matplotlib.collections import LineCollection
from matplotlib.lines import Line2D
from matplotlib.text import Text
import numpy as np
import pandas as pd


from .base import Base


class Mixin:
    def add_artist(self):
        "This method work when ```__init__()``` run."
        return

    def draw_artist(self):
        "This method work before ```figure.canvas.blit()```."
        return

    def generate_data(self):
        "This method work before create segments."
        return

    def on_draw(self, e):
        "If draw event active, This method work."
        return

    def on_pick(self, e):
        "If draw pick active, This method work."
        return

    def set_segment(self, xmin, xmax, simpler=False, set_ma=True):
        "This method work if xlim change."
        return


class CollectionMixin(Base):
    facecolor_volume, edgecolor_volume = ('#1f77b4', 'k')
    watermark = 'seolpyo mplchart'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._add_collection()
        return

    def _add_collection(self):
        self.collection_ma = LineCollection([], animated=True, linewidths=1)
        self.ax_price.add_collection(self.collection_ma)

        self.collection_candle = LineCollection([], animated=True, linewidths=0.8)
        self.ax_price.add_collection(self.collection_candle)

        self.collection_volume = LineCollection([], animated=True, linewidths=1)
        self.ax_volume.add_collection(self.collection_volume)

        x = (self.adjust['right']-self.adjust['left']) / 2
        self.text_watermark = Text(
            x=x, y=0.51, text=self.watermark,
            animated=True,
            fontsize=20, color=self.color_tick_label, alpha=0.2,
            horizontalalignment='center', verticalalignment='center',
        )
        self.figure.add_artist(self.text_watermark)
        return

    def change_background_color(self, color):
        self.figure.set_facecolor(color)
        self.ax_price.set_facecolor(color)
        self.ax_volume.set_facecolor(color)
        legends = self.ax_legend.get_legend()
        if legends: legends.get_frame().set_facecolor(color)
        return

    def change_tick_color(self, color):
        for ax in (self.ax_price, self.ax_volume):
            for i in ['top', 'bottom', 'left', 'right']: ax.spines[i].set_color(self.color_tick)
            ax.tick_params(colors=color)
            ax.tick_params(colors=color)

        legends = self.ax_legend.get_legend()
        if legends: legends.get_frame().set_edgecolor(color)

        self.change_text_color(color)
        return

    def change_text_color(self, color):
        self.text_watermark.set_color(color)
        legends = self.ax_legend.get_legend()
        if legends:
            for i in legends.texts: i.set_color(color)
        return

    def change_line_color(self, color): return


_set_key = {'_x', '_left', '_right', '_volleft', '_volright', '_top', '_bottom', '_pre', '_zero', '_volymax',}

class DataMixin(CollectionMixin):
    df: pd.DataFrame

    date = 'date'
    Open, high, low, close = ('open', 'high', 'low', 'close')
    volume = 'volume'
    list_ma = (5, 20, 60, 120, 240)

    candle_width_half, volume_width_half = (0.24, 0.36)
    color_up, color_down = ('#FF2400', '#1E90FF')
    color_flat = 'k'
    color_up_down, color_down_up = ('w', 'w')

    color_volume_up, color_volume_down = ('#FF4D4D', '#5CA8F4')
    color_volume_flat = '#A9A9A9'

    set_candlecolor, set_volumecolor = (True, True)

    def _generate_data(self, df: pd.DataFrame, sort_df, calc_ma, set_candlecolor, set_volumecolor, *_, **__):
        self._validate_column_key()

        # 오름차순 정렬
        if sort_df: df = df.sort_values([self.date])
        df = df.reset_index()

        self.list_index = df.index.tolist()
        self.xmin, self.xmax = (0, self.list_index[-1])

        if not self.list_ma: self.list_ma = tuple()
        else:
            self.list_ma = sorted(self.list_ma)
            # 가격이동평균선 계산
            if calc_ma:
                for i in self.list_ma: df[f'ma{i}'] = df[self.close].rolling(i).mean()
            else:
                set_key = set(self.df.keys())
                for i in self.list_ma:
                    key = f'ma{i}'
                    if key not in set_key:
                        raise KeyError(f'"{key}" column not found.\nset calc_ma=True or add "{key}" column.')

        df['_x'] = df.index + 0.5
        df['_left'] = df['_x'] - self.candle_width_half
        df['_right'] = df['_x'] + self.candle_width_half
        df['_volleft'] = df['_x'] - self.volume_width_half
        df['_volright'] = df['_x'] + self.volume_width_half
        df.loc[:, '_zero'] = 0

        df['_top'] = np.where(df[self.Open] <= df[self.close], df[self.close], df[self.Open])
        df['_top'] = np.where(df[self.close] < df[self.Open], df[self.Open], df[self.close])
        df['_bottom'] = np.where(df[self.Open] <= df[self.close], df[self.Open], df[self.close])
        df['_bottom'] = np.where(df[self.close] < df[self.Open], df[self.close], df[self.Open])

        df['_pre'] = df[self.close].shift(1)
        if self.volume: df['_volymax'] = df[self.volume] * 1.2

        if not set_candlecolor:
            keys = set(df.keys())
            for i in ('facecolor', 'edgecolor', 'volumefacecolor',):
                if i not in keys:
                    raise Exception(f'"{i}" column not in DataFrame.\nadd column or set set_candlecolor=True.')
        self.set_candlecolor = set_candlecolor

        if not set_volumecolor:
            keys = set(df.keys())
            for i in ('volumefacecolor', 'volumeedgecolor',):
                if i not in keys:
                    raise Exception(f'"{i}" column not in DataFrame.\nadd column or set set_volumecolor=True.')
        self.set_volumecolor = set_volumecolor

        self.df = df
        return

    def _validate_column_key(self):
        for i in ('date', 'Open', 'high', 'low', 'close', 'volume'):
            v = getattr(self, i)
            if v in _set_key: raise Exception(f'you can not set "{i}" to column key.\nself.{i}={v!r}')
        return


class SegmentMixin(DataMixin):
    _visible_ma = set()

    limit_candle = 800
    limit_wick = 4_000
    limit_volume = 800

    color_priceline = 'k'
    format_ma = '{}일선'
    # https://matplotlib.org/stable/gallery/color/named_colors.html
    list_macolor = ('#B22222', '#228B22', '#1E90FF', '#FF8C00', '#4B0082')

    def _get_segments(self):
        # 캔들 세그먼트
        segment_candle = self.df[[
            '_x', self.high,
            '_x', '_top',
            '_left', '_top',
            '_left', '_bottom',
            '_x', '_bottom',
            '_x', self.low,
            '_x', '_bottom',
            '_right', '_bottom',
            '_right', '_top',
            '_x', '_top',
            '_x', self.high,
            '_x', '_top',
        ]].values
        self.segment_candle = segment_candle.reshape(segment_candle.shape[0], 12, 2)

        # 심지 세그먼트
        segment_wick = self.df[[
            '_x', self.high,
            '_x', self.low,
        ]].values
        self.segment_candle_wick = segment_wick.reshape(segment_wick.shape[0], 2, 2)

        # 종가 세그먼트
        segment_priceline = segment_wick = self.df[['_x', self.close]].values
        self.segment_priceline = segment_priceline.reshape(1, *segment_wick.shape)

        if self.volume:
            # 거래량 바 세그먼트
            segment_volume = self.df[[
                '_volleft', '_zero',
                '_volleft', self.volume,
                '_volright', self.volume,
                '_volright', '_zero',
            ]].values
            self.segment_volume = segment_volume.reshape(segment_volume.shape[0], 4, 2)

            # 거래량 심지 세그먼트
            segment_volume_wick = self.df[[
                '_x', '_zero',
                '_x', self.volume,
            ]].values
            self.segment_volume_wick = segment_volume_wick.reshape(segment_volume_wick.shape[0], 2, 2)

        self._get_ma_segment()
        self._get_color_segment()
        return

    def _get_color_segment(self):
        if self.set_candlecolor:
            # 양봉
            self.df.loc[:, ['facecolor', 'edgecolor']] = (self.color_up, self.color_up)
            if self.color_up != self.color_down:
                # 음봉
                self.df.loc[self.df[self.close] < self.df[self.Open], ['facecolor', 'edgecolor']] = (self.color_down, self.color_down)
            if self.color_up != self.color_flat and self.color_down != self.color_flat:
                # 보합
                self.df.loc[self.df[self.close] == self.df[self.Open], ['facecolor', 'edgecolor']] = (self.color_flat, self.color_flat)
            if self.color_up != self.color_up_down:
                # 양봉(비우기)
                self.df.loc[(self.df['facecolor'] == self.color_up) & (self.df[self.close] <= self.df['_pre']), 'facecolor'] = self.color_up_down
            if self.color_down != self.color_down_up:
                # 음봉(비우기)
                self.df.loc[(self.df['facecolor'] == self.color_down) & (self.df['_pre'] <= self.df[self.close]), ['facecolor']] = self.color_down_up

        self.facecolor_candle = self.df['facecolor'].values
        self.edgecolor_candle = self.df['edgecolor'].values

        if self.set_volumecolor:
            # 거래량
            self.df.loc[:, ['volumefacecolor', 'volumeedgecolor']] = (self.color_volume_up, self.color_volume_up)
            if self.color_up != self.color_down:
                # 전일대비 하락
                self.df.loc[self.df[self.close] < self.df['_pre'], ['volumefacecolor', 'volumeedgecolor']] = (self.color_volume_down, self.color_volume_down)
            if self.color_up != self.color_flat:
                # 전일과 동일
                self.df.loc[self.df[self.close] == self.df['_pre'], ['volumefacecolor', 'volumeedgecolor']] = (self.color_volume_flat, self.color_volume_flat)

        self.facecolor_volume = self.df['volumefacecolor'].values
        self.edgecolor_volume = self.df['volumeedgecolor'].values

        # 기존 legend 제거
        legends = self.ax_legend.get_legend()
        if legends: legends.remove()

        self._visible_ma.clear()

        list_handle, list_label, list_color = ([], [], [])
        arr = (0, 1)
        for n, i in enumerate(self.list_ma):
            try: c = self.list_macolor[n]
            except: c = self.color_priceline
            list_color.append(c)

            list_handle.append(Line2D(arr, arr, color=c, linewidth=5, label=i))
            list_label.append(self.format_ma.format(i))

            self._visible_ma.add(i)
        self.edgecolor_ma = list(reversed(list_color))

        # 가격이동평균선 legend 생성
        if list_handle:
            legends = self.ax_legend.legend(
                list_handle, list_label, loc='lower left', ncol=10,
                facecolor=self.color_background, edgecolor=self.color_tick,
                labelcolor=self.color_tick_label,
            )
            for i in legends.legend_handles: i.set_picker(5)
        return

    def _get_ma_segment(self):
        if not self.list_ma: return

        # 주가 차트 가격이동평균선
        key_ma = []
        for i in reversed(self.list_ma):
            key_ma.append('_x')
            key_ma.append(f'ma{i}')
        segment_ma = self.df[key_ma].values
        self.segment_ma = segment_ma.reshape(segment_ma.shape[0], len(self.list_ma), 2).swapaxes(0, 1)
        return

    def _set_segments(self, index_start, index_end, simpler, set_ma):
        indsub = index_end - index_start
        if index_start < 0: index_start = 0
        if index_end < 1: index_end = 1

        index_end += 1
        if indsub < self.limit_candle:
            self._set_candle_segments(index_start, index_end)
        elif indsub < self.limit_wick:
            self._set_wick_segments(index_start, index_end, simpler)
        else:
            self._set_line_segments(index_start, index_end, simpler, set_ma)
        return

    def _set_candle_segments(self, index_start, index_end):
        self.collection_candle.set_segments(self.segment_candle[index_start:index_end])
        self.collection_candle.set_facecolor(self.facecolor_candle[index_start:index_end])
        self.collection_candle.set_edgecolor(self.edgecolor_candle[index_start:index_end])

        if self.volume:
            self.collection_volume.set_segments(self.segment_volume[index_start:index_end])
            self.collection_volume.set_linewidth(0.7)
            self.collection_volume.set_facecolor(self.facecolor_volume[index_start:index_end])
            self.collection_volume.set_edgecolor(self.edgecolor_volume[index_start:index_end])

        self.collection_ma.set_segments(self.segment_ma[:, index_start:index_end])
        self.collection_ma.set_edgecolor(self.edgecolor_ma)
        return

    def _set_wick_segments(self, index_start, index_end, simpler=False):
        self.collection_candle.set_segments(self.segment_candle_wick[index_start:index_end])
        self.collection_candle.set_facecolor([])
        self.collection_candle.set_edgecolor(self.edgecolor_candle[index_start:index_end])

        if self.volume:
            seg = self.segment_volume_wick[index_start:index_end]
            if simpler:
                values = seg[:, 1, 1]
                top_index = np.argsort(-values)[:self.limit_volume]
                seg = seg[top_index]
            self.collection_volume.set_segments(seg)
            self.collection_volume.set_linewidth(1.3)
            self.collection_volume.set_facecolor(self.facecolor_volume[index_start:index_end])
            self.collection_volume.set_edgecolor(self.facecolor_volume[index_start:index_end])

        self.collection_ma.set_segments(self.segment_ma[:, index_start:index_end])
        self.collection_ma.set_edgecolor(self.edgecolor_ma)
        return

    def _set_line_segments(self, index_start, index_end, simpler=False, set_ma=True):
        self.collection_candle.set_segments(self.segment_priceline[:, index_start:index_end])
        self.collection_candle.set_facecolor([])
        self.collection_candle.set_edgecolor(self.color_priceline)

        if self.volume:
            seg = self.segment_volume_wick[index_start:index_end]
            if simpler:
                values = seg[:, 1, 1]
                top_index = np.argsort(-values)[:self.limit_volume]
                seg = seg[top_index]
            self.collection_volume.set_segments(seg)
            self.collection_volume.set_linewidth(1.3)
            self.collection_volume.set_facecolor(self.facecolor_volume[index_start:index_end])
            self.collection_volume.set_edgecolor(self.facecolor_volume[index_start:index_end])

        if not set_ma: self.collection_ma.set_segments([])
        else:
            self.collection_ma.set_segments(self.segment_ma[:, index_start:index_end])
            self.collection_ma.set_edgecolor(self.edgecolor_ma)
        return


class EventMixin(SegmentMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._connect_event()
        return

    def _connect_event(self):
        self.figure.canvas.mpl_connect('pick_event', lambda x: self._on_pick(x))
        return

    def _on_pick(self, e):
        self._pick_ma_action(e)
        return

    def _pick_ma_action(self, e: PickEvent):
        handle = e.artist
        if handle.get_alpha() == 0.2:
            visible = True
            handle.set_alpha(1.0)
        else:
            visible = False
            handle.set_alpha(0.2)

        n = int(handle.get_label())
        if visible: self._visible_ma = {i for i in self.list_ma if i in self._visible_ma or i == n}
        else: self._visible_ma = {i for i in self._visible_ma if i != n}

        alphas = [(1 if i in self._visible_ma else 0) for i in reversed(self.list_ma)]
        self.collection_ma.set_alpha(alphas)

        self._draw()
        return

    def _draw(self):
        self.figure.canvas.draw()
        return


class DrawMixin(EventMixin):
    candle_on_ma = True

    def set_data(self, df, sort_df=True, calc_ma=True, set_candlecolor=True, set_volumecolor=True, *args, **kwargs):
        self._generate_data(df, sort_df, calc_ma, set_candlecolor, set_volumecolor, *args, **kwargs)
        self._get_segments()

        vmin, vmax = self.get_default_lim()
        self._set_lim(vmin, vmax)
        return

    def _connect_event(self):
        super()._connect_event()
        self.figure.canvas.mpl_connect('draw_event', lambda x: self._on_draw(x))
        return

    def _on_draw(self, e):
        self._draw_artist()
        self._blit()
        return

    def _draw_artist(self):
        renderer = self.figure.canvas.renderer

        self.ax_price.xaxis.draw(renderer)
        self.ax_price.yaxis.draw(renderer)

        if self.candle_on_ma:
            self.collection_ma.draw(renderer)
            self.collection_candle.draw(renderer)
        else:
            self.collection_candle.draw(renderer)
            self.collection_ma.draw(renderer)

        if self.watermark:
            self.text_watermark.set_text(self.watermark)
            self.text_watermark.draw(renderer)

        self.ax_volume.xaxis.draw(renderer)
        self.ax_volume.yaxis.draw(renderer)

        self.collection_volume.draw(renderer)
        return

    def _blit(self):
        self.figure.canvas.blit()
        return

    def _set_lim(self, xmin, xmax, simpler=False, set_ma=True):
        self.vxmin, self.vxmax = (xmin, xmax + 1)
        if xmin < 0: xmin = 0
        if xmax < 0: xmax = 0
        if xmin == xmax: xmax += 1

        ymin, ymax = (self.df[self.low][xmin:xmax].min(), self.df[self.high][xmin:xmax].max())
        yspace = (ymax - ymin) / 15
        # 주가 차트 ymin, ymax
        self.price_ymin, self.price_ymax = (ymin-yspace, ymax+yspace)

        # 거래량 차트 ymax
        self.volume_ymax = self.df['_volymax'][xmin:xmax].max() if self.volume else 1

        self._set_segments(xmin, xmax, simpler, set_ma)
        self._change_lim(self.vxmin, self.vxmax)
        return

    def _change_lim(self, xmin, xmax):
        # 주가 차트 xlim
        self.ax_price.set_xlim(xmin, xmax)
        # 거래량 차트 xlim
        self.ax_volume.set_xlim(xmin, xmax)

        # 주가 차트 ylim
        self.ax_price.set_ylim(self.price_ymin, self.price_ymax)
        # 거래량 차트 ylim
        self.ax_volume.set_ylim(0, self.volume_ymax)
        return

    def get_default_lim(self):
        return (0, self.list_index[-1])


class BackgroundMixin(DrawMixin):
    background = None

    _creating_background = False

    def _connect_event(self):
        self.figure.canvas.mpl_connect('pick_event', lambda x: self._on_pick(x))
        self.figure.canvas.mpl_connect('draw_event', lambda x: self._on_draw(x))
        return

    def _create_background(self):
        if self._creating_background: return

        self._creating_background = True
        self._copy_bbox()
        self._creating_background = False
        return

    def _copy_bbox(self):
        self._draw_artist()
        self.background = self.figure.canvas.renderer.copy_from_bbox(self.figure.bbox)
        return

    def _on_draw(self, e):
        self.background = None
        self._restore_region()
        return

    def _restore_region(self):
        if not self.background: self._create_background()

        self.figure.canvas.renderer.restore_region(self.background)
        return


class BaseMixin(BackgroundMixin):
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

