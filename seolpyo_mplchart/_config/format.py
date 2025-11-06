

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

