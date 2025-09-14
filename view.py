import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from config_manager_ui import ConfigManagerUI

class MainAppView(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("数据分析工具")
        self.geometry("1280x800")
        self.minsize(1024, 768)  # 设置最小窗口大小
        
        # 设置全局字体和样式
        self.font_config()
        
        # 设置全局内边距
        self.configure(padx=10, pady=10)
        
        # 添加应用标题栏
        self.create_title_bar()
        
    def font_config(self):
        """配置全局字体和样式"""
        # 设置默认字体为微软雅黑
        self.fonts = {
            "default": ("Microsoft YaHei UI", 10),
            "title": ("Microsoft YaHei UI", 12, "bold"),
            "subtitle": ("Microsoft YaHei UI", 11, "bold"),
            "small": ("Microsoft YaHei UI", 9),
            "monospace": ("Consolas", 10)
        }
        
        # 定义颜色方案
        self.colors = {
            "bg": "#f5f5f7",  # 浅灰背景色
            "accent": "#2196f3",  # 蓝色强调色 - 科技感
            "header_bg": "#e6f0ff",  # 标题背景色
            "button_bg": "#e1e1e1",  # 按钮背景色
            "button_active_bg": "#d1d1d1",  # 按钮激活背景色
            "frame_bg": "#ffffff",  # 框架背景色
            "text": "#000000",  # 黑色文本 - 科技风格
            "light_text": "#666666",  # 浅色文本
            "success": "#4caf50",  # 成功色
            "warning": "#ff9800",  # 警告色
            "error": "#f44336"   # 错误色
        }
        
        # 配置各种控件的字体
        self.option_add("*Font", self.fonts["default"])
        self.configure(background=self.colors["bg"])
        
        # 配置样式
        style = ttk.Style()
        style.theme_use('clam')  # 使用clam主题作为基础
        
        # 基本控件样式
        style.configure(".", background=self.colors["bg"])
        style.configure("TFrame", background="white")
        style.configure("TLabel", font=self.fonts["default"], background="white")
        style.configure("TButton", font=self.fonts["default"], background=self.colors["button_bg"], borderwidth=1)
        style.map("TButton", background=[('active', self.colors["button_active_bg"])])
        style.configure("TRadiobutton", font=self.fonts["default"], background="white")
        style.configure("TCheckbutton", font=self.fonts["default"], background="white")
        style.configure("TEntry", font=self.fonts["default"], fieldbackground="white")
        style.configure("TCombobox", font=self.fonts["default"])
        
        # 标签框架样式
        style.configure("TLabelframe", background=self.colors["frame_bg"], borderwidth=1)
        style.configure("TLabelframe.Label", font=self.fonts["title"], background=self.colors["header_bg"], foreground=self.colors["accent"])
        
        # 标题样式
        style.configure("Title.TLabel", font=self.fonts["title"], background=self.colors["frame_bg"], foreground=self.colors["accent"])
        style.configure("Subtitle.TLabel", font=self.fonts["subtitle"], background=self.colors["frame_bg"], foreground=self.colors["accent"])
        
        # 表格样式
        style.configure("Treeview.Heading", font=self.fonts["default"], background=self.colors["header_bg"])
        style.configure("Treeview", font=self.fonts["default"], background="white", fieldbackground="white")
        style.map("Treeview", background=[("selected", self.colors["accent"])])
        
        # 笔记本样式
        style.configure("TNotebook", background=self.colors["bg"], tabmargins=[2, 5, 2, 0])
        style.configure("TNotebook.Tab", font=self.fonts["default"], padding=[10, 2], background=self.colors["button_bg"])
        style.map("TNotebook.Tab", background=[("selected", self.colors["frame_bg"])], foreground=[("selected", self.colors["accent"])])
        
        # 状态样式
        style.configure("Success.TLabel", foreground=self.colors["success"], font=self.fonts["default"])
        style.configure("Warning.TLabel", foreground=self.colors["warning"], font=self.fonts["default"])
        style.configure("Error.TLabel", foreground=self.colors["error"], font=self.fonts["default"])
        
        # 信息框样式
        style.configure("Info.TFrame", background="white", borderwidth=0, relief="flat")
        style.configure("Info.TLabel", background="white", font=self.fonts["default"], borderwidth=0, relief="flat")
        
        # 科技风格样式
        style.configure("Tech.TLabelframe", background="white", borderwidth=2, relief="groove")
        style.configure("Tech.TLabelframe.Label", font=self.fonts["title"], background="white", 
                       foreground=self.colors["accent"], padding=[5, 2])
        
        # 科技风格按钮
        style.configure("Tech.TButton", font=self.fonts["default"], background="#2d3748", 
                       foreground="white", borderwidth=1, focuscolor="none")
        style.map("Tech.TButton", background=[("active", "#4a5568"), ("pressed", "#1a202c")])
        
        # 科技风格单选按钮
        style.configure("Tech.TRadiobutton", font=self.fonts["default"], background="white",
                       foreground=self.colors["text"], focuscolor="none")
        style.map("Tech.TRadiobutton", background=[("active", "white")])
        
        # 科技风格表格
        style.configure("Tech.Treeview.Heading", font=self.fonts["subtitle"], background="#2d3748", 
                       foreground="white", borderwidth=1, relief="raised")
        style.configure("Tech.Treeview", font=self.fonts["default"], background="white", 
                       fieldbackground="white", borderwidth=1, relief="solid")
        style.map("Tech.Treeview", background=[("selected", "#4a90e2")], foreground=[("selected", "white")])
        
        # 科技风格入口框
        style.configure("Tech.TEntry", font=self.fonts["default"], fieldbackground="#f8f9fa", 
                       borderwidth=1, relief="solid", focuscolor=self.colors["accent"])
        
        # 悬停效果样式
        style.configure("Hover.TLabelframe", background="#e8f4fd", borderwidth=2, relief="raised")
        style.configure("Hover.TLabelframe.Label", background="#e8f4fd", foreground=self.colors["accent"])

        # Main layout - 科技风格布局
        # 顶部单据信息区域
        self.doc_info_frame = ttk.LabelFrame(self, text="📋 单据基本信息", style="Tech.TLabelframe")
        self.doc_info_frame.pack(fill=tk.X, padx=10, pady=(5, 10))
        self.doc_info_view = DocumentInfoView(self.doc_info_frame, self.controller)
        
        # 主工作区域 - 水平分割
        self.main_paned_window = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.main_paned_window.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # 左侧因子分类区域
        self.left_panel = ttk.LabelFrame(self.main_paned_window, text="🔧 因子分类", style="Tech.TLabelframe")
        self.main_paned_window.add(self.left_panel, weight=1)
        self.factor_view = FactorView(self.left_panel, self.controller)
        
        # 右侧子因子详情区域
        self.right_panel = ttk.LabelFrame(self.main_paned_window, text="📊 子因子详情", style="Tech.TLabelframe")
        self.main_paned_window.add(self.right_panel, weight=3)
        
        # 设置初始分割位置（左侧占25%）
        self.after(200, self.set_panel_ratio)
        # 子因子详情视图将在FactorView中创建

        # 创建标准菜单
        self.create_menu()
    
    def set_panel_ratio(self):
        """设置面板比例为1:3"""
        try:
            # 获取PanedWindow的实际宽度
            self.update_idletasks()  # 确保布局完成
            total_width = self.main_paned_window.winfo_width()
            if total_width > 100:  # 确保窗口已经正确初始化
                left_width = int(total_width * 0.25)  # 左侧占25%
                self.main_paned_window.sashpos(0, left_width)
            else:
                # 如果窗口还没有正确初始化，再次延迟执行
                self.after(100, self.set_panel_ratio)
        except Exception as e:
            print(f"设置面板比例时出错: {e}")
            # 使用默认值作为备选方案
            self.main_paned_window.sashpos(0, 250)

    def create_title_bar(self):
        """创建应用标题栏"""
        # 创建标题栏框架
        title_frame = ttk.Frame(self)
        title_frame.pack(fill=tk.X, padx=0, pady=0, before=self.main_paned_window)
        
        # 添加应用图标标签（可以替换为实际图标）
        # app_icon_label = ttk.Label(title_frame, text="📊", font=("Microsoft YaHei UI", 16))
        # app_icon_label.pack(side=tk.LEFT, padx=(10, 5), pady=10)
        
        # 应用标题已移除
        
        # 添加分隔线
        separator = ttk.Separator(self, orient="horizontal")
        separator.pack(fill=tk.X, padx=0, pady=0, before=self.main_paned_window)
    
    def create_menu(self):
        """创建应用菜单"""
        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)
        
        # 文件菜单
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="导入JSON", command=self.controller.load_data_action)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.quit)
        self.menu_bar.add_cascade(label="文件", menu=file_menu)
        
        # 视图菜单
        view_menu = tk.Menu(self.menu_bar, tearoff=0)
        view_menu.add_command(label="刷新", command=lambda: self.controller.refresh_view())
        self.menu_bar.add_cascade(label="视图", menu=view_menu)
    
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
        
        # 工具菜单
        tools_menu = tk.Menu(self.menu_bar, tearoff=0)
        tools_menu.add_command(label="⚙️ 配置管理", command=self.open_config_manager)
        self.menu_bar.add_cascade(label="工具", menu=tools_menu)
        
        # 帮助菜单
        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="关于", command=self.show_about)
        self.menu_bar.add_cascade(label="帮助", menu=help_menu)
    
    def show_about(self):
        """显示关于对话框"""
        about_window = tk.Toplevel(self)
        about_window.title("关于数据分析工具")
        about_window.geometry("400x200")
        about_window.resizable(False, False)
        about_window.transient(self)  # 设置为主窗口的临时窗口
        about_window.grab_set()  # 模态窗口
        
        # 居中显示
        about_window.update_idletasks()
        width = about_window.winfo_width()
        height = about_window.winfo_height()
        x = (about_window.winfo_screenwidth() // 2) - (width // 2)
        y = (about_window.winfo_screenheight() // 2) - (height // 2)
        about_window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        
        # 添加内容
        ttk.Label(about_window, text="数据分析工具", font=("Microsoft YaHei UI", 14, "bold")).pack(pady=10)
        ttk.Label(about_window, text="版本: 1.0.0").pack(pady=5)
        ttk.Label(about_window, text="© 2023 数据分析团队").pack(pady=5)
        
        # 关闭按钮
        ttk.Button(about_window, text="确定", command=about_window.destroy).pack(pady=20)
    
    def open_config_manager(self):
        """打开配置管理器"""
        try:
            if not hasattr(self, 'config_manager'):
                self.config_manager = ConfigManagerUI(parent=self)
            self.config_manager.open_config_window()
        except Exception as e:
            tk.messagebox.showerror("错误", f"打开配置管理器失败：{e}")
    
    def on_config_updated(self):
        """配置更新后的回调函数"""
        try:
            # 通知控制器配置已更新
            if hasattr(self.controller, 'reload_config'):
                self.controller.reload_config()
            
            # 显示成功消息
            tk.messagebox.showinfo("提示", "配置已更新！部分设置需要重启程序后生效。")
        except Exception as e:
            tk.messagebox.showerror("错误", f"应用配置失败：{e}")

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
            
            # 定义字段显示优先级
            priority_fields = ['业务代码', '项目名称', '计算模式', '净销售收入']
            other_fields = [field for field in sorted(data.keys()) if field not in priority_fields]
            
            # 按优先级排序显示字段
            ordered_fields = [field for field in priority_fields if field in data] + other_fields
            
            # 固定布局：每行6个字段，确保对齐
            fields_per_row = 6
            field_groups = []
            
            # 将字段按每行6个分组
            for i in range(0, len(ordered_fields), fields_per_row):
                group = ordered_fields[i:i + fields_per_row]
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
                    
                    # 字段名和值在同一行显示
                    if value_text in ["N/A", "待加载..."]:
                        value_color = "#95a5a6"
                        value_font = ("Microsoft YaHei UI", 9, "italic")
                    else:
                        value_color = "#34495e"
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

class FactorView:
    def __init__(self, parent, controller):
        self.frame = parent
        self.controller = controller
        self.main_app = None  # 延迟获取主应用视图的引用
        
        # 创建因子分类选择区域
        category_frame = ttk.LabelFrame(self.frame, text="📂 分类选择", style="Tech.TLabelframe")
        category_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.category_var = tk.StringVar()
        self.category_radios = {}
        self.category_buttons_frame = ttk.Frame(category_frame)
        self.category_buttons_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 子因子选择区域
        self.subfactor_frame = ttk.LabelFrame(self.frame, text="🔍 子因子选择", style="Tech.TLabelframe")
        self.subfactor_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.subfactor_var = tk.StringVar()
        self.subfactor_radios = {}
        self.subfactor_buttons_frame = ttk.Frame(self.subfactor_frame)
        self.subfactor_buttons_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建滚动区域用于子因子按钮
        self.create_scrollable_subfactor_area()
        
        self.tabs = {}
        self.current_factors = []
        
        # 初始化右侧详情视图（延迟创建）
        self.detail_view = None

    def create_scrollable_subfactor_area(self):
        """创建可滚动的子因子选择区域"""
        # 创建Canvas和Scrollbar
        self.canvas = tk.Canvas(self.subfactor_buttons_frame, highlightthickness=0, bg="white")
        self.scrollbar = ttk.Scrollbar(self.subfactor_buttons_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # 绑定鼠标滚轮事件
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        
    def _on_mousewheel(self, event):
        """处理鼠标滚轮事件"""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def setup_tabs(self, factor_categories):
        # 清除现有的分类按钮
        for widget in self.category_buttons_frame.winfo_children():
            widget.destroy()
        self.category_radios = {}
        
        # 创建分类选择按钮
        for i, (category, factors) in enumerate(factor_categories.items()):
            radio = ttk.Radiobutton(self.category_buttons_frame, text=category,
                                  variable=self.category_var, value=category,
                                  style="Tech.TRadiobutton",
                                  command=lambda cat=category, facs=factors: self.on_category_select(cat, facs))
            radio.pack(anchor=tk.W, pady=2)
            self.category_radios[category] = radio
        
        # 默认选择第一个分类
        if factor_categories:
            first_category = list(factor_categories.keys())[0]
            first_factors = list(factor_categories.values())[0]
            self.category_var.set(first_category)
            self.on_category_select(first_category, first_factors)
    
    def on_category_select(self, category, factors):
        """处理分类选择事件"""
        self.current_factors = factors
        self.setup_subfactor_buttons(factors)
    
    def setup_subfactor_buttons(self, factors):
        """设置子因子按钮"""
        # 清除现有的子因子按钮
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.subfactor_radios = {}
        
        # 创建子因子选择按钮
        for factor in factors:
            factor_name = factor['name']
            display_name = self.controller.config_manager.get_display_name(factor_name)
            radio = ttk.Radiobutton(self.scrollable_frame, text=display_name,
                                  variable=self.subfactor_var, value=factor_name,
                                  style="Tech.TRadiobutton",
                                  command=lambda sf=factor_name: self.on_subfactor_select(sf))
            radio.pack(anchor=tk.W, pady=3, padx=5)
            self.subfactor_radios[factor_name] = radio
        
        # 默认选择第一个子因子
        if factors:
            first_factor_name = factors[0]['name']
            self.subfactor_var.set(first_factor_name)
            self.on_subfactor_select(first_factor_name)
    
    def on_subfactor_select(self, subfactor):
        """处理子因子选择事件"""
        # 延迟获取主应用视图引用
        if self.main_app is None:
            self.main_app = self.controller.view
        
        # 如果右侧详情视图还未创建，则创建它
        if self.detail_view is None:
            self.detail_view = SubFactorDetailView(self.main_app.right_panel, self.controller)
        
        # 调用控制器处理子因子选择
        self.controller.on_sub_factor_select(subfactor)
    
    def setup_sub_factor_framework(self, category, sub_factor_name):
        """为指定的子因子设置空白框架"""
        try:
            # 延迟获取主应用视图引用
            if self.main_app is None:
                self.main_app = self.controller.view
            
            # 如果右侧详情视图还未创建，则创建它
            if self.detail_view is None:
                self.detail_view = SubFactorDetailView(self.main_app.right_panel, self.controller)
            
            # 获取子因子的基本信息字段配置
            basic_info_fields = self.controller.config_manager.get_sub_factor_basic_info(sub_factor_name)
            
            # 创建空白的基本信息显示
            empty_info = {}
            for field in basic_info_fields:
                display_name = self.controller.config_manager.get_display_name(field)
                empty_info[display_name] = ""
            
            # 显示空白基本信息
            self.detail_view.display_basic_info(empty_info)
            
            # 设置数据层次选择框架
            self.detail_view.setup_data_hierarchy_selection()
            
        except Exception as e:
            self.controller.logger.error(f"设置子因子框架失败: {e}")

# SubFactorView类已被集成到FactorView中，不再需要单独的类

class SubFactorDetailView:
    def __init__(self, parent, controller):
        self.frame = parent
        self.controller = controller
        
        # 创建主容器，使用垂直布局
        main_container = ttk.Frame(self.frame)
        main_container.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        
        # 基本信息区域 - 紧凑设计
        self.basic_info_frame = ttk.LabelFrame(main_container, text="📋 基本信息", style="Tech.TLabelframe")
        self.basic_info_frame.pack(fill=tk.X, padx=0, pady=(0, 8))
        self.basic_info_frame.configure(height=100)  # 减小高度
        self.basic_info_frame.pack_propagate(False)
        
        # 创建右键菜单
        self.create_context_menu()
        
        # 控制区域 - 科技风格的紧凑布局
        control_frame = ttk.Frame(main_container)
        control_frame.pack(fill=tk.X, padx=0, pady=(0, 8))
        
        # 数据层次选择部分（左侧）- 更紧凑
        hierarchy_container = ttk.LabelFrame(control_frame, text="🔄 数据层次", style="Tech.TLabelframe")
        hierarchy_container.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 4))
        
        self.hierarchy_var = tk.StringVar()
        self.hierarchy_radios = {}
        self.hierarchy_selection_frame = ttk.Frame(hierarchy_container)
        self.hierarchy_selection_frame.pack(fill=tk.X, padx=8, pady=6)
        
        # 搜索过滤部分（右侧）- 更紧凑
        search_container = ttk.LabelFrame(control_frame, text="🔍 搜索过滤", style="Tech.TLabelframe")
        search_container.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(4, 0))
        
        # 搜索控件框架
        self.search_frame = ttk.Frame(search_container)
        self.search_frame.pack(fill=tk.X, padx=8, pady=6)
        
        # 搜索输入框和按钮 - 科技风格
        search_label = ttk.Label(self.search_frame, text="搜索:", font=("Microsoft YaHei UI", 9))
        search_label.pack(side=tk.LEFT, padx=(0, 4))
        
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.on_search_change)  # 实时搜索
        
        self.search_entry = ttk.Entry(self.search_frame, textvariable=self.search_var, width=20, style="Tech.TEntry")
        self.search_entry.pack(side=tk.LEFT, padx=(0, 3))
        
        # 创建搜索按钮 - 科技风格
        self.search_button = ttk.Button(self.search_frame, text="🔍", command=self.on_search_button_click, width=3, style="Tech.TButton")
        self.search_button.pack(side=tk.LEFT, padx=(0, 2))
        
        # 创建清除按钮 - 科技风格
        self.clear_button = ttk.Button(self.search_frame, text="❌", command=self.on_clear_search, width=3, style="Tech.TButton")
        self.clear_button.pack(side=tk.LEFT, padx=(0, 3))
        
        # 添加提示信息 - 更小字体
        self.search_tooltip = ttk.Label(self.search_frame, text="实时搜索", foreground="#888888", font=("Microsoft YaHei UI", 8))
        self.search_tooltip.pack(side=tk.LEFT)

        # 数据表格区域 - 占用剩余所有空间，科技风格
        self.table_frame = ttk.LabelFrame(main_container, text="📊 数据表格", style="Tech.TLabelframe")
        self.table_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # 创建表格容器框架，用于更好地组织表格和滚动条
        table_container = ttk.Frame(self.table_frame)
        table_container.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        
        # 创建Treeview表格 - 科技风格
        self.data_table = ttk.Treeview(table_container, show='headings', style="Tech.Treeview")
        
        # 创建垂直滚动条
        self.table_scroll_y = ttk.Scrollbar(table_container, orient="vertical", command=self.data_table.yview)
        self.data_table.configure(yscrollcommand=self.table_scroll_y.set)
        
        # 创建水平滚动条
        self.table_scroll_x = ttk.Scrollbar(table_container, orient="horizontal", command=self.data_table.xview)
        self.data_table.configure(xscrollcommand=self.table_scroll_x.set)
        
        # 布局表格和滚动条
        self.data_table.grid(row=0, column=0, sticky="nsew")
        self.table_scroll_y.grid(row=0, column=1, sticky="ns")
        self.table_scroll_x.grid(row=1, column=0, sticky="ew")
        
        # 配置网格权重，让表格占用所有可用空间
        table_container.grid_rowconfigure(0, weight=1)
        table_container.grid_columnconfigure(0, weight=1)
        
        # 绑定表格右键菜单
        self.data_table.bind("<Button-3>", self.show_table_context_menu)
        # 绑定双击事件，用于复制单元格内容
        self.data_table.bind("<Double-1>", self.copy_cell_value)

    def create_context_menu(self):
        """创建右键菜单"""
        self.context_menu = tk.Menu(self.frame, tearoff=0)
        self.context_menu.add_command(label="复制为JSON", command=self.copy_row_as_json)
        
        # 字段值复制菜单
        self.field_menu = tk.Menu(self.frame, tearoff=0)
        self.field_menu.add_command(label="复制值", command=self.copy_field_value)
        
    def show_table_context_menu(self, event):
        """显示表格右键菜单"""
        # 获取点击位置的行
        row_id = self.data_table.identify_row(event.y)
        if row_id:  # 如果点击在某一行上
            # 选中该行
            self.data_table.selection_set(row_id)
            # 显示菜单
            self.context_menu.post(event.x_root, event.y_root)
    
    def copy_row_as_json(self):
        """将选中的行复制为JSON格式"""
        selection = self.data_table.selection()
        if not selection:
            return
            
        # 获取选中行的数据
        row_data = {}
        item_id = selection[0]
        values = self.data_table.item(item_id, 'values')
        columns = self.data_table['columns']
        
        for i, col in enumerate(columns):
            if i < len(values):
                row_data[col] = values[i]
        
        # 转换为JSON字符串
        import json
        json_str = json.dumps(row_data, ensure_ascii=False, indent=2)
        
        # 复制到剪贴板
        self.frame.clipboard_clear()
        self.frame.clipboard_append(json_str)
    
    def copy_cell_value(self, event):
        """双击复制单元格值"""
        # 获取点击位置的行和列
        row_id = self.data_table.identify_row(event.y)
        col_id = self.data_table.identify_column(event.x)
        
        if not (row_id and col_id):
            return
            
        # 获取列索引
        col_index = int(col_id.replace('#', '')) - 1
        
        # 获取单元格值
        values = self.data_table.item(row_id, 'values')
        if col_index < len(values):
            cell_value = values[col_index]
            
            # 复制到剪贴板
            self.frame.clipboard_clear()
            self.frame.clipboard_append(str(cell_value))
    
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
            
        # 创建滚动区域
        canvas = tk.Canvas(self.basic_info_frame, height=120, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.basic_info_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # 布局滚动组件
        canvas.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        scrollbar.pack(side="right", fill="y")
        
        # 创建主容器框架，设置背景色
        info_frame = tk.Frame(scrollable_frame, bg="white")
        info_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 定义字段显示优先级
        priority_fields = ['业务代码', '净销售收入', '总成本毛利率', '描述']
        other_fields = [field for field in sorted(info.keys()) if field not in priority_fields]
        
        # 按优先级排序显示字段
        ordered_fields = [field for field in priority_fields if field in info] + other_fields
        
        # 动态分配每行字段数量，根据字段内容长度智能分配
        def calculate_field_width(field_key, field_value):
            """计算字段显示所需的大概宽度"""
            value_text = str(field_value) if field_value is not None else "N/A"
            field_text = f"{field_key}: {value_text}"
            # 估算字符宽度，中文字符按2个单位计算
            width = 0
            for char in field_text:
                if ord(char) > 127:  # 中文字符
                    width += 2
                else:  # 英文字符
                    width += 1
            return width
        
        # 计算所有字段的宽度
        field_widths = []
        for field_key in ordered_fields:
            field_value = info[field_key]
            width = calculate_field_width(field_key, field_value)
            field_widths.append((field_key, width))
        
        # 动态分组算法：尽可能在一行内放置更多字段
        field_groups = []
        current_group = []
        current_width = 0
        max_width_per_row = 200  # 增加每行最大字符宽度，充分利用空间
        
        for field_key, width in field_widths:
            # 如果当前组为空或者添加当前字段不会超出宽度限制
            if not current_group or (current_width + width + 10) <= max_width_per_row:  # 10为字段间距
                current_group.append(field_key)
                current_width += width + 10
            else:
                # 当前组已满，开始新组
                if current_group:
                    field_groups.append(current_group)
                current_group = [field_key]
                current_width = width + 10
        
        # 添加最后一组
        if current_group:
            field_groups.append(current_group)
        
        # 显示字段组，使用行容器和pack布局确保填满整行
        for row_idx, group in enumerate(field_groups):
            # 创建行容器
            row_frame = tk.Frame(info_frame, bg="white")
            row_frame.pack(fill=tk.X, pady=1)
            
            # 为每个字段创建等宽容器
            for col_idx, field_key in enumerate(group):
                field_value = info[field_key]
                value_text = str(field_value) if field_value is not None else "N/A"
                
                # 字段名和值在同一行显示
                if value_text == "N/A":
                    value_color = "#95a5a6"
                    value_font = ("Microsoft YaHei UI", 9, "italic")
                else:
                    value_color = "#34495e"
                    value_font = ("Microsoft YaHei UI", 9, "normal")
                
                # 创建字段容器，确保等宽分布
                field_container = tk.Frame(row_frame, bg="white")
                field_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=1)
                
                # 创建字段标签，填满容器
                field_text = f"{field_key}: {value_text}"
                field_label = tk.Label(field_container, text=field_text, 
                                     font=("Microsoft YaHei UI", 9),
                                     foreground=value_color,
                                     cursor="hand2",
                                     background="white",
                                     anchor="w",
                                     relief="flat",
                                     padx=8, pady=3)
                field_label.pack(fill=tk.BOTH, expand=True)
                
                # 绑定复制功能
                field_label.bind("<Button-3>", lambda e, text=value_text: self.show_field_menu(e, text))
                field_label.bind("<Double-Button-1>", lambda e, text=value_text: self.copy_value_to_clipboard(text))
                
                # 悬停效果（改变背景色）
                def on_enter(e, label=field_label, container=field_container):
                    label.configure(background="#e8f4fd")
                    container.configure(background="#e8f4fd")
                def on_leave(e, label=field_label, container=field_container):
                    label.configure(background="white")
                    container.configure(background="white")
                
                field_label.bind("<Enter>", on_enter)
                field_label.bind("<Leave>", on_leave)
            
            # 动态分组不需要空白占位符，每行字段数量根据内容自适应
            
        # 绑定鼠标滚轮事件
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind("<MouseWheel>", _on_mousewheel)
        scrollable_frame.bind("<MouseWheel>", _on_mousewheel)
                
    def show_field_menu(self, event, value):
        """显示字段值右键菜单"""
        self.current_field_value = value
        self.field_menu.post(event.x_root, event.y_root)
        
    def copy_value_to_clipboard(self, value):
        """复制值到剪贴板"""
        self.frame.clipboard_clear()
        self.frame.clipboard_append(str(value))

    # 删除树形结构相关方法

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
        default_level = self.controller.config_manager.get_default_hierarchy_level()
        if hierarchy_levels and default_level in hierarchy_levels:
            self.hierarchy_var.set(default_level)
            self.on_hierarchy_level_select(default_level)
        elif hierarchy_levels:
            self.hierarchy_var.set(hierarchy_levels[0])
            self.on_hierarchy_level_select(hierarchy_levels[0])
    
    def on_hierarchy_level_select(self, level):
        """当用户选择数据层次时触发"""
        self.controller.on_hierarchy_node_select(level)
        # 重置搜索框
        self.search_var.set("")
        
    def on_search_change(self, *args):
        """当搜索框内容变化时触发"""
        # 延迟执行搜索，避免频繁更新
        if hasattr(self, "_search_after_id"):
            self.frame.after_cancel(self._search_after_id)
        self._search_after_id = self.frame.after(300, self.apply_search_filter)
        
    def on_search_button_click(self):
        """当点击搜索按钮时触发"""
        self.apply_search_filter()
        
    def on_clear_search(self):
        """当点击清除按钮时触发"""
        self.search_var.set("")
        self.apply_search_filter()
        
    def apply_search_filter(self):
        """应用搜索过滤"""
        search_text = self.search_var.get().lower()
        
        # 获取当前选中的层次
        current_level = self.hierarchy_var.get()
        
        # 通知控制器应用过滤
        self.controller.apply_search_filter(current_level, search_text)
            
    def display_data_table(self, df, display_columns=None, columns_config=None):
        self.data_table.delete(*self.data_table.get_children())
        
        # 清除可能存在的空数据提示
        for widget in self.table_frame.winfo_children():
            if isinstance(widget, ttk.Label) and widget.cget("text") == "暂无数据":
                widget.destroy()
        
        # 确定要显示的列
        if df.empty and columns_config:
            # 如果DataFrame为空但有列配置，使用配置的列
            columns_to_show = columns_config
        elif not df.empty:
            # 如果有数据，使用DataFrame的列
            columns_to_show = list(df.columns)
        else:
            # 既没有数据也没有列配置，显示空数据提示
            empty_label = ttk.Label(self.table_frame, text="暂无数据", font=("Microsoft YaHei UI", 12), foreground="#999999")
            empty_label.place(relx=0.5, rely=0.5, anchor="center")
            return
            
        # 设置表格列
        self.data_table["columns"] = columns_to_show
        
        # 设置列标题和宽度
        for col in columns_to_show:
            # 如果提供了显示名称映射，使用映射的名称
            display_name = display_columns.get(col, col) if display_columns else col
            self.data_table.heading(col, text=display_name, command=lambda c=col: self.sort_by_column(c))
            
            # 根据内容自动调整列宽
            max_width = len(display_name) * 10 + 20  # 基础宽度
            
            # 如果有数据，根据内容调整列宽
            if not df.empty and col in df.columns:
                for i, value in enumerate(df[col]):
                    if i > 100:  # 限制检查的行数以提高性能
                        break
                    width = len(str(value)) * 8 + 20
                    if width > max_width:
                        max_width = width
            
            # 限制最大宽度
            if max_width > 300:
                max_width = 300
                
            self.data_table.column(col, width=max_width, minwidth=50)
            
        # 插入数据到表格（只有在有数据时才插入）
        if not df.empty:
            for index, row in df.iterrows():
                values = [str(row[col]) if pd.notna(row[col]) and col in df.columns else "" for col in columns_to_show]
                self.data_table.insert("", "end", values=values)
        
        # 保存原始数据用于搜索过滤
        self.original_data = df.copy()
            
    def sort_by_column(self, col):
        """按列排序表格数据"""
        # 获取当前数据
        data = [(self.data_table.set(child, col), child) for child in self.data_table.get_children('')]
        
        # 确定排序方向
        if hasattr(self, 'sort_direction') and self.sort_column == col:
            self.sort_direction = not self.sort_direction
        else:
            self.sort_direction = False  # 默认降序
            self.sort_column = col
        
        # 排序
        data.sort(reverse=self.sort_direction)
        
        # 重新排列数据
        for index, (val, child) in enumerate(data):
            self.data_table.move(child, '', index)
            
        # 更新列标题显示排序方向
        for column in self.data_table["columns"]:
            if column == col:
                direction = "▲" if self.sort_direction else "▼"
                self.data_table.heading(column, text=f"{self.data_table.heading(column)['text'].split(' ')[0]} {direction}")
            else:
                # 移除其他列的排序指示器
                current_text = self.data_table.heading(column)["text"]
                if "▲" in current_text or "▼" in current_text:
                    self.data_table.heading(column, text=current_text.split(' ')[0])
        
    def on_row_select(self, event):
        """处理表格行选择事件"""
        selected_items = self.data_table.selection()
        if selected_items:
            # 高亮显示选中行
            self.data_table.focus(selected_items[0])
            
    def on_row_double_click(self, event):
        """处理表格行双击事件"""
        region = self.data_table.identify("region", event.x, event.y)
        if region == "cell":
            # 获取选中的行
            selected_items = self.data_table.selection()
            if selected_items:
                item = selected_items[0]
                # 获取行数据
                values = self.data_table.item(item, "values")
                # 复制单元格值到剪贴板
                col_id = self.data_table.identify_column(event.x)
                if col_id:
                    col_index = int(col_id.replace('#', '')) - 1
                    if col_index < len(values):
                        self.frame.clipboard_clear()
                        self.frame.clipboard_append(str(values[col_index]))
                        # 可以添加提示信息
                        self.search_tooltip.config(text="已复制单元格内容到剪贴板", foreground="#008800")
                        # 2秒后恢复提示
                        self.frame.after(2000, lambda: self.search_tooltip.config(text="输入关键词进行实时搜索", foreground="#666666"))
                        
    def show_context_menu(self, event):
        """显示右键菜单"""
        # 先选中鼠标右键点击的行
        item_id = self.data_table.identify_row(event.y)
        if item_id:
            self.data_table.selection_set(item_id)
            self.data_table.focus(item_id)
            
            # 创建右键菜单
            context_menu = tk.Menu(self.frame, tearoff=0)
            context_menu.add_command(label="复制行", command=self.copy_selected_row)
            context_menu.add_command(label="复制单元格", command=lambda: self.copy_cell_value(event))
            context_menu.add_separator()
            context_menu.add_command(label="导出选中行", command=self.export_selected_row)
            
            # 显示菜单
            try:
                context_menu.tk_popup(event.x_root, event.y_root)
            finally:
                context_menu.grab_release()
                
    def copy_selected_row(self):
        """复制选中行的所有数据"""
        selected_items = self.data_table.selection()
        if selected_items:
            item = selected_items[0]
            values = self.data_table.item(item, "values")
            
            # 将所有值组合成一行文本
            row_text = "\t".join([str(v) for v in values])
            
            # 复制到剪贴板
            self.frame.clipboard_clear()
            self.frame.clipboard_append(row_text)
            
            # 显示提示
            self.search_tooltip.config(text="已复制整行数据到剪贴板", foreground="#008800")
            self.frame.after(2000, lambda: self.search_tooltip.config(text="输入关键词进行实时搜索", foreground="#666666"))
            
    def copy_cell_value(self, event):
        """复制单元格值"""
        item_id = self.data_table.identify_row(event.y)
        column_id = self.data_table.identify_column(event.x)
        
        if item_id and column_id:
            col_index = int(column_id.replace('#', '')) - 1
            values = self.data_table.item(item_id, "values")
            
            if col_index < len(values):
                # 复制到剪贴板
                self.frame.clipboard_clear()
                self.frame.clipboard_append(str(values[col_index]))
                
                # 显示提示
                self.search_tooltip.config(text="已复制单元格内容到剪贴板", foreground="#008800")
                self.frame.after(2000, lambda: self.search_tooltip.config(text="输入关键词进行实时搜索", foreground="#666666"))
                
    def export_selected_row(self):
        """导出选中行数据"""
        selected_items = self.data_table.selection()
        if selected_items:
            # 获取选中行数据
            item = selected_items[0]
            values = self.data_table.item(item, "values")
            columns = self.data_table["columns"]
            
            # 创建临时文件
            import tempfile
            import os
            import csv
            
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.csv', mode='w', newline='', encoding='utf-8')
            with temp_file:
                writer = csv.writer(temp_file)
                # 写入表头
                writer.writerow([self.data_table.heading(col)["text"].split(' ')[0] for col in columns])
                # 写入数据行
                writer.writerow(values)
                
            # 显示成功消息
            messagebox.showinfo("导出成功", f"数据已导出到: {temp_file.name}")
            
            # 尝试打开文件
            try:
                os.startfile(temp_file.name)
            except:
                pass