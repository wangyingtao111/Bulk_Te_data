import json
import pandas as pd
import glob
import os


matched_files = glob.glob("transport_*.json")

if matched_files:
    # 按照文件的修改时间进行排序，找到最新修改的文件
    latest_file = max(matched_files, key=os.path.getmtime)
    print(f"打开最新生成的文件: {latest_file}")
    
    with open(latest_file, "r", encoding="utf-8") as f:
        data = json.load(f)
else:
    print("没有找到符合条件的文件！")


# === 1. 读取 JSON ===
#with open("transport_43x43x29.json", "r") as f:
#    data = json.load(f)

doping = data["doping"]
temperatures = data["temperatures"]
fermi_levels = data["fermi_levels"]

# === 2. 提取对角项 ===
def tensor_diag_to_dict(tensor, prefix):
    return {
        f"{prefix}_xx": tensor[0][0],
        f"{prefix}_yy": tensor[1][1],
        f"{prefix}_zz": tensor[2][2],
    }

rows = []

# === 3. 构建 long format ===
for i, dop in enumerate(doping):
    for j, T in enumerate(temperatures):

        row = {
            "doping": dop,
            "temperature": T,
        }

        row.update(tensor_diag_to_dict(data["conductivity"][i][j], "sigma"))
        row.update(tensor_diag_to_dict(data["seebeck"][i][j], "S"))
        row.update(tensor_diag_to_dict(data["electronic_thermal_conductivity"][i][j], "kappa_e"))

        for mech in data["mobility"]:
            row.update(
                tensor_diag_to_dict(
                    data["mobility"][mech][i][j],
                    f"mu_{mech}"
                )
            )

        rows.append(row)

df = pd.DataFrame(rows)

# === 4. 数据整理 ===
# 删除 temperature 列（如果你确定只计算了一个 300K 的数据点）
if "temperature" in df.columns:
    df = df.drop(columns=["temperature"])

# 按 doping 浓度从小到大排序，保证画图时的 X 轴单调性
df = df.sort_values(by="doping").reset_index(drop=True)

# === 5. 导出 ===
# 直接输出，取消 .T 转置，并设置 index=False 防止输出多余的行号列
df.to_csv("amset_columns.csv", index=False)

print("✅ 已导出 -> amset_columns.csv")
print(df.head())
