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

# 配置日志 - 使用应用统一的日志配置
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')  # 注释掉避免冲突
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
    
    def save_config(self):
        """保存配置文件"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config_data, f, ensure_ascii=False, indent=2)
            logger.info(f"配置文件保存成功: {self.config_path}")
            messagebox.showinfo("成功", "配置保存成功！")
        except Exception as e:
            logger.error(f"保存配置文件失败: {e}")
            messagebox.showerror("错误", f"保存配置文件失败: {e}")
    
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
    
    def verify_password(self):
        """验证密码"""
        if self.password_verified:
            return True
        
        password = simpledialog.askstring("密码验证", "请输入密码访问字段配置页面:", show='*')
        if password == "12345678":  # 可以从配置文件读取或使用更安全的方式
            self.password_verified = True
            return True
        else:
            messagebox.showerror("错误", "密码错误！", parent=self.root)
            return False
    
    def on_tab_changed(self, event):
        """标签切换事件处理"""
        selected_tab = self.notebook.select()
        tab_text = self.notebook.tab(selected_tab, "text")
        
        # 如果切换到字段配置页面，进行密码验证
        if tab_text == "字段配置":
            if not self.verify_password():
                # 密码验证失败，切换回第一个标签
                self.notebook.select(0)
                return
            
            # 密码验证成功，确保字段配置页面内容已加载
            self.ensure_display_names_content()
    
    def open_config_window(self):
        """打开配置管理窗口"""
        if self.root is not None:
            self.root.lift()
            return
        
        self.root = tk.Tk()
        self.root.title("业务配置管理")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        self.root.protocol("WM_DELETE_WINDOW", self.close_config_window)
        
        # 确保窗口居中显示
        self.root.update_idletasks()
        width = 1000
        height = 700
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
        # 创建主框架
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建选项卡
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # 绑定标签切换事件
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)
        
        # 创建各个配置页面
        self.create_document_info_tab()
        self.create_hierarchy_tab()
        self.create_factor_categories_tab()
        self.create_display_names_tab()
        
        # 创建底部按钮
        self.create_bottom_buttons(main_frame)
        
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
        
        # 左侧：当前字段列表
        left_frame = ttk.LabelFrame(main_container, text="当前字段列表")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # 字段列表框
        listbox_frame = ttk.Frame(left_frame)
        listbox_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.document_fields_listbox = tk.Listbox(listbox_frame, selectmode=tk.SINGLE)
        scrollbar_y = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=self.document_fields_listbox.yview)
        self.document_fields_listbox.configure(yscrollcommand=scrollbar_y.set)
        
        self.document_fields_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 右侧：操作按钮
        right_frame = ttk.Frame(main_container)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0))
        
        # 按钮组
        ttk.Button(right_frame, text="添加字段", command=self.add_document_field).pack(pady=2, fill=tk.X)
        ttk.Button(right_frame, text="删除字段", command=self.remove_document_field).pack(pady=2, fill=tk.X)
        ttk.Button(right_frame, text="上移", command=lambda: self.move_document_field(-1)).pack(pady=2, fill=tk.X)
        ttk.Button(right_frame, text="下移", command=lambda: self.move_document_field(1)).pack(pady=2, fill=tk.X)
        ttk.Button(right_frame, text="编辑字段", command=self.edit_document_field).pack(pady=2, fill=tk.X)
        
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
        tab_frame = ttk.Frame(self.notebook)
        self.notebook.add(tab_frame, text="因子分类配置")
        
        # 说明标签
        info_label = ttk.Label(tab_frame, text="配置因子分类及其子因子信息", font=('Arial', 10, 'bold'))
        info_label.pack(pady=(10, 5))
        
        # 主容器
        main_container = ttk.Frame(tab_frame)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 左侧：因子树
        left_frame = ttk.LabelFrame(main_container, text="因子分类树")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # 创建树形控件
        tree_frame = ttk.Frame(left_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.factor_tree = ttk.Treeview(tree_frame, columns=("type", "info"), show="tree headings")
        self.factor_tree.heading("#0", text="名称")
        self.factor_tree.heading("type", text="类型")
        self.factor_tree.heading("info", text="配置信息")
        
        tree_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.factor_tree.yview)
        self.factor_tree.configure(yscrollcommand=tree_scrollbar.set)
        
        self.factor_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 右侧：操作按钮
        right_frame = ttk.Frame(main_container)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0))
        
        ttk.Button(right_frame, text="添加分类", command=self.add_factor_category).pack(pady=2, fill=tk.X)
        ttk.Button(right_frame, text="添加子因子", command=self.add_sub_factor).pack(pady=2, fill=tk.X)
        ttk.Button(right_frame, text="编辑选中项", command=self.edit_factor_item).pack(pady=2, fill=tk.X)
        ttk.Button(right_frame, text="删除选中项", command=self.delete_factor_item).pack(pady=2, fill=tk.X)
        ttk.Separator(right_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)
        ttk.Button(right_frame, text="配置基本信息", command=self.config_basic_info).pack(pady=2, fill=tk.X)
        ttk.Button(right_frame, text="配置表格信息", command=self.config_table_info).pack(pady=2, fill=tk.X)
        
        # 加载因子数据
        self.refresh_factor_tree()
    
    def create_display_names_tab(self):
        """创建字段配置页面"""
        self.display_names_tab_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.display_names_tab_frame, text="字段配置")
        
        # 初始显示提示信息，内容将在首次访问时加载
        self.display_names_placeholder = ttk.Label(self.display_names_tab_frame, 
                                                  text="请点击此标签页进行密码验证后访问字段配置", 
                                                  font=('Arial', 12), foreground='gray')
        self.display_names_placeholder.pack(expand=True)
        
        # 标记内容是否已加载
        self.display_names_content_loaded = False
        
    def ensure_display_names_content(self):
        """确保字段配置页面内容已加载"""
        if self.display_names_content_loaded:
            return
        
        # 移除占位符
        self.display_names_placeholder.destroy()
        
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
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        search_entry.bind('<KeyRelease>', self.filter_display_names)
        
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
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(button_frame, text="保存配置", command=self.save_all_config).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(button_frame, text="重置配置", command=self.reset_config).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(button_frame, text="导出配置", command=self.export_config).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(button_frame, text="导入配置", command=self.import_config).pack(side=tk.RIGHT, padx=(5, 0))
    
    # ==================== 整单基本信息字段操作 ====================
    
    def refresh_document_fields(self):
        """刷新整单基本信息字段列表"""
        self.document_fields_listbox.delete(0, tk.END)
        fields = self.config_data.get("document_info_fields", [])
        display_names = self.config_data.get("display_names", {})
        
        for field in fields:
            field_config = display_names.get(field, field)
            if isinstance(field_config, dict):
                display_name = field_config.get('display_name', field)
            else:
                # 兼容旧格式
                display_name = field_config
            
            self.document_fields_listbox.insert(tk.END, display_name)
    
    def add_document_field(self):
        """添加整单基本信息字段"""
        # 获取作用范围为整单基本信息的字段
        display_names = self.config_data.get("display_names", {})
        available_fields = []
        
        for field_name, field_config in display_names.items():
            if isinstance(field_config, dict):
                if field_config.get('scope') == '整单基本信息':
                    display_name = field_config.get('display_name', field_name)
                    available_fields.append((field_name, display_name))
            else:
                # 兼容旧格式，默认为整单基本信息
                available_fields.append((field_name, field_config))
        
        if not available_fields:
            messagebox.showwarning("警告", "没有可用的整单基本信息字段！\n请先在字段配置页面添加作用范围为'整单基本信息'的字段。")
            return
        
        # 创建字段选择弹窗
        dialog = tk.Toplevel(self.root)
        dialog.title("选择字段")
        dialog.geometry("400x300")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 居中显示
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (300 // 2)
        dialog.geometry(f"400x300+{x}+{y}")
        
        # 说明标签
        ttk.Label(dialog, text="选择要添加的整单基本信息字段:", font=('Arial', 10, 'bold')).pack(pady=(20, 10))
        
        # 字段列表
        listbox_frame = ttk.Frame(dialog)
        listbox_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        field_listbox = tk.Listbox(listbox_frame)
        scrollbar = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=field_listbox.yview)
        field_listbox.configure(yscrollcommand=scrollbar.set)
        
        # 填充可用字段（只显示显示名称）
        field_mapping = {}
        current_fields = self.config_data.get("document_info_fields", [])
        
        for field_name, display_name in available_fields:
            if field_name not in current_fields:  # 只显示未添加的字段
                field_listbox.insert(tk.END, display_name)
                field_mapping[display_name] = field_name
        
        field_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        if field_listbox.size() == 0:
            field_listbox.insert(tk.END, "所有整单基本信息字段都已添加")
            field_listbox.config(state=tk.DISABLED)
        
        # 按钮框架
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=20)
        
        def add_selected_field():
            selection = field_listbox.curselection()
            if selection and field_listbox.size() > 0 and field_listbox.get(0) != "所有整单基本信息字段都已添加":
                display_name = field_listbox.get(selection[0])
                field_name = field_mapping.get(display_name)
                
                if field_name:
                    self.config_data.setdefault("document_info_fields", []).append(field_name)
                    self.refresh_document_fields()
                    logger.info(f"添加整单字段: {field_name} ({display_name})")
                    dialog.destroy()
            else:
                messagebox.showwarning("警告", "请选择一个字段！")
        
        ttk.Button(button_frame, text="添加", command=add_selected_field).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="取消", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        # 双击添加
        field_listbox.bind('<Double-1>', lambda e: add_selected_field())
    
    def remove_document_field(self):
        """删除整单基本信息字段"""
        selection = self.document_fields_listbox.curselection()
        if selection:
            index = selection[0]
            field = self.config_data.get("document_info_fields", [])[index]
            
            # 获取显示名称用于确认对话框
            display_names = self.config_data.get("display_names", {})
            field_config = display_names.get(field, field)
            if isinstance(field_config, dict):
                display_name = field_config.get('display_name', field)
            else:
                display_name = field_config
            
            if messagebox.askyesno("确认删除", f"确定要删除字段 '{display_name}' 吗？", parent=self.root):
                self.config_data.get("document_info_fields", []).pop(index)
                self.refresh_document_fields()
                logger.info(f"删除整单字段: {field} ({display_name})")
    
    def move_document_field(self, direction):
        """移动整单基本信息字段位置"""
        selection = self.document_fields_listbox.curselection()
        if selection:
            index = selection[0]
            fields = self.config_data.get("document_info_fields", [])
            new_index = index + direction
            
            if 0 <= new_index < len(fields):
                fields[index], fields[new_index] = fields[new_index], fields[index]
                self.refresh_document_fields()
                self.document_fields_listbox.selection_set(new_index)
    
    def edit_document_field(self):
        """编辑整单基本信息字段"""
        selection = self.document_fields_listbox.curselection()
        if selection:
            index = selection[0]
            field = self.config_data.get("document_info_fields", [])[index]
            
            # 获取显示名称
            display_names = self.config_data.get("display_names", {})
            field_config = display_names.get(field, field)
            if isinstance(field_config, dict):
                display_name = field_config.get('display_name', field)
            else:
                display_name = field_config
            
            messagebox.showinfo("提示", f"要编辑字段 '{display_name}' 的显示名称或作用范围，请到'字段配置'页面进行操作。")
    
    # ==================== 因子分类操作 ====================
    
    def refresh_factor_tree(self):
        """刷新因子分类树"""
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
        # 添加调试日志
        logger.info(f"刷新显示名称列表 - 配置数据: {display_names}")
        search_text = self.search_var.get().lower() if hasattr(self, 'search_var') else ""
        
        for field, field_config in sorted(display_names.items()):
            # 兼容新旧格式
            if isinstance(field_config, dict):
                display_name = field_config.get('display_name', field)
                scope = field_config.get('scope', '整单基本信息')
            else:
                # 兼容旧格式
                display_name = field_config
                scope = '整单基本信息'
            
            # 搜索过滤
            if not search_text or search_text in field.lower() or search_text in display_name.lower() or search_text in scope.lower():
                # 显示三列数据：字段名、显示名称、作用范围
                item_id = self.display_names_tree.insert("", tk.END, values=(field, display_name, scope))
                # 注意：由于使用show="headings"，不能设置#0列，字段名已经在values中
    
    def filter_display_names(self, event=None):
        """过滤显示名称"""
        self.refresh_display_names()
    
    def add_display_name(self):
        """添加显示名称"""
        # 创建添加字段的弹窗
        dialog = tk.Toplevel(self.root)
        dialog.title("添加字段配置")
        dialog.geometry("450x280")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 居中显示
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (450 // 2)
        y = (dialog.winfo_screenheight() // 2) - (280 // 2)
        dialog.geometry(f"450x280+{x}+{y}")
        
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
        
        # 显示名称输入框
        display_frame = ttk.Frame(main_frame)
        display_frame.pack(fill=tk.X, pady=(0, 15))
        ttk.Label(display_frame, text="显示名称:", width=12, anchor='w').pack(side=tk.LEFT)
        display_name_var = tk.StringVar()
        display_name_entry = ttk.Entry(display_frame, textvariable=display_name_var, width=35)
        display_name_entry.pack(side=tk.LEFT, padx=(10, 0))
        
        # 作用范围下拉框
        scope_frame = ttk.Frame(main_frame)
        scope_frame.pack(fill=tk.X, pady=(0, 20))
        ttk.Label(scope_frame, text="作用范围:", width=12, anchor='w').pack(side=tk.LEFT)
        scope_var = tk.StringVar(value="整单基本信息")
        scope_combo = ttk.Combobox(scope_frame, textvariable=scope_var, 
                                  values=["整单基本信息", "子因子基本信息", "子因子表格"],
                                  state="readonly", width=32)
        scope_combo.pack(side=tk.LEFT, padx=(10, 0))
        
        # 分隔线
        separator = ttk.Separator(main_frame, orient='horizontal')
        separator.pack(fill=tk.X, pady=(10, 20))
        
        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        def save_field():
            field = field_var.get().strip()
            display_name = display_name_var.get().strip()
            scope = scope_var.get()
            
            if not field:
                messagebox.showerror("输入错误", "请输入字段名", parent=dialog)
                field_entry.focus()
                return
            if not display_name:
                messagebox.showerror("输入错误", "请输入显示名称", parent=dialog)
                display_name_entry.focus()
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
                "scope": scope
            }
            self.refresh_all_ui()  # 刷新所有相关页面，确保实时更新
            logger.info(f"添加字段配置: {field} -> {display_name} ({scope})")
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
            dialog.geometry("450x280")
            dialog.resizable(False, False)
            dialog.transient(self.root)
            dialog.grab_set()
            
            # 居中显示
            dialog.update_idletasks()
            x = (dialog.winfo_screenwidth() // 2) - (450 // 2)
            y = (dialog.winfo_screenheight() // 2) - (280 // 2)
            dialog.geometry(f"450x280+{x}+{y}")
            
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
            
            # 添加详细调试日志（在设置值之后）
            logger.info(f"[调试] 初始化显示名称输入框 - StringVar设置后值: '{display_name_var.get()}', Entry显示值: '{display_name_entry.get()}'")
            
            # 绑定输入框变化事件来监控输入
            def on_entry_change(*args):
                logger.info(f"[调试] 输入框内容变化 - StringVar值: '{display_name_var.get()}', Entry值: '{display_name_entry.get()}'")
            
            display_name_var.trace('w', on_entry_change)
            
            # 作用范围下拉框
            scope_frame = ttk.Frame(main_frame)
            scope_frame.pack(fill=tk.X, pady=(0, 20))
            ttk.Label(scope_frame, text="作用范围:", width=12, anchor='w').pack(side=tk.LEFT)
            scope_var = tk.StringVar(value=old_scope)
            scope_combo = ttk.Combobox(scope_frame, textvariable=scope_var, 
                                      values=["整单基本信息", "子因子基本信息", "子因子表格"],
                                      state="readonly", width=32)
            scope_combo.pack(side=tk.LEFT, padx=(10, 0))
            # 确保Combobox显示初始值
            scope_combo.set(old_scope)
            
            # 分隔线
            separator = ttk.Separator(main_frame, orient='horizontal')
            separator.pack(fill=tk.X, pady=(10, 20))
            
            # 按钮框架
            button_frame = ttk.Frame(main_frame)
            button_frame.pack(fill=tk.X)
            
            def save_changes():
                # 直接从Entry和Combobox获取值，避免StringVar同步问题
                new_display_name = display_name_entry.get().strip()
                new_scope = scope_combo.get()
                
                # 添加详细调试日志
                logger.info(f"[调试] 保存前获取值 - StringVar.get(): '{display_name_var.get()}', Entry.get(): '{display_name_entry.get()}'")
                logger.info(f"[调试] 保存前获取值 - scope_var.get(): '{scope_var.get()}', scope_combo.get(): '{scope_combo.get()}'")
                logger.info(f"[调试] 保存前处理后 - new_display_name: '{new_display_name}', new_scope: '{new_scope}'")
                logger.info(f"保存字段配置 - 字段: {field}, 新显示名称: '{new_display_name}', 新作用范围: '{new_scope}'")
                logger.info(f"StringVar原始值: '{display_name_var.get()}', Entry内容: '{display_name_entry.get()}'")
                
                if not new_display_name:
                    messagebox.showerror("输入错误", "请输入显示名称", parent=dialog)
                    display_name_entry.focus()
                    return
                
                # 保存到配置
                self.config_data.setdefault("display_names", {})[field] = {
                    "display_name": new_display_name,
                    "scope": new_scope
                }
                # 直接保存配置到文件，避免重复弹窗
                try:
                    with open(self.config_path, 'w', encoding='utf-8') as f:
                        json.dump(self.config_data, f, ensure_ascii=False, indent=2)
                    logger.info(f"配置文件保存成功: {self.config_path}")
                except Exception as e:
                    logger.error(f"保存配置文件失败: {e}")
                    messagebox.showerror("错误", f"保存配置文件失败: {e}", parent=dialog)
                    return
                
                # 重新加载配置数据并刷新所有界面
                self.load_config()
                self.refresh_all_ui()  # 刷新所有相关页面，确保实时更新
                # 使用实际保存的值而不是重新加载的值来记录日志
                logger.info(f"编辑字段配置: {field} -> {new_display_name} ({new_scope})")
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
    
    def delete_display_name(self):
        """删除显示名称"""
        selection = self.display_names_tree.selection()
        if selection:
            item = selection[0]
            # 从三列数据获取字段信息
            values = self.display_names_tree.item(item, "values")
            field, display_name, scope = values
            
            if messagebox.askyesno("确认删除", f"确定要删除字段 '{display_name}' ({field}) 吗？", parent=self.root):
                self.config_data.get("display_names", {}).pop(field, None)
                self.refresh_all_ui()  # 刷新所有相关页面，确保实时更新
                logger.info(f"删除字段配置: {field}")
    
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
            
        except Exception as e:
            logger.error(f"保存配置失败: {e}")
            messagebox.showerror("错误", f"保存配置失败: {e}")
    
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
            self.refresh_document_fields()
            self.refresh_factor_tree()
            self.refresh_display_names()
            
            # 刷新数据层次配置
            hierarchy_names = self.config_data.get("data_hierarchy_names", {})
            for key, entry in self.hierarchy_name_entries.items():
                entry.delete(0, tk.END)
                entry.insert(0, hierarchy_names.get(key, ""))
            
            enabled_levels = self.config_data.get("enabled_hierarchy_levels", [])
            for key, var in self.hierarchy_vars.items():
                var.set(key in enabled_levels)
            
            self.default_hierarchy_var.set(self.config_data.get("default_hierarchy_level", "part"))
            
            # 刷新主窗口页面字段显示
            if self.app_controller and hasattr(self.app_controller, 'refresh_view'):
                logger.info("正在刷新主窗口页面字段显示...")
                self.app_controller.refresh_view()
            
        except Exception as e:
            logger.error(f"刷新UI失败: {e}")
    
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