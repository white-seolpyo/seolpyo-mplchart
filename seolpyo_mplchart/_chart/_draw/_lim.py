from matplotlib.backend_bases import PickEvent
from matplotlib.text import Text
import numpy as np

from ._data import BaseMixin as Base


class EventMixin(Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.connect_events()
        return

    def connect_events(self):
        self._connect_events()
        return

    def _connect_events(self):
        self.figure.canvas.mpl_connect('pick_event', lambda x: self.on_pick(x))
        return

    def on_pick(self, e):
        self._on_pick(e)
        return

    def _on_pick(self, e):
        self._pick_ma_action(e)
        return

    def _pick_ma_action(self, e: PickEvent):
        handle = e.artist
        ax = handle.axes
        # print(f'{(ax is self.ax_legend)=}')
        if ax is not self.ax_legend:
            return

        visible = handle.get_alpha() == 0.2
        handle.set_alpha(1.0 if visible else 0.2)

        n = int(handle.get_label())
        if visible:
            self._visible_ma = {i for i in self.CONFIG.MA.ma_list if i in self._visible_ma or i == n}
        else:
            self._visible_ma = {i for i in self._visible_ma if i != n}

        alphas = [(1 if i in self._visible_ma else 0) for i in reversed(self.CONFIG.MA.ma_list)]
        self.collection_ma.set_alpha(alphas)

        self.figure.canvas.draw()
        return


class LimMixin(EventMixin):
    candle_on_ma = True

    def _set_data(self, df, *args, **kwargs):
        super()._set_data(df, *args, **kwargs)

        self.set_segments()

        vmin, vmax = self.get_default_lim()
        self.axis(vmin, xmax=vmax, simpler=False, draw_ma=True)

        # 노출 영역에 맞게 collection segment 조정하기
        self.set_collections(self.vxmin, xmax=self.vxmax, simpler=False, draw_ma=True)
        return

    def axis(self, xmin, *, xmax, simpler=False, draw_ma=True):
        self._axis(xmin, xmax=xmax, simpler=simpler, draw_ma=draw_ma)
        return

    def _convert_xlim(self, xmin, *, xmax):
        if xmin < 0:
            xmin = 0
        if xmax < 1:
            xmax = 1
        return (xmin, xmax)

    def _get_price_ylim(self, xmin, *, xmax):
        ymin, ymax = (self.df['low'][xmin:xmax].min(), self.df['high'][xmin:xmax].max())
        ysub = ymax - ymin
        if ysub < 15:
            ysub = 15
        yspace = ysub / 14
        ymin = ymin - yspace
        ymax = ymax + yspace
        if ymin == ymax:
            if ymax:
                ymin, ymax = (round(ymax * 0.9), round(ymax * 1.1))
            else:
                ymin, ymax = (0, 10)
        return (ymin, ymax)

    def _get_volume_ylim(self, xmin, *, xmax):
        if not self.key_volume:
            ymax = 1
        else:
            series = self.df['volume'][xmin:xmax]
            # print(f'{series=}')
            ymax = series.max()
            yspace = ymax / 5
            ymax = ymax + yspace
            if ymax < 1:
                ymax = 1
        # print(f'{ymax=}')
        return (0, ymax)

    def _axis(self, xmin, xmax, simpler=False, draw_ma=True):
        self.set_collections(xmin, xmax=xmax, simpler=simpler, draw_ma=draw_ma)

        self.vxmin, self.vxmax = (xmin, xmax)
        xmin, xmax = self._convert_xlim(xmin, xmax=xmax)

        self.price_ymin, self.price_ymax = self._get_price_ylim(xmin, xmax=xmax)

        # 주가 차트 xlim
        self.ax_price.set_xlim(self.vxmin, xmax)
        # 주가 차트 ylim
        self.ax_price.set_ylim(self.price_ymin, self.price_ymax)

        # 거래량 차트 xlim
        self.ax_volume.set_xlim(self.vxmin, xmax)
        self.key_volume_ymax = 1
        if self.key_volume:
            _, self.key_volume_ymax = self._get_volume_ylim(xmin, xmax=xmax)
            # 거래량 차트 ylim
            self.ax_volume.set_ylim(0, self.key_volume_ymax)

        # x축에 일부 date 표시하기
        # x tick 외부 눈금 표시
        self.ax_volume.xaxis.set_ticks_position('bottom')
        xhalf = (xmax-xmin) // 2
        xmiddle = xmin + xhalf
        indices = []
        aligns = ['left', 'center', 'center']
        for idx in [xmin, xmiddle, xmax-1]:
            if idx <= self.index_list[-1]:
                indices.append(idx)
        # print(f'{indices=}')
        if xmin == 0 and self.vxmin < 0:
            if xhalf / 2 < xmin - indices[-1]:
                indices = [indices[-1]]
                aligns = aligns[2:]
            else:
                indices = [0, indices[-1]]
                aligns = aligns[1:]
        elif len(indices) < 2:
            if xmin - indices[-1] < xhalf / 2:
                indices = [xmin, self.index_list[-1]]
                aligns = [aligns[0], aligns[0]]
        elif len(indices) < 3:
            indices[-1] = self.index_list[-1]
            aligns = aligns[:2]
        
        date_list = [self.df.iloc[idx]['date'] for idx in indices]
        # 라벨을 노출할 틱 위치
        self.ax_volume.set_xticks([idx+0.5 for idx in indices])
        # 라벨
        self.ax_volume.set_xticklabels(date_list)
        labels: list[Text] = self.ax_volume.get_xticklabels()
        for label, align in zip(labels, aligns):
            # 라벨 텍스트 정렬
            label.set_horizontalalignment(align)
        return

    def set_collections(self, xmin, *, xmax, simpler, draw_ma):
        self._set_collections(xmin, index_end=xmax, simpler=simpler, draw_ma=draw_ma)
        return

    def _set_collections(self, index_start, *, index_end, simpler, draw_ma):
        return

    def get_default_lim(self):
        return (0, self.index_list[-1]+1)


class CollectionMixin(LimMixin):
    limit_candle = 400
    limit_wick = 2_000
    limit_volume = 200
    limit_ma = None

    def _set_collections(self, index_start, *, index_end, simpler, draw_ma):
        if index_start < 0:
            index_start = 0
        indsub = index_end - index_start
        # print(f'{indsub=:,}')

        if not self.limit_candle or indsub < self.limit_candle:
            # print('candle')
            self._set_candle_segments(index_start, index_end=index_end)
            self._set_volume_segments(index_start, index_end=index_end)
        else:
            self._set_volume_wick_segments(index_start, index_end, simpler=simpler)

            if not self.limit_wick or indsub < self.limit_wick:
                # print('wick')
                self._set_candle_wick_segments(index_start, index_end)
            else:
                # print('line')
                self._set_priceline_segments(index_start, index_end)

        self._set_ma_segments(index_start, index_end, draw_ma)
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
        self.collection_candle.set_edgecolor(self.CONFIG.CANDLE.line_color)
        return

    def _set_ma_segments(self, index_start, index_end, draw_ma):
        if not draw_ma:
            self.collection_ma.set_segments([])
        else:
            self.collection_ma.set_segments(self.segment_ma[:, index_start:index_end])
            self.collection_ma.set_edgecolor(self.edgecolor_ma)
        return

    def _set_volume_segments(self, index_start, index_end):
        if not self.key_volume:
            self.collection_volume.set_segments([])
            return
        self.collection_volume.set_segments(self.segment_volume[index_start:index_end])
        self.collection_volume.set_linewidth(0.7)
        self.collection_volume.set_facecolor(self.facecolor_volume[index_start:index_end])
        self.collection_volume.set_edgecolor(self.edgecolor_volume[index_start:index_end])
        return

    def _set_volume_wick_segments(self, index_start, index_end, simpler):
        if not self.key_volume:
            self.collection_volume.set_segments([])
            return
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


class BaseMixin(CollectionMixin):
    pass

