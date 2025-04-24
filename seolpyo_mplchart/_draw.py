from matplotlib.backend_bases import PickEvent
from matplotlib.collections import LineCollection
from matplotlib.lines import Line2D
from matplotlib.text import Text
import numpy as np
import pandas as pd


from ._base import Base


class Mixin:
    def draw_artist(self):
        "This method work before ```figure.canvas.blit()```."
        return

    def on_change_xlim(self, xmin, xmax, simpler=False, set_ma=True):
        "This method work if xlim change."
        return

    def on_draw(self, e):
        "If draw event active, This method work."
        return

    def on_pick(self, e):
        "If draw pick active, This method work."
        return


class CollectionMixin(Base):
    facecolor_volume, edgecolor_volume = ('#1f77b4', 'k')
    watermark = 'seolpyo mplchart'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._add_collection()
        return

    def _add_collection(self):
        self.artist_watermark = Text(
            x=0.5, y=0.5, text=self.watermark,
            animated=True,
            fontsize=20, color=self.color_tick_label, alpha=0.2,
            horizontalalignment='center', verticalalignment='center',
            transform=self.ax_price.transAxes
        )
        self.ax_price.add_artist(self.artist_watermark)

        self.collection_candle = LineCollection([], animated=True, linewidths=0.8)
        self.ax_price.add_collection(self.collection_candle)

        self.collection_ma = LineCollection([], animated=True, linewidths=1)
        self.ax_price.add_collection(self.collection_ma)

        self.collection_volume = LineCollection([], animated=True, linewidths=1)
        self.ax_volume.add_collection(self.collection_volume)
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
            for i in ('top', 'bottom', 'left', 'right'): ax.spines[i].set_color(self.color_tick)
            ax.tick_params(colors=color)
            ax.tick_params(colors=color)

        legends = self.ax_legend.get_legend()
        if legends: legends.get_frame().set_edgecolor(color)

        self.change_text_color(color)
        return

    def change_text_color(self, color):
        self.artist_watermark.set_color(color)
        legends = self.ax_legend.get_legend()
        if legends:
            for i in legends.texts: i.set_color(color)
        return

    def change_line_color(self, color): return


class DrawMixin(CollectionMixin):
    candle_on_ma = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._connect_event()
        return

    def _connect_event(self):
        self.figure.canvas.mpl_connect('draw_event', lambda x: self._on_draw(x))
        return

    def _on_draw(self, e):
        self._draw_artist()
        self.figure.canvas.blit()
        return

    def _draw_artist(self):
        self._draw_ax_price()
        self._draw_ax_volume()
        return

    def _draw_ax_price(self):
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
            self.artist_watermark.set_text(self.watermark)
            self.artist_watermark.draw(renderer)
        return

    def _draw_ax_volume(self):
        renderer = self.figure.canvas.renderer

        self.ax_volume.xaxis.draw(renderer)
        self.ax_volume.yaxis.draw(renderer)

        self.collection_volume.draw(renderer)
        return


_set_key = {
    'x', 'zero', 'close_pre', 'ymax_volume',
    'is_up',
    'top_candle', 'bottom_candle',
    'left_candle', 'right_candle',
    'left_volume', 'right_volume',
}

