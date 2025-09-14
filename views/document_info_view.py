import tkinter as tk
from tkinter import ttk


class DocumentInfoView:
    def __init__(self, parent, controller):
        self.frame = parent
        self.controller = controller
        self.labels = {}
        
        # 创建右键菜单
        self.create_context_menu()
        
        # 初始化时根据配置显示字段框架
        self.show_default_info()
    
    def create_context_menu(self):
        """创建右键菜单"""
        self.field_menu = tk.Menu(self.frame, tearoff=0)
        self.field_menu.add_command(label="复制值", command=self.copy_field_value)
    
    def copy_field_value(self):
        """复制字段值"""
        if hasattr(self, 'current_field_value'):
            try:
                self.frame.clipboard_clear()
                self.frame.clipboard_append(str(self.current_field_value))
            except:
                pass
    
    def show_field_menu(self, event, text):
        """显示字段右键菜单"""
        self.current_field_value = text
        try:
            self.field_menu.post(event.x_root, event.y_root)
        except:
            # 如果菜单不存在，创建一个简单的菜单
            field_menu = tk.Menu(self.frame, tearoff=0)
            field_menu.add_command(label="复制值", command=lambda: self.copy_value_to_clipboard(text))
            field_menu.post(event.x_root, event.y_root)
    
    def copy_value_to_clipboard(self, text):
        """复制值到剪贴板"""
        try:
            self.frame.clipboard_clear()
            self.frame.clipboard_append(str(text))
        except:
            pass
        
    def _create_field_display_layout(self, parent_frame, data, is_default=False):
        """统一的字段显示布局方法"""
        try:
            if not data:
                return
            
            # 直接在parent_frame上创建主容器框架，不添加额外滚动条
            info_frame = tk.Frame(parent_frame, bg="white")
            info_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            # 获取配置文件中的字段顺序
            doc_info_fields = self.controller.config_manager.get_document_info_fields()
            
            # 将配置的字段ID转换为显示名称
            ordered_display_names = []
            for field_id in doc_info_fields:
                display_name = self.controller.config_manager.get_display_name(field_id)
                if display_name in data:
                    ordered_display_names.append(display_name)
            
            # 添加配置中没有但data中存在的字段（以防万一）
            for field in data.keys():
                if field not in ordered_display_names:
                    ordered_display_names.append(field)
            
            # 固定布局：每行6个字段，确保对齐
            fields_per_row = 6
            field_groups = []
            
            # 将字段按每行6个分组
            for i in range(0, len(ordered_display_names), fields_per_row):
                group = ordered_display_names[i:i + fields_per_row]
                field_groups.append(group)
            
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
                    field_value = data[field_key]
                    value_text = str(field_value) if field_value is not None else ("待加载..." if is_default else "N/A")
                    
                    # 字段名和值在同一行显示 - 统一字体颜色
                    if value_text in ["N/A", "待加载..."]:
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
                    
                    # 绑定复制功能（仅在非默认模式下）
                    if not is_default:
                        field_label.bind("<Button-3>", lambda e, text=value_text: self.show_field_menu(e, text))
                        field_label.bind("<Double-Button-1>", lambda e, text=value_text: self.copy_value_to_clipboard(text))
                        
                        # 悬停效果（改变背景色）
                        def on_enter(e, label=field_label):
                            label.configure(background="#e8f4fd")
                        def on_leave(e, label=field_label):
                            label.configure(background="white")
                        
                        field_label.bind("<Enter>", on_enter)
                        field_label.bind("<Leave>", on_leave)
            
        except Exception as e:
            self.controller.logger.error(f"创建字段显示布局失败: {e}")
    
    def show_default_info(self):
        """根据配置显示单据基本信息字段框架"""
        # 清除现有控件
        for widget in self.frame.winfo_children():
            widget.destroy()
        
        # 获取配置的文档信息字段
        try:
            doc_info_fields = self.controller.config_manager.get_document_info_fields()
            
            if not doc_info_fields:
                # 如果没有配置字段，显示空白框架
                no_data_label = ttk.Label(self.frame, text="暂无单据信息", style="Info.TLabel")
                no_data_label.pack(pady=20)
                return
            
            # 创建默认数据字典，用于布局计算
            default_data = {}
            for field in doc_info_fields:
                display_name = self.controller.config_manager.get_display_name(field)
                default_data[display_name] = "待加载..."  # 显示占位文本
            
            # 直接使用统一的字段显示布局方法，不使用Canvas滚动
            self._create_field_display_layout(self.frame, default_data, is_default=True)
                    
        except Exception as e:
            # 如果出错，显示空白框架
            no_data_label = ttk.Label(self.frame, text="暂无单据信息", style="Info.TLabel")
            no_data_label.pack(pady=20)

    def display_info(self, data):
        """显示单据基本信息数据"""
        # 清除现有控件
        for widget in self.frame.winfo_children():
            widget.destroy()
        
        # 如果没有数据，显示提示信息
        if not data:
            no_data_label = ttk.Label(self.frame, text="暂无单据信息", style="Info.TLabel")
            no_data_label.pack(pady=20)
            return
        
        # 直接使用统一的字段显示布局方法，不使用Canvas滚动
        self._create_field_display_layout(self.frame, data, is_default=False)