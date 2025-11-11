from ..._config import ConfigData, SliderConfigData


def set_theme(config: ConfigData|SliderConfigData):
    # axes
    config.FIGURE.facecolor = '#0f0f0f'
    config.AX.facecolor = '#0f0f0f'
    config.AX.TICK.edgecolor = '#dbdbdb'
    config.AX.TICK.fontcolor = '#dbdbdb'
    config.AX.GRID.color = '#1c1c1c'

    # candle
    config.CANDLE.line_color = 'w'
    config.CANDLE.FACECOLOR.bull_rise = '#089981'
    config.CANDLE.FACECOLOR.bull_fall = '#0f0f0f'
    config.CANDLE.FACECOLOR.bear_fall = '#f23645'
    config.CANDLE.FACECOLOR.bear_rise = '#0f0f0f'

    config.CANDLE.EDGECOLOR.bull_rise = '#089981'
    config.CANDLE.EDGECOLOR.bull_fall = '#089981'
    config.CANDLE.EDGECOLOR.bear_fall = '#f23645'
    config.CANDLE.EDGECOLOR.bear_rise = '#f23645'
    config.CANDLE.EDGECOLOR.doji = 'w'

    # volume
    config.VOLUME.FACECOLOR.rise = '#2A8076'
    config.VOLUME.FACECOLOR.fall = '#BE4F58'
    config.VOLUME.FACECOLOR.doji = '#82828A'

    config.VOLUME.EDGECOLOR.rise = '#2A8076'
    config.VOLUME.EDGECOLOR.fall = '#BE4F58'
    config.VOLUME.EDGECOLOR.doji = '#82828A'

    # ma
    config.MA.color_default = 'w'
    config.MA.color_list = ['#FFB300', '#03A9F4', '#AB47BC', '#8BC34A', '#EF5350']

    # text
    config.CURSOR.TEXT.BBOX.facecolor = '#3d3d3d'
    config.CURSOR.TEXT.BBOX.edgecolor = '#ffffff'
    config.CURSOR.TEXT.color = '#ffffff'

    # box
    config.CURSOR.BOX.edgecolor = 'w'

    # line
    config.CURSOR.CROSSLINE.edgecolor = '#9c9c9c'

    # wartermark
    config.FIGURE.WATERMARK.color = 'w'

    if getattr(config, 'SLIDER', None):
        config.SLIDER.NAV.edgecolor = "#00A6FF"
        config.SLIDER.NAV.facecolor = '#FFFFFF4D'

    return config

