import numpy as np


unit_data = np.array([
    ['경', 10_000_000_000_000_000],
    ['조',      1_000_000_000_000],
    ['억',            100_000_000],
    ['만',                 10_000],
    ['',                        1],
])

unit_data_en = np.array([
    ['Qd', 1_000_000_000_000_000],
    ['T',      1_000_000_000_000],
    ['B',          1_000_000_000],
    ['M',              1_000_000],
    ['K',                  1_000],
    ['',                       1],
])


unit_info_data = np.array([
    ['경', 10_000_000_000_000_000],
    ['조',      1_000_000_000_000],
    ['억',            100_000_000],
    ['',                       1],
])

unit_info_data_en = np.array([
    ['Qd', 1_000_000_000_000_000],
    ['T',      1_000_000_000_000],
    ['B',          1_000_000_000],
    ['',                       1],
])



def convert_digit(num: float):
    "1.1 => 1.1, 1.0 => 1"
    if num % 1:
        return num
    return int(num)


def num_to_str(value: float, *, pos=None, word='원', unit_data: np.ndarray[np.ndarray[str, int]]=unit_data):
    # print(f'{value=}')

    ind_end = unit_data.shape[0] - 1

    mask = unit_data[:, 1].astype(np.float64) <= abs(value)
    # print(f'{mask=}')
    if not mask.any():
        # print(f'{unit_data.size=}')
        # print(f'{unit_data.shape=}')
        idx = ind_end
    else:
        idx = np.argmax(mask)
    # print(f'{(value, idx)=}')

    arr: list[str, int] = unit_data[idx]
    unit = arr[0]
    num = float(arr[1])
    # print(f'{(unit, num)=}')
    v = value / num
    # print(f'{v=}')
    if value < 1_000:
        v = round(v, 2)
    elif value < 100:
        v = round(v, 3)
    elif value < 10:
        v = round(v, 4)
    elif v < 10:
        if idx == ind_end:
            v = round(v, 3)
        else:
            idx += 1
            arr: list[str, int] = unit_data[idx]
            unit = arr[0]
            num = float(arr[1])
            v = round(value / num)
    elif v < 100:
        v = round(v, 2)
    elif v < 1_000:
        v = round(v, 1)
    else:
        v = round(v)

    # print(f'{v=}')
    v = convert_digit(v)
    # print(f'{v=}')
    if word.startswith(' ') or not unit or unit.endswith(' '):
        return f'{v:,}{unit}{word}'
    return f'{v:,}{unit} {word}'


def num_to_str_en(value, *, pos=None, word='$', unit_data: dict[str, int]=unit_data_en):
    # print('en')
    # print(f'{value=:,}')
    return num_to_str(value, pos=pos, word=word, unit_data=unit_data)

