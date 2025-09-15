import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import pandas as pd

class SubFactorDetailView:
    def __init__(self, parent_frame, controller):
        self.frame = parent_frame
        self.controller = controller
        
        # 初始化变量
        self.hierarchy_var = tk.StringVar()
        self.search_var = tk.StringVar()
        self.hierarchy_radios = {}
        self.current_level = None
        self._last_search_text = ""  # 初始化搜索状态跟踪变量
        
        # 绑定搜索变量变化事件
        self.search_var.trace("w", self.on_search_change)
        
        # 创建界面
        self.create_widgets()
        
        # 设置数据层次选择
        self.setup_data_hierarchy_selection()
        
        # 初始化表格事件绑定
        self.setup_table_events()
        
    def create_widgets(self):
        """创建界面组件"""
        # 创建基本信息区域
        self.create_basic_info_area()
        
        # 创建控制区域
        self.create_control_area()
        
        # 创建数据表格区域
        self.create_data_table_area()
        
    def create_basic_info_area(self):
        """创建基本信息区域"""
        # 基本信息框架
        basic_info_label_frame = ttk.LabelFrame(self.frame, text="基本信息", padding=5)
        basic_info_label_frame.pack(fill=tk.X, padx=5, pady=(5, 2))
        
        # 基本信息内容框架 - 动态高度
        self.basic_info_frame = tk.Frame(basic_info_label_frame, bg="white")
        self.basic_info_frame.pack(fill=tk.X, expand=False, padx=2, pady=2)
        
        # 创建字段值右键菜单
        self.field_menu = tk.Menu(self.frame, tearoff=0)
        self.field_menu.add_command(label="复制", command=self.copy_field_value)
        
    def create_control_area(self):
        """创建控制区域"""
        # 控制区域框架 - 减小高度
        control_frame = ttk.Frame(self.frame)
        control_frame.pack(fill=tk.X, padx=5, pady=1)
        
        # 使用Grid布局实现1:2的宽度占比
        control_frame.grid_columnconfigure(0, weight=1)  # 数据层次选择区域权重1
        control_frame.grid_columnconfigure(1, weight=2)  # 搜索过滤区域权重2
        
        # 数据层次选择区域 - 减小padding
        hierarchy_label_frame = ttk.LabelFrame(control_frame, text="数据层次选择", padding=3)
        hierarchy_label_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 4))
        
        self.hierarchy_selection_frame = ttk.Frame(hierarchy_label_frame)
        self.hierarchy_selection_frame.pack(fill=tk.BOTH, expand=True)
        
        # 搜索过滤区域 - 单行布局，减小padding
        search_label_frame = ttk.LabelFrame(control_frame, text="🔍 搜索过滤", padding=3)
        search_label_frame.grid(row=0, column=1, sticky="nsew", padx=(4, 0))
        
        # 单行搜索容器
        search_frame = ttk.Frame(search_label_frame)
        search_frame.pack(fill=tk.X, pady=1)
        
        # 实时搜索标签
        self.search_tooltip = ttk.Label(search_frame, text="⚡ 实时搜索", 
                                      font=("Microsoft YaHei UI", 9, "bold"), 
                                      foreground="#2563eb")
        self.search_tooltip.pack(side=tk.LEFT, padx=(0, 6))
        
        # 搜索输入框
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, 
                               font=("Microsoft YaHei UI", 10), width=18)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 6))
        
        # 清除按钮 - 正方形设计，科技感图标
        clear_button = ttk.Button(search_frame, text="⌫", width=3, 
                                command=self.on_clear_search)
        clear_button.pack(side=tk.RIGHT)
        
    def create_data_table_area(self):
        """创建数据表格区域"""
        # 数据表格区域
        table_label_frame = ttk.LabelFrame(self.frame, text="数据表格", padding=5)
        table_label_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=(2, 5))
        
        # 表格框架
        self.table_frame = ttk.Frame(table_label_frame)
        self.table_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建tksheet表格
        try:
            from tksheet import Sheet
            self.data_table = Sheet(self.table_frame,
                                  page_up_down_select_row=True,
                                  startup_select=(0, 1, "rows"),
                                  headers=[],
                                  height=400)
            self.data_table.pack(fill=tk.BOTH, expand=True)
            
            # 确保表格完全空白
            self.data_table.set_sheet_data([])
            self.data_table.headers([])
            
            # 启用表格功能
            self.data_table.enable_bindings(("single_select",
                                           "row_select",
                                           "column_width_resize",
                                           "arrowkeys",
                                           "right_click_popup_menu",
                                           "rc_select",
                                           "copy"))
        except ImportError:
            # 如果tksheet不可用，使用Treeview作为备选
            self.create_fallback_table()
            
    def create_fallback_table(self):
        """创建备选表格（使用Treeview）"""
        # 创建Treeview表格作为备选
        tree_frame = ttk.Frame(self.table_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建滚动条
        v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
        
        # 创建Treeview
        self.data_table = ttk.Treeview(tree_frame, 
                                     yscrollcommand=v_scrollbar.set,
                                     xscrollcommand=h_scrollbar.set,
                                     show="tree headings")
        
        # 配置滚动条
        v_scrollbar.config(command=self.data_table.yview)
        h_scrollbar.config(command=self.data_table.xview)
        
        # 布局
        self.data_table.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
    def setup_table_events(self):
        """设置表格事件绑定"""
        try:
            # 如果使用tksheet
            if hasattr(self.data_table, 'extra_bindings'):
                # 绑定右键菜单
                self.data_table.popup_menu_add_command("复制行 (文本)", self.copy_row_as_text)
                self.data_table.popup_menu_add_command("复制行 (JSON)", self.copy_row_as_json)
                self.data_table.popup_menu_add_command("复制行 (Markdown)", self.copy_row_as_markdown)
                
                # 绑定单元格选择事件
                self.data_table.extra_bindings(["cell_select"], func=self.on_cell_select)
                
                # 绑定双击事件
                self.data_table.extra_bindings(["double_click_cell"], func=self.on_cell_double_click)
        except Exception as e:
            print(f"设置表格事件绑定时出错: {e}")
            
    def on_cell_select(self, event):
        """处理单元格选择事件"""
        if hasattr(event, 'row') and hasattr(event, 'column'):
            self.current_cell = (event.row, event.column)
            
    def on_cell_double_click(self, event):
        """处理单元格双击事件"""
        if hasattr(event, 'row') and hasattr(event, 'column'):
            # 复制单元格值
            self.copy_current_cell_value()
            
    def copy_row_as_text(self):
        """复制行数据为文本格式"""
        try:
            # 获取选中的行
            selected_rows = self.data_table.get_selected_rows()
            if not selected_rows:
                # 如果没有选中行，尝试获取当前选中的单元格所在行
                selected_cells = self.data_table.get_selected_cells()
                if selected_cells:
                    # 将set转换为list，然后获取第一个单元格的行号
                    selected_cells_list = list(selected_cells)
                    if selected_cells_list:
                        selected_rows = {selected_cells_list[0][0]}  # 创建包含行号的set
            
            if selected_rows:
                # 将set转换为list获取第一个行号
                row_idx = list(selected_rows)[0]
                # 获取行数据
                row_data = self.data_table.get_row_data(row_idx)
                if row_data:
                    # 将行数据转换为制表符分隔的文本
                    text_data = "\t".join([str(cell) if cell is not None else "" for cell in row_data])
                    
                    # 复制到剪贴板
                    root = self.frame.winfo_toplevel()
                    root.clipboard_clear()
                    root.clipboard_append(text_data)
                    root.update()
                    
                    # 移除搜索提示显示
                    print(f"已复制行数据到剪贴板: {text_data[:100]}...")
                else:
                    print("无法获取行数据")
            else:
                print("请先选择要复制的行")
        except Exception as e:
            print(f"复制行数据为文本格式时出错: {e}")
            import traceback
            traceback.print_exc()
            
    def copy_row_as_json(self):
        """复制行数据为JSON格式"""
        try:
            # 获取选中的行
            selected_rows = self.data_table.get_selected_rows()
            if not selected_rows:
                # 如果没有选中行，尝试获取当前选中的单元格所在行
                selected_cells = self.data_table.get_selected_cells()
                if selected_cells:
                    # 将set转换为list，然后获取第一个单元格的行号
                    selected_cells_list = list(selected_cells)
                    if selected_cells_list:
                        selected_rows = {selected_cells_list[0][0]}  # 创建包含行号的set
            
            if selected_rows:
                # 将set转换为list获取第一个行号
                row_idx = list(selected_rows)[0]
                row_data = self.data_table.get_row_data(row_idx)
                headers = self.data_table.headers()
                
                if row_data and headers:
                    # 创建字典
                    row_dict = {}
                    for i, header in enumerate(headers):
                        if i < len(row_data):
                            row_dict[header] = row_data[i] if row_data[i] is not None else ""
                    
                    # 转换为JSON
                    import json
                    json_data = json.dumps(row_dict, ensure_ascii=False, indent=2)
                    
                    # 复制到剪贴板
                    root = self.frame.winfo_toplevel()
                    root.clipboard_clear()
                    root.clipboard_append(json_data)
                    root.update()
                    
                    # 移除搜索提示显示
                    print(f"已复制JSON数据到剪贴板: {json_data[:100]}...")
                else:
                    print("无法获取行数据或表头")
            else:
                print("请先选择要复制的行")
        except Exception as e:
            print(f"复制行数据为JSON格式时出错: {e}")
            import traceback
            traceback.print_exc()
            
    def copy_row_as_markdown(self):
        """复制行数据为Markdown表格格式"""
        try:
            # 获取选中的行
            selected_rows = self.data_table.get_selected_rows()
            if not selected_rows:
                # 如果没有选中行，尝试获取当前选中的单元格所在行
                selected_cells = self.data_table.get_selected_cells()
                if selected_cells:
                    # 将set转换为list，然后获取第一个单元格的行号
                    selected_cells_list = list(selected_cells)
                    if selected_cells_list:
                        selected_rows = {selected_cells_list[0][0]}  # 创建包含行号的set
            
            if selected_rows:
                # 将set转换为list获取第一个行号
                row_idx = list(selected_rows)[0]
                row_data = self.data_table.get_row_data(row_idx)
                headers = self.data_table.headers()
                
                if row_data and headers:
                    # 创建Markdown表格
                    markdown_lines = []
                    
                    # 表头
                    header_line = "| " + " | ".join(headers) + " |"
                    separator_line = "| " + " | ".join(["---"] * len(headers)) + " |"
                    
                    # 数据行
                    data_cells = [str(cell) if cell is not None else "" for cell in row_data]
                    data_line = "| " + " | ".join(data_cells) + " |"
                    
                    markdown_data = "\n".join([header_line, separator_line, data_line])
                    
                    # 复制到剪贴板
                    root = self.frame.winfo_toplevel()
                    root.clipboard_clear()
                    root.clipboard_append(markdown_data)
                    root.update()
                    
                    # 移除搜索提示显示
                    print(f"已复制Markdown数据到剪贴板: {markdown_data[:100]}...")
                else:
                    print("无法获取行数据或表头")
            else:
                print("请先选择要复制的行")
        except Exception as e:
            print(f"复制行数据为Markdown格式时出错: {e}")
            import traceback
            traceback.print_exc()
            
    def copy_current_cell_value(self):
        """复制当前选中单元格的值"""
        try:
            # 尝试多种方式获取选中的单元格
            cell_value = None
            
            # 方式1：使用current_cell属性
            if hasattr(self, 'current_cell') and self.current_cell:
                row, column = self.current_cell
                cell_value = self.data_table.get_cell_data(row, column)
            
            # 方式2：获取当前选中的单元格
            if cell_value is None:
                selected_cells = self.data_table.get_selected_cells()
                if selected_cells:
                    # 将set转换为list获取第一个单元格
                    selected_cells_list = list(selected_cells)
                    if selected_cells_list:
                        row, col = selected_cells_list[0]
                        cell_value = self.data_table.get_cell_data(row, col)
            
            # 方式3：获取选中行的第一个单元格
            if cell_value is None:
                selected_rows = self.data_table.get_selected_rows()
                if selected_rows:
                    # 将set转换为list获取第一个行号
                    selected_rows_list = list(selected_rows)
                    if selected_rows_list:
                        row_data = self.data_table.get_row_data(selected_rows_list[0])
                        if row_data:
                            cell_value = row_data[0]  # 获取第一列的值
            
            if cell_value is not None:
                # 确保使用根窗口进行剪贴板操作
                root = self.frame.winfo_toplevel()
                root.clipboard_clear()
                root.clipboard_append(str(cell_value))
                root.update()  # 确保更新剪贴板内容
                
                # 显示提示信息
                if hasattr(self, 'search_tooltip'):
                    self.search_tooltip.config(text="✅ 已复制单元格内容", foreground="#006600")
                    # 2秒后恢复提示
                    self.frame.after(2000, lambda: self.search_tooltip.config(text="⚡ 实时搜索", foreground="#2563eb"))
                print(f"已复制单元格内容到剪贴板: {str(cell_value)[:50]}...")
            else:
                print("无法获取选中的单元格值")
        except Exception as e:
            print(f"复制当前单元格值时出错: {e}")
            import traceback
            traceback.print_exc()
    
    def copy_field_value(self):
        """复制字段值"""
        if hasattr(self, 'current_field_value'):
            self.frame.clipboard_clear()
            self.frame.clipboard_append(str(self.current_field_value))
    
    def display_basic_info(self, info):
        # 清空现有内容
        for widget in self.basic_info_frame.winfo_children():
            widget.destroy()
        
        if not info:
            return
        
        # 直接在basic_info_frame上创建主容器框架，不添加额外滚动条
        info_frame = tk.Frame(self.basic_info_frame, bg="white")
        info_frame.pack(fill=tk.X, expand=False, padx=5, pady=5)
        
        # 获取配置文件中的字段顺序
        if hasattr(self.controller, 'current_sub_factor') and self.controller.current_sub_factor:
            # 从配置文件获取字段顺序
            basic_info_fields = self.controller.config_manager.get_sub_factor_basic_info(self.controller.current_sub_factor)
            # 转换为显示名称并保持配置顺序
            ordered_fields = []
            for field_id in basic_info_fields:
                display_name = self.controller.config_manager.get_display_name(field_id)
                if display_name in info:
                    ordered_fields.append(display_name)
            # 添加配置中没有但info中存在的字段（以防万一）
            for field in info.keys():
                if field not in ordered_fields:
                    ordered_fields.append(field)
        else:
            # 如果没有当前子因子，使用原有的排序方式
            ordered_fields = sorted(info.keys())
        
        # 固定布局：每行4个字段，确保对齐
        fields_per_row = 4
        field_groups = []
        
        # 将字段按每行4个分组
        for i in range(0, len(ordered_fields), fields_per_row):
            group = ordered_fields[i:i + fields_per_row]
            field_groups.append(group)
        
        # 计算需要的行数，默认最少2行
        required_rows = max(2, len(field_groups))
        
        # 动态设置基本信息框架的高度（每行约30像素）
        dynamic_height = required_rows * 30
        self.basic_info_frame.configure(height=dynamic_height)
        self.basic_info_frame.pack_propagate(False)  # 固定计算出的高度
        
        # 使用Grid布局确保字段精确对齐
        # 配置列权重，确保每列等宽
        for col in range(fields_per_row):
            info_frame.grid_columnconfigure(col, weight=1, uniform="field_column")
        
        # 显示字段组，使用Grid布局确保对齐
        for row_idx, group in enumerate(field_groups):
            # 配置行权重
            info_frame.grid_rowconfigure(row_idx, weight=0)
            
            # 为每个字段创建标签并放置在Grid中
            for col_idx, field_key in enumerate(group):
                field_value = info[field_key]
                value_text = str(field_value) if field_value is not None else "N/A"
                
                # 字段名和值在同一行显示 - 统一字体颜色
                if value_text == "N/A":
                    value_color = "#333333"  # 统一为深灰色
                    value_font = ("Microsoft YaHei UI", 9, "italic")
                else:
                    value_color = "#000000"  # 统一为黑色
                    value_font = ("Microsoft YaHei UI", 9, "normal")
                
                # 创建字段标签
                field_text = f"{field_key}: {value_text}"
                field_label = tk.Label(info_frame, text=field_text, 
                                     font=("Microsoft YaHei UI", 9),
                                     foreground=value_color,
                                     cursor="hand2",
                                     background="white",
                                     anchor="w",
                                     relief="flat",
                                     padx=8, pady=3)
                # 使用Grid布局放置标签，sticky="ew"确保水平填充
                field_label.grid(row=row_idx, column=col_idx, sticky="ew", padx=2, pady=1)
                
                # 绑定复制功能
                field_label.bind("<Button-3>", lambda e, text=value_text: self.show_field_menu(e, text))
                field_label.bind("<Double-Button-1>", lambda e, text=value_text: self.copy_value_to_clipboard(text))
                
                # 悬停效果（改变背景色）
                def on_enter(e, label=field_label):
                    label.configure(background="#e8f4fd")
                def on_leave(e, label=field_label):
                    label.configure(background="white")
                
                field_label.bind("<Enter>", on_enter)
                field_label.bind("<Leave>", on_leave)
                
    def show_field_menu(self, event, value):
        """显示字段值右键菜单"""
        self.current_field_value = value
        self.field_menu.post(event.x_root, event.y_root)
        
    def copy_value_to_clipboard(self, value):
        """复制值到剪贴板"""
        self.frame.clipboard_clear()
        self.frame.clipboard_append(str(value))

    def setup_data_hierarchy_selection(self):
        """设置数据层次选择单选按钮"""
        # 清除现有的单选按钮
        for widget in self.hierarchy_selection_frame.winfo_children():
            widget.destroy()
            
        # 获取数据层次名称
        hierarchy_levels = self.controller.data_manager.get_hierarchy_levels()
        
        # 创建单选按钮
        for i, level in enumerate(hierarchy_levels):
            display_name = self.controller.config_manager.get_data_hierarchy_name(level)
            radio = ttk.Radiobutton(
                self.hierarchy_selection_frame, 
                text=display_name,
                variable=self.hierarchy_var,
                value=level,
                command=lambda l=level: self.on_hierarchy_level_select(l)
            )
            radio.pack(side=tk.LEFT, padx=5, pady=2)
            self.hierarchy_radios[level] = radio
            
        # 默认选择配置的层次
        if hierarchy_levels:
            default_level = self.controller.config_manager.get_default_hierarchy_level()
            if default_level and default_level in hierarchy_levels:
                selected_level = default_level
            else:
                selected_level = hierarchy_levels[0]
            
            self.hierarchy_var.set(selected_level)
            self.on_hierarchy_level_select(selected_level)
    
    def on_hierarchy_level_select(self, level):
        """当用户选择数据层次时触发"""
        # 标记层级切换状态
        self._hierarchy_changing = True
        
        # 保存当前选择的层级
        self.current_level = level
        self.controller.on_hierarchy_node_select(level)
        # 重置搜索框
        self.search_var.set("")
        
        # 延迟重置层级切换标记
        def reset_hierarchy_changing():
            self._hierarchy_changing = False
        self.frame.after(300, reset_hierarchy_changing)
        
    def on_search_change(self, *args):
        """当搜索框内容变化时触发"""
        # 优化防抖机制 - 进一步增加延迟时间以减少闪动
        if hasattr(self, "_search_after_id"):
            self.frame.after_cancel(self._search_after_id)
        
        # 设置搜索状态指示
        if hasattr(self, 'search_tooltip'):
            self.search_tooltip.config(text="🔍 搜索中...", foreground="#666666")
        
        # 设置延迟到50毫秒，提供极速响应的实时搜索体验
        self._search_after_id = self.frame.after(50, self._delayed_search_filter)
        
    def on_search_button_click(self):
        """当点击搜索按钮时触发"""
        self.apply_search_filter()
        
    def on_clear_search(self):
        """清空搜索条件"""
        self.search_var.set("")
        # 标记为清空搜索状态，保持列宽不变
        self._is_clearing_search = True
        # 重置搜索过滤状态
        self._is_search_filtering = False
        self.apply_search_filter()
        # 延迟重置标记，确保所有相关操作完成后再重置，与搜索过滤保持一致的延迟时间
        self.frame.after(500, lambda: setattr(self, '_is_clearing_search', False))
        
    def _delayed_search_filter(self):
        """延迟执行的搜索过滤"""
        # 恢复搜索提示文本
        if hasattr(self, 'search_tooltip'):
            self.search_tooltip.config(text="⚡ 实时搜索", foreground="#2563eb")
        
        # 获取当前搜索文本
        current_search_text = self.search_var.get().strip()
        
        # 检查是否与上次搜索相同，避免重复搜索
        if hasattr(self, '_last_executed_search') and self._last_executed_search == current_search_text:
            return  # 搜索条件未变化，跳过执行
        
        # 记录本次搜索条件
        self._last_executed_search = current_search_text
        
        # 执行实际的搜索过滤
        self.apply_search_filter()
    
    def apply_search_filter(self):
        """应用搜索过滤"""
        search_text = self.search_var.get().lower()
        
        # 检查搜索文本是否与上次相同，如果相同则跳过
        if hasattr(self, '_last_apply_search_text') and self._last_apply_search_text == search_text:
            return
            
        # 保存当前搜索文本（用于避免重复搜索）
        self._last_apply_search_text = search_text
        
        # 标记为搜索过滤状态
        self._is_search_filtering = bool(search_text.strip())
        
        # 获取当前选中的层次
        current_level = self.hierarchy_var.get()
        
        # 通知控制器应用过滤
        self.controller.apply_search_filter(current_level, search_text)
        
        # 延迟重置搜索过滤标记，确保display_data_table能正确识别搜索状态
        # 增加延迟时间，确保表格更新完成后再重置标记
        def reset_search_filtering():
            self._is_search_filtering = False
        self.frame.after(500, reset_search_filtering)
            
    def display_data_table(self, df, display_columns=None, columns_config=None):
        # 更智能的数据比较 - 检查数据内容、行数和列配置是否真正发生变化
        if hasattr(self, 'current_df') and hasattr(self, 'current_columns'):
            if self.current_df is not None and not df.empty and columns_config is not None:
                # 检查列配置是否相同
                columns_same = self.current_columns == columns_config
                # 检查数据是否相同（更高效的比较方式）
                data_same = (len(self.current_df) == len(df) and 
                           list(self.current_df.columns) == list(df.columns) and 
                           self.current_df.equals(df))
                
                if columns_same and data_same:
                    # 数据和列配置没有变化，跳过更新
                    return
                    
        # 清除可能存在的空数据提示
        for widget in self.table_frame.winfo_children():
            if isinstance(widget, ttk.Label) and widget.cget("text") == "暂无数据":
                widget.destroy()
        
        # 确定要显示的列
        if columns_config and isinstance(columns_config, list) and len(columns_config) > 0:
            # 如果有列配置，优先使用配置的列
            columns_to_show = columns_config
        elif not df.empty:
            # 如果有数据但没有列配置，使用DataFrame的列
            columns_to_show = list(df.columns)
        else:
            # 既没有数据也没有列配置，显示空数据提示
            self.data_table.set_sheet_data([])
            self.data_table.headers([])
            empty_label = ttk.Label(self.table_frame, text="暂无数据", font=("Microsoft YaHei UI", 12), foreground="#333333")
            empty_label.place(relx=0.5, rely=0.5, anchor="center")
            return
        
        # 设置表格列标题
        headers = []
        for col in columns_to_show:
            # 从controller获取字段的中文显示名称
            display_name = self.controller.config_manager.get_display_name(col)
            headers.append(display_name)
        
        # 设置表格数据
        data = []
        if not df.empty:
            for _, row in df.iterrows():
                row_data = []
                for col in columns_to_show:
                    if pd.notna(row[col]) and col in df.columns:
                        value = row[col]
                        # 保持数字精度，避免精度丢失
                        if isinstance(value, (int, float)):
                            # 对于数字类型，保持原始精度
                            if isinstance(value, float):
                                # 浮点数保留足够精度，避免科学计数法
                                formatted_value = f"{value:.10g}"
                            else:
                                formatted_value = str(value)
                        else:
                            formatted_value = str(value)
                        row_data.append(formatted_value)
                    else:
                        row_data.append("")
                data.append(row_data)
        
        # 智能更新表格 - 只在必要时更新标题和数据
        current_headers = getattr(self, 'current_headers', [])
        current_data = self.data_table.get_sheet_data() if hasattr(self.data_table, 'get_sheet_data') else []
        
        # 只在标题发生变化时更新标题
        if current_headers != headers:
            self.data_table.headers(headers)
            
        # 真正的增量数据更新 - 逐行比较和更新
        if current_data != data:
            self._update_table_incrementally(current_data, data)
        
        # 智能列宽调整策略：
        # 1. 只有在非搜索状态下才重新计算列宽
        # 2. 搜索过滤（包括结果为空）和清空搜索时都保持原有列宽
        # 使用搜索文本来判断搜索状态，避免时序问题
        current_search_text = self.search_var.get().strip() if hasattr(self, 'search_var') else ""
        is_search_filter = bool(current_search_text)
        is_clearing_search = hasattr(self, '_is_clearing_search') and self._is_clearing_search
        
        # 搜索状态判断完成
        
        # 列宽重算条件：
        # 1. 非搜索状态下且列配置变化时重算
        # 2. 清空搜索条件时也需要重算（从搜索状态回到正常状态）
        was_searching = hasattr(self, '_last_search_text') and bool(self._last_search_text)
        now_searching = is_search_filter
        search_state_changed = was_searching != now_searching
        
        need_recalc_width = ((not is_search_filter and not is_clearing_search and  # 非搜索状态下的常规重算
                            (not hasattr(self, 'last_columns_config') or 
                             self.last_columns_config != columns_to_show or
                             current_headers != headers)) or
                            (search_state_changed and not now_searching))  # 从搜索状态切换到非搜索状态时重算
        
        # 记录当前搜索状态用于下次比较
        self._last_search_text = current_search_text
        
        if need_recalc_width:
            # 首先获取表格容器的宽度
            self.data_table.update_idletasks()  # 确保尺寸已更新
            table_width = self.table_frame.winfo_width() - 20  # 减去一些边距
            if table_width <= 0:  # 如果宽度无效，使用默认宽度
                table_width = 800
            
            # 计算并应用列宽 - 基于当前数据内容
            col_widths = self._calculate_column_widths(columns_to_show, headers, df, table_width)
            self._apply_column_widths(col_widths)
            
            # 保存列配置用于下次比较
            self.last_columns_config = columns_to_show.copy() if columns_to_show else []
            
            # 保存列宽设置，用于搜索过滤时保持不变
            self._saved_column_widths = col_widths.copy()
        elif (is_search_filter or is_clearing_search):
            # 搜索过滤或清空搜索时的列宽处理
            if df.empty and is_search_filter:
                # 搜索无结果时，重新计算列宽以充分利用空间
                self.data_table.update_idletasks()
                table_width = self.table_frame.winfo_width() - 20
                if table_width <= 0:
                    table_width = 800
                
                # 为空数据重新计算列宽，确保充分利用空间
                col_widths = self._calculate_column_widths(columns_to_show, headers, df, table_width)
                self._apply_column_widths(col_widths)
            elif hasattr(self, '_saved_column_widths'):
                # 有搜索结果或清空搜索时，恢复之前保存的列宽
                def restore_column_widths():
                    if hasattr(self, '_saved_column_widths'):
                        self._apply_column_widths(self._saved_column_widths)
                self.frame.after_idle(restore_column_widths)
            
        # 确保在窗口调整大小时重新计算列宽
        def on_table_configure(event):
            # 避免过于频繁的调整 - 增加延迟时间减少闪动
            if hasattr(self, '_resize_timer'):
                self.frame.after_cancel(self._resize_timer)
            # 增加延迟到300毫秒，减少刷新频率
            self._resize_timer = self.frame.after(300, lambda: self.adjust_column_widths(columns_to_show, headers, df))
            
        # 绑定窗口大小变化事件
        self.table_frame.bind('<Configure>', on_table_configure)
        
        # 保存当前数据和列配置，用于后续调整
        self.current_columns = columns_to_show
        self.current_headers = headers
        self.current_df = df.copy() if not df.empty else None
        
        # 延迟行颜色设置 - 避免频繁重绘导致闪动
        current_row_count = len(data)
        last_row_count = getattr(self, 'last_row_count', -1)
        
        if current_row_count != last_row_count:
            # 延迟设置行颜色，避免与数据更新同时进行
            def apply_row_colors():
                try:
                    self.row_colors = {}
                    for i in range(current_row_count):
                        if i % 2 == 0:
                            self.row_colors[i] = {"bg": "#ffffff", "fg": "#000000"}
                            self.data_table.highlight_rows(rows=i, bg="#ffffff")
                        else:
                            self.row_colors[i] = {"bg": "#f0f0f0", "fg": "#000000"}
                            self.data_table.highlight_rows(rows=i, bg="#f0f0f0")
                except:
                    pass  # 忽略可能的错误，避免影响主流程
            
            # 延迟100毫秒执行，让数据更新先完成
            self.frame.after(100, apply_row_colors)
            
            # 保存行数用于下次比较
            self.last_row_count = current_row_count
        
        # 初始化高亮行变量
        self.highlighted_row = None
        
        # 保存原始数据用于搜索过滤
        self.original_data = df.copy()
        
        # 绑定排序事件
        self.data_table.extra_bindings(["column_select"], func=self.on_column_select)
    
    def _calculate_column_widths(self, columns_to_show, headers, df, table_width):
        """计算列宽度"""
        col_widths = []
        for col_idx, col in enumerate(columns_to_show):
            # 基础宽度 - 确保标题能完整显示
            header_text = headers[col_idx] if col_idx < len(headers) else col
            max_width = len(header_text) * 10 + 30  # 增加一些额外空间
            
            # 如果有数据，根据内容调整列宽
            if not df.empty and col in df.columns:
                # 限制检查的行数以提高性能，使用采样方式
                sample_size = min(100, len(df))
                sample_data = df[col].head(sample_size) if len(df) > sample_size else df[col]
                
                for value in sample_data:
                    if pd.notna(value):  # 确保值不是NaN
                        str_value = str(value)
                        width = len(str_value) * 8 + 20
                        if width > max_width:
                            max_width = width
            
            # 限制最大宽度和确保最小宽度
            max_width = max(80, min(max_width, 300))
            col_widths.append(max_width)
        
        # 计算总宽度和调整系数
        total_width = sum(col_widths)
        if total_width < table_width and len(col_widths) > 0:
            # 如果总宽度小于表格宽度，优先扩展列宽以充分利用空间
            remaining_width = table_width - total_width
            
            # 策略1：如果列数较少（<=3列），平均分配剩余宽度
            if len(col_widths) <= 3:
                extra_width_per_col = remaining_width // len(col_widths)
                col_widths = [w + extra_width_per_col for w in col_widths]
                # 处理除法余数
                remainder = remaining_width % len(col_widths)
                for i in range(remainder):
                    col_widths[i] += 1
            else:
                # 策略2：列数较多时，按比例分配
                ratio = table_width / total_width
                col_widths = [int(w * ratio) for w in col_widths]
                
            # 确保总宽度不超过表格宽度
            actual_total = sum(col_widths)
            if actual_total > table_width:
                # 如果超出，按比例缩减
                reduction_ratio = table_width / actual_total
                col_widths = [int(w * reduction_ratio) for w in col_widths]
        
        return col_widths
    
    def _apply_column_widths(self, col_widths):
        """应用列宽度"""
        for col_idx, width in enumerate(col_widths):
            if col_idx < len(col_widths):  # 确保列索引有效
                self.data_table.column_width(column=col_idx, width=width)
        
        # 强制刷新表格显示
        self.data_table.refresh()
    
    def _update_table_incrementally(self, old_data, new_data):
        """智能表格更新策略：只有实时搜索且有结果时使用增量更新，其他情况都重建表格"""
        try:
            # 如果新数据为空，清空表格
            if not new_data:
                self.data_table.set_sheet_data([])
                return
            
            # 如果旧数据为空，直接设置新数据
            if not old_data:
                self.data_table.set_sheet_data(new_data)
                return
            
            # 检查是否为实时搜索场景（搜索过滤且有结果）
            is_realtime_search = (
                hasattr(self, '_is_search_filtering') and self._is_search_filtering and
                new_data and len(new_data) > 0  # 确保搜索有结果
            )
            
            # 只有实时搜索且有结果时才使用增量更新，其他情况都重建表格
            if is_realtime_search:
                # 获取当前表格行数
                current_rows = len(old_data)
                new_rows = len(new_data)
                
                # 对于行数相同的情况，检查数据内容是否有变化
                if current_rows == new_rows:
                    content_changed = False
                    for i in range(current_rows):
                        if old_data[i] != new_data[i]:
                            content_changed = True
                            break
                    
                    if not content_changed:
                        return  # 数据没有变化，跳过更新
                    
                    # 数据有变化但行数相同，使用优化的批量更新（避免闪动）
                    # 临时禁用表格重绘以减少闪烁
                    if hasattr(self.data_table, 'disable_bindings'):
                        self.data_table.disable_bindings()
                    
                    try:
                        # 批量更新所有变化的单元格
                        for row_idx in range(current_rows):
                            if old_data[row_idx] != new_data[row_idx]:
                                # 逐列更新不同的单元格，禁用重绘
                                for col_idx, cell_value in enumerate(new_data[row_idx]):
                                    if (col_idx >= len(old_data[row_idx]) or 
                                        old_data[row_idx][col_idx] != cell_value):
                                        self.data_table.set_cell_data(row_idx, col_idx, cell_value, redraw=False)
                    finally:
                        # 重新启用绑定
                        if hasattr(self.data_table, 'enable_bindings'):
                            self.data_table.enable_bindings()
                    
                    # 延迟重绘，确保所有更新完成后一次性刷新
                    def delayed_refresh():
                        if hasattr(self.data_table, 'refresh'):
                            self.data_table.refresh()
                        elif hasattr(self.data_table, 'redraw'):
                            self.data_table.redraw()
                    self.frame.after_idle(delayed_refresh)
                else:
                    # 行数不同，即使是实时搜索也要重建表格
                    self.data_table.set_sheet_data(new_data)
            else:
                # 所有其他情况都重建表格：清空搜索、层级切换、搜索结果为空等
                self.data_table.set_sheet_data(new_data)
            
        except Exception as e:
            # 如果更新失败，回退到标准方法
            print(f"表格更新失败，回退到标准方法: {e}")
            self.data_table.set_sheet_data(new_data)
            
    def on_column_select(self, event):
        """处理列选择事件，用于排序"""
        if event.column is not None:
            self.sort_by_column(event.column)
    
    def sort_by_column(self, col_idx):
        """按列排序表格数据"""
        # 获取当前数据
        data = self.data_table.get_sheet_data()
        if not data:
            return
            
        # 确定排序方向
        if hasattr(self, 'sort_direction') and self.sort_column == col_idx:
            self.sort_direction = not self.sort_direction
        else:
            self.sort_direction = False  # 默认降序
            self.sort_column = col_idx
        
        # 排序数据
        sorted_data = sorted(data, key=lambda row: row[col_idx] if row[col_idx] else "", reverse=self.sort_direction)
        
        # 更新表格数据
        self.data_table.set_sheet_data(sorted_data)
        
        # 重新应用交替行颜色
        for i in range(len(sorted_data)):
            if i % 2 == 0:
                self.data_table.highlight_rows(rows=i, bg="#ffffff")  # 偶数行
            else:
                self.data_table.highlight_rows(rows=i, bg="#f0f0f0")  # 奇数行
        
    def adjust_column_widths(self, columns_to_show, headers, df):
        """根据窗口大小调整列宽"""
        # 获取表格容器的当前宽度
        self.data_table.update_idletasks()
        table_width = self.table_frame.winfo_width() - 20  # 减去一些边距
        if table_width <= 0:  # 如果宽度无效，使用默认宽度
            table_width = 800
            
        # 检查表格宽度变化是否足够大，避免微小变化导致的频繁刷新
        if hasattr(self, '_last_table_width'):
            width_change = abs(table_width - self._last_table_width)
            # 如果宽度变化小于阈值(20像素)，则跳过调整
            if width_change < 20:
                return
        
        # 记录当前宽度，用于下次比较
        self._last_table_width = table_width
        
        # 计算每列的基础宽度
        col_widths = []
        for col_idx, col in enumerate(columns_to_show):
            # 基础宽度 - 确保标题能完整显示
            header_text = headers[col_idx] if col_idx < len(headers) else col
            max_width = len(header_text) * 10 + 30  # 增加一些额外空间
            
            # 如果有数据，根据内容调整列宽
            if df is not None and not df.empty and col in df.columns:
                for i, value in enumerate(df[col]):
                    if i > 100:  # 限制检查的行数以提高性能
                        break
                    if pd.notna(value):  # 确保值不是NaN
                        str_value = str(value)
                        width = len(str_value) * 8 + 20
                        if width > max_width:
                            max_width = width
            
            # 限制最大宽度
            if max_width > 300:
                max_width = 300
            # 确保最小宽度
            if max_width < 80:
                max_width = 80
                
            col_widths.append(max_width)
        
        # 计算总宽度和调整系数
        total_width = sum(col_widths)
        if total_width < table_width and len(col_widths) > 0:
            # 如果总宽度小于表格宽度，按比例增加每列宽度
            ratio = table_width / total_width
            col_widths = [int(w * ratio) for w in col_widths]
        
        # 应用列宽
        for col_idx, width in enumerate(col_widths):
            if col_idx < len(columns_to_show):  # 确保列索引有效
                self.data_table.column_width(column=col_idx, width=width)
        
        # 重新应用交替行颜色
        data = self.data_table.get_sheet_data()
        for i in range(len(data)):
            if i % 2 == 0:
                self.data_table.highlight_rows(rows=i, bg="#ffffff")  # 偶数行
            else:
                self.data_table.highlight_rows(rows=i, bg="#f0f0f0")  # 奇数行
                
        # 更新列标题显示排序方向
        if hasattr(self, 'sort_column') and hasattr(self, 'sort_direction'):
            headers = self.data_table.headers()
            for i, header in enumerate(headers):
                if i == self.sort_column:
                    direction = "▲" if self.sort_direction else "▼"
                    # 移除可能存在的排序指示器
                    if "▲" in header or "▼" in header:
                        header = header.split(' ')[0]
                    headers[i] = f"{header} {direction}"
                elif "▲" in header or "▼" in header:
                    # 移除其他列的排序指示器
                    headers[i] = header.split(' ')[0]
                    
            # 更新表头
            self.data_table.headers(headers)
        
    def on_row_select(self, event):
        """处理表格行选择事件"""
        # tksheet的行选择通过extra_bindings绑定
        # 在初始化时添加以下绑定
        if not hasattr(self, "row_select_binding_added"):
            self.data_table.extra_bindings(["row_select"], func=self.on_row_select_event)
            self.row_select_binding_added = True
            
    def on_row_select_event(self, event):
        """处理tksheet的行选择事件"""
        if event.row is not None:
            # 恢复所有行的原始颜色
            self.restore_row_colors()
            
            # 高亮显示选中行
            self.data_table.highlight_rows(rows=event.row, bg="#d0e8ff", fg="#000000")
            
            # 保存当前高亮的行，以便后续恢复
            self.highlighted_row = event.row
            
    def on_row_double_click(self, event):
        """处理表格行双击事件"""
        # tksheet的双击事件通过extra_bindings绑定
        if not hasattr(self, "row_double_click_binding_added"):
            self.data_table.extra_bindings(["double_click_cell"], func=self.on_row_double_click_event)
            self.row_double_click_binding_added = True
            
    def on_row_double_click_event(self, event):
        """处理tksheet的单元格双击事件"""
        if event.row is not None and event.column is not None:
            # 获取单元格数据
            cell_value = self.data_table.get_cell_data(event.row, event.column)
            # 复制单元格值到剪贴板
            self.copy_value_to_clipboard(cell_value)
            # 显示提示信息
            self.search_tooltip.config(text="已复制单元格内容到剪贴板", foreground="#006600")
            # 2秒后恢复提示
            self.frame.after(2000, lambda: self.search_tooltip.config(text="实时搜索", foreground="#333333"))
            
    def restore_row_colors(self):
        """恢复所有行的原始颜色"""
        if hasattr(self, 'row_colors') and self.row_colors:
            # 如果有高亮的行，恢复它的原始颜色
            if hasattr(self, 'highlighted_row') and self.highlighted_row is not None:
                if self.highlighted_row in self.row_colors:
                    try:
                        color_info = self.row_colors[self.highlighted_row]
                        self.data_table.highlight_rows(
                            rows=self.highlighted_row, 
                            bg=color_info["bg"], 
                            fg=color_info["fg"]
                        )
                    except Exception as e:
                        print(f"恢复行颜色失败: {e}")
                self.highlighted_row = None