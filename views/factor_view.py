import tkinter as tk
from tkinter import ttk
from .sub_factor_detail_view import SubFactorDetailView


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
        """初始化空的数据表格，不显示任何字段"""
        try:
            # 创建完全空白的DataFrame，不显示任何字段
            import pandas as pd
            empty_df = pd.DataFrame()
            self.detail_view.display_data_table(empty_df, None, None)
            self.controller.logger.info(f"已初始化空白数据表格")
                    
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