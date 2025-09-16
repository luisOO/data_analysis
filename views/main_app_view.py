import tkinter as tk
from tkinter import ttk, messagebox
from config_manager_ui import ConfigManagerUI
from .document_info_view import DocumentInfoView
from .factor_view import FactorView


class MainAppView(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("数据分析工具")
        self.geometry("1280x800")
        self.minsize(1024, 768)  # 设置最小窗口大小
        
        # 设置全局字体和样式
        self.font_config()
        
        # 创建菜单栏
        self.create_menu()
        
        # 设置全局内边距
        self.configure(padx=10, pady=10)
        
        # 添加应用标题栏
        self.create_title_bar()
        
        # 修复窗口显示问题
        self.fix_window_display()
        
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
    
    def fix_window_display(self):
        """修复窗口显示问题"""
        try:
            # 确保窗口显示在屏幕上
            self.deiconify()  # 取消最小化
            self.lift()       # 提升到前台
            self.focus_force()  # 强制获取焦点
            self.attributes('-topmost', True)  # 置顶
            self.after(100, lambda: self.attributes('-topmost', False))  # 100ms后取消置顶
            
            # 确保窗口在屏幕可见区域内
            self.update_idletasks()
            
            # 获取屏幕尺寸
            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()
            
            # 设置窗口位置到屏幕中央
            window_width = 1280
            window_height = 800
            x = (screen_width - window_width) // 2
            y = (screen_height - window_height) // 2
            
            self.geometry(f"{window_width}x{window_height}+{x}+{y}")
            
        except Exception as e:
            print(f"修复窗口显示时出错: {e}")
    
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
        
        # 工具菜单
        tools_menu = tk.Menu(self.menu_bar, tearoff=0)
        tools_menu.add_command(label="⚙️ 配置管理", command=self.open_config_manager)
        self.menu_bar.add_cascade(label="工具", menu=tools_menu)
        
        # 帮助菜单
        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="关于", command=self.show_about)
        self.menu_bar.add_cascade(label="帮助", menu=help_menu)
    
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
            self.clipboard_clear()
            self.clipboard_append(str(text))
        except:
            pass
    
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
                self.config_manager = ConfigManagerUI()
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