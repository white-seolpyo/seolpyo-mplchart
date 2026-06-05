from ...style import Style


def set_theme(style: Style):
    # 캔버스 배경 스타일 변경
    style.CHART.facecolor = '#fafafa'
    style.CHART.edgecolor = 'k'
    style.CHART.fontcolor = 'k'
    style.CHART.GRID.color = '#d0d0d0'

    # 가격 차트 구성 요소 스타일 변경
    style.CHART.PRICE.line_color = 'k'
    style.CHART.PRICE.FACECOLOR.up_rise = '#FF2400'
    style.CHART.PRICE.FACECOLOR.up_fall = 'w'
    style.CHART.PRICE.FACECOLOR.down_fall = '#1E90FF'
    style.CHART.PRICE.FACECOLOR.down_rise = 'w'

    style.CHART.PRICE.EDGECOLOR.up_rise = '#FF2400'
    style.CHART.PRICE.EDGECOLOR.up_fall = '#FF2400'
    style.CHART.PRICE.EDGECOLOR.down_fall = '#1E90FF'
    style.CHART.PRICE.EDGECOLOR.down_rise = '#1E90FF'
    style.CHART.PRICE.EDGECOLOR.flat = 'k'

    # 거래량 차트 구성 요소 스타일 변경
    style.CHART.VOLUME.FACECOLOR.rise = '#F27663'
    style.CHART.VOLUME.FACECOLOR.fall = '#70B5F2'
    style.CHART.VOLUME.FACECOLOR.unchange = '#BEBEBE'

    style.CHART.VOLUME.EDGECOLOR.rise = '#F27663'
    style.CHART.VOLUME.EDGECOLOR.fall = '#70B5F2'
    style.CHART.VOLUME.EDGECOLOR.unchange = '#BEBEBE'

    # 이평선 색상
    style.CHART.MA.color_default = 'k'
    style.CHART.MA.color_list = ['#8B00FF', '#008000', '#A0522D', '#008B8B', '#FF0080']

    # artist
    # 정보 텍스트, 라벨 텍스트 스타일
    style.ARTIST.TEXT.BBOX.facecolor = 'w'
    style.ARTIST.TEXT.BBOX.edgecolor = 'k'
    style.ARTIST.TEXT.color = 'k'

    # 차트 박스 스타일
    style.ARTIST.BOX.edgecolor = 'k'

    # 마우스 위치를 표시하는 선 스타일
    style.ARTIST.CROSSLINE.edgecolor = 'k'

    # 워터마크 색상
    style.ARTIST.WATERMARK.color = 'k'

    # 슬라이더 네비게이터 색상
    style.SLIDER.NAV.edgecolor = '#2962FF'
    style.SLIDER.NAV.facecolor = '#0000002E'

    return style

