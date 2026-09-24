import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from scipy.interpolate import make_interp_spline

# === 1. Nature 风格全局参数 ===
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = True
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
    'lines.linewidth': 2   
})

# === 2. 加载数据 ===
file_path = "ZTMAX.csv"
df = pd.read_csv(file_path)
df.columns = df.columns.str.strip()

# === 3. 创建画布 ===
fig, ax = plt.subplots(figsize=(7.5, 6))

# === 4. 数据映射 ===
strains = ['Relaxed', '2% Tensile', '2% comp.']
directions = ['XX', 'YY', 'ZZ']

strain_labels = {
    'Relaxed': 'Relaxed',
    '2% Tensile': '2% Tensile',
    '2% comp.': '2% Comp.'
}
direction_labels = {'XX': 'a-axis', 'YY': 'b-axis', 'ZZ': 'c-axis'}

colors = {
    'Relaxed': '#CBCFE9',    
    '2% Tensile': '#E8619F', 
    '2% comp.': '#5EB0A2'    
}

markers = {'XX': 'o', 'YY': 's', 'ZZ': 'D'}

# === 平滑曲线函数 ===
def smooth_curve(x, y, n_points=300):
    if len(x) < 4:
        return x, y
    x_smooth = np.linspace(x.min(), x.max(), n_points)
    spl = make_interp_spline(x, y, k=min(3, len(x)-1))
    y_smooth = spl(x_smooth)
    return x_smooth, y_smooth

# --- 绘制带符号的平滑曲线（与ZT代码完全相同的绘制方式）---
for strain in strains:
    for direction in directions:
        subset = df[(df['Strain Condition'] == strain) & (df['Direction'] == direction)].sort_values(by='Temperature')
        if not subset.empty:
            T_original = subset['Temperature'].values
            # 晶格热导率数据
            Kappa_l_original = subset['lattice thermal conductivity'].values
            label_name = f"{strain_labels[strain]} - {direction_labels[direction]}"
            
            # 生成平滑曲线
            T_smooth, Kappa_l_smooth = smooth_curve(T_original, Kappa_l_original)
            
            # 找到原始温度点在平滑曲线上的最近位置索引
            indices = []
            for t in T_original:
                idx = np.argmin(np.abs(T_smooth - t))
                indices.append(idx)
            
            # 一行代码搞定：plot 同时绘制线和点（与ZT完全一致）
            ax.plot(T_smooth, Kappa_l_smooth,
                    color=colors[strain],
                    linestyle='-',
                    linewidth=2.5,
                    marker=markers[direction],
                    markevery=indices,  # 只在原始数据点位置显示符号
                    markersize=8,
                    markerfacecolor=colors[strain],
                    markeredgewidth=1.5,
                    alpha=0.9,
                    label=label_name,
                    zorder=2)

# === 5. 坐标轴设置 ===
ax.set_xlabel('Temperature (K)', fontweight='bold')
ax.set_ylabel(r'Lattice thermal cond., $\mathbf{\kappa_l}$ (W m$^{-1}$ K$^{-1}$)', fontweight='bold')

# 坐标轴范围
ax.set_xlim(df['Temperature'].min() - 50, df['Temperature'].max() + 50)
# 晶格热导率让matplotlib自动调整Y轴范围

# 刻度设置
ax.tick_params(axis='both', labelsize=16)
ax.xaxis.set_minor_locator(ticker.AutoMinorLocator(2))
ax.yaxis.set_minor_locator(ticker.AutoMinorLocator(2))

# 网格
ax.grid(True, linestyle='--', linewidth=0.8, alpha=0.6, color='#CCCCCC')

# 图例（与ZT完全一致：无边框、左下角、2列、字体12）
ax.legend(frameon=False, 
          loc='upper right',
          ncol=2,
          handlelength=2.0,
          fontsize=12,
          labelspacing=0.3,
          handletextpad=0.5)

# === 6. 输出 ===
plt.tight_layout(pad=0.8)
plt.savefig("Kappa_l_vs_Temperature_Smooth.pdf", dpi=600, bbox_inches='tight')
plt.savefig("Kappa_l_vs_Temperature_Smooth.png", dpi=600, bbox_inches='tight')
plt.show()
