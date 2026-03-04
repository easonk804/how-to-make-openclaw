# Windows 部署故障排除截图指南

本指南提供 Windows 环境下部署 `how-to-make-openclaw-main` 时的常见故障及解决方案，包含截图占位符位置说明。

---

## 截图规格建议

- **分辨率**: 1920x1080 或更高
- **格式**: PNG（推荐）或 JPG
- **命名规范**: `windows-error-{编号}-{简短描述}.png`
- **存储位置**: `docs/assets/screenshots/windows/`

---

## 常见故障 1: Python 未安装或未加入 PATH

### 症状
运行 `python --version` 时提示：
```
'python' 不是内部或外部命令，也不是可运行的程序或批处理文件。
```

### 解决方案
1. 安装 Python 3.10+ 从 [python.org](https://python.org)
2. 安装时勾选 **"Add Python to PATH"**

### 截图位置
📷 **[截图占位符: windows-error-01-python-not-found.png]**
- 应显示：命令提示符中的错误消息
- 关键元素：错误文本、命令提示符窗口标题

### 验证修复
```powershell
python --version
# 预期输出: Python 3.10.x
```

📷 **[截图占位符: windows-error-01-python-fixed.png]**
- 应显示：成功输出版本号

---

## 常见故障 2: 虚拟环境激活失败

### 症状
运行 `.venv\Scripts\activate` 时无反应或报错：
```
无法加载文件 .venv\Scripts\activate.ps1，因为在此系统上禁止运行脚本。
```

### 解决方案（PowerShell 执行策略）
```powershell
# 以管理员身份运行 PowerShell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 截图位置
📷 **[截图占位符: windows-error-02-execution-policy.png]**
- 应显示：红色错误消息，包含 "禁止运行脚本"

📷 **[截图占位符: windows-error-02-execution-policy-fix.png]**
- 应显示：成功执行 Set-ExecutionPolicy 命令

### 备选方案（使用 cmd 而非 PowerShell）
```cmd
.venv\Scripts\activate.bat
```

📷 **[截图占位符: windows-error-02-cmd-alternative.png]**
- 应显示：cmd 中成功激活虚拟环境

---

## 常见故障 3: pip 安装依赖超时/失败

### 症状
```
pip install -r requirements.txt
# ... 长时间无响应或 Connection timeout
```

### 解决方案（使用国内镜像源）
```powershell
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

或使用环境变量配置持久镜像：
```powershell
$env:PIP_INDEX_URL = "https://pypi.tuna.tsinghua.edu.cn/simple"
pip install -r requirements.txt
```

### 截图位置
📷 **[截图占位符: windows-error-03-pip-timeout.png]**
- 应显示：pip 连接超时错误

📷 **[截图占位符: windows-error-03-pip-mirror-fix.png]**
- 应显示：使用镜像源成功安装

---

## 常见故障 4: 测试运行时路径错误

### 症状
```
ERROR: file not found: tests/test_chapterXX.py
# 或 ModuleNotFoundError
```

### 原因
在非项目根目录运行测试

### 解决方案
```powershell
# 确保在项目根目录（包含 README.md 的目录）
cd d:\Eason\OpenClaw\how-to-make-openclaw-main
python -m pytest -q
```

### 截图位置
📷 **[截图占位符: windows-error-04-wrong-directory.png]**
- 应显示：在子目录运行测试时的错误

📷 **[截图占位符: windows-error-04-correct-directory.png]**
- 应显示：在项目根目录成功运行测试

---

## 常见故障 5: 编码错误导致测试失败

### 症状
```
UnicodeDecodeError: 'gbk' codec can't decode byte...
```

### 解决方案
设置 UTF-8 编码：
```powershell
chcp 65001
$env:PYTHONIOENCODING = "utf-8"
```

### 截图位置
📷 **[截图占位符: windows-error-05-encoding-error.png]**
- 应显示：UnicodeDecodeError 堆栈跟踪

📷 **[截图占位符: windows-error-05-encoding-fix.png]**
- 应显示：设置 chcp 65001 后测试通过

---

## 常见故障 6: pytest 命令未找到

### 症状
```
'pytest' 不是内部或外部命令...
```

### 解决方案
```powershell
# 方法 1: 使用 python -m 运行
python -m pytest -q

# 方法 2: 安装 pytest
pip install pytest
```

### 截图位置
📷 **[截图占位符: windows-error-06-pytest-not-found.png]**
- 应显示：pytest 命令未找到错误

📷 **[截图占位符: windows-error-06-pytest-module-fix.png]**
- 应显示：使用 `python -m pytest -q` 成功运行

---

## 常见故障 7: 最终集成 demo 导入错误

### 症状
```
ModuleNotFoundError: No module named 'final_ch01_v1'
```

### 原因
`final/openclaw_full.py` 动态导入模块失败

### 解决方案
确保从项目根目录运行：
```powershell
cd d:\Eason\OpenClaw\how-to-make-openclaw-main
python final/openclaw_full.py
```

### 截图位置
📷 **[截图占位符: windows-error-07-import-error.png]**
- 应显示：ModuleNotFoundError 及堆栈跟踪

📷 **[截图占位符: windows-error-07-import-fixed.png]**
- 应显示：在项目根目录成功运行 demo

---

## 故障速查表

| 故障现象 | 快速解决命令 |
|---------|-------------|
| Python 未找到 | 安装 Python 并勾选 "Add to PATH" |
| 脚本执行被拒绝 | `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` |
| pip 超时 | `pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt` |
| 路径错误 | `cd` 到项目根目录再运行 |
| 编码错误 | `chcp 65001` |
| pytest 未找到 | `python -m pytest -q` |

---

## 截图更新指南

如需添加实际截图：

1. 在 `docs/assets/screenshots/windows/` 目录创建文件夹
2. 按命名规范保存截图
3. 替换本文档中的占位符标记为实际图片引用：
   ```markdown
   ![错误截图](../assets/screenshots/windows/windows-error-01-python-not-found.png)
   ```
