from matplotlib.collections import LineCollection
from matplotlib.text import Text
import pandas as pd

from .._draw import BaseMixin as Base


class ArtistMixin(Base):
    def _add_artists(self):
        super()._add_artists()

        self._add_crosslines()
        self._set_crosslines()

        self._add_label_texts()
        self._set_label_texts()

        self._add_info_texts()
        self._set_info_texts()

        self._add_box_collections()
        self._set_box_collections()
        return

    def _set_artists(self):
        super()._set_artists()

        self._set_crosslines()
        self._set_label_texts()
        self._set_info_texts()
        self._set_box_collections()
        return

    def _add_crosslines(self):
        kwargs = {'segments': [], 'animated': True}

        self.collection_price_crossline = LineCollection(**kwargs)
        self.ax_price.add_artist(self.collection_price_crossline)

        self.collection_volume_crossline = LineCollection(**kwargs)
        self.ax_volume.add_artist(self.collection_volume_crossline)
        return

    def _set_crosslines(self):
        kwargs = self.CONFIG.CURSOR.CROSSLINE.__dict__
        kwargs.update({'segments': [], 'animated': True})

        self.collection_price_crossline.set(**kwargs)
        self.collection_volume_crossline.set(**kwargs)
        return

    def _add_label_texts(self):
        kwargs = {'text': '', 'animated': True, 'horizontalalignment': 'center', 'verticalalignment': 'top'}

        self.artist_text_x = Text(**kwargs)
        self.figure.add_artist(self.artist_text_x)

        kwargs.update({'horizontalalignment': 'left', 'verticalalignment': 'center'})
        self.artist_text_y = Text(**kwargs)
        self.figure.add_artist(self.artist_text_y)
        return

    def _set_label_texts(self):
        kwargs = self.CONFIG.CURSOR.TEXT.to_dict()
        kwargs.update({'text': ' ', 'animated': True, 'horizontalalignment': 'center', 'verticalalignment': 'top'})

        self.artist_text_x.set(**kwargs)

        kwargs.update({'horizontalalignment': 'left', 'verticalalignment': 'center'})
        self.artist_text_y.set(**kwargs)
        return

    def _add_box_collections(self):
        kwargs = {'segments': [], 'animated': True,}

        self.collection_box_price = LineCollection(**kwargs)
        self.ax_price.add_artist(self.collection_box_price)
        self.collection_box_volume = LineCollection(**kwargs)
        self.ax_volume.add_artist(self.collection_box_volume)
        return

    def _set_box_collections(self):
        kwargs = self.CONFIG.CURSOR.BOX.__dict__
        kwargs.update({'segments': [], 'animated': True,})

        self.collection_box_price.set(**kwargs)
        self.collection_box_volume.set(**kwargs)
        return

    def _add_info_texts(self):
        kwargs = {'text': '', 'animated': True, 'horizontalalignment': 'left', 'verticalalignment': 'top',}

        self.artist_info_candle = Text(**kwargs)
        self.ax_price.add_artist(self.artist_info_candle)
        self.artist_info_volume = Text(**kwargs)
        self.ax_volume.add_artist(self.artist_info_volume)
        return

    def _set_info_texts(self):
        kwargs = self.CONFIG.CURSOR.TEXT.to_dict()
        kwargs.update({'text': '', 'animated': True, 'horizontalalignment': 'left', 'verticalalignment': 'top',})

        self.artist_info_candle.set(**kwargs)
        self.artist_info_volume.set(**kwargs)
        return


