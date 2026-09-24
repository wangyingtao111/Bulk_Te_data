import pandas as pd
import numpy as np

# === 1. 数据加载 ===
try:
    df = pd.read_csv("amset_columns.csv")
except FileNotFoundError:
    print("错误：未找到 amset_columns.csv 文件。")
    exit()

# 基础参数
T = 400
doping = np.abs(df["doping"])
kappa_l = {'xx': 0.98, 'yy': 0.98, 'zz': 2.66}

# === 2. 筛选并计算各轴最优值 ===
mask = doping > 1e18
df_filtered = df[mask].copy()
doping_filtered = doping[mask]

# 表头：增加 Kappa_e (W/mK)
print(f"{'='*85}")
print(f"{'方向':<6} | {'Max ZT':<8} | {'Doping (cm^-3)':<14} | {'Seebeck (uV/K)':<14} | {'Sigma (S/m)':<12} | {'Kappa_e (W/mK)':<12}")
print(f"{'-'*85}")

for dir_ in ['xx', 'yy', 'zz']:
    # 提取当前方向的列数据
    S = df_filtered[f'S_{dir_}']
    sigma = df_filtered[f'sigma_{dir_}']
    ke = df_filtered[f'kappa_e_{dir_}']
    
    # 计算 ZT
    ZT = ((S * 1e-6)**2 * sigma * T) / (ke + kappa_l[dir_])
    
    # 找到最大值索引
    idx = ZT.idxmax()
    
    # 提取该点对应的各项参数
    max_zt = ZT.loc[idx]
    best_doping = doping_filtered.loc[idx]
    best_s = S.loc[idx]
    best_sigma = sigma.loc[idx]
    best_ke = ke.loc[idx]
    
    # 输出结果
    print(f"{dir_:<6} | {max_zt:<8.4f} | {best_doping:<14.2e} | {best_s:<14.2f} | {best_sigma:<12.2e} | {best_ke:<12.3f}")

print(f"{'='*85}")
