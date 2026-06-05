from .lim import LimMixin
from .segment import SegmentMixin


class AxisMixn(LimMixin, SegmentMixin):
    def get_visual_indices(self, xmin, xmax, /):
        "조회 영역에 해당하는 index 가져오기"
        if xmin < 0:
            xmin = 0
        if xmax < 1:
            xmax = 1
        xmax += 1

        if xmax < xmin:
            msg = 'xmax < xmin'
            msg += f'  {xmin=:,}'
            msg += f'  {xmax=:,}'
            raise Exception(msg)
        # print(f'{(xmin, xmax)=}')
        return (xmin, xmax)

    def axis(self, x0, x1, /):
        "조회 영역 변경"
        # 조회 영역이 차트 범위를 벗어나지 못하도록 제한
        if x1 < 0 or int(self.df.index[-1]) < x0:
            return

        # 노출 영역에 해당하는 세그먼트 설정
        ind_start, ind_end = self.get_visual_indices(x0, x1)
        # print(f'{(x0, x1)=}')
        self.set_collection_segment(ind_start, ind_end)

        self.axis_chart(x0, x1)
        self.set_collection_nav_segment(x0, x1)

        return

