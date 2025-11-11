from . import xlsx, csv


def xl_to_dataList(path_file):
    pf = str(path_file)
    if pf.endswith('.xlsx'):
        data = xlsx.convert(path_file)
    elif pf.endswith('.csv'):
        data = csv.convert(path_file)
    else:
        msg = '다음 형식의 파일의 데이터만 변환할 수 있습니다.'
        msg += f'  [.xlsx, .csv]'
        raise ValueError(msg)
    return data

