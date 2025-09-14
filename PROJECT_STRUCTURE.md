# 项目结构说明

本项目已经重构为模块化架构，采用MVC设计模式，提高了代码的可维护性和可扩展性。

## 目录结构

```
data_analysis/
├── main.py                    # 应用程序入口点
├── config.json               # 应用配置文件
├── config_manager_ui.py      # 配置管理UI组件
├── controllers/              # 控制器层
│   ├── __init__.py
│   ├── app_controller.py     # 主应用控制器
│   └── logging_setup.py      # 日志配置
├── models/                   # 数据模型层
│   ├── __init__.py
│   ├── config_manager.py     # 配置管理器
│   └── data_manager.py       # 数据管理器
├── views/                    # 视图层
│   ├── __init__.py
│   ├── main_app_view.py      # 主应用视图
│   ├── document_info_view.py # 文档信息视图
│   ├── factor_view.py        # 因子视图
│   └── sub_factor_detail_view.py # 子因子详情视图
├── utils/                    # 工具函数
│   ├── __init__.py
│   ├── validation_utils.py   # 验证工具
│   ├── data_utils.py         # 数据处理工具
│   ├── clipboard_utils.py    # 剪贴板工具
│   └── logging_utils.py      # 日志工具
└── logs/                     # 日志文件目录
```

## 模块依赖关系

### 依赖层次（从上到下）
1. **main.py** → controllers
2. **controllers** → models, views, utils
3. **models** → utils
4. **views** → 内部视图组件
5. **utils** → 基础Python库

### 模块职责

#### Controllers（控制器层）
- `app_controller.py`: 主应用逻辑控制，协调模型和视图
- `logging_setup.py`: 统一的日志配置管理

#### Models（模型层）
- `config_manager.py`: 配置文件的加载、验证和管理
- `data_manager.py`: 数据的加载、处理和缓存管理

#### Views（视图层）
- `main_app_view.py`: 主窗口界面
- `document_info_view.py`: 文档信息显示组件
- `factor_view.py`: 因子数据显示组件
- `sub_factor_detail_view.py`: 子因子详情显示组件

#### Utils（工具层）
- `validation_utils.py`: 输入验证和数据安全获取
- `data_utils.py`: 数据转换和DataFrame优化
- `clipboard_utils.py`: 剪贴板操作功能
- `logging_utils.py`: 日志记录和错误处理

## 设计原则

1. **单一职责原则**: 每个模块都有明确的职责
2. **依赖倒置**: 高层模块不依赖低层模块的具体实现
3. **开闭原则**: 对扩展开放，对修改封闭
4. **模块化**: 便于测试、维护和扩展

## 使用方式

```python
# 启动应用
python main.py
```

应用程序会自动加载配置，初始化各个组件，并启动GUI界面。