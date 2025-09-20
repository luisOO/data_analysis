# CalcAny - 专业数据分析可视化工具

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)]()
[![Version](https://img.shields.io/badge/Version-v1.2.14-brightgreen.svg)]()

> 🚀 **高性能** | 📊 **可视化** | 🔧 **模块化** | 💡 **智能化** | 🎯 **高精度**

CalcAny是一款专业的数据分析可视化工具，专为处理复杂的层级数据结构而设计。采用现代化的MVC架构模式，提供直观的图形界面和强大的数据处理能力，支持高精度数值计算和实时配置管理。

## ✨ 核心特性

### 🎯 数据处理能力
- **多层级数据支持**: 支持total、boq、model、part等多层级数据结构
- **智能数据解析**: 自动解析JSON格式的复杂数据结构
- **高效内存管理**: 优化大数据集处理，支持分块加载和内存监控
- **高精度数值计算**: 集成decimal类型，避免浮点数精度丢失
- **数据类型优化**: 自动优化DataFrame数据类型，提升性能

### 🖥️ 用户界面
- **现代化GUI**: 基于Tkinter构建的直观用户界面
- **响应式布局**: 支持窗口大小调整和组件自适应
- **多选项卡设计**: 清晰的因子分类展示
- **实时搜索过滤**: 支持数据表格的实时搜索和过滤
- **双击事件支持**: 列表框支持双击快速操作

### 🔧 系统功能
- **可视化配置管理**: 集成配置管理界面，支持实时编辑和拖拽排序
- **智能日志系统**: 完整的日志记录和错误处理机制，支持环境区分
- **剪贴板集成**: 支持多种格式的数据复制和导出功能
- **性能监控**: 内置内存使用监控和性能优化
- **EXE优化**: 专业的打包优化，提升启动速度并避免杀毒软件误杀

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
├── sample.json            # 示例数据
├── requirements.txt       # 依赖包列表
├── LICENSE                # 许可证文件
├── README.md              # 项目说明文档
├── config/                # 配置文件目录
│   ├── config.json        # 主配置文件
│   └── version_info.txt   # 版本信息文件
├── scripts/               # 构建和脚本文件目录
│   ├── build_optimized.py # 🚀 优化构建脚本
│   ├── startup_optimizer.py # ⚡ 启动性能优化器
│   └── calc_any.spec      # PyInstaller打包配置
├── docs/                  # 文档目录
│   ├── README_EXE.md      # EXE使用说明
│   ├── CHANGELOG.md       # 更新日志
│   ├── CONFIG_ENHANCEMENT_GUIDE.md # 配置增强指南
│   ├── DEPENDENCY_CLEANUP_REPORT.md # 依赖清理报告
│   ├── EXE_OPTIMIZATION_GUIDE.md # 📖 EXE优化完整指南
│   ├── EXE_OPTIMIZATION_REPORT.md # 📋 EXE优化成果报告
│   ├── PROJECT_STRUCTURE.md # 项目结构说明
│   ├── development_plan.md # 开发计划
│   └── 安装说明.txt       # 安装说明
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
├── logs/                  # 日志目录（根据配置动态创建）
└── config/                # 配置文件目录
    ├── config.json        # 主配置文件
    └── logging_config.json # 日志配置文件
```

## ⚙️ 配置说明

### 配置管理界面

通过菜单栏 "工具" → "⚙️ 配置管理" 打开可视化配置界面，支持：

#### 📋 单据信息配置
- 配置单据基本信息显示字段
- 支持字段的添加、删除和排序
- 实时预览配置效果

#### 🏷️ 因子分类管理
- 管理因子分类和子因子
- 支持分类的增删改操作
- 子因子基本信息字段配置
- 数据表格列配置

#### 🔤 显示名称设置
- 统一管理字段显示名称
- 支持批量编辑和导入导出
- 实时编辑模式

#### 📊 数据层次配置
- 配置启用的数据层次
- 设置默认显示层次
- 层次显示名称定制

### 主配置文件结构 (config.json)

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
          "total": ["netSalesRevenue", "listPriceTotalOutHardware"],
          "model": ["netSalesRevenue", "listPriceTotalOutHardware"],
          "part": ["netSalesRevenue", "listPriceTotalOutHardware"]
        }
      }
    ]
  },
  "enabled_hierarchy_levels": ["model", "part"],
  "default_hierarchy_level": "part",
  "display_names": {
    "netSalesRevenue": "净销售收入",
    "businessCode": "业务代码"
  }
}
```

### 日志配置文件 (logging_config.json)

```json
{
  "log_level": "INFO",
  "log_format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
  "enable_file_logging": true,
  "log_filename_format": "app_{date}.log"
}
```

**配置说明**：
- `log_level`: 日志级别 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `log_format`: 日志格式模板
- `enable_file_logging`: 是否启用文件日志记录
- `log_filename_format`: 日志文件名格式

### 配置管理

程序提供可视化配置管理界面：

1. 菜单栏 → 工具 → 配置管理
2. 支持配置编辑、导入、导出和重置
3. 配置更改后自动刷新程序设置
4. 支持开发环境和生产环境的不同日志配置

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

### 📖 使用说明

#### 基本操作流程

1. **启动程序**
   ```bash
   python main.py
   ```

2. **导入数据**
   - 点击菜单栏 "文件" → "导入JSON"
   - 选择要分析的JSON数据文件
   - 程序会自动解析并显示数据结构

3. **配置管理**
   - 点击菜单栏 "工具" → "⚙️ 配置管理"
   - 可视化配置界面支持：
     - 单据信息字段配置
     - 因子分类和子因子管理
     - 数据层次配置
     - 字段显示名称设置
     - 实时编辑和拖拽排序

4. **查看单据信息**
   - 上半部分显示单据的基本信息
   - 信息字段可通过配置管理界面自定义
   - 支持双击复制字段值

5. **分析因子数据**
   - 下半部分显示因子分类选项卡
   - 点击不同的因子分类查看对应数据
   - 左侧选择具体的子因子（支持双击快速选择）
   - 右侧显示子因子的详细信息和数据表格

6. **数据操作**
   - **搜索**: 在搜索框中输入关键词过滤数据
   - **复制**: 右键点击表格行，选择复制格式（文本/JSON/Markdown）
   - **排序**: 点击列标题对数据进行排序
   - **双击复制**: 双击单元格快速复制值

#### 高级功能

##### 🔧 配置管理
- **可视化配置界面**: 集成的图形化配置管理工具
- **实时编辑**: 支持配置的实时编辑和预览
- **拖拽排序**: 字段顺序支持拖拽调整
- **字段管理**: 动态添加、删除和编辑字段配置
- **显示名称**: 统一的字段显示名称管理
- **层次配置**: 数据层次的显示和启用状态配置
- **因子管理**: 完整的因子分类和子因子配置

##### 📊 数据分析
- **多层次视图**: 支持整单层、BOQ层、模型层、部件层数据查看
- **高精度计算**: decimal类型确保数值计算精度
- **实时过滤**: 支持基于关键词的实时数据过滤
- **智能搜索**: 延迟搜索机制，提升大数据集搜索性能
- **数据导出**: 支持多种格式的数据复制和导出
- **内存优化**: 大数据集分块处理和内存监控

##### 🎨 界面定制
- **现代化UI**: 基于ttk的现代化界面设计
- **响应式布局**: 支持窗口大小和布局的动态调整
- **字体优化**: 微软雅黑字体，优化中文显示效果
- **交互增强**: 双击事件、右键菜单等丰富的交互功能

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

## 🏗️ 技术架构

### 架构模式
- **MVC设计模式**: 清晰的模型-视图-控制器分离
- **模块化设计**: 高内聚、低耦合的模块结构
- **依赖注入**: 灵活的组件依赖管理
- **轻量级数据处理**: 自研轻量级DataFrame替代pandas

### 技术栈
- **Python 3.8+**: 现代Python特性支持
- **Tkinter**: 跨平台GUI框架
- **psutil**: 系统监控和性能优化
- **tksheet**: 高级表格组件
- **decimal**: 高精度数值计算
- **JSON**: 配置和数据存储格式
- **PyInstaller**: EXE打包和优化

### 🛠️ 技术栈详情

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
- 📝 **智能日志**: 生产环境默认禁用文件日志，按需动态创建logs目录

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
3. 或手动编辑 `config.json`

**配置文件位置**: `./config.json`
</details>

### 📋 日志系统

**日志文件位置**: `logs/app_YYYYMMDD.log` (仅在启用文件日志时创建)

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
