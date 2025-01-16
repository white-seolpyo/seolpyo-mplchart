from re import search


def convert_num(num):
    if isinstance(num, float) and num % 1: return num
    return int(num)


def float_to_str(num: float, digit=0, plus=False):
    if 0 < digit:
        num.__round__(digit)
        text = f'{num:+,.{digit}f}' if plus else f'{num:,.{digit}f}'
    else:
        num = round(num, digit).__int__()
        text = f'{num:+,}' if plus else f'{num:,}'
    return text


dict_unit = {
    '경': 10_000_000_000_000_000,
    '조':      1_000_000_000_000,
    '억':            100_000_000,
    '만':                 10_000,
}
dict_unit_en = {
    'Qd': 1_000_000_000_000_000,
    'T':      1_000_000_000_000,
    'B':          1_000_000_000,
    'M':              1_000_000,
    'K':                  1_000,
}


def convert_unit(value, digit=0, word='원'):
    # print(f'{value=:,}')
    v = abs(value)
    du = dict_unit if search('[가-힣]', word) else dict_unit_en
    for unit, n in du.items():
        if n <= v:
            # print(f'{n=:,}')
            # print(f'{unit=}')
            num = value / n
            return f'{float_to_str(num, digit)}{unit} {word}'
    if not value % 1: value = int(value)
    text = f'{float_to_str(value, digit)}{word}'
    # print(f'{text=}')
    return text


if __name__ == '__main__':
    a = 456.123
    print(float_to_str(a))
    print(float_to_str(a, 2))
    print(float_to_str(a, 6))


