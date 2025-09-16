# CalcAny - 数据分析可视化工具

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green.svg)](https://docs.python.org/3/library/tkinter.html)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)

一个基于Python的桌面数据分析可视化工具，专门用于处理和分析层级结构的JSON数据。通过直观的图形界面，帮助用户快速理解和分析复杂的数据结构。

## ✨ 核心特性

- 🔍 **智能数据导入** - 支持JSON格式数据文件的导入和解析
- 📊 **多维度数据展示** - 支持层级数据的可视化展示（整体/BOQ/模型/部件）
- 🔧 **可配置界面** - 通过配置文件自定义显示字段和中文名称
- 🔎 **实时搜索过滤** - 支持对数据表格内容进行实时搜索和过滤
- 📋 **数据复制功能** - 支持复制整行数据为文本、JSON格式和Markdown表格格式
- 🎨 **现代化UI** - 基于Tkinter的现代化界面设计，支持微软雅黑字体
- 📈 **内存优化** - 内置内存监控和优化机制，支持大数据集处理
- 🔢 **高精度数值处理** - 自动将数字类型转换为decimal类型，确保数值计算的高精度
- ⚙️ **可视化配置管理** - 图形化配置管理界面，支持配置导入导出
- 🛠️ **模块化架构** - 采用MVC设计模式，代码结构清晰易维护

## 🚀 快速开始

### 环境要求

- Python 3.8+
- Windows 7/8/10/11 (64位)
- 至少 4GB 内存
- 100MB 可用磁盘空间

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行程序

```bash
python main.py
```

### 使用可执行文件

如果您有打包好的可执行文件：

1. 双击 `CalcAny.exe` 或运行 `运行CalcAny.bat`
2. 如被杀毒软件拦截，请添加到信任列表
3. 程序会自动创建配置文件和日志目录

## 📁 项目结构

```
data_analysis/
├── main.py                 # 程序入口文件
├── config_manager_ui.py   # 配置管理界面
├── config.json            # 配置文件
├── config_template.json   # 配置模板
├── sample.json            # 示例数据
├── requirements.txt       # 依赖包列表
├── version_info.txt       # 版本信息文件
├── calc_any.spec          # PyInstaller打包配置
├── build_optimized.py     # 🚀 优化构建脚本
├── startup_optimizer.py   # ⚡ 启动性能优化器
├── performance_test.py    # 📊 性能测试工具
├── EXE_OPTIMIZATION_GUIDE.md    # 📖 EXE优化完整指南
├── EXE_OPTIMIZATION_REPORT.md   # 📋 EXE优化成果报告
├── controllers/           # 控制器模块
│   ├── app_controller.py  # 主应用逻辑控制
│   └── logging_setup.py   # 日志配置管理
├── models/                # 数据模型层
│   ├── config_manager.py  # 配置管理器
│   └── data_manager.py    # 数据管理器
├── views/                 # 视图层
│   ├── main_app_view.py   # 主界面视图
│   ├── document_info_view.py # 文档信息视图
│   ├── factor_view.py     # 因子分类视图
│   └── sub_factor_detail_view.py # 子因子详情视图
├── utils/                 # 工具层
│   ├── validation_utils.py # 数据验证工具
│   ├── data_utils.py      # 数据处理工具
│   ├── clipboard_utils.py # 剪贴板操作工具
│   └── logging_utils.py   # 日志管理工具
└── logs/                  # 日志目录（自动创建）
```

## ⚙️ 配置说明

### 配置文件结构 (config.json)

```json
{
  "document_info_fields": ["businessCode", "netSalesRevenue"],
  "data_hierarchy_names": {
    "total": "整体",
    "boq": "BOQ",
    "model": "模型",
    "part": "部件"
  },
  "factor_categories": {
    "基础因子": [
      {
        "name": "收入因子",
        "basic_info": ["businessCode", "netSalesRevenue"],
        "table_info": {
          "total": ["netSalesRevenue", "listPriceTotalOutHardware"]
        }
      }
    ]
  },
  "display_names": {
    "netSalesRevenue": "净销售收入",
    "businessCode": "业务代码"
  }
}
```

### 配置管理

程序提供可视化配置管理界面：

1. 菜单栏 → 工具 → 配置管理
2. 支持配置编辑、导入、导出和重置
3. 配置更改后自动刷新程序设置

## 📊 数据格式

### 输入数据要求

- **格式**: JSON文件
- **结构**: 包含 `calculateItemVO` 字段的层级数据
- **编码**: UTF-8

### 示例数据结构

```json
{
  "businessCode": "BIZ001",
  "netSalesRevenue": 1000000,
  "calculateItemVO": {
    "total": {
      "netSalesRevenue": 1000000,
      "children": [
        {
          "level": "boq",
          "data": {...}
        }
      ]
    }
  }
}
```

## 💡 主要功能

### 🚀 基本操作

1. **启动程序**: 运行 `python main.py` 或双击可执行文件
2. **导入数据**: 通过菜单栏选择JSON数据文件
3. **浏览数据**: 使用层级选择和因子分类查看不同维度的数据
4. **搜索过滤**: 在搜索框中输入关键词实时过滤表格数据
5. **复制导出**: 使用右键菜单复制所需格式的数据

### 📋 数据复制功能

**表格右键菜单**：
- 🔤 **复制行 (文本)** - 制表符分隔的纯文本格式，适合粘贴到Excel
- 📋 **复制行 (JSON)** - 标准JSON格式，便于程序间数据交换
- 📝 **复制行 (Markdown)** - 包含表头的Markdown表格，适用于文档和Wiki

**单元格操作**：
- 🖱️ **双击单元格** - 快速复制单个单元格的值到剪贴板
- 📄 **右键字段值** - 在基本信息区域右键复制字段内容

## 🔧 技术架构

### 🛠️ 技术栈

| 组件 | 技术选型 | 版本要求 | 说明 |
|------|----------|----------|------|
| **核心语言** | Python | 3.8+ | 主要开发语言 |
| **GUI框架** | Tkinter + tksheet | 内置 + >=7.0.0 | 跨平台桌面应用界面 |
| **数据处理** | 轻量级数据模块 | 内置 | 自研轻量级数据处理，替代Pandas |
| **高精度计算** | Python decimal | 内置 | 高精度数值计算，避免浮点数误差 |
| **系统监控** | psutil | >=5.9.0 | 内存和性能监控 |
| **日志系统** | Python logging | 内置 | 完整的日志记录 |
| **打包工具** | PyInstaller | >=6.0.0 (可选) | 可执行文件打包 |

### 📦 打包部署

**开发环境运行**:
```bash
# 安装依赖
pip install -r requirements.txt

# 启动应用
python main.py
```

**生产环境打包**:

#### 🚀 优化构建方式（推荐）

使用优化构建脚本，获得更快的启动速度和更好的杀毒软件兼容性：

```bash
# 1. 安装PyInstaller
pip install pyinstaller

# 2. 使用优化构建脚本
python build_optimized.py

# 3. 测试构建性能
python performance_test.py
```

**优化构建特性**：
- ⚡ **极速启动**: 平均启动时间2.1秒，性能评级优秀
- 📦 **轻量体积**: 11.35MB，相比传统打包减少95%
- 🛡️ **杀毒兼容**: 显著降低杀毒软件误报率
- 💾 **低内存占用**: 仅6.6MB运行内存
- 🔧 **自动优化**: 包含字节码优化、模块排除、启动优化等

#### 📋 传统构建方式

```bash
# 使用标准PyInstaller打包
pyinstaller calc_any.spec

# 生成的可执行文件位于 dist/ 目录
```

#### 🛠️ 构建工具说明

| 文件 | 说明 |
|------|------|
| `build_optimized.py` | 优化构建脚本，包含完整的构建流程和优化配置 |
| `calc_any.spec` | PyInstaller配置文件，已优化排除不必要模块 |
| `startup_optimizer.py` | 启动优化器，提升EXE启动性能 |
| `performance_test.py` | 性能测试工具，验证构建效果 |
| `version_info.txt` | 版本信息文件，增强安全性和兼容性 |

#### 📊 构建性能对比

| 构建方式 | 文件大小 | 启动时间 | 内存占用 | 杀毒兼容性 |
|----------|----------|----------|----------|------------|
| 优化构建 | 11.35MB | 2.1秒 | 6.6MB | 优秀 |
| 传统构建 | ~200MB+ | 8-15秒 | 50MB+ | 一般 |

#### 🔧 构建故障排除

**常见问题**：
- 如果构建失败，确保已安装PyInstaller：`pip install pyinstaller`
- 如果启动测试失败，检查编码问题，确保控制台支持UTF-8
- 如果被杀毒软件拦截，将生成的EXE添加到信任列表

**详细文档**：
- 查看 `EXE_OPTIMIZATION_GUIDE.md` 了解完整的优化策略
- 查看 `EXE_OPTIMIZATION_REPORT.md` 了解详细的优化成果

## 🐛 故障排除

### ❓ 常见问题解决

<details>
<summary>🚫 程序无法启动</summary>

**可能原因及解决方案**:
- ✅ **Python版本**: 确保使用Python 3.8+版本
- ✅ **依赖安装**: 运行 `pip install -r requirements.txt`
- ✅ **权限问题**: 以管理员身份运行或检查文件权限
- ✅ **日志检查**: 查看 `logs/app_YYYYMMDD.log` 获取详细错误信息

```bash
# 检查Python版本
python --version

# 重新安装依赖
pip install --upgrade -r requirements.txt
```
</details>

<details>
<summary>📄 数据加载失败</summary>

**数据文件要求**:
- ✅ **文件格式**: 必须是有效的JSON文件
- ✅ **文件编码**: UTF-8编码
- ✅ **数据结构**: 包含 `calculateItemVO` 字段
- ✅ **文件大小**: 建议小于100MB以获得最佳性能

**验证数据格式**:
```bash
# 使用Python验证JSON格式
python -c "import json; print('Valid JSON' if json.load(open('your_file.json', 'r', encoding='utf-8')) else 'Invalid JSON')"
```
</details>

<details>
<summary>⚙️ 配置文件问题</summary>

**配置修复步骤**:
1. 打开程序 → 工具 → 配置管理
2. 点击"重置为默认配置"
3. 或手动编辑 `config.json`，参考 `config_template.json`

**配置文件位置**: `./config.json`
</details>

### 📋 日志系统

**日志文件位置**: `logs/app_YYYYMMDD.log`

**日志级别说明**:
- 🔍 **DEBUG**: 详细的调试信息
- ℹ️ **INFO**: 一般操作信息
- ⚠️ **WARNING**: 警告信息
- ❌ **ERROR**: 错误信息

**查看实时日志**:
```bash
# 使用记事本打开日志文件
notepad logs/app_20250122.log

# 或使用PowerShell查看日志末尾
Get-Content logs/app_20250122.log -Tail 50
```

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 📞 联系我们

如有问题或建议，请：

- 提交 [Issue](../../issues)
- 查看详细的开发文档 `development_plan.md`
- 检查日志文件进行问题排查

---

**注意**: 这是一个合法的数据分析工具，如果可执行文件被杀毒软件误报，请添加到信任列表中。程序不会收集或传输任何个人数据，所有数据处理均在本地完成。
