import matplotlib.pyplot as plt
import matplotlib.style as mplstyle
from matplotlib.axes import Axes
from matplotlib.backends.backend_agg import FigureCanvasAgg


from .utils import convert_unit


try: plt.switch_backend('TkAgg')
except: pass

# 한글 깨짐 문제 방지
try: plt.rcParams['font.family'] ='Malgun Gothic'
except: pass

mplstyle.use('fast')


class Base:
    canvas: FigureCanvasAgg
    unit_price, unit_volume = ('원', '주')

    figsize = (12, 6)
    ratio_ax_slider, ratio_ax_legend, ratio_ax_price, ratio_ax_volume = (3, 2, 18, 5)
    adjust = dict(
        top=0.95, bottom=0.05, left=0.01, right=0.93, # 여백
        wspace=0, hspace=0  # 플롯간 간격
    )
    color_grid = '#d0d0d0'
    color_background = '#fafafa'

    slider_top = True
    title = 'seolpyo mplchart'

    def __init__(self, *args, **kwargs):
        # 기본 툴바 비활성화
        plt.rcParams['toolbar'] = 'None'

        self._set_plot()
        return

    def _set_plot(self):
        if self.slider_top:
            fig, ax = plt.subplots(
                4, # row 수
                figsize=self.figsize, # 기본 크기
                height_ratios=(self.ratio_ax_slider, self.ratio_ax_legend, self.ratio_ax_price, self.ratio_ax_volume) # row 크기 비율
            )
            ax: list[Axes]
            ax_slider, ax_legend, ax_price, ax_volume = ax
        else:
            fig, ax = plt.subplots(
                5, # row 수
                figsize=self.figsize, # 기본 크기
                height_ratios=(self.ratio_ax_legend, self.ratio_ax_price, self.ratio_ax_volume, self.ratio_ax_legend, self.ratio_ax_slider) # row 크기 비율
            )
            ax: list[Axes]
            ax_legend, ax_price, ax_volume, ax_none, ax_slider = ax
            # 사용하지 않는 axes 숨기기
            ax_none.axis('off')
        ax_legend.axis('off')

        ax_slider.xaxis.set_animated(True)
        ax_slider.yaxis.set_animated(True)

        ax_price.xaxis.set_animated(True)
        ax_price.yaxis.set_animated(True)

        ax_volume.xaxis.set_animated(True)
        ax_volume.yaxis.set_animated(True)

        fig.canvas.manager.set_window_title(f'{self.title}')

        # 플롯간 간격 제거(Configure subplots)
        fig.subplots_adjust(**self.adjust)

        # y ticklabel foramt 설정
        ax_slider.yaxis.set_major_formatter(lambda x, _: convert_unit(x, word=self.unit_price))
        ax_price.yaxis.set_major_formatter(lambda x, _: convert_unit(x, word=self.unit_price))
        ax_volume.yaxis.set_major_formatter(lambda x, _: convert_unit(x, word=self.unit_volume))

        # 공통 설정
        for a in [ax_slider, ax_price, ax_volume]:
            # y tick 우측으로 이동
            a.tick_params(left=False, right=True, labelleft=False, labelright=True)
            # 차트 영역 배경 색상
            a.set_facecolor(self.color_background)
            # grid(구분선, 격자) 그리기
            a.grid(True, color=self.color_grid, linewidth=1)
            # x tick 제거
            a.set_xticklabels([])

        self.fig, self.canvas = (fig, fig.canvas)
        self.ax_slider, self.ax_legend, self.ax_price, self.ax_volume = (ax_slider, ax_legend, ax_price, ax_volume)

        return self.set_plot()

    def set_plot(self):
        "This function works after set plot process is done."
        return


class Chart(Base):
    pass


if __name__ == '__main__':
    Base()
    
    plt.show()
