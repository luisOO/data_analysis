import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from config_manager_ui import ConfigManagerUI
from tksheet import Sheet  # 导入tksheet组件
from utils import ClipboardUtils

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
        style.configure("Treeview.Heading", font=self.fonts["default"], background=self.colors["header_bg"], borderwidth=1, relief="raised")
        style.configure("Treeview", font=self.fonts["default"], background="white", fieldbackground="white", borderwidth=1, relief="solid")
        # 设置表格单元格边框
        style.layout("Treeview", [
            ("Treeview.treearea", {"sticky": "nswe", "border": 1})
        ])
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
                       fieldbackground="white", borderwidth=2, relief="solid")
        # 设置表格单元格边框 - 增强边框效果
        style.layout("Tech.Treeview", [
            ("Tech.Treeview.treearea", {"sticky": "nswe", "border": 2})
        ])
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
            
            # 初始化空的数据表格，显示配置的字段
            self._initialize_empty_data_table(sub_factor_name)
            
        except Exception as e:
            self.controller.logger.error(f"设置子因子框架失败: {e}")
    
    def _initialize_empty_data_table(self, sub_factor_name):
        """初始化空的数据表格，显示配置的字段"""
        try:
            # 获取默认层次
            default_level = self._get_default_hierarchy_level()
            
            if default_level:
                # 获取该层次和子因子的列配置
                columns = self.controller.config_manager.get_data_table_columns(default_level, sub_factor_name)
                if columns:
                    # 创建空的DataFrame并显示空表格但包含配置的列标题
                    empty_df = pd.DataFrame()
                    self.detail_view.display_data_table(empty_df, None, columns)
                else:
                    self.controller.logger.warning(f"未找到子因子 '{sub_factor_name}' 在层次 '{default_level}' 的列配置")
            else:
                self.controller.logger.warning("无法获取默认层次，跳过表格初始化")
                    
        except Exception as e:
            self.controller.logger.error(f"初始化空数据表格失败: {e}")
    
    def _get_default_hierarchy_level(self):
        """获取默认层次级别的公共方法"""
        default_level = self.controller.config_manager.get_default_hierarchy_level()
        if not default_level:
            hierarchy_levels = self.controller.data_manager.get_hierarchy_levels()
            if hierarchy_levels:
                default_level = hierarchy_levels[0]
        return default_level

# SubFactorView类已被集成到FactorView中，不再需要单独的类

