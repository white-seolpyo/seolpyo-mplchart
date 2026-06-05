from datetime import datetime, timedelta
from re import findall
from zipfile import ZipFile


base_date = datetime(1899, 12, 30).date()


def convert(path_file: str, sheet=1, row=4, date='A', Open='B', high='C', low='D', close='E', volume='F'):
    "xlsx 파일에서 주가 정보를 추출합니다."
    list_price: list[dict[str, str|float]] = []

    zipfile = ZipFile(path_file)
    # print(f'{zipfile.filelist=}')
    a = zipfile.read(f'xl/worksheets/sheet{sheet}.xml')
    # print(f'{a=}')
    # print(f'{type(a)=}')
    b = a.decode('utf-8')
    for i in findall('<row.+?</row>', b)[row:]:
        # print()
        # print(f'{i=}')
        dt = findall(f'<c r="{date}[0-9].+?<v>([0-9]+)</v>', i)
        c = findall(f'<c r="{close}[0-9].+?<v>([0-9\.]+)</v>', i)
        o = findall(f'<c r="{Open}[0-9].+?<v>([0-9\.]+)</v>', i)
        h = findall(f'<c r="{high}[0-9].+?<v>([0-9\.]+)</v>', i)
        l = findall(f'<c r="{low}[0-9].+?<v>([0-9\.]+)</v>', i)
        v = findall(f'<c r="{volume}[0-9].+?<v>([0-9]+)</v>', i)
        # print(f'{(dt, c, o, h, l, v)=}')
        if not all([dt, o, h, l, c,]):
            continue
        try:
            dt = base_date + timedelta(int(dt[0]))
            c = float(c[0])
            o = float(o[0])
            h = float(h[0])
            l = float(l[0])
        except:
            continue
        try:
            v = float(v[0])
        except:
            v = 0
        # print(f'{(dt, c, o, h, l, v)=}')
        # if 2020 < dt.year and dt.year < 2024: list_price.append({'기준일': f'{dt}', '종가': c, '시가': o, '고가': h, '저가': l, '거래량': v,})
        list_price.append({'기준일': str(dt), '종가': c, '시가': o, '고가': h, '저가': l, '거래량': v,})
    # for i in enumerate(list_price, 1): print(f'  {i}')

    return sorted(list_price, key=lambda x: x['기준일'])

