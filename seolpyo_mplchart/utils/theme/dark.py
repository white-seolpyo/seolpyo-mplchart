from ...style import Style


def set_theme(style: Style):
    # change canvas style
    style.CHART.facecolor = '#0f0f0f'
    style.CHART.edgecolor = '#dbdbdb'
    style.CHART.fontcolor = '#dbdbdb'
    style.CHART.GRID.color = '#1c1c1c'

    # change price chart element style
    style.CHART.PRICE.line_color = 'w'
    style.CHART.PRICE.FACECOLOR.up_rise = '#089981'
    style.CHART.PRICE.FACECOLOR.up_fall = '#0f0f0f'
    style.CHART.PRICE.FACECOLOR.down_fall = '#f23645'
    style.CHART.PRICE.FACECOLOR.down_rise = '#0f0f0f'

    style.CHART.PRICE.EDGECOLOR.up_rise = '#089981'
    style.CHART.PRICE.EDGECOLOR.up_fall = '#089981'
    style.CHART.PRICE.EDGECOLOR.down_fall = '#f23645'
    style.CHART.PRICE.EDGECOLOR.down_rise = '#f23645'
    style.CHART.PRICE.EDGECOLOR.flat = 'w'

    # change volume chart element style
    style.CHART.VOLUME.FACECOLOR.rise = '#2A8076'
    style.CHART.VOLUME.FACECOLOR.fall = '#BE4F58'
    style.CHART.VOLUME.FACECOLOR.unchange = '#82828A'

    style.CHART.VOLUME.EDGECOLOR.rise = '#2A8076'
    style.CHART.VOLUME.EDGECOLOR.fall = '#BE4F58'
    style.CHART.VOLUME.EDGECOLOR.unchange = '#82828A'

    # change ma line color style
    style.CHART.MA.color_default = 'w'
    style.CHART.MA.color_list = ['#FFB300', '#03A9F4', '#AB47BC', '#8BC34A', '#EF5350']

    # artist
    # chage info text, label style
    style.ARTIST.TEXT.BBOX.facecolor = '#3d3d3d'
    style.ARTIST.TEXT.BBOX.edgecolor = '#ffffff'
    style.ARTIST.TEXT.color = '#ffffff'

    # change chart box style
    style.ARTIST.BOX.edgecolor = 'w'

    # change crossline style
    style.ARTIST.CROSSLINE.edgecolor = '#9c9c9c'

    # change watermark color
    style.ARTIST.WATERMARK.color = 'w'

    # change slider nav color
    style.SLIDER.NAV.edgecolor = '#00A6FF'
    style.SLIDER.NAV.facecolor = '#FFFFFF4D'

    return style

