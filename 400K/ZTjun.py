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
T = 400 

# 用户指定的各向晶格热导率 (W m^-1 K^-1)
kappa_l_xx = 0.98
kappa_l_yy = 0.98
kappa_l_zz = 2.66

# 计算平均晶格热导率
kappa_l_ave = (kappa_l_xx + kappa_l_yy + kappa_l_zz) / 3.0

# === 3. 计算多晶平均热电参数 ===
# 电导率和电子热导率取算术平均（张量迹的 1/3）
sigma_ave = (df['sigma_xx'] + df['sigma_yy'] + df['sigma_zz']) / 3.0
kappa_e_ave = (df['kappa_e_xx'] + df['kappa_e_yy'] + df['kappa_e_zz']) / 3.0

# Seebeck 系数必须按电导率加权平均: S_ave = Tr(S * sigma) / Tr(sigma)
#S_ave_uV_K = (df['S_xx'] * df['sigma_xx'] + 
#              df['S_yy'] * df['sigma_yy'] + 
#              df['S_zz'] * df['sigma_zz']) / (df['sigma_xx'] + df['sigma_yy'] + df['sigma_zz'])
S_ave_uV_K = (df['S_xx']+ df['S_yy']+df['S_zz']) / 3
# 核心物理计算: ZT_ave = (S_ave^2 * sigma_ave * T) / (kappa_e_ave + kappa_l_ave)
S_ave_V_K = S_ave_uV_K * 1e-6
ZT_ave = (S_ave_V_K**2 * sigma_ave * T) / (kappa_e_ave + kappa_l_ave)

# === 4. 寻找并输出平均 ZT 的最大值及对应参数 ===
max_idx = ZT_ave.argmax()  # 找到平均 ZT 最大值所在的索引
max_ZT = ZT_ave.iloc[max_idx]
opt_n = doping.iloc[max_idx]
opt_S = S_ave_uV_K.iloc[max_idx]
opt_sigma = sigma_ave.iloc[max_idx]
opt_kappa_e = kappa_e_ave.iloc[max_idx]

print(f"=== {T}K 下多晶平均热电性能 (Average ZT) ===")
print(f"  最大平均 ZT 值:       {max_ZT:.4f}")
print(f"  最佳载流子浓度 (n):   {opt_n:.2e} cm^-3")
print(f"  平均Seebeck系数 (S):  {opt_S:.2f} uV/K")
print(f"  平均电导率 (sigma):   {opt_sigma:.2e} S/m")
print(f"  平均电子热导率(k_e):  {opt_kappa_e:.4f} W/(m K)")
print(f"  平均晶格热导率(k_l):  {kappa_l_ave:.4f} W/(m K)")
print("==============================================")

# === 5. 创建画布并绘图 ===
fig, ax = plt.subplots(figsize=(6.5, 5.5)) 

# 仅绘制平均ZT曲线 (NPG红色)
ax.plot(doping, ZT_ave, color='#E64B35', linestyle='-', label='Average $ZT$')

# 坐标轴与排版精调
ax.set_xscale('log')

ax.set_ylabel('Figure of merit, $ZT$', fontweight='bold')
ax.set_xlabel('Carrier concentration, $n$ (cm$^{-3}$)', fontweight='bold')

# 强制开启 X 轴的副刻度线
locmin = ticker.LogLocator(base=10.0, subs=(0.2,0.4,0.6,0.8), numticks=12)
ax.xaxis.set_minor_locator(locmin)
ax.xaxis.set_minor_formatter(ticker.NullFormatter())

# 图例设置
ax.legend(frameon=False, loc='best', handlelength=2.5, fontsize=13)
ax.grid(True, which='major', linestyle='--', linewidth=1.0, color='gray', alpha=0.15)

# === 6. 输出高精度图片 ===
plt.tight_layout()
plt.savefig("ZT_Average_300K_NPG.pdf", dpi=600, bbox_inches='tight')
plt.savefig("ZT_Average_300K_NPG.png", dpi=600, bbox_inches='tight')

print("✅ 平均热电优值 (ZT) 曲线绘制完成！已保存为 PDF 和 PNG 格式。")
plt.show()
