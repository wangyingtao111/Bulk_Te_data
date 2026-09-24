import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# === 1. 顶刊级全局排版参数设置 (NPG Style, 纯英文) ===
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
    'lines.linewidth': 2.0   
})

# === 2. 加载数据并计算功率因数 PF ===
file_path = "ZTMAX.csv"
df = pd.read_csv(file_path)
df.columns = df.columns.str.strip() 

# 【核心修改点 1】：根据公式 PF = S^2 * sigma 计算功率因数
# S 的单位是 uV/K (即 1e-6 V/K)
# sigma 的单位是 S/m
# 乘以 1e3 是为了将基础单位 W/(m K^2) 转换为学术界常用的 10^-3 W/(m K^2) 或 mW/(m K^2)
df['PF'] = (df['seebeck'] * 1e-6)**2 * df['electrivity'] * 1e3

# === 3. 创建画布 ===
fig, ax = plt.subplots(figsize=(7.5, 6)) 

# === 4. 数据映射与视觉编码 ===
strains = ['Relaxed', '0.2% Tensile', '2% comp.']
directions = ['XX', 'YY', 'ZZ']

# 纯英文图例标签
strain_labels = {
    'Relaxed': 'Relaxed',
    '0.2% Tensile': '0.2% Tensile',
    '2% comp.': '2.0% Comp.'
}
direction_labels = {
    'XX': 'XX',
    'YY': 'YY',
    'ZZ': 'ZZ'
}

colors = {
    'Relaxed': '#2b2639', 
    '0.2% Tensile': '#d52d2a', 
    '2% comp.': '#38841c'
}

# 标记与线型设置
markers = {'XX': 'o', 'YY': 's', 'ZZ': '^'}
linestyles = {'XX': '-', 'YY': '--', 'ZZ': '-.'}

# --- 循环绘制曲线 ---
for strain in strains:
    for direction in directions:
        subset = df[(df['Strain Condition'] == strain) & (df['Direction'] == direction)].sort_values(by='Temperature')
        
        if not subset.empty:
            label_name = f"{strain_labels[strain]} - {direction_labels[direction]}"
            
            # 【核心修改点 2】：读取刚刚计算生成的 'PF' 列进行绘制
            ax.plot(subset['Temperature'], subset['PF'], 
                    color=colors[strain], 
                    marker=markers[direction],
                    linestyle=linestyles[direction],
                    markersize=8,
                    linewidth=2.5,
                    alpha=0.9,
                    zorder=3,
                    markerfacecolor='white', 
                    markeredgewidth=2.0,
                    label=label_name)

# === 5. 坐标轴与排版精调 ===
ax.set_xlabel('Temperature, T (K)', fontweight='bold')
# 【核心修改点 3】：更新 Y 轴标签为功率因数，使用学术规范单位
ax.set_ylabel('Power factor, $\mathbf{PF}$ (10$\mathbf{^{-3}}$ W m$\mathbf{^{-1}}$ K$\mathbf{^{-2}}$)', fontweight='bold')

# 动态调整 x 轴范围
ax.set_xlim(df['Temperature'].min() - 50, df['Temperature'].max() + 50)

# 开启主刻度对应的副刻度线
ax.xaxis.set_minor_locator(ticker.AutoMinorLocator(2))
ax.yaxis.set_minor_locator(ticker.AutoMinorLocator(2))

# 辅助网格线
ax.grid(True, which='major', linestyle='--', linewidth=1.0, color='#BDBDBD', alpha=0.3)

# 图例位置
ax.legend(frameon=False, 
          loc='center right', 
          ncol=2, 
          handlelength=2.0, 
          fontsize=12, 
          columnspacing=0.8,
          labelspacing=0.4)

# === 6. 输出高精度图片 ===
plt.tight_layout() 
# 更新输出文件名
plt.savefig("Power_Factor_vs_Temperature_NatureStyle_EN.pdf", dpi=600, bbox_inches='tight')
plt.savefig("Power_Factor_vs_Temperature_NatureStyle_EN.png", dpi=600, bbox_inches='tight')

plt.show()
