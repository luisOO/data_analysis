# 项目结构说明

本项目采用现代化的模块化架构，基于MVC设计模式构建，集成了高精度数值计算、可视化配置管理和性能优化等先进特性，提供了专业级的数据分析可视化解决方案。

## 目录结构

```
data_analysis/
├── main.py                    # 应用程序入口点
├── config_manager_ui.py      # 可视化配置管理UI组件（集成到主程序菜单）
├── sample.json               # 示例数据文件
├── requirements.txt          # 项目依赖列表
├── LICENSE                   # MIT许可证文件
├── README.md                 # 项目说明文档
├── .gitignore               # Git忽略文件配置
├── config/                   # 配置文件目录
│   ├── config.json          # 主应用配置文件
│   ├── logging_config.json  # 开发环境日志配置
│   ├── logging_config_production.json # 生产环境日志配置
│   └── version_info.txt     # 版本信息文件
├── scripts/                  # 构建和脚本文件
│   ├── __init__.py          # 脚本模块初始化
│   ├── build_optimized.py   # 优化构建脚本（防杀毒软件误杀）
│   ├── startup_optimizer.py # 启动性能优化器
│   └── calc_any.spec        # PyInstaller打包配置
├── docs/                     # 文档目录
│   ├── README_EXE.md        # EXE使用说明
│   ├── CHANGELOG.md         # 详细更新日志
│   ├── PROJECT_STRUCTURE.md # 项目结构说明（本文档）
│   ├── CONFIG_ENHANCEMENT_GUIDE.md # 配置增强功能指南
│   ├── DEPENDENCY_CLEANUP_REPORT.md # 依赖清理报告
│   ├── EXE_OPTIMIZATION_GUIDE.md # EXE优化完整指南
│   ├── EXE_OPTIMIZATION_REPORT.md # EXE优化成果报告
│   ├── development_plan.md  # 开发计划和路线图
│   └── 安装说明.txt         # 中文安装说明
├── controllers/              # 控制器层（MVC架构）
│   ├── __init__.py
│   ├── app_controller.py     # 主应用控制器，协调模型和视图
│   └── logging_setup.py      # 统一日志配置管理器
├── models/                   # 数据模型层（MVC架构）
│   ├── __init__.py
│   ├── config_manager.py     # 配置管理器，支持动态配置加载
│   └── data_manager.py       # 数据管理器，支持高精度数值处理
├── views/                    # 视图层（MVC架构）
│   ├── __init__.py
│   ├── main_app_view.py      # 主应用视图，集成菜单和布局
│   ├── document_info_view.py # 文档信息视图组件
│   ├── factor_view.py        # 因子分类视图组件
│   └── sub_factor_detail_view.py # 子因子详情视图组件
├── utils/                    # 工具函数层
│   ├── __init__.py
│   ├── validation_utils.py   # 输入验证和数据安全工具
│   ├── data_utils.py         # 数据处理和转换工具
│   ├── clipboard_utils.py    # 剪贴板操作工具
│   ├── logging_utils.py      # 日志管理工具
│   └── lightweight_data.py   # 轻量级DataFrame实现（替代pandas）
├── assets/                   # 资源文件目录
│   └── icon1.svg            # 应用程序图标（SVG格式）
└── logs/                     # 日志文件目录（根据配置动态创建）
```

## 模块依赖关系

### 依赖层次（从上到下）
1. **main.py** → controllers
2. **controllers** → models, views, utils
3. **models** → utils
4. **views** → 内部视图组件
5. **utils** → 基础Python库

### 模块职责详解

#### Controllers（控制器层）
- **`app_controller.py`**: 
  - 主应用逻辑控制，实现MVC架构的核心协调功能
  - 管理数据导入、配置加载和界面更新
  - 集成配置管理界面，支持动态配置更新
  - 处理用户交互事件和业务逻辑流程
- **`logging_setup.py`**: 
  - 统一的日志配置管理，支持开发和生产环境区分
  - 动态日志级别调整和文件输出配置
  - 集成psutil进行性能监控和日志优化

