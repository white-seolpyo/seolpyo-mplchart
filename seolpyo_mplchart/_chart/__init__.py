import pandas as pd

from .cursor import Chart as _CC, BaseChart as _OC
from .slider import Chart as _SC


class OnlyChart(_OC):
    r"""
    You can see the guidance document:
        Korean: https://white.seolpyo.com/entry/147/?from=package
        English: https://github.com/white-seolpyo/seolpyo-mplchart

    Quick Start:
        ```
        import seolpyo_mplchart as mc
        chart = mc.SliderChart() # Create instance
        chart.set_data(df) # set stock price data
        mc.show() # show chart(run ```matplotlib.pyplot.show()```)
        mc.close() # run ```matplotlib.pyplot.close('close')```
        ```

    Class Variables:
        df: stock data DataFrame.
        key_date: date column key. default 'date'
        key_open, key_high, key_low, key_close: price column key. default ('open', 'high', 'low', 'close')
        key_volume: volume column key. default 'volume'. If ```if config.VOLUME.EDGECOLOR.volume``` is ```False```, the volume chart is not drawn.

        candle_on_ma: if True: draw candle above ma. else: draw candle below ma lines.

        limit_candle: If (`the number of candles to draw < limit_candle or not limit_candle`): draw candles, else: draw wicks.
        limit_wick: If (`the number of candles to draw < limit_wick or not limit_wick`): draw wicks, else: draw line.

        watermark: watermark text.
    """
    df: pd.DataFrame

    key_date = 'date'
    key_open, key_high, key_low, key_close = ('open', 'high', 'low', 'close')
    key_volume = 'volume'

    candle_on_ma = True

    watermark = 'seolpyo mplchart'

    limit_candle = 400
    limit_wick = 2_000


class CursorChart(_CC):
    r"""
    You can see the guidance document:
        Korean: https://white.seolpyo.com/entry/147/?from=package
        English: https://github.com/white-seolpyo/seolpyo-mplchart

    Quick Start:
        ```
        import seolpyo_mplchart as mc
        chart = mc.SliderChart() # Create instance
        chart.set_data(df) # set stock price data
        mc.show() # show chart(run ```matplotlib.pyplot.show()```)
        mc.close() # run ```matplotlib.pyplot.close('close')```
        ```

    Class Variables:
        df: stock data DataFrame.
        key_date: date column key. default 'date'
        key_open, key_high, key_low, key_close: price column key. default ('open', 'high', 'low', 'close')
        key_volume: volume column key. default 'volume'. If ```if config.VOLUME.EDGECOLOR.volume``` is ```False```, the volume chart is not drawn.

        candle_on_ma: if True: draw candle above ma. else: draw candle below ma lines.
        fraction: if True and number has a fractional part, display it as a fraction.

        limit_candle: If (`the number of candles to draw < limit_candle or not limit_candle`): draw candles, else: draw wicks.
        limit_wick: If (`the number of candles to draw < limit_wick or not limit_wick`): draw wicks, else: draw line.

        watermark: watermark 
    """
    df: pd.DataFrame

    key_date = 'date'
    key_open, key_high, key_low, key_close = ('open', 'high', 'low', 'close')
    key_volume = 'volume'

    candle_on_ma = True
    fraction = False

    watermark = 'seolpyo mplchart'

    limit_candle = 400
    limit_wick = 2_000


class SliderChart(_SC):
    r"""
    You can see the guidance document:
        Korean: https://white.seolpyo.com/entry/147/?from=package
        English: https://github.com/white-seolpyo/seolpyo-mplchart

    Quick Start:
        ```
        import seolpyo_mplchart as mc
        chart = mc.SliderChart() # Create instance
        chart.set_data(df) # set stock price data
        mc.show() # show chart(run ```matplotlib.pyplot.show()```)
        mc.close() # run ```matplotlib.pyplot.close('close')```
        ```

    Class Variables:
        watermark: watermark text.

        df: stock data DataFrame.
        key_date: date column key. default 'date'
        key_open, key_high, key_low, key_close: price column key. default ('open', 'high', 'low', 'close')
        key_volume: volume column key. default 'volume'. If ```if config.VOLUME.EDGECOLOR.volume``` is ```False```, the volume chart is not drawn.

        candle_on_ma: if True: draw candle above ma. else: draw candle below ma lines.
        fraction: if True and number has a fractional part, display it as a fraction.
        slider_top: set slider position. if True: slider top. else: bottom

        limit_candle: If (`the number of candles to draw < limit_candle or not limit_candle`): draw candles, else: draw wicks.
        limit_wick: If (`the number of candles to draw < limit_wick or not limit_wick`): draw wicks, else: draw line.
        limit_volume: If (`the number of candles to draw < limit_volume or not limit_volume`): draw volumebar, else: draw wicks.
        limit_ma: If (`the number of candles to draw < limit_ma or not limit_ma`): draw ma lines, else: don't draw ma lines.

        min_distance: the minimum number of candles displayed on the screen.
    """
    df: pd.DataFrame

    key_date = 'date'
    key_open, key_high, key_low, key_close = ('open', 'high', 'low', 'close')
    key_volume = 'volume'

    candle_on_ma = True
    fraction = False
    slider_top = True

    watermark = 'seolpyo mplchart'

    limit_candle = 400
    limit_wick = 2_000
    limit_volume = 200
    limit_ma = 8_000

    min_distance = 5

