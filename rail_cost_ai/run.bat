@echo off
setlocal EnableExtensions EnableDelayedExpansion
chcp 65001 >nul

echo ==========================================
echo  轨道交通造价AI分析工具 - Windows双击运行版
echo ==========================================
echo.

cd /d "%~dp0"

set "VENV_DIR=.venv"
set "PYTHON_EXE=%VENV_DIR%\Scripts\python.exe"
set "PIP_EXE=%VENV_DIR%\Scripts\pip.exe"

if not exist "%VENV_DIR%" (
  echo [步骤1/6] 正在创建虚拟环境...
  python -m venv "%VENV_DIR%"
  if errorlevel 1 (
    echo [错误] 创建虚拟环境失败。请确认已安装 Python 3.10+ 且已加入 PATH。
    pause
    exit /b 1
  )
) else (
  echo [步骤1/6] 已检测到虚拟环境，跳过创建。
)

echo [步骤2/6] 正在升级 pip...
"%PYTHON_EXE%" -m pip install --upgrade pip
if errorlevel 1 (
  echo [错误] pip 升级失败，请检查网络后重试。
  pause
  exit /b 1
)

echo [步骤3/6] 正在安装项目依赖...
"%PIP_EXE%" install -e .
if errorlevel 1 (
  echo [错误] 依赖安装失败，请检查网络或 Python 环境。
  pause
  exit /b 1
)

echo [步骤4/6] 正在生成示例 Excel...
"%PYTHON_EXE%" samples\create_sample_excel.py
if errorlevel 1 (
  echo [错误] 示例 Excel 生成失败。
  pause
  exit /b 1
)

echo [步骤5/6] 正在运行轨道交通造价分析...
"%VENV_DIR%\Scripts\rail-cost-ai.exe" --input samples\sample_budget.xlsx --history data\history_projects.xlsx --output-dir output
if errorlevel 1 (
  echo [错误] 分析运行失败，请查看上方报错信息。
  pause
  exit /b 1
)

echo [步骤6/6] 分析完成，正在打开 output 文件夹...
if not exist output mkdir output
start "" "%cd%\output"

echo.
echo 全部完成！你可以在 output 文件夹查看：
echo - *_分析结果.xlsx
echo - *_分析报告.docx
echo.
pause
