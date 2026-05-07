# 轨道交通造价AI分析工具（给非程序员的超简单说明）

## 一、这次我新增/修改了哪些文件？它们有什么用？

> 你可以把这个项目理解成：
> - `src/` 里面是“工具本体”；
> - `samples/` 里面是“示例输入”；
> - `data/` 和 `output/` 是“运行后数据和结果”。

### 1) 根目录文件
- `README.md`（仓库根目录）  
  用途：告诉你真正项目在 `rail_cost_ai/` 目录里。

### 2) 项目说明与配置
- `rail_cost_ai/README.md`  
  用途：完整使用说明（安装、运行、Windows 步骤、注意事项）。
- `rail_cost_ai/pyproject.toml`  
  用途：记录项目依赖和启动命令（相当于“安装清单 + 启动入口”）。

### 3) 示例输入
- `rail_cost_ai/samples/create_sample_excel.py`  
  用途：一键生成示例 Excel（`samples/sample_budget.xlsx`），方便你先试跑。

### 4) 核心程序（真正干活的代码）
- `rail_cost_ai/src/rail_cost_ai/cli.py`  
  用途：命令行入口。你运行一条命令，它会自动完成“读取-分析-导出”。
- `rail_cost_ai/src/rail_cost_ai/excel_parser.py`  
  用途：读取 Excel，自动识别项目名称、线路长度、车站数量、总投资、分项费用。
- `rail_cost_ai/src/rail_cost_ai/analyzer.py`  
  用途：计算单公里造价、各专业占比、偏差率。
- `rail_cost_ai/src/rail_cost_ai/history_db.py`  
  用途：维护历史项目库（`data/history_projects.xlsx`）。
- `rail_cost_ai/src/rail_cost_ai/report_exporter.py`  
  用途：导出 Excel 分析结果和 Word 报告。
- `rail_cost_ai/src/rail_cost_ai/models.py`  
  用途：定义项目数据结构（给程序内部统一用）。
- `rail_cost_ai/src/rail_cost_ai/__init__.py`  
  用途：包初始化文件（Python 项目标准文件）。

---

## 二、我下一步应该“点哪里”保存这些修改？

你说你不会编程，我给你两种最简单方式：

### 方式 A：你在 GitHub 网页上操作
1. 打开这个仓库页面。  
2. 点击 **Pull requests**。  
3. 找到我这次提交对应的 PR。  
4. 点 **Merge pull request**（合并）。  
5. 再点 **Confirm merge**。  

这就等于“保存到主分支”。

### 方式 B：你用 VS Code（本地）
1. 打开左侧 **Source Control（源代码管理）** 图标。  
2. 看见文件变化后，点击 **Commit（提交）**。  
3. 再点 **Push（推送）** 到远程仓库。  

---

## 三、Windows 电脑怎么运行（一步一步照抄）

> 下面假设你已经安装：
> - Python 3.10 或更高版本
> - Git

### 0) 打开终端
- 推荐：`Windows Terminal` 或 `PowerShell`

### 1) 进入项目目录
```powershell
cd 你的项目路径\rail_cost_ai
```

### 2) 创建虚拟环境
```powershell
python -m venv .venv
```

### 3) 激活虚拟环境
```powershell
.\.venv\Scripts\activate
```

> 激活成功后，命令行前面通常会出现 `(.venv)`。

### 4) 安装依赖
```powershell
python -m pip install --upgrade pip
pip install -e .
```

### 5) 生成示例 Excel（可选）
```powershell
python samples\create_sample_excel.py
```

### 6) 运行分析
```powershell
rail-cost-ai --input samples\sample_budget.xlsx --history data\history_projects.xlsx --output-dir output
```

### 7) 查看结果
运行成功后，在 `output` 目录会看到：
- `XXX_分析结果.xlsx`
- `XXX_分析报告.docx`

---

## 四、常见问题与注意事项（非常重要）

1. **报错 `No module named pandas`**  
   说明依赖没装好。请重新执行：
   ```powershell
   pip install -e .
   ```

2. **找不到 `rail-cost-ai` 命令**  
   通常是虚拟环境没激活。请先执行：
   ```powershell
   .\.venv\Scripts\activate
   ```

3. **Excel 识别不准确**  
   请尽量在表里使用这些字段名称（或相近名称）：
   - 项目名称
   - 线路长度
   - 车站数量
   - 总投资
   - 分项费用（如土建工程费、机电设备费）

4. **不要直接改 `src/` 里的代码（如果你不熟悉编程）**  
   你可以先只替换输入 Excel，观察输出结果是否符合预期。

---

## 五、快速运行（复制即可）

```powershell
cd 你的项目路径\rail_cost_ai
python -m venv .venv
.\.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -e .
python samples\create_sample_excel.py
rail-cost-ai --input samples\sample_budget.xlsx --history data\history_projects.xlsx --output-dir output
```

如果你愿意，我下一步可以继续帮你做一个“图形界面版本”（双击按钮就能跑，不用命令行）。


## 六、Windows 双击运行（推荐）

如果你不想敲命令，现在可以直接双击：

- `rail_cost_ai\run.bat`

它会自动完成：
1. 创建虚拟环境；
2. 安装依赖；
3. 生成示例 Excel；
4. 运行造价分析；
5. 自动打开 `output` 文件夹。

### 使用步骤
1. 打开 `rail_cost_ai` 文件夹；
2. 双击 `run.bat`；
3. 等待窗口按中文提示执行；
4. 看到“全部完成”后，到自动弹出的 `output` 文件夹查看结果。

### 注意事项
- 第一次运行会下载依赖，时间可能稍长；
- 需要联网安装依赖；
- 如果提示找不到 `python`，请先安装 Python 3.10+，并勾选“Add Python to PATH”。



## 七、Windows 双击运行（自定义输入文件）

如果你要分析“你自己的 Excel”，请双击：

- `rail_cost_ai\run_custom.bat`

它会先让你输入文件路径：
1. 双击后会提示输入“综合概算 Excel 文件路径”；
2. 你可以直接复制粘贴路径，或把 Excel 文件拖到窗口；
3. 如果你直接按回车不输入，会自动使用 `samples\sample_budget.xlsx`。

脚本会自动完成：
- 创建虚拟环境；
- 安装依赖；
- 运行造价分析；
- 输出到 `output` 文件夹；
- 自动打开 `output` 文件夹。

### run_custom.bat 使用步骤（超简单）
1. 打开 `rail_cost_ai` 文件夹；
2. 双击 `run_custom.bat`；
3. 按提示输入 Excel 路径（或直接回车用示例）；
4. 等待执行完成；
5. 在自动打开的 `output` 文件夹查看结果。

