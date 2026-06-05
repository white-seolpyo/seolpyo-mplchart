

class MaData:
    "https://matplotlib.org/stable/gallery/color/named_colors.html"
    def __init__(self):
        self.color_default: str|tuple[float, float, float, float] = 'k'
        self.linewidth = 1
        self.ncol = 10
        self.color_list: list[str|tuple[float, float, float, float]] = ['#8B00FF', '#008000', '#A0522D', '#008B8B', '#FF0080']

MA = MaData()