class DataMixin(ArtistMixin):
    def _set_data(self, df: pd.DataFrame, *args, **kwargs):
        super()._set_data(df, *args, **kwargs)

        self.df['compare'] = (self.df['close'] - self.df['pre_close']).fillna(0)
        self.df['rate'] = (self.df['compare'] * 100 / self.df['pre_close']).__round__(2).fillna(0)
        self.df['rate_open'] = ((self.df['open'] - self.df['pre_close']) * 100 / self.df['pre_close']).__round__(2).fillna(0)
        self.df['rate_high'] = ((self.df['high'] - self.df['pre_close']) * 100 / self.df['pre_close']).__round__(2).fillna(0)
        self.df['rate_low'] = ((self.df['low'] - self.df['pre_close']) * 100 / self.df['pre_close']).__round__(2).fillna(0)
        if self.key_volume:
            self.df['pre_volume'] = self.df['volume'].shift(1)
            self.df['compare_volume'] = (self.df['volume'] - self.df['pre_volume']).fillna(0)
            self.df['rate_volume'] = (self.df['compare_volume'] * 100 / self.df['pre_volume']).__round__(2).fillna(0)

        self.df['space_box_candle'] = (self.df['high'] - self.df['low']) / 5
        self.df['bottom_box_candle'] = self.df['low'] - self.df['space_box_candle']
        self.df['top_box_candle'] = self.df['high'] + self.df['space_box_candle']
        self.df['height_box_candle'] = self.df['top_box_candle'] - self.df['bottom_box_candle']
        if self.key_volume: self.df['max_box_volume'] = self.df['volume'] * 1.15

        self._set_label_texts_position()
        return

    def _refresh(self):
        super()._refresh()
        
        self._set_label_texts_position()
        return

    def _axis(self, xmin, xmax, simpler=False, draw_ma=True):
        super()._axis(xmin, xmax=xmax, simpler=simpler, draw_ma=draw_ma)

        psub = (self.price_ymax - self.price_ymin)
        self.min_height_box_candle = psub / 8

        pydistance = psub / 20

        self.min_height_box_volume = 10
        if self.key_volume:
            self.min_height_box_volume = self.key_volume_ymax / 4

        vxsub = self.vxmax - self.vxmin
        self.vmiddle = self.vxmax - int((vxsub) / 2)

        vxdistance = vxsub / 50
        self.v0, self.v1 = (self.vxmin + vxdistance, self.vxmax - vxdistance)

        yvolume = self.key_volume_ymax * 0.85

        # 정보 텍스트박스 y축 설정
        self.artist_info_candle.set_y(self.price_ymax - pydistance)
        self.artist_info_volume.set_y(yvolume)

        return

    def _set_label_texts_position(self):
        self._set_label_x_position()
        self._set_label_y_position()
        return

    def _set_label_x_position(self):
        renderer = getattr(self.figure.canvas, 'renderer', None)
        if not renderer:
            renderer

        # Axes 우측 경계 좌표
        x1 = self.ax_price.get_position().x1
        # Text bbox 너비
        bbox = self.artist_text_y.get_bbox_patch()\
            .get_window_extent(renderer)
        bbox_width = bbox.width
        # 밀어야 하는 x값
        fig_width = self.figure.bbox.width
        # fig_width = self.figure.get_size_inches()[0] * self.figure.dpi
        box_width_fig = (bbox_width+14) / fig_width
        # print(f'{box_width_fig=}')

        # x축 값(가격 또는 거래량)
        # self.artist_text_y.set_x(x1)
        x = x1 + (box_width_fig / 2)
        # print(f'{(x1, x)=}')
        self.artist_text_y.set_x(x)
        return

    def _set_label_y_position(self):
        renderer = getattr(self.figure.canvas, 'renderer', None)
        if not renderer:
            return

        # Axes 하단 경계 좌표
        y0 = self.ax_volume.get_position().y0
        # Text bbox 높이
        bbox = self.artist_text_x.get_bbox_patch()\
            .get_window_extent(renderer)
        height_px = bbox.height
        # print(f'{height_px=}')
        # 밀어야 하는 y값
        fig_height_px = self.figure.bbox.height
        box_height_fig = (height_px+14) / fig_height_px

        # y축 값(날짜)
        y = y0 - (box_height_fig/2)
        # print(f'{(y0, y)=}')
        self.artist_text_x.set_y(y)
        return


class BaseMixin(DataMixin):
    pass

