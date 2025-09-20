#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置管理界面 - 基于config.json结构的业务配置管理
支持整单基本信息、因子分类、子因子和数据层次配置
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import logging
from typing import Dict, List, Any, Optional
import os

logger = logging.getLogger(__name__)

class ConfigManagerUI:
    """配置管理界面类"""
    
    def __init__(self, config_path: str = "config/config.json", app_controller=None):
        self.config_path = config_path
        self.config_data = {}
        self.root = None
        self.notebook = None
        self.app_controller = app_controller  # 保存主应用控制器引用
        
        # UI组件引用
        self.document_fields_listbox = None
        self.hierarchy_vars = {}
        self.factor_tree = None
        self.display_names_tree = None
        
        # 加载配置
        self.load_config()
        
        # 密码验证状态
        self.password_verified = False
        
        # 字段配置页面内容加载状态
        self.display_names_content_loaded = False
    
    def load_config(self):
        """加载配置文件"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    self.config_data = json.load(f)
                logger.info(f"配置文件加载成功: {self.config_path}")
            else:
                # 创建默认配置
                self.config_data = self.get_default_config()
                self.save_config()
                logger.info("创建默认配置文件")
        except Exception as e:
            logger.error(f"加载配置文件失败: {e}")
            messagebox.showerror("错误", f"加载配置文件失败: {e}")
            self.config_data = self.get_default_config()
    
    def save_config(self, show_success_message=True):
        """保存配置文件
        
        Args:
            show_success_message: 是否显示成功消息弹窗，默认为True
        """
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config_data, f, ensure_ascii=False, indent=2)
            logger.info(f"配置文件保存成功: {self.config_path}")
            
            # 保存成功后刷新所有UI，包括主窗口
            self.refresh_all_ui()
            
            if show_success_message:
                # 指定parent为配置管理窗口，确保弹窗与窗口关联
                messagebox.showinfo("成功", "配置保存成功！", parent=self.root)
                # 弹窗关闭后恢复配置管理窗口焦点
                if self.root:
                    self.root.lift()
                    self.root.focus_force()
        except Exception as e:
            logger.error(f"保存配置文件失败: {e}")
            # 错误弹窗也指定parent
            messagebox.showerror("错误", f"保存配置文件失败: {e}", parent=self.root)
            # 错误弹窗关闭后也要恢复焦点
            if self.root:
                self.root.lift()
                self.root.focus_force()
    
    def get_default_config(self) -> Dict[str, Any]:
        """获取默认配置"""
        return {
            "document_info_fields": [],
            "data_hierarchy_names": {
                "total": "整单层",
                "boq": "BOQ层",
                "model": "模型层",
                "part": "部件层"
            },
            "enabled_hierarchy_levels": ["model", "part"],
            "default_hierarchy_level": "part",
            "default_data_path": "{}",
            "ui_theme": {},
            "factor_categories": {},
            "display_names": {}
        }
    
    def create_password_verification_ui(self):
        """创建密码验证界面"""
        # 密码验证容器
        self.password_frame = ttk.Frame(self.display_names_tab_frame)
        self.password_frame.pack(expand=True, fill=tk.BOTH)
        
        # 居中容器
        center_frame = ttk.Frame(self.password_frame)
        center_frame.pack(expand=True)
        
        # 标题
        title_label = ttk.Label(center_frame, text="字段配置页面访问验证", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=(50, 30))
        
        # 密码输入框架
        input_frame = ttk.Frame(center_frame)
        input_frame.pack(pady=20)
        
        ttk.Label(input_frame, text="请输入密码:", font=('Arial', 12)).pack(pady=(0, 10))
        
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(input_frame, textvariable=self.password_var, 
                                       show='*', font=('Arial', 12), width=20)
        self.password_entry.pack(pady=(0, 20))
        
        # 按钮框架
        button_frame = ttk.Frame(center_frame)
        button_frame.pack(pady=10)
        
        verify_button = ttk.Button(button_frame, text="验证", 
                                  command=self.verify_password_from_ui)
        verify_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # 错误提示标签
        self.error_label = ttk.Label(center_frame, text="", 
                                    foreground='red', font=('Arial', 10))
        self.error_label.pack(pady=(10, 0))
        
        # 绑定回车键
        self.password_entry.bind('<Return>', lambda e: self.verify_password_from_ui())
        
        # 自动聚焦到密码输入框
        self.password_entry.focus()
    
    def verify_password_from_ui(self):
        """从界面验证密码"""
        # 直接从Entry组件获取值，而不是从StringVar获取
        password = self.password_entry.get()
        password_var_value = self.password_var.get()
        logger.info(f"Entry获取的密码: '{password}', StringVar获取的密码: '{password_var_value}', Entry长度: {len(password)}")
        
        if password == "12345678":  # 可以从配置文件读取或使用更安全的方式
            self.password_verified = True
            # 隐藏密码验证界面，显示字段配置内容
            self.password_frame.destroy()
            self.ensure_display_names_content()
            logger.info("密码验证成功，进入字段配置页面")
        else:
            self.error_label.config(text="密码错误，请重新输入")
            self.password_entry.delete(0, tk.END)  # 直接清空Entry组件
            self.password_var.set("")  # 同时清空StringVar
            self.password_entry.focus()
            logger.warning(f"密码验证失败，Entry输入的密码: '{password}', StringVar值: '{password_var_value}'")
    
    def verify_password(self):
        """验证密码（保留兼容性）"""
        if self.password_verified:
            return True
        # 如果还没有验证过密码，返回False让界面显示密码输入框
        return False
    
    def on_tab_changed(self, event):
        """标签切换事件处理"""
        selected_tab = self.notebook.select()
        tab_text = self.notebook.tab(selected_tab, "text")
        
        # 如果切换到字段配置页面，检查密码验证状态
        if tab_text == "字段配置":
            if self.password_verified:
                # 密码已验证，确保字段配置页面内容已加载
                self.ensure_display_names_content()
            # 如果密码未验证，界面会显示密码输入框，无需额外处理
    
    def open_config_window(self):
        """打开配置管理窗口"""
        if self.root is not None:
            self.root.lift()
            return
        
        self.root = tk.Tk()
        self.root.title("业务配置管理")
        self.root.geometry("1000x750")
        self.root.minsize(800, 650)
        self.root.protocol("WM_DELETE_WINDOW", self.close_config_window)
        
        # 确保窗口居中显示
        self.root.update_idletasks()
        width = 1000
        height = 750
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
        # 创建主框架
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建内容框架（用于选项卡）
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # 创建选项卡
        self.notebook = ttk.Notebook(content_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # 绑定标签切换事件
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)
        
        # 创建各个配置页面
        try:
            self.create_document_info_tab()
            self.create_hierarchy_tab()
            self.create_factor_categories_tab()
            self.create_display_names_tab()
        except Exception as e:
            logger.error(f"创建配置页面时出错: {e}")
            # 确保基本的UI组件存在
            if not hasattr(self, 'table_info_content_frame'):
                self.table_info_content_frame = ttk.Frame(self.notebook)
                logger.info("在异常处理中创建了 table_info_content_frame")
            raise
        
        # 创建底部按钮
        self.create_bottom_buttons(main_frame)
        
        # 同步主应用的当前选择状态
        self.sync_main_app_selection_state()
        
        logger.info("配置管理窗口已打开")
    
    def create_document_info_tab(self):
        """创建整单基本信息配置页面"""
        tab_frame = ttk.Frame(self.notebook)
        self.notebook.add(tab_frame, text="整单基本信息配置")
        
        # 说明标签
        info_label = ttk.Label(tab_frame, text="配置整单基本信息需要显示的字段", font=('Arial', 10, 'bold'))
        info_label.pack(pady=(10, 5))
        
        # 主容器
        main_container = ttk.Frame(tab_frame)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 左侧：可选择字段
        left_frame = ttk.LabelFrame(main_container, text="可选择字段", padding=5)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # 可选字段列表框
        available_listbox_frame = ttk.Frame(left_frame)
        available_listbox_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.available_fields_listbox = tk.Listbox(available_listbox_frame, selectmode=tk.SINGLE, 
                                                  font=('Arial', 9), height=15,
                                                  bg='#f8f9fa', selectbackground='#007acc',
                                                  selectforeground='white', borderwidth=1,
                                                  relief='solid', highlightthickness=0)
        available_scrollbar_y = ttk.Scrollbar(available_listbox_frame, orient=tk.VERTICAL, 
                                            command=self.available_fields_listbox.yview)
        self.available_fields_listbox.configure(yscrollcommand=available_scrollbar_y.set)
        
        self.available_fields_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        available_scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 中间：操作按钮
        middle_frame = ttk.Frame(main_container)
        middle_frame.pack(side=tk.LEFT, fill=tk.Y, padx=8)
        
        # 添加一些垂直空间使按钮居中
        ttk.Label(middle_frame, text="").pack(pady=30)
        
        # 左右移动按钮组
        move_frame = ttk.LabelFrame(middle_frame, text="字段操作", padding=5)
        move_frame.pack(pady=5)
        
        ttk.Button(move_frame, text="添加 →", width=12, 
                  command=self.add_selected_field,
                  style='Accent.TButton').pack(pady=3)
        ttk.Button(move_frame, text="← 移除", width=12, 
                  command=self.remove_selected_field).pack(pady=3)
        
        # 分隔线
        ttk.Separator(middle_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=15)
        
        # 上下移动按钮组
        sort_frame = ttk.LabelFrame(middle_frame, text="排序操作", padding=5)
        sort_frame.pack(pady=5)
        
        ttk.Button(sort_frame, text="上移 ↑", width=12, 
                  command=lambda: self.move_selected_field(-1)).pack(pady=2)
        ttk.Button(sort_frame, text="下移 ↓", width=12, 
                  command=lambda: self.move_selected_field(1)).pack(pady=2)
        
        # 右侧：已选择字段
        right_frame = ttk.LabelFrame(main_container, text="已选择字段（显示顺序）", padding=5)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # 已选字段列表框
        selected_listbox_frame = ttk.Frame(right_frame)
        selected_listbox_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.selected_fields_listbox = tk.Listbox(selected_listbox_frame, selectmode=tk.SINGLE, 
                                                 font=('Arial', 9), height=15,
                                                 bg='#f0f8ff', selectbackground='#28a745',
                                                 selectforeground='white', borderwidth=1,
                                                 relief='solid', highlightthickness=0)
        selected_scrollbar_y = ttk.Scrollbar(selected_listbox_frame, orient=tk.VERTICAL, 
                                           command=self.selected_fields_listbox.yview)
        self.selected_fields_listbox.configure(yscrollcommand=selected_scrollbar_y.set)
        
        self.selected_fields_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        selected_scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 底部提示信息
        tip_frame = ttk.Frame(tab_frame)
        tip_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        tip_label = ttk.Label(tip_frame, 
                             text="💡 提示：双击字段可快速添加/移除，右侧字段顺序决定页面显示顺序",
                             font=('Arial', 8), foreground='#666666')
        tip_label.pack(anchor=tk.W)
        
        # 绑定双击事件
        self.available_fields_listbox.bind('<Double-1>', lambda e: self.add_selected_field())
        self.selected_fields_listbox.bind('<Double-1>', lambda e: self.remove_selected_field())
        logger.info("已绑定字段列表双击事件")
        
        # 加载数据
        self.refresh_document_fields()
    
    def create_hierarchy_tab(self):
        """创建数据层次配置页面"""
        tab_frame = ttk.Frame(self.notebook)
        self.notebook.add(tab_frame, text="数据层次配置")
        
        # 说明标签
        info_label = ttk.Label(tab_frame, text="配置数据层次名称和启用状态", font=('Arial', 10, 'bold'))
        info_label.pack(pady=(10, 5))
        
        # 主容器
        main_container = ttk.Frame(tab_frame)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 层次名称配置
        names_frame = ttk.LabelFrame(main_container, text="层次名称配置")
        names_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.hierarchy_name_entries = {}
        hierarchy_names = self.config_data.get("data_hierarchy_names", {})
        
        for i, (key, name) in enumerate(hierarchy_names.items()):
            row_frame = ttk.Frame(names_frame)
            row_frame.pack(fill=tk.X, padx=5, pady=2)
            
            ttk.Label(row_frame, text=f"{key}:", width=10).pack(side=tk.LEFT)
            entry = ttk.Entry(row_frame, width=20)
            entry.insert(0, name)
            entry.pack(side=tk.LEFT, padx=(5, 0))
            self.hierarchy_name_entries[key] = entry
        
        # 启用层次配置
        enabled_frame = ttk.LabelFrame(main_container, text="启用层次配置")
        enabled_frame.pack(fill=tk.X, pady=(0, 10))
        
        enabled_levels = self.config_data.get("enabled_hierarchy_levels", [])
        
        for key in hierarchy_names.keys():
            var = tk.BooleanVar(value=key in enabled_levels)
            self.hierarchy_vars[key] = var
            ttk.Checkbutton(enabled_frame, text=f"{key} ({hierarchy_names[key]})", 
                          variable=var).pack(anchor=tk.W, padx=5, pady=2)
        
        # 默认层次配置
        default_frame = ttk.LabelFrame(main_container, text="默认层次配置")
        default_frame.pack(fill=tk.X)
        
        ttk.Label(default_frame, text="默认层次:").pack(side=tk.LEFT, padx=5)
        self.default_hierarchy_var = tk.StringVar(value=self.config_data.get("default_hierarchy_level", "part"))
        default_combo = ttk.Combobox(default_frame, textvariable=self.default_hierarchy_var, 
                                   values=list(hierarchy_names.keys()), state="readonly")
        default_combo.pack(side=tk.LEFT, padx=5)
    
    def create_factor_categories_tab(self):
        """创建因子分类配置页面"""
        logger.info("开始创建因子分类配置页面")
        try:
            tab_frame = ttk.Frame(self.notebook)
            self.notebook.add(tab_frame, text="因子分类配置")
        
            # 说明标签
            info_label = ttk.Label(tab_frame, text="配置因子分类及其子因子信息", font=('Arial', 10, 'bold'))
            info_label.grid(row=0, column=0, pady=(10, 5))
        
            # 配置tab_frame使用grid布局
            tab_frame.grid_columnconfigure(0, weight=1)
            tab_frame.grid_rowconfigure(1, weight=1)  # 主容器行
            
            # 主容器 - 左右结构，使用grid布局精确控制宽度占比
            main_container = ttk.Frame(tab_frame)
            main_container.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
            
            # 使用grid布局管理器来控制左右区域的宽度比例
            # 配置主容器的列权重，左侧占1，右侧占3，实现1:3的宽度比例
            main_container.grid_columnconfigure(0, weight=1)  # 左侧占1/4
            main_container.grid_columnconfigure(1, weight=3)  # 右侧占3/4
            main_container.grid_rowconfigure(0, weight=1)
            
            # 左侧容器 - 上下结构，设置宽度占比1/4
            left_container = ttk.Frame(main_container, width=250)
            left_container.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
            left_container.grid_propagate(False)  # 防止子组件改变容器大小
            
            # 使用grid布局来精确控制左侧区域的高度分配
            left_container.grid_rowconfigure(0, weight=1)  # 因子分类区域占1/3
            left_container.grid_rowconfigure(1, weight=1)  # 子因子区域占1/3
            left_container.grid_rowconfigure(2, weight=1)  # 预留区域占1/3
            left_container.grid_columnconfigure(0, weight=1)
        
            # 左侧上部分：因子分类 - 占整体高度的1/3
            category_frame = ttk.LabelFrame(left_container, text="因子分类")
            category_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 5))
            
            # 因子分类列表框架
            category_list_frame = ttk.Frame(category_frame)
            category_list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            # 因子分类树形控件
            self.category_treeview = ttk.Treeview(category_list_frame, selectmode='browse', height=6)
            self.category_treeview.heading('#0', text='因子分类', anchor='w')
            self.category_treeview.column('#0', width=200, minwidth=100)
            self.category_treeview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            
            category_scrollbar = ttk.Scrollbar(category_list_frame, orient=tk.VERTICAL, command=self.category_treeview.yview)
            self.category_treeview.configure(yscrollcommand=category_scrollbar.set)
            category_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # 因子分类操作按钮
            category_btn_frame = ttk.Frame(category_frame)
            category_btn_frame.pack(fill=tk.X, padx=5, pady=(0, 5))
            
            ttk.Button(category_btn_frame, text="添加分类", command=self.add_factor_category).pack(side=tk.LEFT, padx=(0, 2))
            ttk.Button(category_btn_frame, text="编辑分类", command=self.edit_factor_category).pack(side=tk.LEFT, padx=2)
            ttk.Button(category_btn_frame, text="删除分类", command=self.delete_factor_category).pack(side=tk.LEFT, padx=2)
            
            # 左侧中部分：子因子 - 占整体高度的1/3
            subfactor_frame = ttk.LabelFrame(left_container, text="子因子")
            subfactor_frame.grid(row=1, column=0, sticky="nsew", pady=5)
            
            # 子因子选择区域
            subfactor_container = ttk.Frame(subfactor_frame)
            subfactor_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            # 创建滚动区域用于子因子按钮
            self.subfactor_canvas = tk.Canvas(subfactor_container, highlightthickness=0, bg="#f8f9fa")
            subfactor_scrollbar = ttk.Scrollbar(subfactor_container, orient="vertical", command=self.subfactor_canvas.yview)
            self.subfactor_scrollable_frame = ttk.Frame(self.subfactor_canvas)
            
            # 设置滚动区域
            self.subfactor_scrollable_frame.bind(
                "<Configure>",
                lambda e: self.subfactor_canvas.configure(scrollregion=self.subfactor_canvas.bbox("all"))
            )
            
            # 在画布上创建窗口
            self.subfactor_canvas.create_window((0, 0), window=self.subfactor_scrollable_frame, anchor="nw")
            self.subfactor_canvas.configure(yscrollcommand=subfactor_scrollbar.set)
            
            # 布局滚动区域组件
            self.subfactor_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            subfactor_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # 子因子选择变量
            self.subfactor_var = tk.StringVar()
            self.subfactor_radios = {}
            
            # 子因子操作按钮
            subfactor_btn_frame = ttk.Frame(subfactor_frame)
            subfactor_btn_frame.pack(fill=tk.X, padx=5, pady=(0, 5))
            
            # 操作按钮
            operation_frame = ttk.Frame(subfactor_btn_frame)
            operation_frame.pack(fill=tk.X)
            
            ttk.Button(operation_frame, text="添加子因子", command=self.add_sub_factor_new).pack(side=tk.LEFT, padx=(0, 2))
            ttk.Button(operation_frame, text="编辑子因子", command=self.edit_sub_factor_new).pack(side=tk.LEFT, padx=2)
            ttk.Button(operation_frame, text="删除子因子", command=self.delete_sub_factor_new).pack(side=tk.LEFT, padx=2)
            
            # 右侧容器 - 上下结构，设置宽度占比3/4
            right_container = ttk.Frame(main_container)
            right_container.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
            
            # 使用grid布局来精确控制右侧区域的高度分配
            right_container.grid_rowconfigure(0, weight=40, uniform="content")  # 子因子基本信息配置占40%
            right_container.grid_rowconfigure(1, weight=0, minsize=60)  # 数据层次选择固定高度
            right_container.grid_rowconfigure(2, weight=60, uniform="content")  # 数据表格字段配置占60%
            right_container.grid_columnconfigure(0, weight=1)
        
            # 右侧上部分：子因子基本信息配置
            basic_info_frame = ttk.LabelFrame(right_container, text="子因子基本信息配置")
            basic_info_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 5))
            
            # 基本信息配置内容区域
            self.basic_info_content_frame = ttk.Frame(basic_info_frame)
            self.basic_info_content_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            # 显示默认提示信息
            self.clear_config_areas()
            
            # 中间：数据层次选择区域
            hierarchy_selection_frame = ttk.LabelFrame(right_container, text="数据层次选择")
            hierarchy_selection_frame.grid(row=1, column=0, sticky="ew", pady=5)
            

            
            # 从配置文件获取默认层次级别
            default_hierarchy = self.config_data.get("default_hierarchy_level", "part")
            self.table_hierarchy_var = tk.StringVar(value=default_hierarchy)
            logger.info(f"🔍 数据层次选择单选按钮初始化，默认层次: {default_hierarchy}")
            
            hierarchy_buttons_frame = ttk.Frame(hierarchy_selection_frame)
            hierarchy_buttons_frame.pack(fill=tk.X, padx=10, pady=5)
            
            hierarchies = [("total", "整单层"), ("boq", "BOQ层"), ("model", "模型层"), ("part", "部件层")]
            radio_buttons = {}
            for value, text in hierarchies:
                radio = ttk.Radiobutton(hierarchy_buttons_frame, text=text, variable=self.table_hierarchy_var,
                               value=value, command=lambda v=value: self.on_hierarchy_change_with_value(v))
                radio.pack(side=tk.LEFT, padx=10)
                radio_buttons[value] = radio
                logger.info(f"🔍 创建数据层次单选按钮: {text}({value}), 是否选中: {value == default_hierarchy}")
            
            # 强制更新单选按钮显示状态
            hierarchy_buttons_frame.update_idletasks()
            
            # 强制触发默认选中的单选按钮 - 使用多重方法确保UI正确显示
            if default_hierarchy in radio_buttons:
                # 方法1: 先清除所有选择，强制刷新
                self.table_hierarchy_var.set("")
                hierarchy_buttons_frame.update_idletasks()
                
                # 方法2: 重新设置目标选择
                self.table_hierarchy_var.set(default_hierarchy)
                hierarchy_buttons_frame.update_idletasks()
                
                # 方法3: 延迟调用invoke方法确保UI渲染完成
                def force_select():
                    radio_buttons[default_hierarchy].invoke()
                    logger.info(f"🔍 强制触发单选按钮选中状态: {default_hierarchy}")
                    logger.info(f"🔍 invoke后变量值: {self.table_hierarchy_var.get()}")
                
                self.root.after(50, force_select)
                logger.info(f"🔍 准备强制触发单选按钮选中状态: {default_hierarchy}")
            
            logger.info(f"🔍 数据层次选择变量当前值: {self.table_hierarchy_var.get()}")
            
            # 延迟验证选中状态
            self.root.after(100, lambda: logger.info(f"🔍 延迟验证 - 数据层次选择变量值: {self.table_hierarchy_var.get()}"))
            
            # 右侧下部分：数据表格字段配置
            table_info_frame = ttk.LabelFrame(right_container, text="数据表格字段配置")
            table_info_frame.grid(row=2, column=0, sticky="nsew")
            
            # 表格字段配置内容区域
            self.table_info_content_frame = ttk.Frame(table_info_frame)
            self.table_info_content_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            logger.info("table_info_content_frame 创建成功")
            
            # 绑定选择事件
            self.category_treeview.bind('<<TreeviewSelect>>', self.on_category_select)
            # Radiobutton组件不需要绑定ListboxSelect事件
            
            # 初始化数据
            self.refresh_factor_categories()
            
            # 保留原有的树形控件用于兼容性（隐藏）
            self.factor_tree = None
            
            # 标记因子分类页面已创建完成
            self.factor_categories_tab_created = True
            
            logger.info("因子分类配置页面创建完成")
        
        except Exception as e:
            logger.error(f"创建因子分类配置页面时出错: {e}")
            # 确保即使出错也要创建基本的 table_info_content_frame
            if not hasattr(self, 'table_info_content_frame'):
                self.table_info_content_frame = ttk.Frame(self.notebook)
                logger.info("创建了备用的 table_info_content_frame")
            raise
    

    
    def create_display_names_tab(self):
        """创建字段配置页面"""
        self.display_names_tab_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.display_names_tab_frame, text="字段配置")
        
        # 创建密码验证界面
        self.create_password_verification_ui()
        
        # 标记内容是否已加载
        self.display_names_content_loaded = False
        
    def ensure_display_names_content(self):
        """确保字段配置页面内容已加载"""
        if self.display_names_content_loaded:
            return
        
        # 说明标签
        info_label = ttk.Label(self.display_names_tab_frame, text="配置字段的显示名称和作用范围", font=('Arial', 10, 'bold'))
        info_label.pack(pady=(10, 5))
        
        # 主容器
        main_container = ttk.Frame(self.display_names_tab_frame)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 搜索框
        search_frame = ttk.Frame(main_container)
        search_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(search_frame, text="搜索:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        
        # 添加搜索按钮，避免仅依赖KeyRelease事件
        search_button = ttk.Button(search_frame, text="搜索", command=self.filter_display_names)
        search_button.pack(side=tk.RIGHT, padx=(5, 0))
        
        # 同时保留KeyRelease事件绑定
        self.search_entry.bind('<KeyRelease>', self.filter_display_names)
        
        # 显示名称树（三列：字段名、显示名称、作用范围）
        tree_frame = ttk.Frame(main_container)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        self.display_names_tree = ttk.Treeview(tree_frame, columns=("field_name", "display_name", "scope"), show="headings")
        self.display_names_tree.heading("field_name", text="字段名")
        self.display_names_tree.heading("display_name", text="显示名称")
        self.display_names_tree.heading("scope", text="作用范围")
        self.display_names_tree.column("field_name", width=200)
        self.display_names_tree.column("display_name", width=200)
        self.display_names_tree.column("scope", width=150)
        
        tree_scrollbar2 = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.display_names_tree.yview)
        self.display_names_tree.configure(yscrollcommand=tree_scrollbar2.set)
        
        self.display_names_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scrollbar2.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 双击编辑
        self.display_names_tree.bind('<Double-1>', self.edit_display_name)
        
        # 底部按钮（去掉批量导入）
        button_frame = ttk.Frame(main_container)
        button_frame.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Button(button_frame, text="添加字段", command=self.add_display_name).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="删除字段", command=self.delete_display_name).pack(side=tk.LEFT, padx=(0, 5))
        
        # 加载显示名称数据
        self.refresh_display_names()
        
        # 标记内容已加载
        self.display_names_content_loaded = True
    
    def create_bottom_buttons(self, parent):
        """创建底部按钮"""
        # 创建底部按钮框架，固定在底部
        button_frame = ttk.Frame(parent)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(5, 0))
        
        # 创建按钮容器，右对齐
        button_container = ttk.Frame(button_frame)
        button_container.pack(side=tk.RIGHT)
        
        # 按钮从右到左排列
        ttk.Button(button_container, text="保存配置", command=self.save_all_config).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(button_container, text="导出配置", command=self.export_config).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(button_container, text="导入配置", command=self.import_config).pack(side=tk.RIGHT, padx=(5, 0))
    
    # ==================== 整单基本信息字段操作 ====================
    
    def refresh_document_fields(self):
        """刷新整单基本信息字段列表"""
        # 清空两个列表框
        self.available_fields_listbox.delete(0, tk.END)
        self.selected_fields_listbox.delete(0, tk.END)
        
        # 获取所有可用字段和已选择字段
        display_names = self.config_data.get("display_names", {})
        selected_fields = self.config_data.get("document_info_fields", [])
        
        # 获取作用范围包含整单基本信息的所有字段
        available_fields = []
        for field_name, field_config in display_names.items():
            if isinstance(field_config, dict):
                scope = field_config.get('scope')
                # 支持多选作用范围：检查scope是否包含'整单基本信息'
                if isinstance(scope, list):
                    # 作用范围是列表，检查是否包含'整单基本信息'
                    if '整单基本信息' in scope:
                        display_name = field_config.get('display_name', field_name)
                        available_fields.append((field_name, display_name))
                elif isinstance(scope, str):
                    # 作用范围是字符串，检查是否等于'整单基本信息'
                    if scope == '整单基本信息':
                        display_name = field_config.get('display_name', field_name)
                        available_fields.append((field_name, display_name))
            else:
                # 兼容旧格式，默认为整单基本信息
                available_fields.append((field_name, field_config))
        
        # 填充已选择字段列表（按配置顺序）
        for field in selected_fields:
            field_config = display_names.get(field, field)
            if isinstance(field_config, dict):
                display_name = field_config.get('display_name', field)
            else:
                display_name = field_config
            self.selected_fields_listbox.insert(tk.END, display_name)
        
        # 填充可选择字段列表（排除已选择的）
        for field_name, display_name in available_fields:
            if field_name not in selected_fields:
                self.available_fields_listbox.insert(tk.END, display_name)
    
    def add_selected_field(self):
        """将字段从可选择列表添加到已选择列表"""
        try:
            logger.debug("执行add_selected_field方法")
            selection = self.available_fields_listbox.curselection()
            if not selection:
                logger.warning("未选择字段，无法添加")
                messagebox.showwarning("警告", "请先选择一个字段！")
                return
            
            # 获取选中的显示名称
            display_name = self.available_fields_listbox.get(selection[0])
            logger.info(f"选中字段: {display_name}")
            
            # 根据显示名称找到对应的字段名
            display_names = self.config_data.get("display_names", {})
            field_name = None
            for fname, fconfig in display_names.items():
                if isinstance(fconfig, dict):
                    if fconfig.get('display_name', fname) == display_name:
                        field_name = fname
                        break
                else:
                    if fconfig == display_name:
                        field_name = fname
                        break
            
            # 如果在display_names中找不到，可能是直接使用字段名作为显示名
            if not field_name:
                # 检查是否有完全匹配的字段名
                all_fields = self.config_data.get("all_fields", [])
                if display_name in all_fields:
                    field_name = display_name
            
            if field_name:
                # 添加到已选择字段配置
                self.config_data.setdefault("document_info_fields", []).append(field_name)
                
                # 从可选列表中移除该项
                self.available_fields_listbox.delete(selection[0])
                
                # 添加到已选择列表
                self.selected_fields_listbox.insert(tk.END, display_name)
                
                # 选中新添加的字段
                self.selected_fields_listbox.selection_set(tk.END)
                
                # 保存配置到文件
                self.save_config(show_success_message=False)
                
                # 确保更新UI
                self.root.update_idletasks()
                
                logger.info(f"添加字段成功: {field_name} ({display_name})，已保存到配置文件")
            else:
                logger.error(f"无法找到字段名称: {display_name}")
                messagebox.showerror("错误", f"无法找到字段名称: {display_name}")
        except Exception as e:
            logger.error(f"添加字段时发生错误: {str(e)}")
            messagebox.showerror("错误", f"添加字段时发生错误: {str(e)}")
    
    def remove_selected_field(self):
        """将字段从已选择列表移除到可选择列表"""
        try:
            logger.debug("执行remove_selected_field方法")
            selection = self.selected_fields_listbox.curselection()
            if not selection:
                logger.warning("未选择字段，无法移除")
                messagebox.showwarning("警告", "请先选择一个字段！")
                return
            
            index = selection[0]
            fields = self.config_data.get("document_info_fields", [])
            
            if index < len(fields):
                field_name = fields[index]
                
                # 获取显示名称用于日志
                display_names = self.config_data.get("display_names", {})
                field_config = display_names.get(field_name, field_name)
                if isinstance(field_config, dict):
                    display_name = field_config.get('display_name', field_name)
                else:
                    display_name = field_config
                
                # 从配置中移除
                fields.pop(index)
                
                # 从已选择列表中移除
                display_name = self.selected_fields_listbox.get(index)
                self.selected_fields_listbox.delete(index)
                
                # 添加到可选择列表
                self.available_fields_listbox.insert(tk.END, display_name)
                
                # 保存配置到文件
                self.save_config(show_success_message=False)
                
                # 确保更新UI
                self.root.update_idletasks()
                
                logger.info(f"移除字段成功: {field_name} ({display_name})，已保存到配置文件")
            else:
                logger.error(f"索引超出范围: {index} >= {len(fields)}")
                messagebox.showerror("错误", "无法移除字段，索引超出范围")
        except Exception as e:
            logger.error(f"移除字段时发生错误: {str(e)}")
            messagebox.showerror("错误", f"移除字段时发生错误: {str(e)}")
    
    def move_selected_field(self, direction):
        """移动已选择字段的位置"""
        selection = self.selected_fields_listbox.curselection()
        if not selection:
            messagebox.showwarning("警告", "请先选择一个字段！")
            return
        
        index = selection[0]
        fields = self.config_data.get("document_info_fields", [])
        new_index = index + direction
        
        if 0 <= new_index < len(fields):
            # 交换位置
            fields[index], fields[new_index] = fields[new_index], fields[index]
            
            # 保存配置到文件
            self.save_config(show_success_message=False)
            
            # 刷新界面
            self.refresh_document_fields()
            
            # 保持选中状态
            self.selected_fields_listbox.selection_set(new_index)
            
            logger.info(f"移动字段位置: {index} -> {new_index}，已保存到配置文件")
    

    
    # ==================== 因子分类操作 ====================
    
    def refresh_factor_categories(self):
        """刷新因子分类列表"""
        # 保存当前选中的分类
        current_selection = None
        selection = self.category_treeview.selection()
        if selection:
            current_selection = self.category_treeview.item(selection[0], 'text')
            logger.debug(f"保存当前选中的分类: {current_selection}")
        
        # 临时解绑事件，防止清空列表时触发选择事件
        self.category_treeview.unbind('<<TreeviewSelect>>')
        
        # 清空分类树
        for item in self.category_treeview.get_children():
            self.category_treeview.delete(item)
        
        # 加载因子分类
        factor_categories = self.config_data.get("factor_categories", {})
        for category_name in factor_categories.keys():
            self.category_treeview.insert('', 'end', text=category_name, open=True)
        
        # 恢复之前的选择状态或默认选择第一个分类
        if current_selection and current_selection in factor_categories:
            self.select_category_by_name(current_selection)
            logger.debug(f"恢复分类选择状态: {current_selection}")
            # 恢复分类选择后，也要默认选择第一个子因子
            self.on_category_select_default(current_selection)
        else:
            # 如果之前没有选择或选择的分类已不存在，默认选择第一个分类
            if factor_categories:
                first_category = list(factor_categories.keys())[0]
                self.select_category_by_name(first_category)
                logger.info(f"默认选择第一个因子分类: {first_category}")
                # 触发分类选择事件，加载子因子并默认选择第一个
                self.on_category_select_default(first_category)
            else:
                # 如果没有分类，清空子因子列表和右侧配置区域
                for widget in self.subfactor_scrollable_frame.winfo_children():
                    widget.destroy()
                self.subfactor_radios = {}
                self.subfactor_var.set("")
                self.clear_config_areas()
        
        # 重新绑定分类选择事件
        self.category_treeview.bind('<<TreeviewSelect>>', self.on_category_select)
    
    def refresh_factor_tree(self):
        """刷新因子分类树（兼容性方法）"""
        if self.factor_tree is not None:
            # 清空树
            for item in self.factor_tree.get_children():
                self.factor_tree.delete(item)
            
            # 加载因子分类
            factor_categories = self.config_data.get("factor_categories", {})
            for category_name, sub_factors in factor_categories.items():
                category_id = self.factor_tree.insert("", tk.END, text=category_name, 
                                                    values=("分类", f"{len(sub_factors)}个子因子"))
                
                # 加载子因子
                for sub_factor in sub_factors:
                    factor_name = sub_factor.get("name", "未命名")
                    basic_info_count = len(sub_factor.get("basic_info", []))
                    table_info_count = sum(len(v) for v in sub_factor.get("table_info", {}).values())
                    
                    self.factor_tree.insert(category_id, tk.END, text=factor_name,
                                            values=("子因子", f"基本信息:{basic_info_count}, 表格信息:{table_info_count}"))
        
        # 同时刷新新的列表界面
        self.refresh_factor_categories()
    
    def clear_config_areas(self):
        """清空配置区域"""
        # 清空基本信息配置区域
        if hasattr(self, 'basic_info_content_frame') and self.basic_info_content_frame:
            for widget in self.basic_info_content_frame.winfo_children():
                widget.destroy()
            # 显示提示信息
            ttk.Label(self.basic_info_content_frame, text="请选择子因子以配置基本信息", 
                     font=('微软雅黑', 10), foreground='gray').pack(expand=True)
        
        # 清空表格字段配置区域
        if hasattr(self, 'table_info_content_frame') and self.table_info_content_frame:
            for widget in self.table_info_content_frame.winfo_children():
                widget.destroy()
            # 显示提示信息
            ttk.Label(self.table_info_content_frame, text="请选择子因子以配置表格字段", 
                     font=('微软雅黑', 10), foreground='gray').pack(expand=True)
        
        logger.debug("配置区域已清空")
    
    def on_category_select(self, event):
        """处理因子分类选择事件 - 严格按照父级->子级选择流程"""
        # 检查是否正在从主应用同步，如果是则跳过处理
        if getattr(self, '_syncing_from_main_app', False):
            logger.info("🔍 正在从主应用同步，跳过on_category_select处理")
            return
            
        import traceback
        logger.info(f"🔍 on_category_select被调用，调用栈: {traceback.format_stack()[-3:-1]}")
        
        selection = self.category_treeview.selection()
        logger.info(f"🔍 当前分类选择状态: {selection}")
        
        if not selection:
            logger.info("因子分类选择已清空")
            self.clear_config_areas()
            return
        
        # 步骤1：保存因子分类的值
        category_name = self.category_treeview.item(selection[0], 'text')
        logger.info(f"步骤1完成：因子分类已选择并保存 -> {category_name}")
        
        # 刷新子因子列表
        logger.info(f"刷新分类 '{category_name}' 下的子因子列表")
        self.refresh_subfactors(category_name)
        
        # 清空配置区域，等待选择子因子
        self.clear_config_areas()
        logger.info("等待选择子因子以完成步骤2")
    
    def on_category_select_default(self, category_name):
        """处理默认分类选择事件，自动选择第一个子因子"""
        logger.info(f"默认分类选择事件: {category_name}")
        
        # 刷新子因子列表
        self.refresh_subfactors(category_name)
        
        # 默认选择第一个子因子
        factor_categories = self.config_data.get("factor_categories", {})
        sub_factors = factor_categories.get(category_name, [])
        
        logger.info(f"🔍 检查子因子列表: {len(sub_factors) if sub_factors else 0} 个子因子")
        if sub_factors:
            first_subfactor = sub_factors[0].get("name", "")
            logger.info(f"🔍 第一个子因子: {first_subfactor}")
            if first_subfactor:
                logger.info(f"🔍 准备延迟设置默认选择: {first_subfactor}")
                # 使用after方法延迟设置选中状态，确保单选按钮已创建完成
                self.root.after(10, lambda: self._set_default_subfactor_selection(category_name, first_subfactor))
            else:
                logger.warning("🔍 第一个子因子名称为空")
        else:
            logger.warning("🔍 没有找到子因子，清空配置区域")
            # 如果没有子因子，清空配置区域
            self.clear_config_areas()
    
    def _set_default_subfactor_selection(self, category_name, first_subfactor):
        """延迟设置默认子因子选择状态"""
        logger.info(f"🔍 延迟设置默认子因子选择状态被调用: {first_subfactor}")
        
        # 检查子因子单选按钮是否已创建
        if first_subfactor in self.subfactor_radios:
            logger.info(f"🔍 找到子因子单选按钮: {first_subfactor}")
        else:
            logger.warning(f"🔍 未找到子因子单选按钮: {first_subfactor}, 可用按钮: {list(self.subfactor_radios.keys())}")
        
        # 设置第一个子因子为选中状态
        old_value = self.subfactor_var.get()
        self.subfactor_var.set(first_subfactor)
        new_value = self.subfactor_var.get()
        logger.info(f"🔍 子因子变量设置: {old_value} -> {new_value}")
        
        # 加载第一个子因子的配置
        self.load_subfactor_config(category_name, first_subfactor)
        logger.info(f"🔍 已加载子因子配置: {first_subfactor}")
    
    # 清除标志的方法已移除
    
    def safe_subfactor_selection_set(self, factor_name):
        """安全的子因子选择方法，保护分类选择状态"""
        # 保存当前分类选择状态
        current_category_selection = self.category_treeview.selection()
        if current_category_selection:
            self._temp_saved_category_selection = current_category_selection
            logger.info(f"🔍 预保存分类选择状态: {current_category_selection}")
        
        # 设置子因子选择变量
        if factor_name in self.subfactor_radios:
            self.subfactor_var.set(factor_name)
            logger.info(f"已选择子因子: {factor_name}")
        
        # 如果分类选择被清空，立即恢复
        if current_category_selection and not self.category_treeview.selection():
            logger.info(f"🔍 检测到分类选择被清空，立即恢复: {current_category_selection}")
            self.category_treeview.selection_set(current_category_selection[0])
        
        # 手动触发子因子选择事件，此时分类选择状态已经恢复
        self.on_subfactor_select(None)
    
    def on_subfactor_select_with_name(self, subfactor_name):
        """处理子因子选择事件 - 使用传入的子因子名称"""
        logger.info(f"子因子选择事件被触发，传入的子因子名称: {subfactor_name}")
        
        # 确保subfactor_var与传入的名称一致
        current_var_value = self.subfactor_var.get()
        logger.info(f"当前subfactor_var的值: {current_var_value}")
        
        if current_var_value != subfactor_name:
            logger.warning(f"subfactor_var值({current_var_value})与传入名称({subfactor_name})不一致，强制更新")
            self.subfactor_var.set(subfactor_name)
        
        # 调用原有的选择处理逻辑
        self.on_subfactor_select(None)

    def on_subfactor_select(self, event):
        """处理子因子选择事件 - 严格按照父级->子级选择流程"""
        logger.info("子因子选择事件被触发")
        logger.info(f"事件类型: {'用户点击' if event else '程序触发'}")
        
        # 保护分类选择状态：使用预保存的分类选择状态
        saved_category_selection = getattr(self, '_temp_saved_category_selection', self.category_treeview.selection())
        logger.info(f"🔍 使用的分类选择状态: {saved_category_selection}")
        
        # 清除临时保存的状态
        if hasattr(self, '_temp_saved_category_selection'):
            delattr(self, '_temp_saved_category_selection')
            logger.info("🔍 已清除临时保存的分类选择状态")
        
        # 强制确保分类选择状态不丢失
        if saved_category_selection and not self.category_treeview.selection():
            logger.info(f"🔍 检测到分类选择被清空，立即恢复: {saved_category_selection}")
            self.category_treeview.selection_set(saved_category_selection)
        
        # 获取当前选中的子因子
        subfactor_name = self.subfactor_var.get()
        
        logger.info(f"子因子选择状态: {subfactor_name}")
        logger.info(f"可用子因子按钮: {list(self.subfactor_radios.keys())}")
        logger.info(f"当前选中的RadioButton值: {subfactor_name}")
        
        # 验证子因子名称是否在可用列表中
        if subfactor_name and subfactor_name not in self.subfactor_radios:
            logger.warning(f"选中的子因子 '{subfactor_name}' 不在可用列表中: {list(self.subfactor_radios.keys())}")
        
        if not subfactor_name:
            logger.info("子因子未选择，可能是列表刷新导致的事件触发，退出处理")
            # 即使退出也要恢复分类选择状态
            self._restore_category_selection_if_needed(saved_category_selection)
            return
        
        logger.info(f"步骤2完成：子因子已选择并保存 -> {subfactor_name}")
        
        # 严格验证：必须先选择因子分类
        category_selection = self.category_treeview.selection()
        logger.info(f"🔍 验证时分类选择状态: {category_selection}")
        
        if not category_selection:
            logger.warning("验证失败：未完成步骤1（选择因子分类），无法加载子因子配置")
            logger.info("🔍 调用clear_config_areas前的分类选择状态")
            self.clear_config_areas()
            logger.info(f"🔍 调用clear_config_areas后的分类选择状态: {self.category_treeview.selection()}")
            # 恢复分类选择状态
            self._restore_category_selection_if_needed(saved_category_selection)
            return
        
        # 获取当前选中的分类名称
        selected_category_name = self.category_treeview.item(category_selection[0], 'text')
        logger.info(f"验证步骤1的值：因子分类 = {selected_category_name}")
        
        # 验证子因子是否属于当前选中的分类
        if self.validate_subfactor_belongs_to_category(subfactor_name, selected_category_name):
            logger.info(f"验证通过：子因子 '{subfactor_name}' 属于分类 '{selected_category_name}'")
            # 步骤3：根据分类名和子因子名查找并加载配置信息
            logger.info(f"步骤3开始：根据分类='{selected_category_name}' 和子因子='{subfactor_name}' 查找配置信息")
            
            # 清空配置区域，确保UI重置
            self.clear_config_areas()
            
            # 强制更新子因子变量值，确保使用最新选择
            self.subfactor_var.set(subfactor_name)
            logger.info(f"🔍 强制更新子因子变量值: {self.subfactor_var.get()}")
            
            # 加载子因子配置
            self.load_subfactor_config(selected_category_name, subfactor_name)
            logger.info(f"步骤3完成：配置信息加载完成")
        else:
            logger.error(f"验证失败：子因子 '{subfactor_name}' 不属于当前选中的分类 '{selected_category_name}'")
            logger.error("请确保先选择正确的因子分类，再选择对应的子因子")
            self.clear_config_areas()
        
        # 保护分类选择状态：恢复分类选择（如果之前有选择的话）
        self._restore_category_selection_if_needed(saved_category_selection)
    
    def _restore_category_selection_if_needed(self, saved_category_selection):
        """恢复分类选择状态的统一方法"""
        if saved_category_selection:
            current_selection = self.category_treeview.selection()
            if not current_selection:
                logger.info(f"🔍 恢复分类选择状态: {saved_category_selection}")
                # 临时解绑事件避免触发递归
                self.category_treeview.unbind('<<TreeviewSelect>>')
                self.category_treeview.selection_set(saved_category_selection[0])
                self.category_treeview.bind('<<TreeviewSelect>>', self.on_category_select)
                logger.info(f"🔍 分类选择状态已恢复: {self.category_treeview.selection()}")
            else:
                logger.info(f"🔍 分类选择状态正常，无需恢复: {current_selection}")
    
    def get_selected_category(self):
        """获取当前选中的分类名称"""
        selection = self.category_treeview.selection()
        if selection:
            return self.category_treeview.item(selection[0], 'text')
        return None
    
    def get_category_selection(self):
        """获取当前分类选择状态"""
        return self.category_treeview.selection()
    
    def find_category_for_subfactor(self, subfactor_name):
        """查找子因子所属的分类"""
        factor_categories = self.config_data.get("factor_categories", {})
        
        for category_name, sub_factors in factor_categories.items():
            if isinstance(sub_factors, list):
                for factor in sub_factors:
                    if isinstance(factor, dict) and factor.get("name") == subfactor_name:
                        return category_name
        
        return None
    
    def validate_subfactor_belongs_to_category(self, subfactor_name, category_name):
        """验证子因子是否属于指定的分类"""
        factor_categories = self.config_data.get("factor_categories", {})
        sub_factors = factor_categories.get(category_name, [])
        
        if isinstance(sub_factors, list):
            for factor in sub_factors:
                if isinstance(factor, dict) and factor.get("name") == subfactor_name:
                    return True
        
        return False
    
    def select_category_by_name(self, category_name):
        """根据分类名称选中对应的分类项"""
        for item in self.category_treeview.get_children():
            if self.category_treeview.item(item, 'text') == category_name:
                self.category_treeview.selection_set(item)
                self.category_treeview.see(item)
                logger.info(f"已选中分类: {category_name}")
                break
    
    def refresh_subfactors(self, category_name):
        """刷新子因子列表（仅显示指定分类的子因子）"""
        # 清空现有的子因子按钮
        for widget in self.subfactor_scrollable_frame.winfo_children():
            widget.destroy()
        
        self.subfactor_radios = {}
        
        # 加载选中分类的子因子
        factor_categories = self.config_data.get("factor_categories", {})
        sub_factors = factor_categories.get(category_name, [])
        
        # 创建子因子选择按钮
        for sub_factor in sub_factors:
            factor_name = sub_factor.get("name", "未命名")
            
            radio = ttk.Radiobutton(
                self.subfactor_scrollable_frame, 
                text=factor_name,
                variable=self.subfactor_var, 
                value=factor_name,
                style="Tech.TRadiobutton" if hasattr(ttk, "Style") else None,
                command=lambda sf=factor_name: self.on_subfactor_select_with_name(sf)
            )
            radio.pack(anchor=tk.W, pady=3, padx=5)
            self.subfactor_radios[factor_name] = radio
        
        logger.debug(f"刷新子因子列表完成，分类: {category_name}, 子因子数量: {len(sub_factors)}")
    
    def load_subfactor_config(self, category_name, subfactor_name):
        """加载子因子配置到右侧区域"""
        logger.info(f"加载子因子配置: 分类={category_name}, 子因子={subfactor_name}")
        
        # 直接使用已加载的配置数据，不再尝试从config_manager获取
        # 找到对应的子因子数据
        factor_categories = self.config_data.get("factor_categories", {})
        sub_factors = factor_categories.get(category_name, [])
        
        logger.info(f"找到分类 '{category_name}' 下的子因子数量: {len(sub_factors)}")
        
        target_factor = None
        for factor in sub_factors:
            if factor.get("name") == subfactor_name:
                target_factor = factor
                logger.info(f"找到目标子因子: {factor}")
                break
        
        if target_factor:
            logger.info(f"找到目标子因子数据: {target_factor.get('name')}")
            logger.info(f"子因子basic_info字段: {target_factor.get('basic_info', [])}")
            
            # 保存当前子因子数据到实例变量
            self.current_factor_data = target_factor
            logger.info(f"当前子因子的basic_info: {self.current_factor_data.get('basic_info', [])}")
            
            # 清空现有内容，确保UI重置
            for widget in self.basic_info_content_frame.winfo_children():
                widget.destroy()
            
            for widget in self.table_info_content_frame.winfo_children():
                widget.destroy()
            
            # 保存当前子因子数据到实例变量
            self.current_factor_data = target_factor
            logger.info(f"当前子因子的basic_info: {self.current_factor_data.get('basic_info', [])}")
            
            # 设置基本信息配置界面
            self.setup_basic_info_config(target_factor)
            
            # 设置表格信息配置界面
            self.setup_table_info_config(target_factor)
            
            # 刷新UI显示
            self.refresh_basic_info_fields(target_factor)
            
            logger.info(f"因子切换完成，当前展示的是子因子 '{target_factor.get('name')}' 的基本信息")
            
            logger.info(f"因子切换完成，当前展示的是子因子 '{subfactor_name}' 的基本信息")
        else:
            logger.error(f"未找到子因子 '{subfactor_name}' 在分类 '{category_name}' 中")
    
    def setup_basic_info_config(self, factor_data):
        """设置基本信息配置界面"""
        # 清空现有内容
        for widget in self.basic_info_content_frame.winfo_children():
            widget.destroy()
        
        # 保存当前子因子数据到实例变量，确保其他方法可以访问
        self.current_factor_data = factor_data
        logger.info(f"在setup_basic_info_config中保存子因子数据: {self.current_factor_data.get('name')}")
        
        # 创建左右分栏布局，参照整单基本信息页面
        main_frame = ttk.Frame(self.basic_info_content_frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 左侧：可选择字段
        left_frame = ttk.LabelFrame(main_frame, text="可选择字段", padding=5)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # 可选字段列表框
        available_frame = ttk.Frame(left_frame)
        available_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.basic_available_listbox = tk.Listbox(available_frame, selectmode=tk.SINGLE,
                                                 font=('微软雅黑', 9),
                                                 bg='#f8f9fa', selectbackground='#007acc',
                                                 selectforeground='white', borderwidth=1,
                                                 relief='solid', highlightthickness=0)
        self.basic_available_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        basic_available_scrollbar = ttk.Scrollbar(available_frame, orient=tk.VERTICAL, command=self.basic_available_listbox.yview)
        self.basic_available_listbox.configure(yscrollcommand=basic_available_scrollbar.set)
        basic_available_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 中间：操作按钮
        middle_frame = ttk.Frame(main_frame)
        middle_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        ttk.Button(middle_frame, text="→ 添加", command=self.add_basic_field).pack(pady=5, fill=tk.X)
        ttk.Button(middle_frame, text="← 移除", command=self.remove_basic_field).pack(pady=5, fill=tk.X)
        ttk.Button(middle_frame, text="↑ 上移", command=self.move_basic_field_up).pack(pady=5, fill=tk.X)
        ttk.Button(middle_frame, text="↓ 下移", command=self.move_basic_field_down).pack(pady=5, fill=tk.X)
        
        # 右侧：已选择字段
        right_frame = ttk.LabelFrame(main_frame, text="已选择字段", padding=5)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # 已选字段列表框
        selected_frame = ttk.Frame(right_frame)
        selected_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.basic_selected_listbox = tk.Listbox(selected_frame, selectmode=tk.SINGLE,
                                                font=('微软雅黑', 9),
                                                bg='#f0f8ff', selectbackground='#007acc',
                                                selectforeground='white', borderwidth=1,
                                                relief='solid', highlightthickness=0)
        self.basic_selected_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        basic_selected_scrollbar = ttk.Scrollbar(selected_frame, orient=tk.VERTICAL, command=self.basic_selected_listbox.yview)
        self.basic_selected_listbox.configure(yscrollcommand=basic_selected_scrollbar.set)
        basic_selected_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 加载数据
        self.refresh_basic_info_fields(factor_data)
    
    def setup_table_info_config(self, factor_data):
        """设置表格字段配置界面"""
        logger.info(f"开始设置表格字段配置界面，factor_data: {factor_data.get('name', 'Unknown')}")
        
        # 检查table_info_content_frame是否存在
        if not hasattr(self, 'table_info_content_frame') or self.table_info_content_frame is None:
            logger.error("table_info_content_frame 不存在，无法设置表格字段配置界面")
            return
        
        # 清空现有内容
        for widget in self.table_info_content_frame.winfo_children():
            widget.destroy()
        
        logger.info("已清空表格字段配置区域的现有内容")
        
        # 字段配置区域（左右分栏）- 直接在table_info_content_frame中创建
        fields_frame = ttk.Frame(self.table_info_content_frame)
        fields_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 左侧：可选择字段
        left_frame = ttk.LabelFrame(fields_frame, text="可选择字段", padding=5)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        available_frame = ttk.Frame(left_frame)
        available_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.table_available_listbox = tk.Listbox(available_frame, selectmode=tk.SINGLE,
                                                 font=('微软雅黑', 9),
                                                 bg='#f8f9fa', selectbackground='#007acc',
                                                 selectforeground='white', borderwidth=1,
                                                 relief='solid', highlightthickness=0)
        self.table_available_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        table_available_scrollbar = ttk.Scrollbar(available_frame, orient=tk.VERTICAL, command=self.table_available_listbox.yview)
        self.table_available_listbox.configure(yscrollcommand=table_available_scrollbar.set)
        table_available_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 中间：操作按钮
        middle_frame = ttk.Frame(fields_frame)
        middle_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        ttk.Button(middle_frame, text="→ 添加", command=self.add_table_field).pack(pady=5, fill=tk.X)
        ttk.Button(middle_frame, text="← 移除", command=self.remove_table_field).pack(pady=5, fill=tk.X)
        ttk.Button(middle_frame, text="↑ 上移", command=self.move_table_field_up).pack(pady=5, fill=tk.X)
        ttk.Button(middle_frame, text="↓ 下移", command=self.move_table_field_down).pack(pady=5, fill=tk.X)
        
        # 右侧：已选择字段
        right_frame = ttk.LabelFrame(fields_frame, text="已选择字段", padding=5)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        selected_frame = ttk.Frame(right_frame)
        selected_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.table_selected_listbox = tk.Listbox(selected_frame, selectmode=tk.SINGLE,
                                                font=('微软雅黑', 9),
                                                bg='#f0f8ff', selectbackground='#007acc',
                                                selectforeground='white', borderwidth=1,
                                                relief='solid', highlightthickness=0)
        self.table_selected_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        table_selected_scrollbar = ttk.Scrollbar(selected_frame, orient=tk.VERTICAL, command=self.table_selected_listbox.yview)
        self.table_selected_listbox.configure(yscrollcommand=table_selected_scrollbar.set)
        table_selected_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 加载数据
        logger.info("开始刷新表格字段数据")
        self.refresh_table_info_fields(factor_data)
        logger.info("表格字段配置界面设置完成")
        
        # 注意：不在这里清除忽略标志，由load_subfactor_config统一管理
    
    # ==================== 新的因子分类操作方法 ====================
    
    def edit_factor_category(self):
        """编辑因子分类"""
        selection = self.get_category_selection()
        if not selection:
            messagebox.showwarning("警告", "请先选择一个分类！")
            return
        
        old_name = self.get_selected_category()
        new_name = simpledialog.askstring("编辑分类", f"请输入新的分类名称:", initialvalue=old_name)
        
        if new_name and new_name.strip() and new_name.strip() != old_name:
            new_name = new_name.strip()
            factor_categories = self.config_data.get("factor_categories", {})
            
            if new_name not in factor_categories:
                # 重命名分类
                factor_categories[new_name] = factor_categories.pop(old_name)
                self.refresh_factor_categories()
                logger.info(f"编辑因子分类: {old_name} -> {new_name}")
            else:
                messagebox.showwarning("警告", "分类名称已存在！")
    
    def delete_factor_category(self):
        """删除因子分类"""
        selection = self.get_category_selection()
        if not selection:
            messagebox.showwarning("警告", "请先选择一个分类！")
            return
        
        category_name = self.get_selected_category()
        
        if messagebox.askyesno("确认删除", f"确定要删除分类 '{category_name}' 及其所有子因子吗？"):
            factor_categories = self.config_data.get("factor_categories", {})
            if category_name in factor_categories:
                del factor_categories[category_name]
                self.refresh_factor_categories()
                logger.info(f"删除因子分类: {category_name}")
    
    def add_sub_factor_new(self):
        """添加子因子（新方法）"""
        selection = self.get_category_selection()
        if not selection:
            messagebox.showwarning("警告", "请先选择一个分类！")
            return
        
        category_name = self.get_selected_category()
        factor_name = simpledialog.askstring("添加子因子", f"请输入子因子名称 (分类: {category_name}):")
        
        if factor_name and factor_name.strip():
            factor_name = factor_name.strip()
            
            # 检查是否已存在
            existing_factors = [f.get("name") for f in self.config_data.get("factor_categories", {}).get(category_name, [])]
            if factor_name not in existing_factors:
                new_factor = {
                    "name": factor_name,
                    "basic_info": [],
                    "table_info": {}
                }
                self.config_data.setdefault("factor_categories", {}).setdefault(category_name, []).append(new_factor)
                self.refresh_subfactors(category_name)
                logger.info(f"添加子因子: {category_name} -> {factor_name}")
            else:
                messagebox.showwarning("警告", "子因子已存在！")
    
    def edit_sub_factor_new(self):
        """编辑子因子（新方法）"""
        category_selection = self.get_category_selection()
        subfactor_name = self.subfactor_var.get()
        
        if not category_selection or not subfactor_name:
            messagebox.showwarning("警告", "请先选择一个子因子！")
            return
        
        category_name = self.get_selected_category()
        old_name = subfactor_name
        new_name = simpledialog.askstring("编辑子因子", f"请输入新的子因子名称:", initialvalue=old_name)
        
        if new_name and new_name.strip() and new_name.strip() != old_name:
            new_name = new_name.strip()
            factors = self.config_data.get("factor_categories", {}).get(category_name, [])
            existing_names = [f.get("name") for f in factors]
            
            if new_name not in existing_names:
                for factor in factors:
                    if factor.get("name") == old_name:
                        factor["name"] = new_name
                        break
                self.refresh_subfactors(category_name)
                logger.info(f"编辑子因子名称: {old_name} -> {new_name}")
            else:
                messagebox.showwarning("警告", "子因子名称已存在！")
    
    def delete_sub_factor_new(self):
        """删除子因子（新方法）"""
        category_selection = self.get_category_selection()
        subfactor_name = self.subfactor_var.get()
        
        if not category_selection or not subfactor_name:
            messagebox.showwarning("警告", "请先选择一个子因子！")
            return
        
        category_name = self.get_selected_category()
        
        if messagebox.askyesno("确认删除", f"确定要删除子因子 '{subfactor_name}' 吗？"):
            factors = self.config_data.get("factor_categories", {}).get(category_name, [])
            self.config_data["factor_categories"][category_name] = [f for f in factors if f.get("name") != subfactor_name]
            self.refresh_subfactors(category_name)
            self.clear_config_areas()
            logger.info(f"删除子因子: {category_name} -> {subfactor_name}")
    
    # ==================== 右侧配置区域数据刷新方法 ====================
    
    def refresh_basic_info_fields(self, factor_data):
        """刷新基本信息字段列表"""
        logger.info(f"开始刷新基本信息字段，因子: {factor_data.get('name', '未知')}")
        
        # 清空列表
        self.basic_available_listbox.delete(0, tk.END)
        self.basic_selected_listbox.delete(0, tk.END)
        
        # 获取所有字段定义
        display_names = self.config_data.get("display_names", {})
        selected_fields = factor_data.get("basic_info", [])
        
        logger.info(f"display_names字段总数: {len(display_names)}")
        logger.info(f"子因子 '{factor_data.get('name')}' 的已选字段: {selected_fields}")
        
        # 过滤出作用范围包含"子因子基本信息"的字段
        available_fields = []
        for field, field_info in display_names.items():
            scope = field_info.get("scope", [])
            # scope可能是字符串或列表
            if isinstance(scope, str):
                scope = [scope]
            if "子因子基本信息" in scope:
                available_fields.append(field)
                logger.debug(f"字段 '{field}' 符合条件，scope: {scope}")
        
        logger.info(f"过滤后可用字段数: {len(available_fields)}, 字段列表: {available_fields}")
        
        # 填充可选字段（排除已选择的）
        added_to_available = 0
        for field in available_fields:
            if field not in selected_fields:
                display_name = display_names.get(field, {}).get("display_name", field)
                self.basic_available_listbox.insert(tk.END, f"{display_name}")
                added_to_available += 1

        

        
        # 填充已选择字段（按顺序显示）
        added_to_selected = 0
        for field in selected_fields:
            if field in display_names:
                display_name = display_names.get(field, {}).get("display_name", field)
                self.basic_selected_listbox.insert(tk.END, f"{display_name}")
                added_to_selected += 1

            else:
                logger.warning(f"已选字段 '{field}' 在display_names中不存在")
        


    
    def refresh_table_info_fields(self, factor_data):
        """刷新表格字段列表"""
        # 清空列表
        self.table_available_listbox.delete(0, tk.END)
        self.table_selected_listbox.delete(0, tk.END)
        
        # 获取当前数据层次
        hierarchy = getattr(self, 'table_hierarchy_var', None)
        if hierarchy is None:
            logger.warning("table_hierarchy_var未初始化，使用默认值part")
            hierarchy = "part"
        else:
            hierarchy = hierarchy.get()
        
        logger.info(f"刷新表格字段列表，当前层次: {hierarchy}")
        
        # 获取该层次的所有可用字段（作用范围包含子因子表格的字段）
        all_fields = self.config_data.get("display_names", {})
        hierarchy_fields = []
        
        for field, info in all_fields.items():
            scope = info.get("scope", [])
            # 处理scope可能是字符串或数组的情况
            if isinstance(scope, str):
                scope = [scope]
            # 检查作用范围是否包含"子因子表格"
            if "子因子表格" in scope:
                hierarchy_fields.append(field)
        
        logger.info(f"找到作用范围包含子因子表格的字段: {hierarchy_fields}")
        
        # 获取已选择字段
        selected_fields = factor_data.get("table_info", {}).get(hierarchy, [])
        
        # 填充可选字段（排除已选择的）- 只显示中文名称
        for field in hierarchy_fields:
            if field not in selected_fields:
                display_name = all_fields.get(field, {}).get("display_name", field)
                self.table_available_listbox.insert(tk.END, display_name)
        
        # 填充已选择字段 - 只显示中文名称
        for field in selected_fields:
            display_name = all_fields.get(field, {}).get("display_name", field)
            self.table_selected_listbox.insert(tk.END, display_name)
        
        # 注意：不在这里清除忽略标志，由调用方统一管理
    
    def on_hierarchy_change_with_value(self, hierarchy_value):
        """数据层次选择改变时刷新表格字段配置（带参数版本）"""
        # 确保变量值正确更新
        old_value = self.table_hierarchy_var.get()
        self.table_hierarchy_var.set(hierarchy_value)
        new_value = self.table_hierarchy_var.get()
        logger.info(f"🔍 on_hierarchy_change_with_value被调用，层次变化: {old_value} -> {new_value}")
        
        factor_data = self.get_current_factor_data()
        if factor_data and hasattr(self, 'table_available_listbox'):
            logger.info(f"🔍 准备刷新表格字段，使用层次: {new_value}")
            self.refresh_table_info_fields(factor_data)
        else:
            logger.warning(f"🔍 无法刷新表格字段 - factor_data: {factor_data is not None}, has_listbox: {hasattr(self, 'table_available_listbox')}")
    
    def on_hierarchy_change(self):
        """数据层次选择改变时刷新表格字段配置（无参数版本，保持兼容性）"""
        # 添加调试日志确认变量值变化
        current_hierarchy = self.table_hierarchy_var.get()
        logger.info(f"🔍 on_hierarchy_change被调用，当前层次变量值: {current_hierarchy}")
        
        factor_data = self.get_current_factor_data()
        if factor_data and hasattr(self, 'table_available_listbox'):
            logger.info(f"🔍 准备刷新表格字段，使用层次: {current_hierarchy}")
            self.refresh_table_info_fields(factor_data)
        else:
            logger.warning(f"🔍 无法刷新表格字段 - factor_data: {factor_data is not None}, has_listbox: {hasattr(self, 'table_available_listbox')}")
    
    def on_table_hierarchy_change(self, factor_data):
        """数据层次改变时刷新字段列表"""
        self.refresh_table_info_fields(factor_data)
    
    # ==================== 基本信息字段操作方法 ====================
    
    def add_basic_field(self):
        """添加基本信息字段"""
        selection = self.basic_available_listbox.curselection()
        if not selection:
            messagebox.showwarning("警告", "请先选择一个字段！")
            return
        
        # 获取选中的字段
        selected_display_name = self.basic_available_listbox.get(selection[0])
        # 根据显示名找到对应的字段名
        field_name = None
        display_names = self.config_data.get("display_names", {})
        for field, field_info in display_names.items():
            if field_info.get("display_name", field) == selected_display_name:
                field_name = field
                break
        
        if not field_name:
            # 如果找不到对应字段，直接从界面删除该项
            self.table_selected_listbox.delete(selection[0])
            logger.info(f"删除了不存在的字段: {selected_display_name}")
            return
        
        # 获取当前选中的子因子
        subfactor_name = self.subfactor_var.get()
        
        if subfactor_name:
            category_name = self.find_category_for_subfactor(subfactor_name)
            
            if not category_name:
                messagebox.showerror("错误", "无法找到子因子所属的分类！")
                return
            
            # 更新配置数据
            factors = self.config_data.get("factor_categories", {}).get(category_name, [])
            for factor in factors:
                if factor.get("name") == subfactor_name:
                    if "basic_info" not in factor:
                        factor["basic_info"] = []
                    factor["basic_info"].append(field_name)
                    break
            
            # 保存配置并刷新界面
            self.save_config(show_success_message=False)
            self.refresh_basic_info_fields(self.get_current_factor_data())
            logger.info(f"添加基本信息字段: {field_name}")
    
    def remove_basic_field(self):
        """移除基本信息字段"""
        selection = self.basic_selected_listbox.curselection()
        if not selection:
            messagebox.showwarning("警告", "请先选择一个字段！")
            return
        
        # 获取选中的字段
        selected_display_name = self.basic_selected_listbox.get(selection[0])
        # 根据显示名找到对应的字段名
        field_name = None
        display_names = self.config_data.get("display_names", {})
        for field, field_info in display_names.items():
            if field_info.get("display_name", field) == selected_display_name:
                field_name = field
                break
        
        if not field_name:
            # 如果找不到对应字段，直接从界面删除该项
            self.table_selected_listbox.delete(selection[0])
            logger.info(f"删除了不存在的字段: {selected_display_name}")
            return
        
        # 获取当前选中的子因子
        subfactor_name = self.subfactor_var.get()
        
        if subfactor_name:
            category_name = self.find_category_for_subfactor(subfactor_name)
            
            if not category_name:
                messagebox.showerror("错误", "无法找到子因子所属的分类！")
                return
            
            # 更新配置数据
            factors = self.config_data.get("factor_categories", {}).get(category_name, [])
            for factor in factors:
                if factor.get("name") == subfactor_name:
                    if field_name in factor.get("basic_info", []):
                        factor["basic_info"].remove(field_name)
                    break
            
            # 保存配置并刷新界面
            self.save_config(show_success_message=False)
            self.refresh_basic_info_fields(self.get_current_factor_data())
            logger.info(f"移除基本信息字段: {field_name}")
    
    def move_basic_field_up(self):
        """上移基本信息字段"""
        selection = self.basic_selected_listbox.curselection()
        if not selection or selection[0] == 0:
            return
        
        index = selection[0]
        selected_display_name = self.basic_selected_listbox.get(index)
        # 根据显示名找到对应的字段名
        field_name = None
        display_names = self.config_data.get("display_names", {})
        for field, field_info in display_names.items():
            if field_info.get("display_name", field) == selected_display_name:
                field_name = field
                break
        
        if not field_name:
            return
        
        # 获取当前选中的子因子
        subfactor_name = self.subfactor_var.get()
        
        if subfactor_name:
            category_name = self.find_category_for_subfactor(subfactor_name)
            
            if not category_name:
                return
            
            # 更新配置数据
            factors = self.config_data.get("factor_categories", {}).get(category_name, [])
            for factor in factors:
                if factor.get("name") == subfactor_name:
                    basic_info = factor.get("basic_info", [])
                    if index > 0 and index < len(basic_info):
                        basic_info[index], basic_info[index-1] = basic_info[index-1], basic_info[index]
                    break
            
            # 保存配置并刷新界面，保持选择
            self.save_config(show_success_message=False)
            self.refresh_basic_info_fields(self.get_current_factor_data())
            self.basic_selected_listbox.selection_set(index-1)
    
    def move_basic_field_down(self):
        """下移基本信息字段"""
        selection = self.basic_selected_listbox.curselection()
        if not selection:
            return
        
        index = selection[0]
        max_index = self.basic_selected_listbox.size() - 1
        if index == max_index:
            return
        
        selected_display_name = self.basic_selected_listbox.get(index)
        # 根据显示名找到对应的字段名
        field_name = None
        display_names = self.config_data.get("display_names", {})
        for field, field_info in display_names.items():
            if field_info.get("display_name", field) == selected_display_name:
                field_name = field
                break
        
        if not field_name:
            return
        
        # 获取当前选中的子因子
        subfactor_name = self.subfactor_var.get()
        
        if subfactor_name:
            category_name = self.find_category_for_subfactor(subfactor_name)
            
            if not category_name:
                return
            
            # 更新配置数据
            factors = self.config_data.get("factor_categories", {}).get(category_name, [])
            for factor in factors:
                if factor.get("name") == subfactor_name:
                    basic_info = factor.get("basic_info", [])
                    if index < len(basic_info) - 1:
                        basic_info[index], basic_info[index+1] = basic_info[index+1], basic_info[index]
                    break
            
            # 保存配置并刷新界面，保持选择
            self.save_config(show_success_message=False)
            self.refresh_basic_info_fields(self.get_current_factor_data())
            self.basic_selected_listbox.selection_set(index+1)
    
    # ==================== 表格字段操作方法 ====================
    
    def add_table_field(self):
        """添加表格字段"""
        selection = self.table_available_listbox.curselection()
        if not selection:
            messagebox.showwarning("警告", "请先选择一个字段！")
            return
        
        # 获取选中的中文名称
        selected_display_name = self.table_available_listbox.get(selection[0])
        
        # 根据中文名称找到对应的字段名
        field_name = None
        display_names = self.config_data.get("display_names", {})
        for field, field_info in display_names.items():
            if field_info.get("display_name", field) == selected_display_name:
                field_name = field
                break
        
        if not field_name:
            # 如果找不到对应字段，直接从界面删除该项
            self.table_selected_listbox.delete(selection[0])
            logger.info(f"删除了不存在的字段: {selected_display_name}")
            return
        
        # 获取当前选中的子因子和数据层次
        factor_data = self.get_current_factor_data()
        hierarchy = self.table_hierarchy_var.get()
        
        if factor_data and factor_data.get("name"):
            subfactor_name = factor_data.get("name")
            category_name = self.find_category_for_subfactor(subfactor_name)
            
            # 更新配置数据
            factors = self.config_data.get("factor_categories", {}).get(category_name, [])
            for factor in factors:
                if factor.get("name") == subfactor_name:
                    if "table_info" not in factor:
                        factor["table_info"] = {}
                    if hierarchy not in factor["table_info"]:
                        factor["table_info"][hierarchy] = []
                    factor["table_info"][hierarchy].append(field_name)
                    break
            
            # 刷新界面
            self.refresh_table_info_fields(self.get_current_factor_data())
            # 保存配置文件
            self.save_config(show_success_message=False)
            logger.info(f"添加表格字段: {field_name} ({hierarchy})")
    
    def remove_table_field(self):
        """移除表格字段"""
        selection = self.table_selected_listbox.curselection()
        if not selection:
            messagebox.showwarning("警告", "请先选择一个字段！")
            return
        
        # 获取选中的中文名称
        selected_display_name = self.table_selected_listbox.get(selection[0])
        
        # 根据中文名称找到对应的字段名
        field_name = None
        display_names = self.config_data.get("display_names", {})
        for field, field_info in display_names.items():
            if field_info.get("display_name", field) == selected_display_name:
                field_name = field
                break
        
        if not field_name:
            # 如果在display_names中找不到，尝试用显示名称作为字段名
            field_name = selected_display_name
            logger.info(f"未在display_names中找到字段，使用显示名称作为字段名: {field_name}")
        
        # 直接删除选中项
        self.table_selected_listbox.delete(selection[0])
        
        # 获取当前选中的子因子和数据层次
        factor_data = self.get_current_factor_data()
        hierarchy = self.table_hierarchy_var.get()
        
        if factor_data and factor_data.get("name"):
            subfactor_name = factor_data.get("name")
            category_name = self.find_category_for_subfactor(subfactor_name)
            
            # 更新配置数据
            factors = self.config_data.get("factor_categories", {}).get(category_name, [])
            for factor in factors:
                if factor.get("name") == subfactor_name:
                    table_info = factor.get("table_info", {})
                    if hierarchy in table_info and field_name in table_info[hierarchy]:
                        table_info[hierarchy].remove(field_name)
                    break
            
            # 刷新界面
            self.refresh_table_info_fields(self.get_current_factor_data())
            # 保存配置文件
            self.save_config(show_success_message=False)
            logger.info(f"移除表格字段: {field_name} ({hierarchy})")
    
    def move_table_field_up(self):
        """上移表格字段"""
        selection = self.table_selected_listbox.curselection()
        if not selection or selection[0] == 0:
            return
        
        index = selection[0]
        hierarchy = self.table_hierarchy_var.get()
        
        # 获取当前选中的子因子
        factor_data = self.get_current_factor_data()
        
        if factor_data and factor_data.get("name"):
            subfactor_name = factor_data.get("name")
            category_name = self.find_category_for_subfactor(subfactor_name)
            
            # 更新配置数据
            factors = self.config_data.get("factor_categories", {}).get(category_name, [])
            for factor in factors:
                if factor.get("name") == subfactor_name:
                    table_info = factor.get("table_info", {}).get(hierarchy, [])
                    if index > 0 and index < len(table_info):
                        table_info[index], table_info[index-1] = table_info[index-1], table_info[index]
                    break
            
            # 刷新界面并保持选择
            self.refresh_table_info_fields(self.get_current_factor_data())
            self.table_selected_listbox.selection_set(index-1)
            # 保存配置文件
            self.save_config(show_success_message=False)
    
    def move_table_field_down(self):
        """下移表格字段"""
        selection = self.table_selected_listbox.curselection()
        if not selection:
            return
        
        index = selection[0]
        max_index = self.table_selected_listbox.size() - 1
        if index == max_index:
            return
        
        hierarchy = self.table_hierarchy_var.get()
        
        # 获取当前选中的子因子
        factor_data = self.get_current_factor_data()
        
        if factor_data and factor_data.get("name"):
            subfactor_name = factor_data.get("name")
            category_name = self.find_category_for_subfactor(subfactor_name)
            
            # 更新配置数据
            factors = self.config_data.get("factor_categories", {}).get(category_name, [])
            for factor in factors:
                if factor.get("name") == subfactor_name:
                    table_info = factor.get("table_info", {}).get(hierarchy, [])
                    if index < len(table_info) - 1:
                        table_info[index], table_info[index+1] = table_info[index+1], table_info[index]
                    break
            
            # 刷新界面并保持选择
            self.refresh_table_info_fields(self.get_current_factor_data())
            self.table_selected_listbox.selection_set(index+1)
            # 保存配置文件
            self.save_config(show_success_message=False)
    
    def get_current_factor_data(self):
        """获取当前选中子因子的数据"""
        subfactor_name = self.subfactor_var.get()
        
        if subfactor_name:
            category_name = self.find_category_for_subfactor(subfactor_name)
            
            if category_name:
                factors = self.config_data.get("factor_categories", {}).get(category_name, [])
                for factor in factors:
                    if factor.get("name") == subfactor_name:
                        return factor
        
        return {"basic_info": [], "table_info": {}}
      
    def add_factor_category(self):
        """添加因子分类"""
        category_name = simpledialog.askstring("添加分类", "请输入分类名称:")
        if category_name and category_name.strip():
            category_name = category_name.strip()
            if category_name not in self.config_data.get("factor_categories", {}):
                self.config_data.setdefault("factor_categories", {})[category_name] = []
                self.refresh_factor_tree()
                logger.info(f"添加因子分类: {category_name}")
            else:
                messagebox.showwarning("警告", "分类已存在！")
    
    def add_sub_factor(self):
        """添加子因子"""
        selection = self.factor_tree.selection()
        if not selection:
            messagebox.showwarning("警告", "请先选择一个分类！")
            return
        
        item = selection[0]
        item_values = self.factor_tree.item(item, "values")
        
        # 如果选中的是子因子，获取其父分类
        if item_values[0] == "子因子":
            item = self.factor_tree.parent(item)
        
        category_name = self.factor_tree.item(item, "text")
        
        factor_name = simpledialog.askstring("添加子因子", f"请输入子因子名称 (分类: {category_name}):")
        if factor_name and factor_name.strip():
            factor_name = factor_name.strip()
            
            # 检查是否已存在
            existing_factors = [f.get("name") for f in self.config_data.get("factor_categories", {}).get(category_name, [])]
            if factor_name not in existing_factors:
                new_factor = {
                    "name": factor_name,
                    "basic_info": [],
                    "table_info": {}
                }
                self.config_data.setdefault("factor_categories", {}).setdefault(category_name, []).append(new_factor)
                self.refresh_factor_tree()
                logger.info(f"添加子因子: {category_name} -> {factor_name}")
            else:
                messagebox.showwarning("警告", "子因子已存在！")
    
    def edit_factor_item(self):
        """编辑因子项目"""
        selection = self.factor_tree.selection()
        if not selection:
            messagebox.showwarning("警告", "请先选择一个项目！")
            return
        
        item = selection[0]
        item_text = self.factor_tree.item(item, "text")
        item_values = self.factor_tree.item(item, "values")
        
        new_name = simpledialog.askstring("编辑名称", f"请输入新名称 (当前: {item_text}):")
        if new_name and new_name.strip() and new_name.strip() != item_text:
            new_name = new_name.strip()
            
            if item_values[0] == "分类":
                # 编辑分类名称
                factor_categories = self.config_data.get("factor_categories", {})
                if new_name not in factor_categories:
                    factor_categories[new_name] = factor_categories.pop(item_text)
                    self.refresh_factor_tree()
                    logger.info(f"编辑分类名称: {item_text} -> {new_name}")
                else:
                    messagebox.showwarning("警告", "分类名称已存在！")
            
            elif item_values[0] == "子因子":
                # 编辑子因子名称
                parent_item = self.factor_tree.parent(item)
                category_name = self.factor_tree.item(parent_item, "text")
                
                factors = self.config_data.get("factor_categories", {}).get(category_name, [])
                existing_names = [f.get("name") for f in factors]
                
                if new_name not in existing_names:
                    for factor in factors:
                        if factor.get("name") == item_text:
                            factor["name"] = new_name
                            break
                    self.refresh_factor_tree()
                    logger.info(f"编辑子因子名称: {item_text} -> {new_name}")
                else:
                    messagebox.showwarning("警告", "子因子名称已存在！")
    
    def delete_factor_item(self):
        """删除因子项目"""
        selection = self.factor_tree.selection()
        if not selection:
            messagebox.showwarning("警告", "请先选择一个项目！")
            return
        
        item = selection[0]
        item_text = self.factor_tree.item(item, "text")
        item_values = self.factor_tree.item(item, "values")
        
        if messagebox.askyesno("确认删除", f"确定要删除 '{item_text}' 吗？", parent=self.root):
            if item_values[0] == "分类":
                # 删除分类
                self.config_data.get("factor_categories", {}).pop(item_text, None)
                logger.info(f"删除因子分类: {item_text}")
            
            elif item_values[0] == "子因子":
                # 删除子因子
                parent_item = self.factor_tree.parent(item)
                category_name = self.factor_tree.item(parent_item, "text")
                
                factors = self.config_data.get("factor_categories", {}).get(category_name, [])
                self.config_data["factor_categories"][category_name] = [
                    f for f in factors if f.get("name") != item_text
                ]
                logger.info(f"删除子因子: {category_name} -> {item_text}")
            
            self.refresh_factor_tree()
    
    def config_basic_info(self):
        """配置子因子基本信息"""
        selection = self.factor_tree.selection()
        if not selection:
            messagebox.showwarning("警告", "请先选择一个子因子！")
            return
        
        item = selection[0]
        item_values = self.factor_tree.item(item, "values")
        
        if item_values[0] != "子因子":
            messagebox.showwarning("警告", "请选择一个子因子！")
            return
        
        factor_name = self.factor_tree.item(item, "text")
        parent_item = self.factor_tree.parent(item)
        category_name = self.factor_tree.item(parent_item, "text")
        
        # 找到对应的子因子数据
        factors = self.config_data.get("factor_categories", {}).get(category_name, [])
        target_factor = None
        for factor in factors:
            if factor.get("name") == factor_name:
                target_factor = factor
                break
        
        if target_factor:
            self.open_basic_info_config_window(category_name, factor_name, target_factor)
    
    def config_table_info(self):
        """配置子因子表格信息"""
        selection = self.factor_tree.selection()
        if not selection:
            messagebox.showwarning("警告", "请先选择一个子因子！")
            return
        
        item = selection[0]
        item_values = self.factor_tree.item(item, "values")
        
        if item_values[0] != "子因子":
            messagebox.showwarning("警告", "请选择一个子因子！")
            return
        
        factor_name = self.factor_tree.item(item, "text")
        parent_item = self.factor_tree.parent(item)
        category_name = self.factor_tree.item(parent_item, "text")
        
        # 找到对应的子因子数据
        factors = self.config_data.get("factor_categories", {}).get(category_name, [])
        target_factor = None
        for factor in factors:
            if factor.get("name") == factor_name:
                target_factor = factor
                break
        
        if target_factor:
            self.open_table_info_config_window(category_name, factor_name, target_factor)
    
    def open_basic_info_config_window(self, category_name, factor_name, factor_data):
        """打开基本信息配置窗口"""
        config_window = tk.Toplevel(self.root)
        config_window.title(f"配置基本信息 - {category_name} > {factor_name}")
        config_window.geometry("500x400")
        config_window.transient(self.root)
        config_window.grab_set()
        
        # 说明标签
        ttk.Label(config_window, text="配置子因子的基本信息字段", font=('Arial', 10, 'bold')).pack(pady=10)
        
        # 字段列表
        list_frame = ttk.LabelFrame(config_window, text="基本信息字段")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        basic_info_listbox = tk.Listbox(list_frame)
        basic_info_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 加载现有字段
        basic_info = factor_data.get("basic_info", [])
        for field in basic_info:
            display_name = self.config_data.get("display_names", {}).get(field, field)
            basic_info_listbox.insert(tk.END, f"{field} ({display_name})")
        
        # 按钮框架
        button_frame = ttk.Frame(config_window)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        def add_basic_field():
            field = simpledialog.askstring("添加字段", "请输入字段名:")
            if field and field.strip():
                field = field.strip()
                if field not in basic_info:
                    basic_info.append(field)
                    display_name = self.config_data.get("display_names", {}).get(field, field)
                    basic_info_listbox.insert(tk.END, f"{field} ({display_name})")
        
        def remove_basic_field():
            selection = basic_info_listbox.curselection()
            if selection:
                index = selection[0]
                basic_info.pop(index)
                basic_info_listbox.delete(index)
        
        def save_basic_config():
            factor_data["basic_info"] = basic_info
            self.refresh_factor_tree()
            config_window.destroy()
            logger.info(f"保存基本信息配置: {category_name} > {factor_name}")
        
        ttk.Button(button_frame, text="添加字段", command=add_basic_field).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="删除字段", command=remove_basic_field).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="保存", command=save_basic_config).pack(side=tk.RIGHT, padx=2)
        ttk.Button(button_frame, text="取消", command=config_window.destroy).pack(side=tk.RIGHT, padx=2)
    
    def open_table_info_config_window(self, category_name, factor_name, factor_data):
        """打开表格信息配置窗口"""
        config_window = tk.Toplevel(self.root)
        config_window.title(f"配置表格信息 - {category_name} > {factor_name}")
        config_window.geometry("600x500")
        config_window.transient(self.root)
        config_window.grab_set()
        
        # 说明标签
        ttk.Label(config_window, text="配置子因子在不同数据层次的表格字段", font=('Arial', 10, 'bold')).pack(pady=10)
        
        # 创建选项卡
        notebook = ttk.Notebook(config_window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        table_info = factor_data.setdefault("table_info", {})
        hierarchy_names = self.config_data.get("data_hierarchy_names", {})
        
        listboxes = {}
        
        # 为每个数据层次创建选项卡
        for hierarchy_key, hierarchy_name in hierarchy_names.items():
            tab_frame = ttk.Frame(notebook)
            notebook.add(tab_frame, text=f"{hierarchy_name} ({hierarchy_key})")
            
            # 字段列表
            list_frame = ttk.LabelFrame(tab_frame, text=f"{hierarchy_name}表格字段")
            list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            listbox = tk.Listbox(list_frame)
            listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            listboxes[hierarchy_key] = listbox
            
            # 加载现有字段
            fields = table_info.get(hierarchy_key, [])
            for field in fields:
                display_name = self.config_data.get("display_names", {}).get(field, field)
                listbox.insert(tk.END, f"{field} ({display_name})")
            
            # 按钮框架
            tab_button_frame = ttk.Frame(tab_frame)
            tab_button_frame.pack(fill=tk.X, padx=5, pady=5)
            
            def make_add_func(key):
                def add_table_field():
                    field = simpledialog.askstring("添加字段", f"请输入{hierarchy_names[key]}表格字段名:")
                    if field and field.strip():
                        field = field.strip()
                        current_fields = table_info.setdefault(key, [])
                        if field not in current_fields:
                            current_fields.append(field)
                            display_name = self.config_data.get("display_names", {}).get(field, field)
                            listboxes[key].insert(tk.END, f"{field} ({display_name})")
                return add_table_field
            
            def make_remove_func(key):
                def remove_table_field():
                    selection = listboxes[key].curselection()
                    if selection:
                        index = selection[0]
                        table_info.setdefault(key, []).pop(index)
                        listboxes[key].delete(index)
                return remove_table_field
            
            ttk.Button(tab_button_frame, text="添加字段", command=make_add_func(hierarchy_key)).pack(side=tk.LEFT, padx=2)
            ttk.Button(tab_button_frame, text="删除字段", command=make_remove_func(hierarchy_key)).pack(side=tk.LEFT, padx=2)
        
        # 底部按钮
        bottom_button_frame = ttk.Frame(config_window)
        bottom_button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        def save_table_config():
            factor_data["table_info"] = table_info
            self.refresh_factor_tree()
            config_window.destroy()
            logger.info(f"保存表格信息配置: {category_name} > {factor_name}")
        
        ttk.Button(bottom_button_frame, text="保存", command=save_table_config).pack(side=tk.RIGHT, padx=2)
        ttk.Button(bottom_button_frame, text="取消", command=config_window.destroy).pack(side=tk.RIGHT, padx=2)
    
    # ==================== 显示名称操作 ====================
    
    def refresh_display_names(self):
        """刷新显示名称列表"""
        # 清空树
        for item in self.display_names_tree.get_children():
            self.display_names_tree.delete(item)
        
        # 加载显示名称
        display_names = self.config_data.get("display_names", {})
        # 确保search_var已初始化并正确获取值
        if hasattr(self, 'search_var'):
            search_text = self.search_var.get().lower()
        else:
            search_text = ""
        
        for field, field_config in sorted(display_names.items()):
            # 兼容新旧格式
            if isinstance(field_config, dict):
                display_name = field_config.get('display_name', field)
                scope = field_config.get('scope', '整单基本信息')
            else:
                # 兼容旧格式
                display_name = field_config
                scope = '整单基本信息'
            
            # 搜索过滤 - 处理scope可能是列表的情况
            scope_str = ', '.join(scope) if isinstance(scope, list) else scope
            if not search_text or search_text in field.lower() or search_text in display_name.lower() or search_text in scope_str.lower():
                # 显示三列数据：字段名、显示名称、作用范围
                item_id = self.display_names_tree.insert("", tk.END, values=(field, display_name, scope))

    
    def filter_display_names(self, event=None):
        """过滤显示名称"""
        # 直接从输入框获取文本，而不是从StringVar获取
        if hasattr(self, 'search_entry') and self.search_entry:
            search_text = self.search_entry.get()
        else:
            search_text = self.search_var.get() if hasattr(self, 'search_var') else ""
        

        
        # 直接在这里进行过滤，而不是调用refresh_display_names
        # 清空树
        for item in self.display_names_tree.get_children():
            self.display_names_tree.delete(item)
        
        # 加载显示名称
        display_names = self.config_data.get("display_names", {})

        
        # 确保搜索文本是字符串并转为小写
        search_text = search_text.lower()
        
        # 计数器，用于记录匹配的项目数
        match_count = 0
        
        for field, field_config in sorted(display_names.items()):
            # 兼容新旧格式
            if isinstance(field_config, dict):
                display_name = field_config.get('display_name', field)
                scope = field_config.get('scope', '整单基本信息')
            else:
                # 兼容旧格式
                display_name = field_config
                scope = '整单基本信息'
            
            # 搜索过滤 - 处理scope可能是列表的情况
            scope_str = ', '.join(scope) if isinstance(scope, list) else scope
            if not search_text or search_text in field.lower() or search_text in display_name.lower() or search_text in scope_str.lower():
                # 显示三列数据：字段名、显示名称、作用范围
                item_id = self.display_names_tree.insert("", tk.END, values=(field, display_name, scope))
                match_count += 1
        

    
    def add_display_name(self):
        """添加显示名称"""
        # 创建添加字段的弹窗
        dialog = tk.Toplevel(self.root)
        dialog.title("添加字段配置")
        dialog.geometry("450x350")  # 增加高度确保按钮显示
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 居中显示
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (450 // 2)
        y = (dialog.winfo_screenheight() // 2) - (350 // 2)
        dialog.geometry(f"450x350+{x}+{y}")
        
        # 主框架
        main_frame = ttk.Frame(dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_label = ttk.Label(main_frame, text="添加新字段配置", font=('Arial', 12, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # 字段名输入框
        field_frame = ttk.Frame(main_frame)
        field_frame.pack(fill=tk.X, pady=(0, 15))
        ttk.Label(field_frame, text="字段名:", width=12, anchor='w').pack(side=tk.LEFT)
        field_var = tk.StringVar()
        field_entry = ttk.Entry(field_frame, textvariable=field_var, width=35)
        field_entry.pack(side=tk.LEFT, padx=(10, 0))
        field_entry.focus()
        
        # 添加调试日志
        logger.info(f"添加字段配置 - 初始化字段名输入框")
        
        # 显示名称输入框
        display_frame = ttk.Frame(main_frame)
        display_frame.pack(fill=tk.X, pady=(0, 15))
        ttk.Label(display_frame, text="显示名称:", width=12, anchor='w').pack(side=tk.LEFT)
        display_name_var = tk.StringVar()
        display_name_entry = ttk.Entry(display_frame, textvariable=display_name_var, width=35)
        display_name_entry.pack(side=tk.LEFT, padx=(10, 0))
        
        # 添加调试日志
        logger.info(f"添加字段配置 - 初始化显示名称输入框")
        
        # 作用范围多选复选框
        scope_frame = ttk.Frame(main_frame)
        scope_frame.pack(fill=tk.X, pady=(0, 20))
        ttk.Label(scope_frame, text="作用范围:", width=12, anchor='w').pack(side=tk.LEFT)
        
        # 创建复选框框架
        scope_checkboxes_frame = ttk.Frame(scope_frame)
        scope_checkboxes_frame.pack(side=tk.LEFT, padx=(10, 0), fill=tk.X, expand=True)
        
        # 添加复选框选项 - 包含三个选项
        scope_options = ["整单基本信息", "子因子基本信息", "子因子表格"]
        scope_vars = {}  # 用于存储复选框变量
        scope_checkboxes = {}  # 用于存储复选框对象
        
        for option in scope_options:
            var = tk.BooleanVar(value=False)
            scope_vars[option] = var
            cb = ttk.Checkbutton(scope_checkboxes_frame, text=option, variable=var)
            cb.pack(anchor=tk.W, pady=2)
            scope_checkboxes[option] = cb
        
        # 默认选中第一项
        scope_vars[scope_options[0]].set(True)
        
        # 强制刷新所有复选框状态，避免alternate状态
        for option, cb in scope_checkboxes.items():
            cb.update_idletasks()
            if scope_vars[option].get():
                cb.state(['!alternate', 'selected'])
            else:
                cb.state(['!alternate', '!selected'])
        
        # 添加调试日志
        logger.info(f"添加字段配置 - 初始化作用范围选项: {scope_options}, 默认选中: ['整单基本信息']")
        logger.info(f"[调试] 添加字段配置 - 复选框变量值: {[(option, var.get()) for option, var in scope_vars.items()]}")
        logger.info(f"[修复] 复选框现在只有两种状态：选中(True)和未选中(False)，不再有三态问题")
        
        # 分隔线
        separator = ttk.Separator(main_frame, orient='horizontal')
        separator.pack(fill=tk.X, pady=(10, 20))
        
        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))  # 添加底部边距
        
        def save_field():
            # 直接从输入框获取值，而不是从StringVar获取
            field = field_entry.get().strip()
            display_name = display_name_entry.get().strip()
            
            # 添加调试日志
            logger.info(f"添加字段配置 - 保存时获取值 - 字段名: '{field}', 显示名称: '{display_name}'")
            
            # 获取复选框选中的值
            selected_scopes = [option for option, var in scope_vars.items() if var.get()]
            
            if not field:
                messagebox.showerror("输入错误", "请输入字段名", parent=dialog)
                field_entry.focus()
                return
            if not display_name:
                messagebox.showerror("输入错误", "请输入显示名称", parent=dialog)
                display_name_entry.focus()
                return
            if not selected_scopes:
                messagebox.showerror("输入错误", "请至少选择一个作用范围", parent=dialog)
                return
            
            # 检查字段名是否已存在
            if field in self.config_data.get("display_names", {}):
                messagebox.showerror("字段重复", f"字段名 '{field}' 已存在，请使用其他名称", parent=dialog)
                field_entry.focus()
                field_entry.select_range(0, tk.END)
                return
            
            # 保存到配置
            self.config_data.setdefault("display_names", {})[field] = {
                "display_name": display_name,
                "scope": selected_scopes  # 保存为列表
            }
            

            
            # 保存配置到文件
            try:
                with open(self.config_path, 'w', encoding='utf-8') as f:
                    json.dump(self.config_data, f, ensure_ascii=False, indent=2)

            except Exception as e:
                logger.error(f"保存配置文件失败: {e}")
                messagebox.showerror("错误", f"保存配置文件失败: {e}", parent=dialog)
                return
                
            self.refresh_all_ui()  # 刷新所有相关页面，确保实时更新
            logger.info(f"添加字段配置: {field} -> {display_name} ({selected_scopes})")
            messagebox.showinfo("成功", f"字段 '{field}' 添加成功！", parent=dialog)
            dialog.destroy()
        
        # 右对齐按钮
        button_right_frame = ttk.Frame(button_frame)
        button_right_frame.pack(side=tk.RIGHT)
        
        ttk.Button(button_right_frame, text="取消", command=dialog.destroy).pack(side=tk.LEFT, padx=(0, 10))
        save_btn = ttk.Button(button_right_frame, text="保存", command=save_field)
        save_btn.pack(side=tk.LEFT)
        
        # 绑定回车键和ESC键
        dialog.bind('<Return>', lambda e: save_field())
        dialog.bind('<Escape>', lambda e: dialog.destroy())
        
        # 设置默认按钮样式
        save_btn.focus()
    
    def edit_display_name(self, event=None):
        """编辑显示名称"""
        selection = self.display_names_tree.selection()
        if selection:
            item = selection[0]
            # 从三列数据获取字段信息
            values = self.display_names_tree.item(item, "values")
            # 添加调试日志
            logger.info(f"编辑字段配置 - 选中项数据: {values}")
            if len(values) >= 3:
                field, old_display_name, old_scope = values[0], values[1], values[2]
                logger.info(f"编辑字段配置 - 字段: {field}, 旧显示名称: '{old_display_name}', 旧作用范围: '{old_scope}'")
            else:
                return            
            # 创建编辑弹窗
            dialog = tk.Toplevel(self.root)
            dialog.title("编辑字段配置")
            dialog.geometry("450x350")  # 增加高度确保按钮显示
            dialog.resizable(False, False)
            dialog.transient(self.root)
            dialog.grab_set()
            
            # 居中显示
            dialog.update_idletasks()
            x = (dialog.winfo_screenwidth() // 2) - (450 // 2)
            y = (dialog.winfo_screenheight() // 2) - (350 // 2)
            dialog.geometry(f"450x350+{x}+{y}")
            
            # 主框架
            main_frame = ttk.Frame(dialog, padding="20")
            main_frame.pack(fill=tk.BOTH, expand=True)
            
            # 标题
            title_label = ttk.Label(main_frame, text="编辑字段配置", font=('Arial', 12, 'bold'))
            title_label.pack(pady=(0, 20))
            
            # 字段名（只读）
            field_frame = ttk.Frame(main_frame)
            field_frame.pack(fill=tk.X, pady=(0, 15))
            ttk.Label(field_frame, text="字段名:", width=12, anchor='w').pack(side=tk.LEFT)
            field_label = ttk.Label(field_frame, text=field, font=('Arial', 10, 'bold'), 
                                   foreground='#666666', background='#f0f0f0', 
                                   relief='sunken', padding=(5, 2))
            field_label.pack(side=tk.LEFT, padx=(10, 0), fill=tk.X, expand=True)
            
            # 显示名称输入框
            display_frame = ttk.Frame(main_frame)
            display_frame.pack(fill=tk.X, pady=(0, 15))
            ttk.Label(display_frame, text="显示名称:", width=12, anchor='w').pack(side=tk.LEFT)
            display_name_var = tk.StringVar(value=old_display_name)
            display_name_entry = ttk.Entry(display_frame, textvariable=display_name_var, width=35)
            display_name_entry.pack(side=tk.LEFT, padx=(10, 0))
            # 确保Entry显示初始值（参考作用范围的做法）
            display_name_entry.insert(0, old_display_name)
            display_name_entry.delete(0, tk.END)
            display_name_entry.insert(0, old_display_name)
            display_name_entry.focus()
            display_name_entry.select_range(0, tk.END)
            

            
            # 作用范围多选复选框
            scope_frame = ttk.Frame(main_frame)
            scope_frame.pack(fill=tk.X, pady=(0, 20))
            ttk.Label(scope_frame, text="作用范围:", width=12, anchor='w').pack(side=tk.LEFT)
            
            # 创建复选框框架
            scope_checkboxes_frame = ttk.Frame(scope_frame)
            scope_checkboxes_frame.pack(side=tk.LEFT, padx=(10, 0), fill=tk.X, expand=True)
            
            # 添加复选框选项
            scope_options = ["整单基本信息", "子因子基本信息", "子因子表格"]
            scope_vars = {}  # 用于存储复选框变量
            scope_checkboxes = {}  # 用于存储复选框对象
            
            # 如果old_scope是字符串，转换为列表
            old_scopes = []
            if isinstance(old_scope, str):
                # 处理可能的逗号分隔或空格分隔字符串
                if ',' in old_scope:
                    old_scopes = [s.strip() for s in old_scope.split(',')]
                elif ' ' in old_scope:
                    # 处理空格分隔的字符串（如'整单基本信息 子因子基本信息'）
                    old_scopes = [s.strip() for s in old_scope.split() if s.strip()]
                else:
                    old_scopes = [old_scope.strip()]
            elif isinstance(old_scope, list):
                old_scopes = old_scope
            
            # 添加调试日志
            logger.info(f"编辑字段配置 - 原始作用范围: {old_scope}, 类型: {type(old_scope)}")
            logger.info(f"编辑字段配置 - 解析后作用范围列表: {old_scopes}")
            
            # 确保复选框正确初始化
            for option in scope_options:
                # 直接使用字符串比较，不区分列表或字符串格式
                is_selected = False
                
                # 检查选项是否在作用范围列表中
                if isinstance(old_scope, str) and old_scope == option:
                    is_selected = True
                elif isinstance(old_scope, list) and option in old_scope:
                    is_selected = True
                elif option in old_scopes:
                    is_selected = True
                
                logger.info(f"编辑字段配置 - 复选框 '{option}' 初始状态: {is_selected}")
                
                var = tk.BooleanVar(value=is_selected)
                scope_vars[option] = var
                cb = ttk.Checkbutton(scope_checkboxes_frame, text=option, variable=var)
                cb.pack(anchor=tk.W, pady=2)
                scope_checkboxes[option] = cb  # 存储复选框对象
                
                # 强制刷新复选框状态，避免alternate状态
                cb.update_idletasks()
                if is_selected:
                    cb.state(['!alternate', 'selected'])
                else:
                    cb.state(['!alternate', '!selected'])
                
                logger.info(f"编辑字段配置 - 复选框 '{option}' BooleanVar值: {var.get()}, 组件状态: {cb.state()}")
                

            
            # 分隔线
            separator = ttk.Separator(main_frame, orient='horizontal')
            separator.pack(fill=tk.X, pady=(10, 20))
            
            # 按钮框架
            button_frame = ttk.Frame(main_frame)
            button_frame.pack(fill=tk.X)
            
            def save_changes():
                # 直接从Entry获取值
                new_display_name = display_name_entry.get().strip()
                
                # 获取复选框选中的值
                new_scopes = []
                
                # 通过BooleanVar获取复选框的选中状态
                for option, var in scope_vars.items():
                    is_selected = var.get()
                    logger.info(f"[调试] 复选框 '{option}' 变量值: {is_selected}")
                    if is_selected:
                        new_scopes.append(option)
                

                logger.info(f"保存字段配置 - 字段: {field}, 新显示名称: '{new_display_name}', 新作用范围: {new_scopes}")
                
                if not new_display_name:
                    messagebox.showerror("输入错误", "请输入显示名称", parent=dialog)
                    display_name_entry.focus()
                    return
                
                if not new_scopes:
                    messagebox.showerror("输入错误", "请至少选择一个作用范围", parent=dialog)
                    return
                
                # 获取原有作用范围
                old_config = self.config_data.get("display_names", {}).get(field, {})
                old_scope = old_config.get("scope", [])
                if isinstance(old_scope, str):
                    old_scope = [old_scope]
                
                # 检查作用范围是否发生变化
                scope_changed = set(old_scope) != set(new_scopes)
                cleaned_references = []
                
                if scope_changed:
                    # 清理不符合新作用范围的因子配置
                    cleaned_references = self.clean_factor_configs_by_scope(field, new_scopes)
                    
                    if cleaned_references:
                        # 显示清理确认对话框
                        clean_message = f"作用范围已变更，以下配置项将被清理：\n" + "\n".join([f"• {ref}" for ref in cleaned_references])
                        clean_message += "\n\n是否继续保存？"
                        
                        if not messagebox.askyesno("确认清理", clean_message, parent=dialog):
                            return
                
                # 保存到配置
                # 检查是否只有一个作用范围，如果是则保存为字符串，否则保存为列表
                if len(new_scopes) == 1:
                    scope_value = new_scopes[0]  # 保存为字符串
                else:
                    scope_value = new_scopes  # 保存为列表
                
                # 更新配置数据
                self.config_data.setdefault("display_names", {})[field] = {
                    "display_name": new_display_name,
                    "scope": scope_value
                }
                
                if cleaned_references:
                    logger.info(f"作用范围变更清理的配置: {cleaned_references}")
                

                
                # 直接保存配置到文件，避免重复弹窗
                try:

                    
                    # 保存配置文件
                    with open(self.config_path, 'w', encoding='utf-8') as f:
                        json.dump(self.config_data, f, ensure_ascii=False, indent=2)
                    
                    # 验证配置文件是否成功保存
                    if os.path.exists(self.config_path):
                        file_size = os.path.getsize(self.config_path)

                        
                        # 读取保存后的文件内容进行验证
                        try:
                            with open(self.config_path, 'r', encoding='utf-8') as f:
                                saved_data = json.load(f)
                                saved_field_config = saved_data.get("display_names", {}).get(field, {})

                        except Exception as e:
                            logger.error(f"读取保存后的配置文件失败: {e}")
                    else:
                        logger.error(f"配置文件保存后不存在: {self.config_path}")
                except Exception as e:
                    logger.error(f"保存配置文件失败: {e}")
                    messagebox.showerror("错误", f"保存配置文件失败: {e}", parent=dialog)
                    return
                
                # 重新加载配置数据并刷新所有界面
                self.load_config()
                self.refresh_all_ui()  # 刷新所有相关页面，确保实时更新
                # 使用实际保存的值而不是重新加载的值来记录日志
                logger.info(f"编辑字段配置: {field} -> {new_display_name} ({new_scopes})")
                messagebox.showinfo("成功", f"字段 '{field}' 更新成功！", parent=dialog)
                dialog.destroy()
            
            # 右对齐按钮
            button_right_frame = ttk.Frame(button_frame)
            button_right_frame.pack(side=tk.RIGHT)
            
            ttk.Button(button_right_frame, text="取消", command=dialog.destroy).pack(side=tk.LEFT, padx=(0, 10))
            save_btn = ttk.Button(button_right_frame, text="保存", command=save_changes)
            save_btn.pack(side=tk.LEFT)
            
            # 绑定回车键和ESC键
            dialog.bind('<Return>', lambda e: save_changes())
            dialog.bind('<Escape>', lambda e: dialog.destroy())
            
            # 设置默认按钮样式
            save_btn.focus()
    
    def find_field_references(self, field_name):
        """查找字段在配置中的所有引用"""
        references = []
        
        # 检查document_info_fields
        if field_name in self.config_data.get("document_info_fields", []):
            references.append("整单基本信息字段列表")
        
        # 检查factor_categories中的引用
        factor_categories = self.config_data.get("factor_categories", {})
        for category_name, factors in factor_categories.items():
            for factor in factors:
                # 检查basic_info
                if field_name in factor.get("basic_info", []):
                    references.append(f"因子分类 '{category_name}' - 子因子 '{factor['name']}' 的基本信息")
                
                # 检查table_info
                table_info = factor.get("table_info", {})
                for level, fields in table_info.items():
                    if field_name in fields:
                        references.append(f"因子分类 '{category_name}' - 子因子 '{factor['name']}' 的 {level} 层表格信息")
        
        return references
    
    def cascade_delete_field(self, field_name):
        """级联删除字段的所有引用"""
        deleted_references = []
        
        # 从document_info_fields中删除
        document_fields = self.config_data.get("document_info_fields", [])
        if field_name in document_fields:
            document_fields.remove(field_name)
            deleted_references.append("整单基本信息字段列表")
        
        # 从factor_categories中删除
        factor_categories = self.config_data.get("factor_categories", {})
        for category_name, factors in factor_categories.items():
            for factor in factors:
                # 从basic_info中删除
                basic_info = factor.get("basic_info", [])
                if field_name in basic_info:
                    basic_info.remove(field_name)
                    deleted_references.append(f"因子分类 '{category_name}' - 子因子 '{factor['name']}' 的基本信息")
                
                # 从table_info中删除
                table_info = factor.get("table_info", {})
                for level, fields in table_info.items():
                    if field_name in fields:
                        fields.remove(field_name)
                        deleted_references.append(f"因子分类 '{category_name}' - 子因子 '{factor['name']}' 的 {level} 层表格信息")
        
        return deleted_references
    
    def clean_factor_configs_by_scope(self, field_name, new_scopes):
        """根据新的作用范围清理不符合的因子配置"""
        cleaned_references = []
        
        # 将作用范围转换为列表格式
        if isinstance(new_scopes, str):
            new_scopes = [new_scopes]
        
        # 定义作用范围与因子配置位置的映射
        scope_mapping = {
            "整单基本信息": "document_info_fields",
            "子因子基本信息": "basic_info",
            "子因子表格": "table_info"
        }
        
        # 检查document_info_fields
        if "整单基本信息" not in new_scopes:
            document_fields = self.config_data.get("document_info_fields", [])
            if field_name in document_fields:
                document_fields.remove(field_name)
                cleaned_references.append("整单基本信息字段列表")
        
        # 检查factor_categories中的配置
        factor_categories = self.config_data.get("factor_categories", {})
        for category_name, factors in factor_categories.items():
            for factor in factors:
                # 检查basic_info
                if "子因子基本信息" not in new_scopes:
                    basic_info = factor.get("basic_info", [])
                    if field_name in basic_info:
                        basic_info.remove(field_name)
                        cleaned_references.append(f"因子分类 '{category_name}' - 子因子 '{factor['name']}' 的基本信息")
                
                # 检查table_info
                if "子因子表格" not in new_scopes:
                    table_info = factor.get("table_info", {})
                    for level, fields in table_info.items():
                        if field_name in fields:
                            fields.remove(field_name)
                            cleaned_references.append(f"因子分类 '{category_name}' - 子因子 '{factor['name']}' 的 {level} 层表格信息")
        
        return cleaned_references
    
    def delete_display_name(self):
        """删除显示名称（带级联清理）"""
        selection = self.display_names_tree.selection()
        if selection:
            item = selection[0]
            # 从三列数据获取字段信息
            values = self.display_names_tree.item(item, "values")
            field, display_name, scope = values
            
            # 查找字段引用
            references = self.find_field_references(field)
            
            # 构建确认消息
            confirm_message = f"确定要删除字段 '{display_name}' ({field}) 吗？"
            if references:
                confirm_message += "\n\n以下配置项也将被删除：\n" + "\n".join([f"• {ref}" for ref in references])
            
            if messagebox.askyesno("确认删除", confirm_message, parent=self.root):
                # 记住当前选中项的索引，用于后续恢复焦点
                current_index = self.display_names_tree.index(item)
                
                # 级联删除字段引用
                deleted_references = self.cascade_delete_field(field)
                
                # 删除display_names中的字段
                self.config_data.get("display_names", {}).pop(field, None)
                
                logger.info(f"删除字段配置: {field}")
                if deleted_references:
                    logger.info(f"级联删除的引用: {deleted_references}")
                
                # 保存配置到文件，不显示成功弹窗
                try:
                    self.save_config(show_success_message=False)
                    logger.info(f"成功保存配置到文件")
                except Exception as e:
                    logger.error(f"保存配置到文件失败: {str(e)}")
                    messagebox.showerror("保存失败", f"保存配置到文件失败: {str(e)}", parent=self.root)
                
                self.refresh_all_ui()  # 刷新所有相关页面，确保实时更新
                
                # 恢复焦点到删除项后的位置或最后一项
                self.root.update()  # 确保UI已更新
                items = self.display_names_tree.get_children()
                if items:
                    # 如果删除的是最后一项，选择新的最后一项
                    if current_index >= len(items):
                        current_index = len(items) - 1
                    
                    # 选择并聚焦到相应项
                    item_to_select = items[current_index]
                    self.display_names_tree.selection_set(item_to_select)
                    self.display_names_tree.focus_set()
                    self.display_names_tree.focus(item_to_select)
                    self.display_names_tree.see(item_to_select)
                    
                    # 将窗口提到前台
                    self.root.lift()
                    self.root.focus_force()
    
    def batch_import_display_names(self):
        """批量导入显示名称"""
        import_text = simpledialog.askstring("批量导入", 
                                            "请输入字段映射 (格式: 字段名=显示名称，每行一个):")
        if import_text:
            lines = import_text.strip().split('\n')
            imported_count = 0
            
            for line in lines:
                line = line.strip()
                if '=' in line:
                    field, display_name = line.split('=', 1)
                    field = field.strip()
                    display_name = display_name.strip()
                    
                    if field and display_name:
                        self.config_data.setdefault("display_names", {})[field] = display_name
                        imported_count += 1
            
            if imported_count > 0:
                self.refresh_display_names()
                messagebox.showinfo("导入完成", f"成功导入 {imported_count} 个字段显示名称")
                logger.info(f"批量导入显示名称: {imported_count} 个")
    
    # ==================== 配置管理操作 ====================
    
    def save_all_config(self):
        """保存所有配置"""
        try:
            # 保存数据层次配置
            hierarchy_names = {}
            for key, entry in self.hierarchy_name_entries.items():
                hierarchy_names[key] = entry.get().strip()
            self.config_data["data_hierarchy_names"] = hierarchy_names
            
            # 保存启用层次配置
            enabled_levels = []
            for key, var in self.hierarchy_vars.items():
                if var.get():
                    enabled_levels.append(key)
            self.config_data["enabled_hierarchy_levels"] = enabled_levels
            
            # 保存默认层次
            self.config_data["default_hierarchy_level"] = self.default_hierarchy_var.get()
            
            # 保存配置文件
            self.save_config()
            
            # 确保配置管理窗口保持焦点，避免跑到主窗口后面
            if self.root:
                self.root.lift()
                self.root.focus_force()
                self.root.attributes('-topmost', True)
                self.root.after(100, lambda: self.root.attributes('-topmost', False))
            
        except Exception as e:
            logger.error(f"保存配置失败: {e}")
            messagebox.showerror("错误", f"保存配置失败: {e}")
            # 即使出错也要确保窗口焦点
            if self.root:
                self.root.lift()
                self.root.focus_force()
    
    def reset_config(self):
        """重置配置"""
        if messagebox.askyesno("确认重置", "确定要重置所有配置吗？这将清除所有自定义设置！"):
            self.config_data = self.get_default_config()
            self.refresh_all_ui()
            logger.info("配置已重置")
    
    def export_config(self):
        """导出配置"""
        from tkinter import filedialog
        
        file_path = filedialog.asksaveasfilename(
            title="导出配置",
            defaultextension=".json",
            filetypes=[("JSON文件", "*.json"), ("所有文件", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(self.config_data, f, ensure_ascii=False, indent=2)
                messagebox.showinfo("成功", f"配置已导出到: {file_path}")
                logger.info(f"配置已导出: {file_path}")
            except Exception as e:
                messagebox.showerror("错误", f"导出配置失败: {e}")
    
    def import_config(self):
        """导入配置"""
        from tkinter import filedialog
        
        file_path = filedialog.askopenfilename(
            title="导入配置",
            filetypes=[("JSON文件", "*.json"), ("所有文件", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    imported_config = json.load(f)
                
                if messagebox.askyesno("确认导入", "确定要导入配置吗？这将覆盖当前配置！"):
                    self.config_data = imported_config
                    self.refresh_all_ui()
                    messagebox.showinfo("成功", "配置导入成功！")
                    logger.info(f"配置已导入: {file_path}")
            
            except Exception as e:
                messagebox.showerror("错误", f"导入配置失败: {e}")
    
    def refresh_all_ui(self):
        """刷新所有UI"""
        try:
            # 检查UI组件是否存在，避免在组件未初始化时调用
            if hasattr(self, 'available_fields_listbox') and self.available_fields_listbox:
                self.refresh_document_fields()
            
            if hasattr(self, 'factor_tree') and self.factor_tree:
                self.refresh_factor_tree()
            
            if hasattr(self, 'display_names_tree') and self.display_names_tree:
                self.refresh_display_names()
            
            # 刷新数据层次配置
            if hasattr(self, 'hierarchy_name_entries') and self.hierarchy_name_entries:
                hierarchy_names = self.config_data.get("data_hierarchy_names", {})
                for key, entry in self.hierarchy_name_entries.items():
                    if entry:  # 确保entry不为None
                        entry.delete(0, tk.END)
                        entry.insert(0, hierarchy_names.get(key, ""))
            
            if hasattr(self, 'hierarchy_vars') and self.hierarchy_vars:
                enabled_levels = self.config_data.get("enabled_hierarchy_levels", [])
                for key, var in self.hierarchy_vars.items():
                    if var:  # 确保var不为None
                        var.set(key in enabled_levels)
            
            if hasattr(self, 'default_hierarchy_var') and self.default_hierarchy_var:
                self.default_hierarchy_var.set(self.config_data.get("default_hierarchy_level", "part"))
            
            # 刷新主窗口页面字段显示
            if self.app_controller and hasattr(self.app_controller, 'refresh_view'):
                logger.info("正在刷新主窗口页面字段显示...")
                self.app_controller.refresh_view()
            
        except Exception as e:
            logger.error(f"刷新UI失败: {e}")
    
    def sync_main_app_selection_state(self):
        """同步主应用的当前选择状态到配置管理器"""
        try:
            # 检查必要的UI组件是否已创建
            if not hasattr(self, 'category_treeview') or not hasattr(self, 'subfactor_scrollable_frame'):
                logger.info("🔍 UI组件尚未创建完成，延迟同步")
                # 延迟执行同步
                if hasattr(self, 'root') and self.root:
                    self.root.after(500, self.sync_main_app_selection_state)
                return
            
            if self.app_controller and hasattr(self.app_controller, 'view'):
                main_view = self.app_controller.view
                if hasattr(main_view, 'factor_view'):
                    factor_view = main_view.factor_view
                    
                    # 获取主应用当前选择的分类
                    current_category = factor_view.category_var.get()
                    logger.info(f"🔍 从主应用获取的分类选择状态: '{current_category}'")
                    
                    if current_category and hasattr(self, 'category_treeview'):
                        # 在配置管理器中选择对应的分类
                        categories = list(self.config_data.get("factor_categories", {}).keys())
                        if current_category in categories:
                            # 设置同步标志，防止事件处理中的递归调用
                            self._syncing_from_main_app = True
                            
                            # 临时解绑事件避免触发递归
                            self.category_treeview.unbind('<<TreeviewSelect>>')
                            
                            
                            # 直接刷新子因子列表，不触发事件
                            self.refresh_subfactors(current_category)
                            
                            # 重新绑定事件
                            self.category_treeview.bind('<<TreeviewSelect>>', self.on_category_select)
                            
                            logger.info(f"🔍 已同步分类选择状态到配置管理器: {current_category}")
                            
                            # 获取主应用当前选择的子因子
                            current_subfactor = factor_view.subfactor_var.get()
                            logger.info(f"🔍 从主应用获取的子因子选择状态: '{current_subfactor}'")
                            
                            if current_subfactor:
                                # 在配置管理器中选择对应的子因子
                                if current_subfactor in self.subfactor_radios:
                                    # 设置单选按钮的值
                                    old_value = self.subfactor_var.get()
                                    self.subfactor_var.set(current_subfactor)
                                    new_value = self.subfactor_var.get()
                                    logger.info(f"🔍 子因子变量设置: {old_value} -> {new_value}")
                                    
                                    # 强制更新单选按钮的显示状态
                                    radio_button = self.subfactor_radios[current_subfactor]
                                    radio_button.invoke()
                                    logger.info(f"🔍 已强制更新单选按钮显示状态: {current_subfactor}")
                                    
                                    # 直接加载子因子配置，不触发事件
                                    self.load_subfactor_config(current_category, current_subfactor)
                                    
                                    logger.info(f"🔍 已同步子因子选择状态到配置管理器: {current_subfactor}")
                                else:
                                    logger.warning(f"🔍 未找到子因子单选按钮: {current_subfactor}, 可用按钮: {list(self.subfactor_radios.keys())}")
                            
                            # 清除同步标志
                            self._syncing_from_main_app = False
                        else:
                            logger.info(f"🔍 主应用选择的分类 '{current_category}' 在配置中不存在")
                            # 清除同步标志
                            self._syncing_from_main_app = False
                    else:
                        logger.info("🔍 主应用未选择分类或配置管理器分类列表未初始化")
                        # 清除同步标志
                        self._syncing_from_main_app = False
                else:
                    logger.info("🔍 主应用视图中没有factor_view组件")
                    # 清除同步标志
                    self._syncing_from_main_app = False
            else:
                logger.info("🔍 没有可用的主应用控制器引用")
                # 清除同步标志
                self._syncing_from_main_app = False
        except Exception as e:
            logger.error(f"同步主应用选择状态失败: {e}")
            # 清除同步标志
            self._syncing_from_main_app = False
    
    def close_config_window(self):
        """关闭配置窗口"""
        if self.root:
            self.root.destroy()
            self.root = None
            # 重置内容加载标志，确保下次打开时重新创建内容
            self.display_names_content_loaded = False
            logger.info("配置管理窗口已关闭")


def main():
    """主函数 - 用于测试"""
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    
    config_manager = ConfigManagerUI()
    config_manager.open_config_window()
    
    root.mainloop()


if __name__ == "__main__":
    main()