class SubFactorDetailView:
    def __init__(self, parent, controller):
        self.frame = parent
        self.controller = controller
        
        # 设置默认层级
        self.current_level = self.controller.config_manager.get_default_hierarchy_level()
        
        # 创建主容器，使用垂直布局
        main_container = ttk.Frame(self.frame)
        main_container.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        
        # 基本信息区域 - 紧凑设计
        self.basic_info_frame = ttk.LabelFrame(main_container, text="📋 基本信息", style="Tech.TLabelframe")
        self.basic_info_frame.pack(fill=tk.X, padx=0, pady=(0, 8))
        # 不再固定高度，允许根据内容自适应
        # 但仍然保持紧凑设计
        
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
        self.search_tooltip = ttk.Label(self.search_frame, text="实时搜索", foreground="#333333", font=("Microsoft YaHei UI", 8))
        self.search_tooltip.pack(side=tk.LEFT)

        # 数据表格区域 - 占用剩余所有空间，科技风格
        self.table_frame = ttk.LabelFrame(main_container, text="📊 数据表格", style="Tech.TLabelframe")
        self.table_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # 创建表格容器框架，用于更好地组织表格
        table_container = ttk.Frame(self.table_frame)
        table_container.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        
        # 配置网格权重，让表格占用所有可用空间
        table_container.grid_rowconfigure(0, weight=1)
        table_container.grid_columnconfigure(0, weight=1)
        
        # 创建tksheet表格 - 替代Treeview
        self.data_table = Sheet(table_container,
                               theme="light blue",  # 使用内置主题
                               show_horizontal_grid=True,  # 显示水平网格线
                               show_vertical_grid=True,    # 显示垂直网格线
                               show_header=True,           # 显示表头
                               show_row_index=False,       # 不显示行索引
                               show_top_left=False,        # 不显示左上角单元格
                               headers=[],                 # 初始化空表头
                               data=[],                    # 初始化空数据
                               height=400,                 # 初始高度
                               width=800)                  # 初始宽度
        
        # 设置表格样式
        self.data_table.grid_color = "#a0a0a0"  # 网格线颜色
        self.data_table.font = ("Microsoft YaHei UI", 10)  # 表格字体
        self.data_table.header_font = ("Microsoft YaHei UI", 10, "bold")  # 表头字体
        self.data_table.header_bg = "#e6f0ff"  # 表头背景色
        
        # 绑定事件
        self.data_table.extra_bindings(["row_select"], func=self.on_row_select_event)
        self.data_table.extra_bindings(["double_click_cell"], func=self.on_row_double_click_event)
        self.row_select_binding_added = True
        self.row_double_click_binding_added = True
        
        # 布局表格 - tksheet自带滚动条，不需要额外添加
        self.data_table.grid(row=0, column=0, sticky="nsew")
        
        # 配置网格权重，让表格占用所有可用空间
        table_container.grid_rowconfigure(0, weight=1)
        table_container.grid_columnconfigure(0, weight=1)
        
        # 绑定表格右键菜单
        self.data_table.bind("<Button-3>", self.show_table_context_menu)

    def create_context_menu(self):
        """创建右键菜单"""
        self.context_menu = tk.Menu(self.frame, tearoff=0)
        self.context_menu.add_command(label="复制行", command=self.copy_row_as_text)
        self.context_menu.add_command(label="复制为JSON", command=self.copy_row_as_json)
        self.context_menu.add_command(label="复制为Markdown", command=self.copy_row_as_markdown)
        
        # 字段值复制菜单
        self.field_menu = tk.Menu(self.frame, tearoff=0)
        self.field_menu.add_command(label="复制值", command=self.copy_field_value)
        
    def show_table_context_menu(self, event):
        """显示表格右键菜单"""
        try:
            # 检查event是否为事件对象
            if hasattr(event, 'x') and hasattr(event, 'y'):
                try:
                    # 尝试直接获取鼠标下方的行
                    # 直接使用事件坐标
                    x = event.x
                    y = event.y
                    print(f"鼠标坐标: x={x}, y={y}")
                    
                    # 尝试使用不同的方法获取行
                    try:
                        # 尝试方法1：使用identify_region
                        if hasattr(self.data_table, 'identify_region'):
                            try:
                                # 直接使用事件坐标，不使用canvasx方法
                                # 注意：tksheet的identify_region可能需要不同的参数形式
                                try:
                                    # 尝试方式1：直接传递x和y参数
                                    region_info = self.data_table.identify_region(x=event.x, y=event.y)
                                except Exception as e1:
                                    try:
                                        # 尝试方式2：直接传递事件对象
                                        region_info = self.data_table.identify_region(event)
                                    except Exception as e2:
                                        print(f"identify_region调用失败: {e1}, {e2}")
                                        region_info = "table"  # 默认值
                                print(f"identify_region返回: {region_info}")
                                
                                # 根据返回值类型处理
                                if isinstance(region_info, str) and region_info == "table":
                                    # 如果返回"table"，尝试使用get_row_clicked方法
                                    if hasattr(self.data_table, 'get_row_clicked'):
                                        try:
                                            # 尝试方式1：传递事件对象
                                            row = self.data_table.get_row_clicked(event)
                                        except Exception as e1:
                                            try:
                                                # 尝试方式2：只传递y坐标
                                                row = self.data_table.get_row_clicked(y=event.y)
                                            except Exception as e2:
                                                print(f"get_row_clicked调用失败: {e1}, {e2}")
                                                row = None
                                        print(f"使用get_row_clicked获取行: {row}")
                                    else:
                                        row = None
                                elif isinstance(region_info, tuple) and len(region_info) >= 2:
                                    # 如果返回元组，第一个元素是行
                                    row = region_info[0]
                                    print(f"从identify_region获取行: {row}")
                                else:
                                    # 无法从identify_region获取行
                                    row = None
                            except Exception as e:
                                print(f"使用identify_region出错: {e}")
                                row = None
                        else:
                            row = None
                            
                        # 如果上面的方法失败，尝试使用identify_row方法
                        if row is None and hasattr(self.data_table, 'identify_row'):
                            try:
                                # 尝试不同的调用方式
                                try:
                                    # 尝试直接传递事件对象
                                    row = self.data_table.identify_row(event)
                                    print(f"使用identify_row(event)获取行: {row}")
                                except Exception as e1:
                                    try:
                                        # 尝试传递y坐标，但不作为关键字参数
                                        row = self.data_table.identify_row(event.y)
                                        print(f"使用identify_row(event.y)获取行: {row}")
                                    except Exception as e2:
                                        print(f"identify_row调用失败: {e1}, {e2}")
                                        row = None
                            except Exception as e:
                                print(f"identify_row调用失败: {e}")
                                row = None
                        
                        # 如果仍然失败，尝试使用当前选中行
                        if row is None:
                            try:
                                selected_rows = self.data_table.get_selected_rows()
                                if selected_rows and len(selected_rows) > 0:
                                    # 如果返回的是集合，转换为列表
                                    if isinstance(selected_rows, set):
                                        row = list(selected_rows)[0]
                                    else:
                                        row = selected_rows[0]
                                    print(f"使用当前选中行: {row}")
                                else:
                                    # 如果没有选中行，使用第一行
                                    row = 0
                                    print(f"使用默认行: {row}")
                            except Exception as e:
                                print(f"获取选中行失败: {e}")
                                row = 0
                    except Exception as e:
                        print(f"获取行时出错: {e}")
                        # 使用默认值
                        row = 0
                    
                    # 如果无法获取行，使用当前选中的行
                    if row is None or not isinstance(row, int):
                        try:
                            selected_rows = self.data_table.get_selected_rows()
                            if selected_rows and len(selected_rows) > 0:
                                # 如果返回的是集合，转换为列表
                                if isinstance(selected_rows, set):
                                    row = list(selected_rows)[0]
                                else:
                                    row = selected_rows[0]
                            else:
                                # 如果没有选中的行，使用第一行
                                row = 0
                        except Exception as e:
                            print(f"获取选中行失败: {e}")
                            row = 0
                    
                    # 保存当前选中的单元格位置（列设为0）
                    self.current_cell = (row, 0)
                    print(f"右键菜单：选中行 {row}")
                    
                    # 使用颜色高亮显示当前行，而不是使用默认的选中效果
                    try:
                        # 恢复所有行的原始颜色
                        self.restore_row_colors()
                        
                        # 检查行索引是否有效
                        total_rows = len(self.row_colors) if hasattr(self, 'row_colors') else 0
                        if row < 0 or row >= total_rows:
                            print(f"行索引超出范围: {row}, 总行数: {total_rows}")
                            return
                        
                        # 高亮显示当前行
                        self.data_table.highlight_rows(rows=row, bg="#d0e8ff", fg="#000000")
                        
                        # 保存当前高亮的行，以便后续恢复
                        self.highlighted_row = row
                        
                        # 确保行可见
                        if hasattr(self.data_table, 'see'):
                            self.data_table.see(row, 0)
                    except Exception as e:
                        print(f"高亮显示行失败: {e}")
                        # 如果高亮失败，回退到默认的选中方式
                        self.data_table.select_row(row)
                    selected_rows = self.data_table.get_selected_rows()
                    print(f"选中的行: {selected_rows}")
                    
                    # 显示右键菜单
                    self._show_context_menu(event.x_root, event.y_root)
                    return
                except Exception as e:
                    print(f"显示表格右键菜单出错: {e}")
                    
                # 如果上面的方法都失败了，显示菜单
                self._show_context_menu(event.x_root, event.y_root)
            elif isinstance(event, int):
                # 如果是整数，直接使用作为行索引
                row = event
                
                # 使用颜色高亮显示当前行，而不是使用默认的选中效果
                try:
                    # 恢复所有行的原始颜色
                    self.restore_row_colors()
                    
                    # 检查行索引是否有效
                    total_rows = len(self.row_colors) if hasattr(self, 'row_colors') else 0
                    if row < 0 or row >= total_rows:
                        print(f"行索引超出范围: {row}, 总行数: {total_rows}")
                        return
                    
                    # 高亮显示当前行
                    self.data_table.highlight_rows(rows=row, bg="#d0e8ff", fg="#000000")
                    
                    # 保存当前高亮的行，以便后续恢复
                    self.highlighted_row = row
                except Exception as e:
                    print(f"高亮显示行失败: {e}")
                    # 如果高亮失败，回退到默认的选中方式
                    self.data_table.select_row(row)
                
                # 获取鼠标当前位置显示组合菜单
                x, y = self.frame.winfo_pointerxy()
                combined_menu = tk.Menu(self.frame, tearoff=0)
                combined_menu.add_command(label="复制行", command=self.copy_row_as_text)
                combined_menu.add_command(label="复制为JSON", command=self.copy_row_as_json)
                combined_menu.post(x, y)
        except Exception as e:
            print(f"显示菜单时出错: {e}")
            # 记录错误但不中断程序
    
    def _get_selected_row_index(self):
        """获取当前选中的行索引，统一处理逻辑"""
        # 首先检查是否有高亮的行
        if hasattr(self, 'highlighted_row') and self.highlighted_row is not None:
            return self.highlighted_row
        
        # 获取当前选中的行（tksheet API）
        selected_rows = self.data_table.get_selected_rows()
        if not selected_rows:
            print("没有选中的行")
            # 尝试获取当前鼠标位置下的行
            if hasattr(self, 'current_cell') and self.current_cell:
                row_index = self.current_cell[0]
                # 高亮显示该行
                self.restore_row_colors()
                self.data_table.highlight_rows(rows=row_index, bg="#d0e8ff", fg="#000000")
                self.highlighted_row = row_index
                return row_index
            else:
                # 仍然没有选中行，显示提示信息
                self._show_tooltip_message("请先选择一行数据", "#FF0000")
                return None
        else:
            # 获取选中行的数据
            # 处理selected_rows可能是集合的情况
            if isinstance(selected_rows, set):
                return list(selected_rows)[0]  # 使用第一个选中的行
            else:
                return selected_rows[0]  # 使用第一个选中的行
    
    def _show_tooltip_message(self, message, color="#006600", duration=2000):
        """显示提示信息的通用方法"""
        if hasattr(self, 'search_tooltip'):
            self.search_tooltip.config(text=message, foreground=color)
            # 指定时间后恢复提示
            self.frame.after(duration, lambda: self.search_tooltip.config(text="实时搜索", foreground="#333333"))
    
    def _copy_to_clipboard(self, content, success_message):
        """复制内容到剪贴板的通用方法"""
        success = ClipboardUtils.copy_to_clipboard(content, success_message)
        if success:
            self._show_tooltip_message(success_message)
            print(f"{success_message}: {str(content)[:50]}...")
        return success
    
    def _show_context_menu(self, x, y):
        """显示右键菜单的通用方法"""
        try:
            combined_menu = tk.Menu(self.frame, tearoff=0)
            combined_menu.add_command(label="复制行", command=self.copy_row_as_text)
            combined_menu.add_command(label="复制为JSON", command=self.copy_row_as_json)
            combined_menu.add_command(label="复制为Markdown", command=self.copy_row_as_markdown)
            combined_menu.post(x, y)
        except Exception as e:
            print(f"显示右键菜单时出错: {e}")
    
    def copy_row_as_text(self):
        """将选中的行复制为文本格式"""
        try:
            row_index = self._get_selected_row_index()
            if row_index is None:
                return
            
            # 获取表头和行数据
            headers = self.data_table.headers()
            values = self.data_table.get_row_data(row_index)
            
            # 创建包含表头和值的格式化文本
            row_text = ""  # 初始化文本
            
            # 添加表头和值的对应关系
            for i, header in enumerate(headers):
                if i < len(values):
                    row_text += f"{header}: {values[i]}\n"
            
            # 移除最后一个换行符
            if row_text.endswith("\n"):
                row_text = row_text[:-1]
            
            # 使用通用复制方法
            self._copy_to_clipboard(row_text, "已复制行数据到剪贴板")
        except Exception as e:
            print(f"复制行为文本时出错: {e}")
            # 记录错误但不中断程序
            
    def copy_row_as_email(self):
        """将选中的行复制为邮件格式"""
        try:
            row_index = self._get_selected_row_index()
            if row_index is None:
                return
            
            # 获取表头和行数据
            headers = self.data_table.headers()
            values = self.data_table.get_row_data(row_index)
            
            # 创建HTML表格格式
            html = "<table border='1' cellpadding='3' cellspacing='0' style='border-collapse:collapse;'>\n"
            
            # 添加表头行
            html += "<tr style='background-color:#e6f0ff;'>\n"
            for header in headers:
                html += f"<th style='font-weight:bold;'>{header}</th>\n"
            html += "</tr>\n"
            
            # 添加数据行
            html += "<tr>\n"
            for value in values:
                html += f"<td>{value}</td>\n"
            html += "</tr>\n"
            
            html += "</table>"
            
            # 使用通用复制方法
            self._copy_to_clipboard(html, "已复制为邮件HTML格式到剪贴板")
        except Exception as e:
            print(f"复制行为邮件格式时出错: {e}")
            # 记录错误但不中断程序
    
    def copy_row_as_json(self):
        """将选中的行复制为JSON格式"""
        try:
            row_index = self._get_selected_row_index()
            if row_index is None:
                return
                
            row_data = {}
            
            # 获取表头和行数据
            headers = self.data_table.headers()
            values = self.data_table.get_row_data(row_index)
            
            # 将表头和值组合成字典
            for i, header in enumerate(headers):
                if i < len(values):
                    # 使用当前列的原始字段名（如果有保存）
                    if hasattr(self, 'current_columns') and i < len(self.current_columns):
                        field_name = self.current_columns[i]
                    else:
                        field_name = header
                    row_data[field_name] = values[i]
            
            # 转换为JSON字符串
            import json
            json_str = json.dumps(row_data, ensure_ascii=False, indent=2)
            
            # 使用通用复制方法
            self._copy_to_clipboard(json_str, "已复制JSON数据到剪贴板")
        except Exception as e:
            print(f"复制行为JSON时出错: {e}")
            # 记录错误但不中断程序
    
    def copy_row_as_markdown(self):
        """将选中的行复制为Markdown表格格式"""
        print("开始执行复制为Markdown功能")
        try:
            row_index = self._get_selected_row_index()
            if row_index is None:
                return
            
            # 获取表头和行数据
            headers = self.data_table.headers()
            values = self.data_table.get_row_data(row_index)
            
            # 创建Markdown表格格式
            markdown_lines = []
            
            # 添加表头行
            header_line = "| " + " | ".join(str(header) for header in headers) + " |"
            markdown_lines.append(header_line)
            
            # 添加分隔行
            separator_line = "| " + " | ".join("---" for _ in headers) + " |"
            markdown_lines.append(separator_line)
            
            # 添加数据行
            # 处理值中的特殊字符，避免破坏Markdown表格格式
            escaped_values = []
            for value in values:
                if value is None:
                    escaped_values.append("")
                else:
                    # 转换为字符串并转义Markdown特殊字符
                    str_value = str(value)
                    # 转义管道符和换行符
                    str_value = str_value.replace("|", "\\|").replace("\n", "<br>")
                    escaped_values.append(str_value)
            
            data_line = "| " + " | ".join(escaped_values) + " |"
            markdown_lines.append(data_line)
            
            # 合并所有行
            markdown_str = "\n".join(markdown_lines)
            
            # 使用通用复制方法
            self._copy_to_clipboard(markdown_str, "已复制Markdown表格到剪贴板")
        except Exception as e:
            print(f"复制行为Markdown时出错: {e}")
            # 记录错误但不中断程序
    
    def copy_cell_value(self, event):
        """双击复制单元格值"""
        try:
            # 检查event是否为事件对象或整数
            if isinstance(event, int):
                row = event
                column = 0  # 默认第一列
            else:
                # 获取点击位置的行和列（tksheet API）
                rc = self.data_table.identify_region(event)
                if rc and len(rc) >= 2 and isinstance(rc[0], int) and isinstance(rc[1], int):
                    row, column = rc[0], rc[1]
                else:
                    print("无法识别单元格位置")
                    return
                
            # 获取单元格值
            cell_value = self.data_table.get_cell_data(row, column)
            if cell_value is not None:
                # 确保使用根窗口进行剪贴板操作
                root = self.frame.winfo_toplevel()
                root.clipboard_clear()
                root.clipboard_append(str(cell_value))
                root.update()  # 确保更新剪贴板内容
                
                # 显示提示信息
                if hasattr(self, 'search_tooltip'):
                    self.search_tooltip.config(text="已复制单元格内容到剪贴板", foreground="#006600")
                    # 2秒后恢复提示
                    self.frame.after(2000, lambda: self.search_tooltip.config(text="实时搜索", foreground="#333333"))
                print(f"已复制单元格内容到剪贴板: {str(cell_value)[:50]}...")
        except Exception as e:
            print(f"复制单元格值时出错: {e}")
            # 记录错误但不中断程序
            # 可以添加提示信息
            self.search_tooltip.config(text="已复制单元格内容到剪贴板", foreground="#006600")
            self.frame.after(2000, lambda: self.search_tooltip.config(text="输入关键词进行实时搜索", foreground="#333333"))
    
    def copy_field_value(self):
        """复制字段值"""
        if hasattr(self, 'current_field_value'):
            self.frame.clipboard_clear()
            self.frame.clipboard_append(str(self.current_field_value))
    
    def copy_current_cell_value(self):
        """复制当前选中单元格的值"""
        try:
            if hasattr(self, 'current_cell'):
                row, column = self.current_cell
                # 获取单元格值
                cell_value = self.data_table.get_cell_data(row, column)
                if cell_value is not None:
                    # 确保使用根窗口进行剪贴板操作
                    root = self.frame.winfo_toplevel()
                    root.clipboard_clear()
                    root.clipboard_append(str(cell_value))
                    root.update()  # 确保更新剪贴板内容
                    
                    # 显示提示信息
                    if hasattr(self, 'search_tooltip'):
                        self.search_tooltip.config(text="已复制单元格内容到剪贴板", foreground="#006600")
                        # 2秒后恢复提示
                        self.frame.after(2000, lambda: self.search_tooltip.config(text="实时搜索", foreground="#333333"))
                    print(f"已复制单元格内容到剪贴板: {str(cell_value)[:50]}...")
        except Exception as e:
            print(f"复制当前单元格值时出错: {e}")
            # 记录错误但不中断程序
    
    def display_basic_info(self, info):
        # 清空现有内容
        for widget in self.basic_info_frame.winfo_children():
            widget.destroy()
        
        if not info:
            return
        
        # 直接在basic_info_frame上创建主容器框架，不添加额外滚动条
        info_frame = tk.Frame(self.basic_info_frame, bg="white")
        info_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 定义字段显示优先级
        priority_fields = ['业务代码', '净销售收入', '总成本毛利率', '描述']
        other_fields = [field for field in sorted(info.keys()) if field not in priority_fields]
        
        # 按优先级排序显示字段
        ordered_fields = [field for field in priority_fields if field in info] + other_fields
        
        # 固定布局：每行4个字段，确保对齐
        fields_per_row = 4
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
        # 保存当前选择的层级
        self.current_level = level
        self.controller.on_hierarchy_node_select(level)
        # 重置搜索框
        self.search_var.set("")
        
    def on_search_change(self, *args):
        """当搜索框内容变化时触发"""
        # 延迟执行搜索，避免频繁更新 - 增加延迟时间减少闪动
        if hasattr(self, "_search_after_id"):
            self.frame.after_cancel(self._search_after_id)
        # 增加延迟到500毫秒，减少刷新频率
        self._search_after_id = self.frame.after(500, self.apply_search_filter)
        
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
        
        # 检查搜索文本是否与上次相同，如果相同则跳过
        if hasattr(self, '_last_search_text') and self._last_search_text == search_text:
            return
            
        # 保存当前搜索文本
        self._last_search_text = search_text
        
        # 获取当前选中的层次
        current_level = self.hierarchy_var.get()
        
        # 通知控制器应用过滤
        self.controller.apply_search_filter(current_level, search_text)
            
    def display_data_table(self, df, display_columns=None, columns_config=None):
        # 检查是否需要更新表格 - 如果数据和列配置与当前相同，则跳过更新以减少闪动
        if hasattr(self, 'current_df') and hasattr(self, 'current_columns'):
            if self.current_df is not None and not df.empty and columns_config is not None:
                if self.current_df.equals(df) and self.current_columns == columns_config:
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
                row_data = [str(row[col]) if pd.notna(row[col]) and col in df.columns else "" for col in columns_to_show]
                data.append(row_data)
        
        # 更新表格数据和标题
        self.data_table.headers(headers)
        self.data_table.set_sheet_data(data)
        
        # 设置列宽 - 自适应填满整个表格宽度
        # 首先获取表格容器的宽度
        self.data_table.update_idletasks()  # 确保尺寸已更新
        table_width = self.table_frame.winfo_width() - 20  # 减去一些边距
        if table_width <= 0:  # 如果宽度无效，使用默认宽度
            table_width = 800
        
        # 计算并应用列宽
        col_widths = self._calculate_column_widths(columns_to_show, headers, df, table_width)
        self._apply_column_widths(col_widths)
            
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
        
        # 设置交替行颜色并保存原始颜色信息
        self.row_colors = {}
        for i in range(len(data)):
            if i % 2 == 0:
                self.row_colors[i] = {"bg": "#ffffff", "fg": "#000000"}  # 偶数行
                self.data_table.highlight_rows(rows=i, bg="#ffffff")  # 偶数行
            else:
                self.row_colors[i] = {"bg": "#f0f0f0", "fg": "#000000"}  # 奇数行
                self.data_table.highlight_rows(rows=i, bg="#f0f0f0")  # 奇数行
        
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
            # 如果总宽度小于表格宽度，按比例增加每列宽度
            ratio = table_width / total_width
            col_widths = [int(w * ratio) for w in col_widths]
        
        return col_widths
    
    def _apply_column_widths(self, col_widths):
        """应用列宽度"""
        for col_idx, width in enumerate(col_widths):
            if col_idx < len(col_widths):  # 确保列索引有效
                self.data_table.column_width(column=col_idx, width=width)
            
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
    def show_context_menu(self, event):
        """显示右键菜单"""
        # 先选中鼠标右键点击的行
        try:
            rc = self.data_table.identify_region(event)
            if rc and len(rc) >= 1 and isinstance(rc[0], int):
                item_id = rc[0]
                # 只有当item_id有效时才继续
                self.data_table.selection_set(item_id)
                self.data_table.focus(item_id)
        except Exception as e:
            print(f"右键菜单选择行出错: {e}")
            
            # 创建右键菜单
            context_menu = tk.Menu(self.frame, tearoff=0)
            context_menu.add_command(label="复制行", command=self.copy_selected_row)
            
            # 获取当前选中的行和列
            try:
                current_row = self.data_table.get_selected_rows()[0] if self.data_table.get_selected_rows() else None
                if current_row is not None:
                    context_menu.add_command(label="复制单元格", command=lambda: self.copy_cell_value(current_row))
            except Exception as e:
                print(f"设置复制单元格菜单出错: {e}")
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
            self.search_tooltip.config(text="已复制整行数据到剪贴板", foreground="#006600")
            self.frame.after(2000, lambda: self.search_tooltip.config(text="输入关键词进行实时搜索", foreground="#333333"))
            
    def copy_cell_value(self, event):
        """复制单元格值"""
        try:
            # 检查event是否为事件对象或整数
            if hasattr(event, 'y') and hasattr(event, 'x'):
                # 如果是事件对象，获取点击位置的行和列
                item_id = self.data_table.identify_row(event.y)
                column_id = self.data_table.identify_column(event.x)
            elif isinstance(event, tuple) and len(event) == 2:
                # 如果是元组，假设是(行ID, 列ID)
                item_id, column_id = event
            else:
                # 其他情况，无法处理
                return
        except Exception as e:
            print(f"复制单元格值时出错: {e}")
            # 记录错误但不中断程序
            return
            
        if 'item_id' in locals() and 'column_id' in locals() and item_id and column_id:
            col_index = int(column_id.replace('#', '')) - 1
            values = self.data_table.item(item_id, "values")
            
            if col_index < len(values):
                # 复制到剪贴板
                self.frame.clipboard_clear()
                self.frame.clipboard_append(str(values[col_index]))
                
                # 显示提示
                self.search_tooltip.config(text="已复制单元格内容到剪贴板", foreground="#006600")
                self.frame.after(2000, lambda: self.search_tooltip.config(text="输入关键词进行实时搜索", foreground="#333333"))
                
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