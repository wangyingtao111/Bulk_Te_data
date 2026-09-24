import matplotlib
matplotlib.use('TkAgg') 
import matplotlib.pyplot as plt
import numpy as np

# 1. 全局字体设置 (适应学术期刊排版)
matplotlib.rcParams.update({'font.size': 22, 'font.family': 'sans-serif'})

# 2. 读取 Vaspkit 生成的 TDOS 数据
# TDOS.dat 的第一列是能量，第二列是总态密度
data = np.loadtxt('TDOS.dat')
energy = data[:, 0]
dos = data[:, 1]

# 3. 创建画布
fig, ax = plt.subplots(figsize=(6, 8)) # DOS 图通常采用纵向细长的画布，以便与能带图并排拼图

# 4. 绘制 DOS 曲线并填充阴影
ax.plot(dos, energy, color='#1f77b4', linewidth=2) 
# 填充曲线到 0 轴之间的区域，增加视觉质感
ax.fill_betweenx(energy, 0, dos, color='#1f77b4', alpha=0.3) 

# 5. 绘制费米能级辅助线 (Vaspkit 已将费米能级归零)
ax.axhline(0, linestyle='--', color='gray', linewidth=1.5)

# 6. 设置轴标签和显示范围
ax.set_ylabel("Energy - $E_F$ (eV)")
ax.set_xlabel("Density of States (states/eV)")

# 限制能量范围，建议与您的能带图 Y 轴范围保持完全一致（例如 -3 到 3 eV）
ax.set_ylim(-3, 3)
# 限制 X 轴的下限为 0，防止坐标轴左侧留白过多
ax.set_xlim(left=0)

# 7. 优化边距并保存为高分辨率 TIFF
plt.tight_layout()
plt.savefig('Te_TDOS.tiff', dpi=300, bbox_inches='tight')
plt.show()