class DataMixin(DrawMixin):
    df: pd.DataFrame

    date = 'date'
    Open, high, low, close = ('open', 'high', 'low', 'close')
    volume = 'volume'
    list_ma = (5, 20, 60, 120, 240)

    candle_width_half, volume_width_half = (0.24, 0.36)
    color_up, color_down = ('#FF2400', '#1E90FF')
    color_flat = 'k'
    color_up_down, color_down_up = ('w', 'w')

    color_volume_up, color_volume_down = ('#FF5555', '#5CA8F4')
    color_volume_flat = '#909090'

    set_candlecolor, set_volumecolor = (True, True)

    def _generate_data(self, df: pd.DataFrame, sort_df, calc_ma, set_candlecolor, set_volumecolor, *_, **__):
        self.set_candlecolor = set_candlecolor
        self.set_volumecolor = set_volumecolor

        self.chart_price_ymax = df[self.high].max() * 1.3
        self.chart_volume_ymax = df[self.volume].max() * 1.3

        self._validate_column_key(df)

        # 오름차순 정렬
        if sort_df: df = df.sort_values([self.date])
        df = df.reset_index(drop=True)

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

        df['x'] = df.index + 0.5
        df['left_candle'] = df['x'] - self.candle_width_half
        df['right_candle'] = df['x'] + self.candle_width_half
        df['left_volume'] = df['x'] - self.volume_width_half
        df['right_volume'] = df['x'] + self.volume_width_half
        df.loc[:, 'zero'] = 0

        df['is_up'] = np.where(df[self.Open] < df[self.close], True, False)
        df['top_candle'] = np.where(df['is_up'], df[self.close], df[self.Open])
        df['bottom_candle'] = np.where(df['is_up'], df[self.Open], df[self.close])

        df['close_pre'] = df[self.close].shift(1)
        if self.volume: df['ymax_volume'] = df[self.volume] * 1.2

        self.df = df
        return

    def _validate_column_key(self, df: pd.DataFrame):
        for i in ('date', 'Open', 'high', 'low', 'close', 'volume'):
            v = getattr(self, i)
            if v in _set_key: raise Exception(f'you can not set "{i}" to column key.\nself.{i}={v!r}')

        if not self.set_candlecolor:
            keys = set(df.keys())
            for i in ('facecolor', 'edgecolor', 'facecolor_volume', 'edgecolor_volume',):
                if i not in keys:
                    raise Exception(f'"{i}" column not in DataFrame.\nadd column or set set_candlecolor=True.')

        if not self.set_volumecolor:
            keys = set(df.keys())
            for i in ('facecolor_volume', 'edgecolor_volume',):
                if i not in keys:
                    raise Exception(f'"{i}" column not in DataFrame.\nadd column or set set_volumecolor=True.')
        return


class CandleSegmentMixin(DataMixin):
    color_priceline = 'k'
    limit_candle = 800

    def get_candle_segment(self, *, is_up, x, left, right, top, bottom, high, low):
        """
        get candle segment

        Args:
            is_up (bool): (True if open < close else False)
            x (float): center of candle
            left (float): left of candle
            right (float): right of candle
            top (float): top of candle(close if open < close else open)
            bottom (float): bottom of candle(open if open < close else close)
            high (float): top of candle wick
            low (float): bottom of candle wick

        Returns:
            tuple[tuple[float, float]]: candle segment
        """
        return (
            (x, high),
            (x, top),
            (left, top),
            (left, bottom),
            (x, bottom),
            (x, low),
            (x, bottom),
            (right, bottom),
            (right, top),
            (x, top),
            (x, high),
            (x, top),
        )

    def _create_candle_segments(self):
        # 캔들 세그먼트
        segment_candle = []
        for x, left, right, top, bottom, is_up, high, low in zip(
            self.df['x'].to_numpy().tolist(),
            self.df['left_candle'].to_numpy().tolist(), self.df['right_candle'].to_numpy().tolist(),
            self.df['top_candle'].to_numpy().tolist(), self.df['bottom_candle'].to_numpy().tolist(),
            self.df['is_up'].to_numpy().tolist(),
            self.df[self.high].to_numpy().tolist(), self.df[self.low].to_numpy().tolist(),
        ):
            segment_candle.append(
                self.get_candle_segment(
                    is_up=is_up,
                    x=x,
                    left=left, right=right,
                    top=top, bottom=bottom,
                    high=high, low=low,
                )
            )
        self.segment_candle = np.array(segment_candle)

        # 심지 세그먼트
        segment_wick = self.df[[
            'x', self.high,
            'x', self.low,
        ]].values
        self.segment_candle_wick = segment_wick.reshape(segment_wick.shape[0], 2, 2)

        # 종가 세그먼트
        segment_priceline = segment_wick = self.df[['x', self.close]].values
        self.segment_priceline = segment_priceline.reshape(1, *segment_wick.shape)

        self._create_candle_color_segments()
        return

    def add_candle_color_column(self):
        columns = ['facecolor', 'edgecolor']
        # 양봉
        self.df.loc[:, columns] = (self.color_up, self.color_up)
        if self.color_up != self.color_down:
            # 음봉
            self.df.loc[self.df[self.close] < self.df[self.Open], columns] = (self.color_down, self.color_down)
        if self.color_up != self.color_flat and self.color_down != self.color_flat:
            # 보합
            self.df.loc[self.df[self.close] == self.df[self.Open], columns] = (self.color_flat, self.color_flat)
        if self.color_up != self.color_up_down:
            # 양봉(비우기)
            self.df.loc[(self.df['facecolor'] == self.color_up) & (self.df[self.close] <= self.df['close_pre']), 'facecolor'] = self.color_up_down
        if self.color_down != self.color_down_up:
            # 음봉(비우기)
            self.df.loc[(self.df['facecolor'] == self.color_down) & (self.df['close_pre'] <= self.df[self.close]), ['facecolor']] = self.color_down_up
        return

    def _create_candle_color_segments(self):
        if self.set_candlecolor: self.add_candle_color_column()

        self.facecolor_candle = self.df['facecolor'].values
        self.edgecolor_candle = self.df['edgecolor'].values
        return

    def _set_candle_segments(self, index_start, index_end):
        self.collection_candle.set_segments(self.segment_candle[index_start:index_end])
        self.collection_candle.set_facecolor(self.facecolor_candle[index_start:index_end])
        self.collection_candle.set_edgecolor(self.edgecolor_candle[index_start:index_end])
        return

    def _set_candle_wick_segments(self, index_start, index_end):
        self.collection_candle.set_segments(self.segment_candle_wick[index_start:index_end])
        self.collection_candle.set_facecolor([])
        self.collection_candle.set_edgecolor(self.edgecolor_candle[index_start:index_end])
        return

    def _set_priceline_segments(self, index_start, index_end):
        self.collection_candle.set_segments(self.segment_priceline[:, index_start:index_end])
        self.collection_candle.set_facecolor([])
        self.collection_candle.set_edgecolor(self.color_priceline)
        return


