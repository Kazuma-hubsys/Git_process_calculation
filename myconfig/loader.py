import pandas as pd
import csv

# --------------------------------------------------------
# Dot-access object（行名.列名でアクセスできる）
# --------------------------------------------------------
class DotDict:
    def __init__(self, dictionary):
        for key, value in dictionary.items():
            setattr(self, key, value)
    def __repr__(self):
        keys = ", ".join(self.__dict__.keys())
        return f"<DotDict: {keys}>"
# --------------------------------------------------------
# CSV を読み込み、行名 → DotDict の辞書として返す関数
# --------------------------------------------------------
def load_csv(csv_path: str):
    df = pd.read_csv(csv_path)
    index_col = df.columns[0]
    df = df.set_index(index_col)
    result = {}
    for row_name, row in df.iterrows():
        cleaned = {col: (None if pd.isna(v) else v) for col, v in row.items()}
        result[row_name] = DotDict(cleaned)
    return DotDict(result)

def load_csv_as_dict(csv_path: str):
    with open(csv_path, encoding='utf-8') as f:
        data_dict = dict()
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            key = int(row[0])
            value = int(row[1])
            data_dict[key] = value
    return data_dict

# --------------------------------------------------------
# DotDictのリストをマージして単一のDotDictを返す関数
# --------------------------------------------------------
def merge_dotdicts(dotdict_list):
    merged_dict = {}
    for dd in dotdict_list:
        merged_dict.update(dd.__dict__)
    return DotDict(merged_dict)