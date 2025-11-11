

class VolumeFaceColorData:
    def __init__(self):
        self.rise: str|tuple[float, float, float, float] = '#F27663'
        self.fall: str|tuple[float, float, float, float] = '#70B5F2'
        self.doji: str|tuple[float, float, float, float] = '#BEBEBE'

VOLUMEFACECOLOR = VolumeFaceColorData()

class VolumeEdgeColorData:
    def __init__(self):
        self.rise: str|tuple[float, float, float, float] = '#F27663'
        self.fall: str|tuple[float, float, float, float] = '#70B5F2'
        self.doji: str|tuple[float, float, float, float] = '#BEBEBE'

VOLUMEEDGECOLOR = VolumeEdgeColorData()

class VolumeData:
    def __init__(self):
        self.half_width = 0.36
        self.linewidth = 0.7
        self.FACECOLOR = VOLUMEFACECOLOR
        self.EDGECOLOR = VOLUMEEDGECOLOR

VOLUME = VolumeData()