class MaSegmentMixin(CandleSegmentMixin):
    format_ma = '{}일선'
    # https://matplotlib.org/stable/gallery/color/named_colors.html
    list_macolor = ('#006400', '#8B008B', '#FFA500', '#0000FF', '#FF0000')

    _visible_ma = set()

    def _create_ma_segments(self):
        # 주가 차트 가격이동평균선
        key_ma = []
        for i in reversed(self.list_ma):
            key_ma.append('x')
            key_ma.append(f'ma{i}')
        if key_ma:
            segment_ma = self.df[key_ma].values
            self.segment_ma = segment_ma.reshape(segment_ma.shape[0], len(self.list_ma), 2).swapaxes(0, 1)

        self._create_ma_color_segments()
        return

    def _create_ma_color_segments(self):
        # 기존 legend 제거
        legends = self.ax_legend.get_legend()
        if legends: legends.remove()

        self._visible_ma.clear()

        list_handle, list_label, list_color = ([], [], [])
        arr = [0, 1]
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

    def _set_ma_segments(self, index_start, index_end, set_ma):
        if not set_ma: self.collection_ma.set_segments([])
        else:
            self.collection_ma.set_segments(self.segment_ma[:, index_start:index_end])
            self.collection_ma.set_edgecolor(self.edgecolor_ma)
        return


class VolumeSegmentMixin(MaSegmentMixin):
    limit_volume = 200

    def get_volume_segment(self, *, x, left, right, top):
        """
        get volume bar segment

        Args:
            x (float): center of volume bar
            left (float): left of volume bar
            right (float): right of volume bar
            top (float): top of volume bar

        Returns:
            tuple[tuple[float, float]]: volume bar segment
        """
        return (
            (left, top),
            (left, 0),
            (right, 0),
            (right, top),
            (left, top),
        )

    def _create_volume_segments(self):
        # 거래량 바 세그먼트
        segment_volume = []
        for x, left, right, top in zip(
            self.df['x'].to_numpy().tolist(),
            self.df['left_volume'].to_numpy().tolist(), self.df['right_volume'].to_numpy().tolist(),
            self.df[self.volume].to_numpy().tolist(),
        ):
            segment_volume.append(
                self.get_volume_segment(x=x, left=left, right=right, top=top)
            )
        self.segment_volume = np.array(segment_volume)

        # 거래량 심지 세그먼트
        segment_volume_wick = self.df[[
            'x', 'zero',
            'x', self.volume,
        ]].values
        self.segment_volume_wick = segment_volume_wick.reshape(segment_volume_wick.shape[0], 2, 2)

        self._create_volume_color_segments()
        return

    def add_volume_color_column(self):
        columns = ['facecolor_volume', 'edgecolor_volume']
        # 거래량
        self.df.loc[:, columns] = (self.color_volume_up, self.color_volume_up)
        if self.color_up != self.color_down:
            # 전일대비 하락
            condition = self.df[self.close] < self.df['close_pre']
            self.df.loc[condition, columns] = (self.color_volume_down, self.color_volume_down)
        if self.color_up != self.color_flat:
            # 전일과 동일
            condition = self.df[self.close] == self.df['close_pre']
            self.df.loc[condition, columns] = (self.color_volume_flat, self.color_volume_flat)
        return

    def _create_volume_color_segments(self):
        if self.set_volumecolor: self.add_volume_color_column()

        self.facecolor_volume = self.df['facecolor_volume'].values
        self.edgecolor_volume = self.df['edgecolor_volume'].values
        return

    def _set_volume_segments(self, index_start, index_end):
        self.collection_volume.set_segments(self.segment_volume[index_start:index_end])
        self.collection_volume.set_linewidth(0.7)
        self.collection_volume.set_facecolor(self.facecolor_volume[index_start:index_end])
        self.collection_volume.set_edgecolor(self.edgecolor_volume[index_start:index_end])
        return

    def _set_volume_wick_segments(self, index_start, index_end, simpler):
        seg_volume = self.segment_volume_wick[index_start:index_end]
        seg_facecolor_volume = self.facecolor_volume[index_start:index_end]
        seg_edgecolor_volume = self.edgecolor_volume[index_start:index_end]
        if simpler:
            values = seg_volume[:, 1, 1]
            top_index = np.argsort(-values)[:self.limit_volume]
            seg_volume = seg_volume[top_index]
            seg_facecolor_volume = seg_facecolor_volume[top_index]
            seg_edgecolor_volume = seg_edgecolor_volume[top_index]
        self.collection_volume.set_segments(seg_volume)
        self.collection_volume.set_linewidth(1.3)
        self.collection_volume.set_facecolor(seg_facecolor_volume)
        self.collection_volume.set_edgecolor(seg_edgecolor_volume)
        return


