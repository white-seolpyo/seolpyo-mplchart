from ..._config import ConfigData, SliderConfigData


def set_theme(config: ConfigData|SliderConfigData):
    # axes
    config.FIGURE.facecolor = '#fafafa'
    config.AX.facecolor = '#fafafa'
    config.AX.TICK.edgecolor = 'k'
    config.AX.TICK.fontcolor = 'k'
    config.AX.GRID.color = '#d0d0d0'

    # candle
    config.CANDLE.line_color = 'k'
    config.CANDLE.FACECOLOR.bull_rise = '#FF2400'
    config.CANDLE.FACECOLOR.bull_fall = 'w'
    config.CANDLE.FACECOLOR.bear_fall = '#1E90FF'
    config.CANDLE.FACECOLOR.bear_rise = 'w'

    config.CANDLE.EDGECOLOR.bull_rise = '#FF2400'
    config.CANDLE.EDGECOLOR.bull_fall = '#FF2400'
    config.CANDLE.EDGECOLOR.bear_fall = '#1E90FF'
    config.CANDLE.EDGECOLOR.bear_rise = '#1E90FF'
    config.CANDLE.EDGECOLOR.doji = 'k'

    # volume
    config.VOLUME.FACECOLOR.rise = '#F27663'
    config.VOLUME.FACECOLOR.fall = '#70B5F2'
    config.VOLUME.FACECOLOR.doji = '#BEBEBE'

    config.VOLUME.EDGECOLOR.rise = '#F27663'
    config.VOLUME.EDGECOLOR.fall = '#70B5F2'
    config.VOLUME.EDGECOLOR.doji = '#BEBEBE'

    # ma
    config.MA.color_default = 'k'
    config.MA.color_list = ['#8B00FF', '#008000', '#A0522D', '#008B8B', '#FF0080']
    # text
    config.CURSOR.TEXT.BBOX.facecolor = 'w'
    config.CURSOR.TEXT.BBOX.edgecolor = 'k'
    config.CURSOR.TEXT.color = 'k'

    # box
    config.CURSOR.BOX.edgecolor = 'k'

    # line
    config.CURSOR.CROSSLINE.edgecolor = 'k'

    # wartermark
    config.FIGURE.WATERMARK.color = 'k'

    if getattr(config, 'SLIDER', None):
        config.SLIDER.NAV.edgecolor = '#2962FF'
        config.SLIDER.NAV.facecolor = '#0000002E'

    return config

