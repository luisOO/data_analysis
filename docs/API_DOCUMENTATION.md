# API 文档

本文档详细说明了数据分析可视化工具各个模块的类和方法。

## 目录

- [Controllers（控制器层）](#controllers控制器层)
  - [AppController](#appcontroller)
  - [LoggingSetup](#loggingsetup)
- [Models（模型层）](#models模型层)
  - [ConfigManager](#configmanager)
  - [DataManager](#datamanager)
- [Views（视图层）](#views视图层)
  - [MainAppView](#mainappview)
  - [DocumentInfoView](#documentinfoview)
  - [FactorView](#factorview)
  - [SubFactorDetailView](#subfactordetailview)
- [Utils（工具层）](#utils工具层)
  - [ValidationUtils](#validationutils)
  - [DataUtils](#datautils)
  - [ClipboardUtils](#clipboardutils)
  - [LoggingUtils](#loggingutils)
  - [LightweightData](#lightweightdata)

---

## Controllers（控制器层）

### AppController

**文件位置**: `controllers/app_controller.py`

主应用控制器，实现MVC架构的核心协调功能。

#### 主要方法

##### `__init__(self, view, config_manager, data_manager)`
- **功能**: 初始化应用控制器
- **参数**:
  - `view`: 主视图实例
  - `config_manager`: 配置管理器实例
  - `data_manager`: 数据管理器实例

##### `load_data_from_file(self, file_path)`
- **功能**: 从文件加载数据
- **参数**:
  - `file_path` (str): 数据文件路径
- **返回值**: 加载成功返回True，失败返回False

##### `update_view_with_data(self, data)`
- **功能**: 使用数据更新视图
- **参数**:
  - `data`: 要显示的数据

##### `open_config_manager(self)`
- **功能**: 打开配置管理界面
- **返回值**: 无

---

### LoggingSetup

**文件位置**: `controllers/logging_setup.py`

统一的日志配置管理，支持开发和生产环境区分。

#### 主要方法

##### `load_logging_config(config_path=None)`
- **功能**: 加载日志配置
- **参数**:
  - `config_path` (str, 可选): 配置文件路径
- **返回值**: 配置字典

##### `setup_logging(config_path=None, environment='development')`
- **功能**: 设置日志系统
- **参数**:
  - `config_path` (str, 可选): 配置文件路径
  - `environment` (str): 环境类型（development/production）
- **返回值**: 无

---

## Models（模型层）

### ConfigManager

**文件位置**: `models/config_manager.py`

配置文件的加载、验证和管理。

#### 主要方法

##### `__init__(self, config_path='config/config.json')`
- **功能**: 初始化配置管理器
- **参数**:
  - `config_path` (str): 配置文件路径

##### `load_config(self)`
- **功能**: 加载配置文件
- **返回值**: 配置加载成功返回True，失败返回False

##### `get_factor_config(self)`
- **功能**: 获取因子配置
- **返回值**: 因子配置字典

##### `get_display_names(self)`
- **功能**: 获取显示名称映射
- **返回值**: 显示名称字典

##### `get_data_levels(self)`
- **功能**: 获取数据层级配置
- **返回值**: 数据层级列表

##### `validate_config(self, config)`
- **功能**: 验证配置文件格式
- **参数**:
  - `config` (dict): 配置字典
- **返回值**: 验证通过返回True，失败返回False

---

### DataManager

**文件位置**: `models/data_manager.py`

数据的加载、处理和缓存管理，支持高精度数值处理。

#### 主要方法

##### `__init__(self)`
- **功能**: 初始化数据管理器

##### `load_data(self, file_path)`
- **功能**: 从文件加载数据
- **参数**:
  - `file_path` (str): 数据文件路径
- **返回值**: 加载的数据或None

##### `process_data(self, data, config)`
- **功能**: 处理数据，应用配置
- **参数**:
  - `data`: 原始数据
  - `config`: 配置信息
- **返回值**: 处理后的数据

##### `get_factor_data(self, factor_name)`
- **功能**: 获取指定因子的数据
- **参数**:
  - `factor_name` (str): 因子名称
- **返回值**: 因子数据或None

##### `convert_to_decimal(self, value)`
- **功能**: 转换数值为高精度decimal类型
- **参数**:
  - `value`: 要转换的数值
- **返回值**: Decimal对象或原值

##### `optimize_memory_usage(self, data)`
- **功能**: 优化数据内存使用
- **参数**:
  - `data`: 要优化的数据
- **返回值**: 优化后的数据

---

## Views（视图层）

### MainAppView

**文件位置**: `views/main_app_view.py`

主窗口界面，集成菜单栏和工具栏。

#### 主要方法

##### `__init__(self, root)`
- **功能**: 初始化主应用视图
- **参数**:
  - `root`: Tkinter根窗口

##### `create_menu(self)`
- **功能**: 创建菜单栏
- **返回值**: 无

##### `create_main_layout(self)`
- **功能**: 创建主布局
- **返回值**: 无

##### `update_data_display(self, data)`
- **功能**: 更新数据显示
- **参数**:
  - `data`: 要显示的数据
- **返回值**: 无

##### `show_status_message(self, message, message_type='info')`
- **功能**: 显示状态消息
- **参数**:
  - `message` (str): 消息内容
  - `message_type` (str): 消息类型（info/warning/error）
- **返回值**: 无

---

### DocumentInfoView

**文件位置**: `views/document_info_view.py`

文档信息显示组件，支持字段动态配置。

#### 主要方法

##### `__init__(self, parent, config_manager)`
- **功能**: 初始化文档信息视图
- **参数**:
  - `parent`: 父容器
  - `config_manager`: 配置管理器实例

##### `create_info_fields(self)`
- **功能**: 创建信息字段
- **返回值**: 无

##### `update_document_info(self, doc_info)`
- **功能**: 更新文档信息
- **参数**:
  - `doc_info` (dict): 文档信息字典
- **返回值**: 无

##### `on_field_double_click(self, event, field_name)`
- **功能**: 处理字段双击事件
- **参数**:
  - `event`: 事件对象
  - `field_name` (str): 字段名称
- **返回值**: 无

---

### FactorView

**文件位置**: `views/factor_view.py`

因子分类视图组件，支持动态选项卡。

#### 主要方法

##### `__init__(self, parent, config_manager, on_sub_factor_select)`
- **功能**: 初始化因子视图
- **参数**:
  - `parent`: 父容器
  - `config_manager`: 配置管理器实例
  - `on_sub_factor_select`: 子因子选择回调函数

##### `create_factor_tabs(self)`
- **功能**: 创建因子选项卡
- **返回值**: 无

##### `create_scrollable_sub_factor_area(self, parent, sub_factors)`
- **功能**: 创建可滚动的子因子区域
- **参数**:
  - `parent`: 父容器
  - `sub_factors` (list): 子因子列表
- **返回值**: 无

##### `on_sub_factor_double_click(self, event, sub_factor)`
- **功能**: 处理子因子双击事件
- **参数**:
  - `event`: 事件对象
  - `sub_factor` (str): 子因子名称
- **返回值**: 无

---

### SubFactorDetailView

**文件位置**: `views/sub_factor_detail_view.py`

子因子详情显示组件，集成数据表格。

#### 主要方法

##### `__init__(self, parent, config_manager)`
- **功能**: 初始化子因子详情视图
- **参数**:
  - `parent`: 父容器
  - `config_manager`: 配置管理器实例

##### `create_search_frame(self)`
- **功能**: 创建搜索框架
- **返回值**: 无

##### `create_data_table(self)`
- **功能**: 创建数据表格
- **返回值**: 无

##### `update_data_display(self, data, sub_factor_name)`
- **功能**: 更新数据显示
- **参数**:
  - `data`: 要显示的数据
  - `sub_factor_name` (str): 子因子名称
- **返回值**: 无

##### `on_search_change(self, event=None)`
- **功能**: 处理搜索变化事件
- **参数**:
  - `event`: 事件对象（可选）
- **返回值**: 无

##### `copy_selection(self, format_type='text')`
- **功能**: 复制选中内容
- **参数**:
  - `format_type` (str): 复制格式（text/json/markdown）
- **返回值**: 无

---

## Utils（工具层）

### ValidationUtils

**文件位置**: `utils/validation_utils.py`

输入验证和数据安全获取工具。

#### 主要方法

##### `validate_input(value, expected_type, allow_none=False)`
- **功能**: 验证输入值类型
- **参数**:
  - `value`: 要验证的值
  - `expected_type`: 期望的类型
  - `allow_none` (bool): 是否允许None值
- **返回值**: 验证通过返回True，失败返回False

##### `safe_get_dict_value(dictionary, key, default=None)`
- **功能**: 安全获取字典值
- **参数**:
  - `dictionary` (dict): 字典对象
  - `key`: 键名
  - `default`: 默认值
- **返回值**: 字典值或默认值

##### `validate_file_path(file_path)`
- **功能**: 验证文件路径
- **参数**:
  - `file_path` (str): 文件路径
- **返回值**: 路径有效返回True，无效返回False

---

### DataUtils

**文件位置**: `utils/data_utils.py`

数据转换和处理工具。

#### 主要方法

##### `convert_data_dict(data_dict, display_names)`
- **功能**: 转换数据字典，应用显示名称
- **参数**:
  - `data_dict` (dict): 数据字典
  - `display_names` (dict): 显示名称映射
- **返回值**: 转换后的数据字典

##### `optimize_dataframe_memory(df)`
- **功能**: 优化DataFrame内存使用
- **参数**:
  - `df`: DataFrame对象
- **返回值**: 优化后的DataFrame

##### `format_number_with_precision(value, precision=2)`
- **功能**: 格式化数字精度
- **参数**:
  - `value`: 数值
  - `precision` (int): 精度位数
- **返回值**: 格式化后的字符串

---

### ClipboardUtils

**文件位置**: `utils/clipboard_utils.py`

剪贴板操作工具。

#### 主要方法

##### `copy_to_clipboard(content, format_type='text')`
- **功能**: 复制内容到剪贴板
- **参数**:
  - `content`: 要复制的内容
  - `format_type` (str): 内容格式类型
- **返回值**: 复制成功返回True，失败返回False

##### `format_as_json(data)`
- **功能**: 将数据格式化为JSON
- **参数**:
  - `data`: 要格式化的数据
- **返回值**: JSON格式字符串

##### `format_as_markdown_table(data)`
- **功能**: 将数据格式化为Markdown表格
- **参数**:
  - `data`: 要格式化的数据
- **返回值**: Markdown表格字符串

---

### LoggingUtils

**文件位置**: `utils/logging_utils.py`

日志记录和错误处理工具。

#### 主要方法

##### `log_performance(func_name, start_time, end_time)`
- **功能**: 记录性能日志
- **参数**:
  - `func_name` (str): 函数名称
  - `start_time` (float): 开始时间
  - `end_time` (float): 结束时间
- **返回值**: 无

##### `log_memory_usage(context='')`
- **功能**: 记录内存使用情况
- **参数**:
  - `context` (str): 上下文信息
- **返回值**: 无

##### `handle_exception(exception, context='')`
- **功能**: 处理异常并记录日志
- **参数**:
  - `exception`: 异常对象
  - `context` (str): 上下文信息
- **返回值**: 无

---

### LightweightData

**文件位置**: `utils/lightweight_data.py`

轻量级DataFrame实现，替代pandas。

#### 主要方法

##### `__init__(self, data=None, columns=None)`
- **功能**: 初始化轻量级DataFrame
- **参数**:
  - `data`: 数据（列表或字典）
  - `columns` (list): 列名列表

##### `add_row(self, row_data)`
- **功能**: 添加行数据
- **参数**:
  - `row_data`: 行数据（列表或字典）
- **返回值**: 无

##### `filter_rows(self, condition_func)`
- **功能**: 过滤行数据
- **参数**:
  - `condition_func`: 条件函数
- **返回值**: 新的LightweightData实例

##### `sort_by_column(self, column_name, ascending=True)`
- **功能**: 按列排序
- **参数**:
  - `column_name` (str): 列名
  - `ascending` (bool): 是否升序
- **返回值**: 无

##### `to_dict(self)`
- **功能**: 转换为字典格式
- **返回值**: 字典格式的数据

##### `get_memory_usage(self)`
- **功能**: 获取内存使用情况
- **返回值**: 内存使用字节数

---

## 使用示例

### 基本使用流程

```python
# 1. 初始化组件
config_manager = ConfigManager()
data_manager = DataManager()
root = tk.Tk()
view = MainAppView(root)
controller = AppController(view, config_manager, data_manager)

# 2. 加载数据
controller.load_data_from_file('sample.json')

# 3. 启动应用
root.mainloop()
```

### 配置管理示例

```python
# 加载配置
config_manager = ConfigManager()
if config_manager.load_config():
    factor_config = config_manager.get_factor_config()
    display_names = config_manager.get_display_names()
```

### 数据处理示例

```python
# 处理数据
data_manager = DataManager()
raw_data = data_manager.load_data('data.json')
processed_data = data_manager.process_data(raw_data, config)
```

---

## 注意事项

1. **线程安全**: 大部分类不是线程安全的，在多线程环境中使用时需要额外的同步机制。
2. **内存管理**: 处理大数据集时，建议使用`optimize_memory_usage`方法优化内存使用。
3. **错误处理**: 所有公共方法都包含适当的错误处理和日志记录。
4. **配置验证**: 在使用配置前，建议先调用`validate_config`方法验证配置格式。
5. **高精度计算**: 涉及数值计算时，使用`convert_to_decimal`方法确保计算精度。

---

## 版本信息

- **文档版本**: 1.0.0
- **API版本**: 1.2.14
- **最后更新**: 2024年
- **兼容性**: Python 3.7+, Tkinter 8.6+