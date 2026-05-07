@echo off
setlocal EnableExtensions EnableDelayedExpansion
chcp 65001 >nul

echo ================================================
echo  轨道交通造价AI分析工具 - 自定义Excel双击运行版
echo ================================================
echo.

cd /d "%~dp0"

set "DEFAULT_INPUT=samples\sample_budget.xlsx"
set "HISTORY_FILE=data\history_projects.xlsx"
set "OUTPUT_DIR=output"
set "VENV_DIR=.venv"
set "PYTHON_EXE=%VENV_DIR%\Scripts\python.exe"
set "PIP_EXE=%VENV_DIR%\Scripts\pip.exe"

echo [步骤1/7] 请输入你的综合概算 Excel 文件路径（可直接拖拽文件到此窗口）：
echo            直接按回车将使用示例文件：%DEFAULT_INPUT%
set /p USER_INPUT=请输入路径: 

if "%USER_INPUT%"=="" (
  set "INPUT_FILE=%DEFAULT_INPUT%"
  echo [提示] 你未输入路径，将使用示例文件：%INPUT_FILE%
) else (
  set "INPUT_FILE=%USER_INPUT%"
)

set "INPUT_FILE=%INPUT_FILE:"=%"

if not exist "%INPUT_FILE%" (
  echo [错误] 找不到输入文件：%INPUT_FILE%
  echo [提示] 请确认路径正确，或把文件拖拽到窗口再试一次。
  pause
  exit /b 1
)

if not exist "%DEFAULT_INPUT%" (
  echo [提示] 未检测到示例文件，正在自动生成示例文件...
  if not exist "%VENV_DIR%" (
    python -m venv "%VENV_DIR%"
  )
  "%PYTHON_EXE%" -m pip install --upgrade pip >nul 2>nul
  "%PIP_EXE%" install -e . >nul 2>nul
  "%PYTHON_EXE%" samples\create_sample_excel.py >nul 2>nul
)

if not exist "%VENV_DIR%" (
  echo [步骤2/7] 正在创建虚拟环境...
  python -m venv "%VENV_DIR%"
  if errorlevel 1 (
    echo [错误] 创建虚拟环境失败。请确认已安装 Python 3.10+ 且已加入 PATH。
    pause
    exit /b 1
  )
) else (
  echo [步骤2/7] 已检测到虚拟环境，跳过创建。
)

echo [步骤3/7] 正在升级 pip...
"%PYTHON_EXE%" -m pip install --upgrade pip
if errorlevel 1 (
  echo [错误] pip 升级失败，请检查网络后重试。
  pause
  exit /b 1
)

echo [步骤4/7] 正在安装依赖...
"%PIP_EXE%" install -e .
if errorlevel 1 (
  echo [错误] 依赖安装失败，请检查网络或 Python 环境。
  pause
  exit /b 1
)

echo [步骤5/7] 准备输入文件...
if /I "%INPUT_FILE%"=="%DEFAULT_INPUT%" (
  if not exist "%DEFAULT_INPUT%" (
    echo [提示] 示例文件不存在，正在生成示例 Excel...
    "%PYTHON_EXE%" samples\create_sample_excel.py
    if errorlevel 1 (
      echo [错误] 示例 Excel 生成失败。
      pause
      exit /b 1
    )
  )
)

echo [步骤6/7] 正在运行造价分析...
"%VENV_DIR%\Scripts\rail-cost-ai.exe" --input "%INPUT_FILE%" --history "%HISTORY_FILE%" --output-dir "%OUTPUT_DIR%"
if errorlevel 1 (
  echo [错误] 分析运行失败，请查看上方报错信息。
  pause
  exit /b 1
)

echo [步骤7/7] 分析完成，正在打开 output 文件夹...
if not exist "%OUTPUT_DIR%" mkdir "%OUTPUT_DIR%"
start "" "%cd%\%OUTPUT_DIR%"

echo.
echo 全部完成！结果已输出到：%OUTPUT_DIR%
echo.
pause
