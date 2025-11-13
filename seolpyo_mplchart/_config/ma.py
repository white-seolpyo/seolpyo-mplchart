

class MaData:
    "https://matplotlib.org/stable/gallery/color/named_colors.html"
    def __init__(self):
        self.color_default: str|tuple[float, float, float, float] = 'k'
        self.format = '{}일선'
        self.linewidth = 1
        self.ncol = 10
        self.color_list: list[str|tuple[float, float, float, float]] = ['#8B00FF', '#008000', '#A0522D', '#008B8B', '#FF0080']
        self.ma_list = (5, 20, 60, 120, 240)

MA = MaData()

MA_EN = MaData()
MA_EN.format = 'ma{}'

