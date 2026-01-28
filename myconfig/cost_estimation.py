import numpy as np
import pandas as pd
from pathlib import Path
import csv
import matplotlib.pyplot as plt

Q0 = 1
def fit_powerlaw(Q, C):
    """
    Fit C = C0 * Q^s with Q0 = 1 fixed, using least squares on log-log data.
    
    Inputs:
        Q : array-like of positive numbers
        C : array-like of positive numbers
    
    Returns:
        C0, s  (scalars)
    """
    Q = np.asarray(Q, dtype=float)
    C = np.asarray(C, dtype=float)

    if np.any(Q <= 0) or np.any(C <= 0):
        raise ValueError("All Q and C must be positive.")

    x = np.log(Q)
    y = np.log(C)

    # 線形回帰: y = a + b x  (a = ln C0, b = s)
    A = np.vstack([np.ones_like(x), x]).T
    # 最小二乗解
    a, s = np.linalg.lstsq(A, y, rcond=None)[0]
    # 予測値と決定係数
    y_pred = a + s * x
    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 1.0

    C0 = np.exp(a)
    pd_data = pd.Series([C0, s, r2])
    pd_data = pd_data.round(3)
    output = list(pd_data)
    return output[0], output[1], output[2]

### csv_path, Q, output_csvの3か所を必要に応じて変える

if __name__ == "__main__":
    DATA_DIR = Path(__file__).resolve().parent.parent / "DATA"
    csv_path = DATA_DIR / "AWE_adv_cost.csv"
    df = pd.read_csv(csv_path)
    index_col = df.columns[0]
    df = df.set_index(index_col)
    columns = df.columns
    rows = df.index

    Q = [5.0, 10.0, 100, 1000] # [MW]
    # Q = [5.0, 10.0, 100] # [MW]

    output_csv = DATA_DIR / "AWE_adv_parameter.csv"
    with open(output_csv, "w",newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Process", "Base_cost", "Base_scale", "Scaling_factor", "Year"])
        prm_list = []
        # プロット保存先ディレクトリ
        plot_dir = DATA_DIR / "plots"
        plot_dir.mkdir(exist_ok=True)
        for i in range(len(columns.values) - 1):
            # 元コードと同様にデータ取得（必要に応じてインデックス調整してください）
            C = list(df[columns[i]][1:])
            # 数値配列に変換（欠損値があれば除外）
            Q_arr = np.array(Q, dtype=float)
            C_arr = np.array([float(v) for v in C], dtype=float)
            # フィッティング
            C0, s, r2 = fit_powerlaw(Q_arr, C_arr)
            name = columns.values[i]
            writer.writerow([name, C0, Q0, s, 2019])

            # 単位変換：capex [USD] -> USD/kW
            # Q_arr は MW 単位なので kW に直すために *1000 で割る
            unit_data = C_arr / (Q_arr * 1000.0)

            # フィット曲線（単位換算後）
            q_min = Q_arr.min() * 0.8
            q_max = Q_arr.max() * 1.2
            q_grid = np.linspace(q_min, q_max, 200)  # 線形スケール
            # 元のフィットは C = C0 * Q^s なので、単位換算後は (C0 * Q^s) / (Q*1000) = C0 * Q^(s-1) / 1000
            y_fit_unit = (C0 * (q_grid ** (s - 1))) / 1000.0

            plt.figure(figsize=(6,5))
            plt.scatter(Q_arr, unit_data, color='red', s=40, label='data (USD/kW)')
            plt.plot(q_grid, y_fit_unit, color='blue', lw=2, label=f'fit (USD/kW): C0={C0:.3g}, s={s:.3g}')
            plt.xlabel('Q [MW]')
            plt.ylabel('Capex [USD / kW]')
            plt.title(f'{name}  (R^2={r2:.3f})')
            plt.legend()
            plt.grid(True, ls='--', lw=0.5)
            save_path = plot_dir / f"{name.replace(' ', '_')}_unit_cost_PEM.png"
            plt.tight_layout()
            plt.savefig(save_path)
            plt.close()
            print(f"Saved unit-cost plot: {save_path}  (R^2={r2:.3f})")