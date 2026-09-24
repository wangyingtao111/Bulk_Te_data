import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# === 1. 顶刊级全局排版参数设置 (NPG Style) ===
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
plt.rcParams['mathtext.fontset'] = 'custom'
plt.rcParams['mathtext.rm'] = 'Arial'
plt.rcParams['mathtext.it'] = 'Arial:italic'

plt.rcParams.update({
    'font.size': 14,          
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

# === 2. 加载数据与物理常数设定 ===
df = pd.read_csv("amset_columns.csv")
doping = np.abs(df["doping"])

# 设定温度 (K)
T = 300 

# 用户指定的晶格热导率 kappa_l (W m^-1 K^-1)
kappa_l = {
    'xx': 1.31,
    'yy': 1.31,
    'zz': 3.53
}

# === 3. 创建画布 ===
fig, ax = plt.subplots(figsize=(6.5, 5.5)) 

# NPG 经典配色
styles = {'xx': ('#E64B35', '-'),  
          'yy': ('#4DBBD5', '--'), 
          'zz': ('#00A087', '-.')}

# --- 循环计算并绘制三个方向的 ZT 值 ---
for dir_ in ['xx', 'yy', 'zz']:
    # 读取各向数据
    S_uV_K = df[f'S_{dir_}']        # uV/K
    sigma = df[f'sigma_{dir_}']     # S/m
    kappa_e = df[f'kappa_e_{dir_}'] # W/(m K)
    
    # 核心物理计算: ZT = (S^2 * sigma * T) / (kappa_e + kappa_l)
    # 注意：需要将 Seebeck 系数还原为标准单位 V/K 进行计算
    S_V_K = S_uV_K * 1e-6
    ZT = (S_V_K**2 * sigma * T) / (kappa_e + kappa_l[dir_])
    
    # 绘图
    color, ls = styles[dir_]
    ax.plot(doping, ZT, color=color, linestyle=ls, label=f'${dir_}$')

# === 4. 坐标轴与排版精调 ===
ax.set_xscale('log')

# ZT 是无量纲物理量，因此不需要单位
ax.set_ylabel('Figure of merit, $ZT$', fontweight='bold')
ax.set_xlabel('Carrier concentration, $n$ (cm$^{-3}$)', fontweight='bold')

# 强制开启 X 轴的副刻度线
locmin = ticker.LogLocator(base=10.0, subs=(0.2,0.4,0.6,0.8), numticks=12)
ax.xaxis.set_minor_locator(locmin)
ax.xaxis.set_minor_formatter(ticker.NullFormatter())

# 图例设置
ax.legend(frameon=False, loc='best', handlelength=2.5, fontsize=13)
ax.grid(True, which='major', linestyle='--', linewidth=1.0, color='gray', alpha=0.15)

# === 5. 输出高精度图片 ===
plt.tight_layout()
plt.savefig("ZT_300K_NPG_Style.pdf", dpi=600, bbox_inches='tight')
plt.savefig("ZT_300K_NPG_Style.png", dpi=600, bbox_inches='tight')

print("✅ 热电优值 (ZT) 曲线绘制完成！已保存为 PDF 和 PNG 格式。")
plt.show()
