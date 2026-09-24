import matplotlib
matplotlib.use('TkAgg') 
import matplotlib.pyplot as plt
import numpy as np

# 1. 全局字体设置 (适应学术排版)
matplotlib.rcParams.update({'font.size': 22, 'font.family': 'sans-serif'})

# 2. 读取 vaspkit 格式的数据
# 注意：确保将 REFORMATTED_BAND.dat 下载到代码同目录下
data = np.loadtxt('REFORMATTED_BAND.dat')

# 第一列是 K 路径，后面所有列是能带能量
k_path = data[:, 0]
bands_energy = data[:, 1:]

fig, ax = plt.subplots(figsize=(8, 6))

# 3. 循环绘制每一条能带
# bands_energy.shape[1] 代表总共有多少条能带
for i in range(bands_energy.shape[1]):
    ax.plot(k_path, bands_energy[:, i], color='b', linewidth=1.5, alpha=0.8)

# 4. 绘制费米能级 (vaspkit 已默认将其归零)
ax.axhline(0, linestyle='--', color='gray', linewidth=1.5)

# ==========================================
# 5. 高对称点设置 (需要您手动打开 KLABELS 文件查看)
# 请打开 KLABELS 文件，将其中的坐标和对应字母填入下方：
k_nodes = [0.000, 0.804, 1.268, 2.196, 2.723, 3.526, 3.990, 4.918, 5.445, 5.973]  # <--- 替换为 KLABELS 第二列的数值
k_labels = ['$\Gamma$', 'M', 'K', '$\Gamma$', 'A', 'L', 'H', 'A|L', 'M|H', 'K',] # <--- 替换为 KLABELS 第一列的字母
# ==========================================

for node in k_nodes:
    ax.axvline(node, color='k', linewidth=1, alpha=0.5)

ax.set_xticks(k_nodes)
ax.set_xticklabels(k_labels)
ax.set_xlim(min(k_path), max(k_path))
ax.set_ylim(-3, 3) # 根据需要聚焦带隙附近
ax.set_ylabel("Energy - $E_F$ (eV)")

plt.tight_layout()
plt.savefig('Te_VASP_Bands.tiff', dpi=300)
plt.show()
