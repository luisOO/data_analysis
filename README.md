# CalcAny - 数据分析可视化工具

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green.svg)](https://docs.python.org/3/library/tkinter.html)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)

一个基于Python的桌面数据分析可视化工具，专门用于处理和分析层级结构的JSON数据。通过直观的图形界面，帮助用户快速理解和分析复杂的数据结构。

## ✨ 主要特性

- 🔍 **智能数据导入** - 支持JSON格式数据文件的导入和解析
- 📊 **多维度数据展示** - 支持层级数据的可视化展示（整体/BOQ/模型/部件）
- 🔧 **可配置界面** - 通过配置文件自定义显示字段和中文名称
- 🔎 **实时搜索过滤** - 支持对数据表格内容进行实时搜索和过滤
- 📋 **数据复制功能** - 支持复制单元格、整行JSON数据和字段值
- 🎨 **现代化UI** - 基于Tkinter的现代化界面设计，支持微软雅黑字体
- 📈 **内存优化** - 内置内存监控和优化机制，支持大数据集处理
- 📝 **完整日志** - 详细的日志记录系统，便于问题排查
- ⚙️ **可视化配置管理** - 图形化配置管理界面，支持配置导入导出

## 🖼️ 界面预览

### 主界面
- **单据基本信息区域** - 以6列网格布局显示JSON文件的顶层字段信息，支持字段优先级排序和等宽对齐
- **因子展示区域** - 以选项卡形式组织不同的因子分类
- **子因子详情区域** - 显示选中子因子的基本信息（采用与单据信息相同的6列网格布局）和数据表格

### 功能模块
- **数据层次选择** - 单选按钮形式展示数据层级
- **搜索过滤** - 实时搜索和过滤数据内容
- **右键菜单** - 支持复制、导出等快捷操作

## 🚀 快速开始

### 环境要求

- Python 3.8+
- Windows 7/8/10/11 (64位)
- 至少 4GB 内存
- 100MB 可用磁盘空间

### 安装依赖

```bash
pip install pandas psutil
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
├── main.py                 # 程序入口
├── controller.py           # 主控制器
├── data_model.py          # 数据模型和配置管理
├── view.py                # 用户界面
├── config_manager_ui.py   # 配置管理界面
├── config.json            # 配置文件
├── config_template.json   # 配置模板
├── sample.json            # 示例数据
├── development_plan.md    # 开发设计文档
├── version_info.txt       # 版本信息
├── calc_any.spec          # PyInstaller打包配置
├── 安装说明.txt           # 安装说明
├── README_EXE.md          # 可执行文件说明
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

## 🔧 开发说明

### 技术栈

- **语言**: Python 3.12
- **GUI框架**: Tkinter + ttk
- **数据处理**: Pandas
- **内存监控**: psutil
- **日志系统**: Python logging
- **缓存机制**: functools.lru_cache

### 架构设计

- **MVC模式**: 控制器(Controller) + 数据模型(DataModel) + 视图(View)
- **配置管理**: 独立的配置管理器，支持动态加载
- **内存优化**: 分块处理大数据集，自动垃圾回收
- **错误处理**: 完整的异常处理和日志记录

### 打包部署

使用PyInstaller打包为独立可执行文件：

```bash
pyinstaller calc_any.spec
```

## 🐛 故障排除

### 常见问题

1. **程序无法启动**
   - 检查Python版本是否为3.8+
   - 确认所有依赖已正确安装
   - 查看logs目录下的错误日志

2. **数据加载失败**
   - 确认JSON文件格式正确
   - 检查文件编码是否为UTF-8
   - 验证数据结构是否包含必要字段

3. **配置文件错误**
   - 使用配置管理界面重置为默认配置
   - 检查JSON语法是否正确
   - 参考config_template.json模板

4. **表格字段显示问题**
   - 启动时表格显示配置的字段名和中文名称
   - 如果字段显示异常，检查配置文件中的display_names设置
   - 确保table_info配置与display_names中的字段名一致

5. **内存不足**
   - 程序已内置内存优化
   - 建议处理大文件时分批导入
   - 定期清理缓存

### 日志查看

程序运行时会在 `logs/` 目录下生成日志文件：
- 文件名格式: `app_YYYYMMDD.log`
- 包含详细的操作记录和错误信息

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 👥 开发团队

- **CalcAny Development Team** - *初始开发* 

## 📞 联系我们

如有问题或建议，请：

- 提交 [Issue](../../issues)
- 查看详细的开发文档 `development_plan.md`
- 检查日志文件进行问题排查

---

**注意**: 这是一个合法的数据分析工具，如果可执行文件被杀毒软件误报，请添加到信任列表中。程序不会收集或传输任何个人数据，所有数据处理均在本地完成。