class SegmentMixin(VolumeSegmentMixin):
    limit_wick = 4_000

    def _create_segments(self):
        self._create_candle_segments()
        self._create_ma_segments()
        if self.volume: self._create_volume_segments()
        return

    def _set_collection_segments(self, index_start, index_end, indsub, simpler, set_ma=True):
        if indsub < self.limit_candle:
            self._set_candle_segments(index_start, index_end)
            self._set_ma_segments(index_start, index_end, set_ma)
            if self.volume: self._set_volume_segments(index_start, index_end)
        elif indsub < self.limit_wick:
            self._set_candle_wick_segments(index_start, index_end)
            self._set_ma_segments(index_start, index_end, set_ma)
            if self.volume: self._set_volume_wick_segments(index_start, index_end, simpler)
        else:
            self._set_priceline_segments(index_start, index_end)
            self._set_ma_segments(index_start, index_end, set_ma)
            if self.volume: self._set_volume_wick_segments(index_start, index_end, simpler)
        return


class EventMixin(SegmentMixin):
    def _connect_event(self):
        super()._connect_event()

        self.figure.canvas.mpl_connect('pick_event', lambda x: self._on_pick(x))
        return

    def _on_pick(self, e):
        self._pick_ma_action(e)
        return

    def _pick_ma_action(self, e: PickEvent):
        handle = e.artist

        visible = handle.get_alpha() == 0.2
        handle.set_alpha(1.0 if visible else 0.2)

        n = int(handle.get_label())
        if visible: self._visible_ma = {i for i in self.list_ma if i in self._visible_ma or i == n}
        else: self._visible_ma = {i for i in self._visible_ma if i != n}

        alphas = [(1 if i in self._visible_ma else 0) for i in reversed(self.list_ma)]
        self.collection_ma.set_alpha(alphas)

        self.figure.canvas.draw()
        return


class LimMixin(EventMixin):
    candle_on_ma = True

    def set_data(self, df, sort_df=True, calc_ma=True, set_candlecolor=True, set_volumecolor=True, *args, **kwargs):
        self._generate_data(df, sort_df, calc_ma, set_candlecolor, set_volumecolor, *args, **kwargs)
        self._create_segments()

        vmin, vmax = self.get_default_lim()
        self._set_lim(vmin, vmax)
        return

    def _set_lim(self, xmin, xmax, simpler=False, set_ma=True):
        self.vxmin, self.vxmax = (xmin, xmax)
        if xmin < 0: xmin = 0
        if xmax < 1: xmax = 1

        ymin, ymax = (self.df[self.low][xmin:xmax].min(), self.df[self.high][xmin:xmax].max())
        yspace = (ymax - ymin) / 15
        # 주가 차트 ymin, ymax
        self.price_ymin, self.price_ymax = (ymin-yspace, ymax+yspace)

        # 거래량 차트 ymax
        self.volume_ymax = self.df['ymax_volume'][xmin:xmax].max() if self.volume else 1

        self._change_lim(self.vxmin, self.vxmax)
        xsub = xmax - xmin
        self._set_collection_segments(xmin, xmax, xsub, simpler, set_ma)
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
        return (0, self.list_index[-1]+1)


class BackgroundMixin(LimMixin):
    background = None

    _creating_background = False

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

