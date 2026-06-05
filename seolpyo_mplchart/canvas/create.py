import matplotlib.pyplot as plt

from ..models import Figure, AxData


class FigureMixin:
    def get_ax_config_list(self) -> list[AxData]:
        return [
        {
            'name': 'slider',
            'is_px': True,
            'size': 100,
        },
        {
            'name': 'none',
            'is_px': True,
            'size': 40,
        },
        {
            'name': 'legend',
            'is_px': True,
            'size': 60,
        },
        {
            'name': 'price',
            'is_px': False,
            'size': 8,
        },
        {
            'name': 'volume',
            'is_px': False,
            'size': 3,
        },
    ]

    def _get_ax_config_list(self):
        ax_config_list: list[AxData] = self.get_ax_config_list()

        name_set = {config['name'] for config in ax_config_list}

        name_list = []
        for name in [
            'slider', 'none',
            'legend',
            'price', 'volume',
        ]:
            if name not in name_set:
                name_list.append(name)

        if name_list:
            names = ', '.join(name_list)
            msg = 'some Ax Config does not exist.\n  not exist ax config names=' + names
            raise Exception(msg)

        return ax_config_list

    def get_default_figsize(self):
        return (14, 7)

    def create_figure(self):
        ax_config_list = self.get_ax_config_list()
        ax_count = len(ax_config_list) + 2

        self.figure, *_ = plt.subplots(
            ax_count, # row 수
            figsize=self.get_default_figsize(), # 기본 크기
        )
        for ax, ax_config in zip(self.figure.axes, ax_config_list):
            ax.set_label(ax_config['name'])

        return


class AxMixin:
    slider_top: bool

    figure: Figure

    def get_ax_slider_top(self):
        return self.figure.axes[0]

    def get_ax_none_top(self):
        return self.figure.axes[1]

    def get_ax_none_bottom(self):
        return self.figure.axes[-2]

    def get_ax_slider_bottom(self):
        return self.figure.axes[-1]

    def get_ax_slider(self):
        # slider ax 설정
        if self.slider_top:
            ax = self.get_ax_slider_top()
        else:
            ax = self.get_ax_slider_bottom()
        return ax

    def _get_ax(self, name):
        for ax in self.figure.axes[2:-2]:
            label = ax.get_label()
            if label == name:
                return ax
        raise Exception(f'Find Ax Failed.\n    {name=}')

    def get_ax_legend(self):
        return self._get_ax('legend')

    def get_ax_price(self):
        return self._get_ax('price')

    def get_ax_volume(self):
        return self._get_ax('volume')


class CreateMixin(FigureMixin, AxMixin):
    pass

