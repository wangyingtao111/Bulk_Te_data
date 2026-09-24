import matplotlib
matplotlib.use('TkAgg') 
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker

# === 1. 顶刊级全局排版参数设置 (NPG Style) ===
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = True 
plt.rcParams['mathtext.fontset'] = 'custom'
plt.rcParams['mathtext.rm'] = 'Arial'
plt.rcParams['mathtext.it'] = 'Arial:italic'

plt.rcParams.update({
    'font.size': 18,          
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
    'lines.linewidth': 1.5   # 能带较密，线宽设为1.5避免糊在一起
})

# === 2. 读取 Vaspkit 格式数据 ===
# 能带数据
data_band = np.loadtxt('REFORMATTED_BAND.dat')
k_path = data_band[:, 0]
bands_energy = data_band[:, 1:]

# DOS 数据
data_dos = np.loadtxt('TDOS.dat')
energy = data_dos[:, 0]
dos = data_dos[:, 1]

# === 3. 创建合并画布 (宽比例 3:1) ===
# sharey=True 确保左右两张图的能量轴完全一致
fig, (ax_band, ax_dos) = plt.subplots(1, 2, figsize=(10, 6.5), 
                                      gridspec_kw={'width_ratios': [3, 1], 'wspace': 0.08},
                                      sharey=True)

# ==========================================
# === 4. 绘制左侧图：电子能带 (Band Structure) ===
# ==========================================
# 采用沉稳深灰色绘制能带
for i in range(bands_energy.shape[1]):
    ax_band.plot(k_path, bands_energy[:, i], color='#2b2639', linewidth=1.5, alpha=0.85)

# 高对称点设置
k_nodes = [0.000, 0.804, 1.268, 2.196, 2.723, 3.526, 3.990, 4.918, 5.445, 5.973]  
k_labels = ['$\mathbf{\Gamma}$', '$\mathbf{M}$', '$\mathbf{K}$', '$\mathbf{\Gamma}$', 
            '$\mathbf{A}$', '$\mathbf{L}$', '$\mathbf{H}$', '$\mathbf{A|L}$', '$\mathbf{M|H}$', '$\mathbf{K}$'] 

# 绘制高对称点垂直辅助线
for node in k_nodes:
    ax_band.axvline(node, color='black', linewidth=1.2, alpha=0.3)

# 坐标轴限制与刻度格式
ax_band.set_xlim(min(k_path), max(k_path))
ax_band.set_ylim(-3, 3) # 聚焦带隙附近
ax_band.set_xticks(k_nodes)
ax_band.set_xticklabels(k_labels)
# === 修改/添加以下两行：设置能带图的横纵坐标标签 ===
ax_band.set_xlabel(r'Wave vector, $\mathbf{k}$', fontweight='bold')
ax_band.set_ylabel(r'Energy $\mathbf{-}$ $\mathbf{E_F}$ (eV)', fontweight='bold')
ax_band.set_ylim(-1.5, 1.5)
# Y 轴开启副刻度
ax_band.yaxis.set_minor_locator(ticker.AutoMinorLocator(2))

# ==========================================
# === 5. 绘制右侧图：电子态密度 (DOS) ===
# ==========================================
# 采用 Nature 蓝绘制并填充 DOS
ax_dos.plot(dos, energy, color='#4DBBD5', linewidth=2.0) 
ax_dos.fill_betweenx(energy, 0, dos, color='#4DBBD5', alpha=0.4) 

ax_dos.set_xlim(left=0)
# 简化X轴标签以防拥挤
ax_dos.set_xlabel('DOS', fontweight='bold') 

# X 轴开启副刻度
ax_dos.xaxis.set_minor_locator(ticker.AutoMinorLocator(2))

# ==========================================
# === 6. 全局美化与费米能级贯穿线 ===
# ==========================================
# 绘制费米能级虚线，贯穿左右两图
ax_band.axhline(0, linestyle='--', color='#E64B35', linewidth=1.5, zorder=5) # 费米能级使用 Nature 红，高亮
ax_dos.axhline(0, linestyle='--', color='#E64B35', linewidth=1.5, zorder=5)

# 由于 sharey=True，ax_dos 的 y 轴标签会被自动隐藏，无需额外操作

# ==========================================
# === 7. 保存与输出 ===
# ==========================================
# bbox_inches='tight' 自动裁剪多余空白边缘
plt.savefig('Te_Band_DOS_Combined_NPG.pdf', dpi=600, bbox_inches='tight')
plt.savefig('Te_Band_DOS_Combined_NPG.png', dpi=600, bbox_inches='tight')
plt.savefig('Te_Band_DOS_Combined_NPG.tiff', dpi=600, bbox_inches='tight')

print("✅ 能带与态密度(DOS)合并绘图成功！已按 NPG 顶级学术排版规范生成高清图片。")
plt.show()
