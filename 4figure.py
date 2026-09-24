import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# === 1. 顶刊级全局排版参数设置 (NPG Style) ===
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica']
plt.rcParams['mathtext.fontset'] = 'custom'
plt.rcParams['mathtext.rm'] = 'Arial'
plt.rcParams['mathtext.it'] = 'Arial:italic'

plt.rcParams.update({
    'font.size': 16,
    'axes.linewidth': 2.0,
    'xtick.major.width': 2.0,
    'xtick.major.size': 6,
    'ytick.major.width': 2.0,
    'ytick.major.size': 6,
    'xtick.minor.width': 1.5,
    'xtick.minor.size': 4,
    'ytick.minor.width': 1.5,
    'ytick.minor.size': 4,
    'xtick.direction': 'in',
    'ytick.direction': 'in',
    'lines.linewidth': 2.5
})

# === 2. 加载与数据准备 ===
df = pd.read_csv("amset_columns.csv")
doping = np.abs(df["doping"])

# === 3. 创建画布 (1x4 子图结构) ===
fig, axs = plt.subplots(1, 4, figsize=(26, 5))
fig.subplots_adjust(wspace=0.25) 

# 定义样式 (NPG 配色)
styles = {'xx': ('#80C7A7', '-'), 
          'yy': ('#F3A8A8', '-'), 
          'zz': ('#3D73B9', '-')}

# --- 循环绘制前三个属性 (这里替代了手动写 axs[0], axs[1], axs[2]) ---
# 【修复点】：在这里为每个物理量加上了 r 前缀，并修复了 \boldsymbol 等所有的 LaTeX 语法
properties = [
    ('sigma', r'Electrical conductivity, $\boldsymbol{\sigma}$ ($\mathrm{S \cdot m^{-1}}$)'),
    ('S', r'Seebeck coefficient, $\mathbf{S}$ ($\boldsymbol{\mu}\mathrm{V \cdot K^{-1}}$)'),
    ('kappa_e', r'Electronic thermal condu., $\boldsymbol{\kappa}_e$ ($\mathrm{W \cdot m^{-1} \cdot K^{-1}}$)')
]

# i 会依次等于 0, 1, 2，分别对应前三个子图
for i, (prop, ylabel) in enumerate(properties):
    for dir_ in ['xx', 'yy', 'zz']:
        col = f'{prop}_{dir_}'
        color, ls = styles[dir_]
        axs[i].plot(doping, df[col], color=color, linestyle=ls, label=f'${dir_}$')
    
    axs[i].set_ylabel(ylabel, fontweight='bold')

# --- 图 4 (axs[3]): 功率因子 (Power Factor, PF) ---
for dir_ in ['xx', 'yy', 'zz']:
    S_col = f'S_{dir_}'
    sigma_col = f'sigma_{dir_}'
    # PF = S^2 * sigma，转换为 10^-3 W/(m K^2) 量级
    pf_values = (df[S_col] * 1e-6)**2 * df[sigma_col] * 1e3
    
    color, ls = styles[dir_]
    axs[3].plot(doping, pf_values, color=color, linestyle=ls, label=f'${dir_}$')

# PF 的 Y 轴标签也修复了正体单位语法
axs[3].set_ylabel(r'Power factor, $\mathbf{PF}$ ($\mathrm{10^{-3} \cdot W \cdot m^{-1} \cdot K^{-2}}$)', fontweight='bold')

# === 4. 统一格式设置 ===
for i, ax in enumerate(axs): # 遍历 4 个子图
    ax.set_xscale('log')
    # 设置 X 轴从 10^17 开始
    ax.set_xlim(1e13, 1e22) 
    
    # X 轴标签统一修复正体单位
    ax.set_xlabel(r'Carrier concentration, $\mathbf{n}$ ($\mathrm{cm^{-3}}$)', fontweight='bold')
    
    # 副刻度线设置
    locmin = ticker.LogLocator(base=10.0, subs=(0.2, 0.4, 0.6, 0.8), numticks=12)
    ax.xaxis.set_minor_locator(locmin)
    ax.xaxis.set_minor_formatter(ticker.NullFormatter())
    
    # 网格与图例
    ax.grid(True, which='major', linestyle='--', linewidth=1.0, color='gray', alpha=0.15)
    ax.legend(frameon=False, loc='best', handlelength=2.5, fontsize=12)

# === 5. 输出图片 ===
plt.savefig("TE_properties_all_NPG.pdf", dpi=600, bbox_inches='tight')
plt.savefig("TE_properties_all_NPG.png", dpi=600, bbox_inches='tight')

print("✅ 包含 4 个子图的 NPG 顶级期刊风格图表绘制完成（所有物理量加粗与 LaTeX 语法均已修正）。")
plt.show()
