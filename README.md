# Donation
Bitcoin: 1MKCHW8smDZv5DFMiVkA5G3DeXcMn871ZX

Ethereum: 0x1c5fb8a5e0b1153cd4116c91736bd16fabf83520


# Document
[English Document](https://github.com/white-seolpyo/seolpyo-mplchart/blob/main/README.md)

[한글 설명서](https://white.seolpyo.com/entry/147/?from=github)


# This document was originally written in Korean and translated using a machine translation tool.


reference version
----

2.0.0

Package Introduction
------

![](https://github.com/white-seolpyo/seolpyo-mplchart/blob/main/images/candle.png?raw=true)![](https://github.com/white-seolpyo/seolpyo-mplchart/blob/main/images/40000.gif?raw=true)

Sample Charts with Over 40,000 Stock Price Data Points

seolpyo-mplchart is a Python package built on top of matplotlib.

While libraries like finplot and plotly are commonly used to draw candlestick charts in Python, I created this package because none of the existing tools fully met my needs.



**Key Features**

* Provides three types of Chart classes for flexible charting.
* Includes an overview slider (SliderChart) that highlights the visible range, allowing users to select or move the viewing window interactively.
* Integrates smoothly with various GUI frameworks, including tkinter, ensuring responsive performance.
* Displays stock price information as text (CursorChart, SliderChart). Simply hover your mouse over a candlestick or volume bar to view the corresponding data.
- Built-in support for toggling moving average lines on and off.

![](https://github.com/white-seolpyo/seolpyo-mplchart/blob/main/images/ma%20on%20off.gif?raw=true)

You can check out a sample of drawing candlestick charts integrated with tkinter at the following link:

[View tkinter sample code](https://white.seolpyo.com//entry/214/)

![](https://github.com/white-seolpyo/seolpyo-mplchart/blob/main/images/with%20tkinter.gif?raw=true)

✅ Verified to work with 32-bit Python 3.11, pandas 2.0.0, and matplotlib 3.7.0.

Installation
-----

    > pip install seolpyo-mplchart

Quick Start
-----

### OnlyChart

It is a chart that simply renders without any interaction.

    import seolpyo_mplchart as mc
    
    chart = mc.OnlyChart()
    df: pandas.DataFrame = {stock price data frame}
    chart.set_data(df)
    mc.show()
    

![](https://github.com/white-seolpyo/seolpyo-mplchart/blob/main/images/chart%20only.png?raw=true)

### CursorChart

This chart is an enhanced version of OnlyChart with mouse interaction capabilities.
It displays the date information corresponding to the mouse cursor position at the bottom of the chart, and price or volume data on the right side.
When the mouse cursor hovers over a candlestick or volume bar, the relevant information is shown as text.


    import seolpyo_mplchart as mc
    
    chart = mc.CursorChart()
    df: pandas.DataFrame = {stock price data frame}
    chart.set_data(df)
    mc.show()
    

![](https://github.com/white-seolpyo/seolpyo-mplchart/blob/main/images/chart%20cursor.png?raw=true)

### SliderChart

This chart is an extended version of CursorChart with an added overview slider.
The slider allows users to select or move the viewing range, and users can also click and drag within the chart area to shift the visible region.


    import seolpyo_mplchart as mc
    
    chart = mc.SliderChart()
    df: pandas.DataFrame = {stock price data frame}
    chart.set_data(df)
    mc.show()
    

![](https://github.com/white-seolpyo/seolpyo-mplchart/blob/main/images/sample.gif?raw=true)

Chart Description
--------

### Chart Class Variables

#### CONFIG

Chart Configuration File
If not provided, the predefined CONFIG\* settings will be used.

\* CONFIG: mc.DEFAULTCONFIG(OnlyChart, CursorChart) 또는 mc.SLIDERCONFIG(SliderChart)


#### wartermark

Watermark text displayed at the center of the chart.
If if not self.wartermark evaluates to true, the watermark will not be rendered.


#### candle\_on\_ma

If true, candlesticks are drawn above the moving average line.
If false, candlesticks are drawn below the moving average line, as shown in the following image.


![](https://github.com/white-seolpyo/seolpyo-mplchart/blob/main/images/ma%20above%20candle.png?raw=true)

#### limit\_candle

If the number of candlesticks to be drawn on the screen is less than or equal to this value, full candlesticks are rendered.
If it exceeds the value, only wicks are drawn.


![](https://github.com/white-seolpyo/seolpyo-mplchart/blob/main/images/wick.png?raw=true)

#### limit\_wick

If the number of candlesticks to be drawn on the screen is less than or equal to this value, only wicks are rendered.
If it exceeds the value, a line chart is drawn instead.


![](https://github.com/white-seolpyo/seolpyo-mplchart/blob/main/images/line.png?raw=true)

#### limit\_volume

If the number of candlesticks drawn on the screen is less than or equal to self.limit_wick, the entire volume data is rendered.
If it exceeds that value, only a subset of volume data is drawn — specifically, the top limit_volume entries sorted in descending order of volume.
If you experience buffering when moving across a wide range, lowering this value may help improve performance.


#### limit\_ma

If the number of candlesticks drawn on the screen is less than or equal to this value, the moving average line is rendered.
If you experience buffering when navigating across a wide range, lowering this value may help improve performance.


#### key\_date, key\_open, key\_high, key\_low, key\_close, key\_volume

Keys for each column used in the provided data
If if not self.key_volume evaluates to true at the time of executing Chart.set_data(df), the volume chart will not be rendered.


    import seolpyo_mplchart as mc
    
    df: pandas.DataFrame = {stock price data frame}
    
    c = mc.SliderChart()
    c.key_date= '시간'
    c.key_open = '시가'
    c.key_high = '고가'
    c.key_low = '저가'
    c.key_close = '종가'
    # c.key_volume = '거래량'
    c.key_volume = None
    c.set_data(df)
    
    mc.show() # same as matplotlib.pyplot.show()
    
    
    ### OR ###
    
    
    import json
    
    import seolpyo_mplchart as mc
    import pandas as pd
    
    file = {stock price data path}
    with open(file, 'r', encoding='utf-8') as txt:
        data = json.load(txt)
    df = pd.DataFrame(data)
    
    class Chart(mc.SliderChart):
      key_date = '시간'
      key_open, key_high, key_low, key_close = ('시가', '고가', '저가', '종가')
      # key_volume = '거래량'
      key_volume = None
    
    c = Chart()'
    c.set_data(df)
    
    mc.show() # same as matplotlib.pyplot.show()
    
    

![](https://github.com/white-seolpyo/seolpyo-mplchart/blob/main/images/en%20no%20vol%20(2).png?raw=true)

#### fraction

If true, decimal values are displayed as fractions.

![](https://github.com/white-seolpyo/seolpyo-mplchart/blob/main/images/fraction.png?raw=true)

#### slider\_top

If true, the slider is positioned above the chart.

![](https://github.com/white-seolpyo/seolpyo-mplchart/blob/main/images/slider%20bottom.png?raw=true)

#### min\_distance

Minimum number of candlesticks required when selecting a slider range
If the selected range contains fewer candlesticks than this value, the previous range will be retained.


![](https://github.com/white-seolpyo/seolpyo-mplchart/blob/main/images/min%20distance.gif?raw=true)

#### in\_chart

Determines whether the mouse cursor is located within the price chart or volume chart area.


#### in\_slider

Determines whether the mouse cursor is located within the slider area.


#### in\_price\_chart

Determines whether the mouse cursor is located within the price chart area.


#### in\_volume\_chart

Determines whether the mouse cursor is located within the volume chart area.


### Chart class method
#### Chart.\_\_init\_\_(config=DEFAULTCONFIG or SLIDERCONFIG)

Creates a chart object.

#### Chart.set\_data(df)

Passes stock price data to the chart object.
The chart object generates chart data based on the received input.
When retrieving data from a DataFrame, the predefined keys — Chart.key\_date, Chart.key\_open, Chart.key\_high, Chart.key\_low, Chart.key\_close, and Chart.key\_volume — are used.
Therefore, these keys should be properly set before calling set\_data.


#### Chart.refresh()

Refreshes the chart.
During the refresh, any changes made to self.CONFIG are applied.


#### Chart.add\_artists()

Function that adds the Artists used in the chart. Called during initialization (init).


#### Chart.draw\_artists()

Function that renders the Artists on the chart.
Called when the on_draw event is triggered.


#### Chart.set\_artists()

Function that applies the settings of chart Artists.
Called during refresh.


#### Chart.set\_collections()

Function that applies the settings of candlestick and volume chart Artists.
Called during refresh or when the display area changes.


#### Chart.add\_candle\_color\_column(), Chart.add\_volume\_color\_column()

This method determines the colors of candlesticks and volume bars drawn on the chart.
It adds the following columns to self.df:
- ['facecolor', 'edgecolor'] for candlesticks
- ['facecolor_volume', 'edgecolor_volume'] for volume bars
By modifying the values in these columns, you can customize the colors as desired.


##### Candlestick Colors
- Open < Close, Previous Close < Close
→ self.CONFIG.CANDLE.FACECOLOR.bull_rise, self.CONFIG.CANDLE.EDGECOLOR.bull_rise
- Open < Close, Previous Close > Close
→ self.CONFIG.CANDLE.FACECOLOR.bull_fall, self.CONFIG.CANDLE.EDGECOLOR.bull_fall
- Close < Open, Close < Previous Close
→ self.CONFIG.CANDLE.FACECOLOR.bear_fall, self.CONFIG.CANDLE.EDGECOLOR.bear_fall
- Close < Open, Close > Previous Close
→ self.CONFIG.CANDLE.FACECOLOR.bear_rise, self.CONFIG.CANDLE.EDGECOLOR.bear_rise
- Open == Close
→ self.CONFIG.CANDLE.EDGECOLOR.doji




##### Volume Bar Colors
- Previous Close < Current Close
→ self.CONFIG.VOLUME.FACECOLOR.rise, self.CONFIG.VOLUME.EDGECOLOR.rise
- Previous Close > Current Close
→ self.CONFIG.VOLUME.FACECOLOR.fall, self.CONFIG.VOLUME.EDGECOLOR.fall
- Previous Close == Current Close
→ self.CONFIG.VOLUME.FACECOLOR.doji, self.CONFIG.VOLUME.EDGECOLOR.doji




#### Chart.get\_cnadle\_segment(x, left, right, top, bottom, is\_up, high, low)

This method is provided to modify the appearance of candlesticks drawn on the chart.


    import pandas as pd
    import seolpyo_mplchart as mc
    
    class Chart(mc.SliderChart):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.collection_candle.set_linewidth(1.5)
            return
    
        def get_candle_segment(self, *, x, left, right, top, bottom, is_up, high, low):
            if is_up:
                return (
                    (x, high),
                    (x, top), (right, top), (x, top),
                    (x, bottom), (left, bottom),
                    (x, bottom), (x, low), (x, high)
                )
            else:
                return (
                    (x, high),
                    (x, bottom), (right, bottom), (x, bottom),
                    (x, top), (left, top), (x, top),
                    (x, low), (x, high)
                )
    
    
    C = Chart()
    
    data = {stock price data}
    df = pd.DataFrame(data)
    
    C.set_data(df)
    
    mc.show()

![](https://github.com/white-seolpyo/seolpyo-mplchart/blob/main/images/en%20bar%20chart.png?raw=true)

### Chart.get\_info\_kwargs(is\_price, \*\*kwargs)

You can modify or add the data displayed in the text box using the get_info_kwargs method.
The **kwargs parameter receives predefined keyword arguments.

If you'd like, I can help format this as a docstring or comment for your code. For example:
Allows customization of the data shown in the text box.
Predefined keyword arguments are passed via **kwargs.


    import pandas as pd
    import seolpyo_mplchart as mc
    
    
    class Chart(mc.SliderChart):
        format_candleinfo = mc.format_candleinfo_ko + '\nCustom info: {ci}'
    
        def get_info_kwargs(self, is_price, **kwargs):
            if is_price:
                kwargs['ci'] = 'You can add Custom text Info or Change text info.'
                kwargs['close'] = 'You can Change close price info.'
            return kwargs
    
    C = Chart()
    data = {stock price data}
    df = pd.DataFrame(data)
    
    C.set_data(df)
    
    mc.show()

#### Chart.on\_draw(e)

Method called when the draw event is triggered.
Only invoked in CursorChart and SliderChart.


#### Chart.on\_resize(e)

Method called when the resize event is triggered.
Only invoked in SliderChart.


#### Chart.on\_pick(e)

Method called when the pick event is triggered.


#### Chart.on\_move(e)

Method called when a mouse movement event occurs.
Only invoked in CursorChart and SliderChart.


#### Chart.on\_click(e)

Method called when a mouse click event occurs.

Only invoked in SliderChart.

#### Chart.on\_release(e)

Method called when a mouse release event occurs.

Only invoked in SliderChart.

### CONFIG

A configuration that includes setting class objects such as FIGURE, AX, FORMAT, UNIT, CURSOR, CANDLE, VOLUME, MA, and SLIDER.


### DEFAULTCONFIG

CONFIG applied to OnlyChart and CursorChart.


### DEFAULTCONFIG\_EN

CONFIG applied to OnlyChart and CursorChart, with the price unit set to $, the volume unit set to Vol, and the formatting based on English conventions.


### SLIDERCONFIG

CONFIG applied to SliderChart.


### SLIDERCONFIG\_EN

CONFIG applied to SliderChart, with the price unit set to $, the volume unit set to Vol, and the formatting based on English conventions.


    # seolpyo_mplchart/_config/slider/config.py
    
    from .. import config
    from .figure import FIGURE, SliderFigureData
    from .nav import NAVIGATOR
    
    
    class SliderData:
        def __init__(self):
            self.NAVIGATOR = NAVIGATOR
    
    SLIDER = SliderData()
    
    class SliderConfigData(config.ConfigData):
        FIGURE: SliderFigureData
        SLIDER: SliderData
    
    
    SLIDERCONFIG: SliderConfigData = config.DEFAULTCONFIG
    SLIDERCONFIG.FIGURE = FIGURE
    SLIDERCONFIG.SLIDER = SLIDER
    
    SLIDERCONFIG_EN: SliderConfigData = config.DEFAULTCONFIG_EN
    SLIDERCONFIG_EN.FIGURE = FIGURE
    SLIDERCONFIG_EN.SLIDER = SLIDER
    
    

    # seolpyo_mplchart/_config/config.py
    
    from . import figure, ax, candle, volume, ma, unit, cursor, format
    
    
    class ConfigData:
        def __init__(self):
            self.FIGURE = figure.FIGURE
            self.UNIT = unit.UNIT
            self.AX = ax.AX
            self.CANDLE = candle.CANDLE
            self.VOLUME = volume.VOLUME
            self.MA = ma.MA
            self.CURSOR = cursor.CURSOR
            self.FORMAT = format.FORMAT
    
    DEFAULTCONFIG = ConfigData()
    
    DEFAULTCONFIG_EN = ConfigData()
    DEFAULTCONFIG_EN.UNIT = unit.UNIT_EN
    DEFAULTCONFIG_EN.MA = ma.MA_EN
    DEFAULTCONFIG_EN.FORMAT = format.FORMAT_EN
    
    

# Others

---

# Required data
-------

A chart object must be provided with a DataFrame that contains the following columns:
[timestamp, open, high, low, close, volume]


## How to Change Language and Text Format
The default language is Korean.
If needed, you can change the units for price and volume, and customize the text format to match your preferred style.


### How to Change Display Units

![](https://github.com/white-seolpyo/seolpyo-mplchart/blob/main/images/en%20no%20vol%20(2).png?raw=true)

The price and volume units, as well as the number of decimal places for price and volume, are managed in CONFIG.UNIT.

    from .utils import convert_unit, convert_unit_en
    # seolpyo_mplchart._config.unit.py
    
    class UnitData:
        def __init__(self):
            self.price = '원'
            self.volume = '주'
            self.digit = 0
            self.digit_volume = 0
            self.func = convert_unit
    
    UNIT = UnitData()
    
    UNIT_EN = UnitData()
    UNIT_EN.price = ' $'
    UNIT_EN.volume = ' Vol'
    UNIT_EN.digit = 2
    UNIT_EN.func = convert_unit_en
    
    

### How to Change the Information Text Format

![](https://github.com/white-seolpyo/seolpyo-mplchart/blob/main/images/en%20no%20vol%20(2).png?raw=true)![](https://github.com/white-seolpyo/seolpyo-mplchart/blob/main/images/kor%20vol.png?raw=true)

You can customize the name of the price moving average line and the text displayed in the information box.
Text formatting is managed through CONFIG.FORMAT.
Additional kwargs for customizing the text can be passed via the chart’s get_info_kwargs method.


    # seolpyo_mplchart/_config/format.py
    
    format_candleinfo_ko = """\
    {dt}
    
    종가:　 {close}
    등락률: {rate}
    대비:　 {compare}
    시가:　 {open}({rate_open})
    고가:　 {high}({rate_high})
    저가:　 {low}({rate_low})
    거래량: {volume}({rate_volume})\
    """
    format_volumeinfo_ko = """\
    {dt}
    
    거래량:　　　 {volume}
    거래량증가율: {rate_volume}
    대비:　　　　 {compare}\
    """
    
    class FormatData:
        def __init__(self):
            self.candle = format_candleinfo_ko
            self.volume = format_volumeinfo_ko
    
    FORMAT = FormatData()
    
    format_candleinfo_en = """\
    {dt}
    
    close:      {close}
    rate:        {rate}
    compare: {compare}
    open:      {open}({rate_open})
    high:       {high}({rate_high})
    low:        {low}({rate_low})
    volume:  {volume}({rate_volume})\
    """
    format_volumeinfo_en = """\
    {dt}
    
    volume:      {volume}
    volume rate: {rate_volume}
    compare:     {compare}\
    """
    
    FORMAT_EN = FormatData()
    FORMAT_EN.candle = format_candleinfo_en
    FORMAT_EN.volume = format_volumeinfo_en
    
    

How to Change Chart Style
-----------

![](https://github.com/white-seolpyo/seolpyo-mplchart/blob/main/images/theme%20light.png?raw=true)![](https://github.com/white-seolpyo/seolpyo-mplchart/blob/main/images/theme%20dark.png?raw=true)

Since I prefer a white background, the default chart style is set to light mode.
If you want to change the chart style, simply modify the color values defined in CONFIG.
A function named set_theme has been created to switch between light and dark themes.
You can either use this function directly, or check which values it modifies and adjust them to suit your preferences.


    import json
    
    import seolpyo_mplchart as mc
    import pandas as pd
    
    
    class Chart(mc.SliderChart):
        def __init__(self, config, *args, **kwargs):
            config = mc.set_theme(config, theme='dark')
    
    
    file = {stock price data path}
    with open(file, 'r', encoding='utf-8') as txt:
        data = json.load(txt)
    df = pd.DataFrame(data)
    
    c = Chart()
    c.set_data(df)
    
    mc.show()
    

How to Change Chart Aspect Ratio
--------

![](https://github.com/white-seolpyo/seolpyo-mplchart/blob/main/images/ratio.png?raw=true)

You can adjust the proportions of each chart area using the values of
ratio_ax_slider, ratio_ax_legend, ratio_ax_price, ratio_ax_volume, and ratio_ax_none.
Note: ratio_ax_none is only used when the value of slider_top is set to False.


    # seolpyo_mplchart/_config/slider/figure.py
    
    
    class RatioData:
        def __init__(self):
            self.legend = 2
            self.price = 18
            self.volume = 5
            self.slider = 3
            self.none = 2
    
    RATIO = RatioData()
    
    class SliderFigureData(figure.FigureData):
        def __init__(self):
            super().__init__()
            self.RATIO: RatioData = RATIO
    
    FIGURE = SliderFigureData()
