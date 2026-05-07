import pandas as pd

rows = [
    ["项目名称", "示例地铁A线"],
    ["线路长度", "39.6 公里"],
    ["车站数量", "28"],
    ["总投资", "31600"],
    ["土建工程费", 15000],
    ["机电设备费", 7200],
    ["车辆购置费", 3600],
    ["其他费用", 5800],
]

df = pd.DataFrame(rows)
df.to_excel("samples/sample_budget.xlsx", index=False, header=False)
print("Created samples/sample_budget.xlsx")
