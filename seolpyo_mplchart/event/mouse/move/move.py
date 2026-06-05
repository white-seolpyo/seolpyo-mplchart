from matplotlib.backend_bases import MouseEvent
from matplotlib.collections import LineCollection
import pandas as pd


class ChartMoveMixin:
    collection_slider_vline: LineCollection

    df: pd.DataFrame

    in_chart: bool
    in_slider: bool

    is_click_chart: bool
    is_click_slider: bool
    is_move_chart: bool

    _click_nav_side: str

    _click_x_coord: int

    def _move_chart(self, e: MouseEvent):
        ind_end = int(self.df.index[-1]) + 1

        if self.is_click_chart and self.in_chart:
            xdata = int(e.xdata)
            # print(f'{(self._click_x_coord, xdata)=}')
            xsub = self._click_x_coord - xdata
            if xsub:
                pre_xmin, pre_xmax = self._nav_x_coords
                xmin, xmax = (pre_xmin+xsub, pre_xmax+xsub)
                # print(f'{(xmin, xmax)=}')
                if 0 <= xmax and xmin <= ind_end and xmin != xmax:
                    self.axis(xmin, xmax)
                    self._nav_x_coords = (xmin, xmax)

        elif self.is_click_slider and self.in_slider:
            xdata = round(e.xdata)
            pre_xmin, pre_xmax = self._nav_x_coords
            if self.is_move_chart:
                xsub = self._click_x_coord - xdata
                xmax = -1
                if xsub:
                    pre_xmin, pre_xmax = self._nav_x_coords
                    xmin, xmax = (pre_xmin-xsub, pre_xmax-xsub)

            elif self._click_nav_side:
                match self._click_nav_side:
                    case 'left':
                        if xdata < pre_xmax:
                            xmin, xmax = (xdata, pre_xmax)
                        else:
                            xmin, xmax = (pre_xmax, xdata)
                    case 'right':
                        if xdata < pre_xmin:
                            xmin, xmax = (xdata, pre_xmin)
                        else:
                            xmin, xmax = (pre_xmin, xdata)

            else:
                if xdata == self._click_x_coord:
                    xmax = -1
                elif xdata < self._click_x_coord:
                    xmin, xmax = (xdata, self._click_x_coord)
                else:
                    xmin, xmax = (self._click_x_coord, xdata)
    
            if 0 <= xmax and xmin <= ind_end and xmin != xmax:
                self.axis(xmin, xmax)
        return

