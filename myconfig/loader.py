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
    df = pd.read_csv(csv_path, keep_default_na=False, na_values=[''])
    data_dict = dict()
    for _, row in df.iterrows():
        key = row.iloc[0]
        value = row.iloc[1]
        # 空白セルはNaNとして保持、それ以外は型変換
        if pd.isna(value):
            data_dict[int(key)] = float('nan')
        else:
            try:
                data_dict[int(key)] = int(value)
            except (ValueError, TypeError):
                data_dict[int(key)] = value
    return data_dict

# --------------------------------------------------------
# DotDictのリストをマージして単一のDotDictを返す関数
# --------------------------------------------------------
def merge_dotdicts(dotdict_list):
    merged_dict = {}
    for dd in dotdict_list:
        merged_dict.update(dd.__dict__)
    return DotDict(merged_dict)