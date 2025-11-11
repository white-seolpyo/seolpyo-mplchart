from datetime import datetime
import json


base_date = datetime(1899, 12, 30).date()


def convert(path_file: str, row=1, index_date=0, index_open=1, index_high=2, index_low=3, index_close=4, index_volume=5):
    "csv 파일에서 주가 정보를 추출합니다."
    item_list: list[dict[str, str|float]] = []

    with open(path_file, 'r', encoding='utf-8') as txt:
        j = json.load(txt)

    if len(j[1]) < 6:
        index_volume = None
    for i in j[row:]:
        if index_volume:
            dt = i[index_date]
            o = i[index_open]
            h = i[index_high]
            l = i[index_low]
            c = i[index_close]
            v = None
        else:
            dt = i[index_date]
            o = i[index_open]
            h = i[index_high]
            l = i[index_low]
            c = i[index_close]
            v = i[index_volume]

        o = float(o)
        h = float(h)
        l = float(l)
        c = float(c)
        if v:
            v = float(v)
            item = {'기준일': dt, '시가': o, '고가': h, '저가': l, '종가': c, '거래량': v}
        else:
            item = {'기준일': dt, '시가': o, '고가': h, '저가': l, '종가': c}

        item_list.append(item)

    return sorted(item_list, key=lambda x: x['기준일'])