#### Models（模型层）
- **`config_manager.py`**: 
  - 配置文件的加载、验证和管理
  - 支持因子分类、显示名称和数据层次配置
  - 提供配置项的动态获取和验证功能
  - 集成输入验证和错误处理机制
- **`data_manager.py`**: 
  - 数据的加载、处理和缓存管理
  - 高精度数值处理，集成decimal类型转换
  - 大数据集分块处理和内存优化
  - 支持多层级数据结构的解析和处理

#### Views（视图层）
- **`main_app_view.py`**: 
  - 主窗口界面，集成菜单栏和工具栏
  - 响应式布局设计，支持窗口大小调整
  - 集成配置管理界面的调用入口
  - 现代化UI设计，优化用户体验
- **`document_info_view.py`**: 
  - 文档信息显示组件，支持字段动态配置
  - 双击复制功能和右键菜单集成
  - 自适应布局和字体优化
- **`factor_view.py`**: 
  - 因子分类视图组件，支持动态选项卡
  - 子因子选择和滚动区域优化
  - 双击事件支持和交互增强
- **`sub_factor_detail_view.py`**: 
  - 子因子详情显示组件，集成数据表格
  - 实时搜索过滤和延迟搜索优化
  - 多格式数据复制（文本/JSON/Markdown）
  - 高级表格功能，支持排序和列宽调整

#### Utils（工具层）
- **`validation_utils.py`**: 
  - 输入验证和数据安全获取
  - 类型检查和参数验证
  - 统一的错误处理机制
- **`data_utils.py`**: 
  - 数据转换和处理工具
  - DataFrame内存优化和性能提升
  - 显示名称转换和列配置管理
- **`clipboard_utils.py`**: 
  - 剪贴板操作功能
  - 多格式内容复制支持
  - 跨平台兼容性处理
- **`logging_utils.py`**: 
  - 日志记录和错误处理
  - 性能监控和调试信息记录
- **`lightweight_data.py`**: 
  - 轻量级DataFrame实现，替代pandas
  - 高性能数据处理和内存优化
  - 支持decimal类型和高精度计算

#### Scripts（构建脚本层）
- **`build_optimized.py`**: 
  - 优化构建脚本，支持生产环境配置
  - 防杀毒软件误杀的多重策略
  - 启动速度优化和文件体积压缩
  - Windows清单文件生成和兼容性优化
- **`startup_optimizer.py`**: 
  - 启动性能优化器
  - 垃圾回收优化和模块预加载
  - 内存管理和线程优化
- **`calc_any.spec`**: 
  - PyInstaller打包配置文件
  - 模块排除和优化设置
  - 资源文件和依赖管理

#### Config（配置文件）
- **`config.json`**: 
  - 主应用配置，包含完整的业务逻辑配置
  - 因子分类、子因子和数据层次配置
  - 显示名称映射和字段配置
- **`logging_config.json`**: 
  - 开发环境日志配置
  - 详细的调试信息和文件输出
- **`logging_config_production.json`**: 
  - 生产环境日志配置
  - 优化的日志级别和性能设置

## 设计原则与架构特性

### 核心设计原则
1. **单一职责原则**: 每个模块都有明确的职责和边界
2. **依赖倒置**: 高层模块不依赖低层模块的具体实现
3. **开闭原则**: 对扩展开放，对修改封闭
4. **模块化**: 便于测试、维护和扩展
5. **高内聚低耦合**: 模块内部功能紧密相关，模块间依赖最小化

### 架构特性
- **MVC架构模式**: 清晰的模型-视图-控制器分离
- **轻量级设计**: 自研轻量级DataFrame，避免重型依赖
- **高精度计算**: 集成decimal类型，确保数值计算精度
- **性能优化**: 内存监控、分块处理和启动优化
- **可视化配置**: 图形化配置管理，支持实时编辑
- **跨环境支持**: 开发和生产环境的配置区分
- **防误杀优化**: 专业的EXE打包策略，避免杀毒软件误报

## 使用方式

```python
# 启动应用
python main.py
```

应用程序会自动加载配置，初始化各个组件，并启动GUI界面。