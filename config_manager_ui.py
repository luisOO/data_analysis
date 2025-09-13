#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置管理器UI模块
提供用户友好的配置管理界面
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os
from typing import Dict, Any
import logging

class ConfigManagerUI:
    """配置管理器UI类"""
    
    def __init__(self, parent=None, config_path="config.json"):
        self.config_path = config_path
        self.config_data = {}
        self.window = None
        self.parent = parent
        self.logger = logging.getLogger(__name__)
        
        # 配置项描述
        self.config_descriptions = {
            "data_hierarchy_names": {
                "name": "数据层次名称",
                "description": "定义数据的层次结构名称",
                "type": "dict"
            },
            "default_data_path": {
                "name": "默认数据路径",
                "description": "程序启动时默认加载的数据文件路径",
                "type": "string"
            },
            "ui_theme": {
                "name": "界面主题",
                "description": "程序界面的主题设置",
                "type": "dict"
            },
            "factor_categories": {
                "name": "因子分类配置",
                "description": "定义计算因子的分类和配置",
                "type": "dict"
            },
            "display_names": {
                "name": "显示名称映射",
                "description": "字段和因子的中文显示名称映射",
                "type": "dict"
            },
            "document_info_fields": {
                "name": "单据信息字段",
                "description": "单据基本信息要显示的字段列表",
                "type": "list"
            },
            "performance": {
                "name": "性能设置",
                "description": "程序性能相关的配置",
                "type": "dict"
            },
            "logging": {
                "name": "日志设置",
                "description": "日志记录相关的配置",
                "type": "dict"
            }
        }
        
    def load_config(self):
        """加载配置文件"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    self.config_data = json.load(f)
                self.logger.info(f"配置文件加载成功: {self.config_path}")
            else:
                self.config_data = self.get_default_config()
                self.logger.warning(f"配置文件不存在，使用默认配置: {self.config_path}")
        except Exception as e:
            self.logger.error(f"加载配置文件失败: {e}")
            self.config_data = self.get_default_config()
            messagebox.showerror("错误", f"加载配置文件失败：{e}\n将使用默认配置")
    
    def save_config(self):
        """保存配置文件"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config_data, f, ensure_ascii=False, indent=2)
            self.logger.info(f"配置文件保存成功: {self.config_path}")
            return True
        except Exception as e:
            self.logger.error(f"保存配置文件失败: {e}")
            messagebox.showerror("错误", f"保存配置文件失败：{e}")
            return False
    
    def get_default_config(self) -> Dict[str, Any]:
        """获取默认配置"""
        return {
            "data_hierarchy_names": {
                "total": "总计",
                "boq": "清单项",
                "model": "模型构件",
                "part": "零部件"
            },
            "enabled_hierarchy_levels": ["total", "boq", "model", "part"],
            "default_hierarchy_level": "part",
            "default_data_path": "sample.json",
            "ui_theme": {
                "font_family": "微软雅黑",
                "font_size": 9,
                "colors": {
                    "primary": "#2196F3",
                    "secondary": "#FFC107",
                    "success": "#4CAF50",
                    "warning": "#FF9800",
                    "error": "#F44336"
                }
            },
            "factor_categories": {
                "基础因子": [
                    {
                        "name": "收入因子",
                        "basic_info": ["businessCode", "netSalesRevenue", "description", "unit", "category"],
                        "table_info": [["total", "boq", "model", "part"], ["businessCode", "netSalesRevenue", "description"]]
                    },
                    {
                        "name": "成本因子",
                        "basic_info": ["businessCode", "totalCost", "description", "unit", "category"],
                        "table_info": [["total", "boq", "model", "part"], ["businessCode", "totalCost", "description"]]
                    }
                ]
            },
            "display_names": {
                "businessCode": "业务编码",
                "netSalesRevenue": "净销售收入",
                "totalCost": "总成本",
                "description": "描述",
                "unit": "单位",
                "category": "类别",
                "收入因子": "收入因子",
                "成本因子": "成本因子"
            },
            "document_info_fields": ["businessCode", "description", "unit"],
            "performance": {
                "max_memory_usage_mb": 512,
                "chunk_size": 1000,
                "enable_memory_optimization": True,
                "gc_threshold": 100
            },
            "logging": {
                "level": "INFO",
                "max_file_size_mb": 10,
                "backup_count": 5,
                "enable_console_output": False
            }
        }
    
    def open_config_window(self):
        """打开配置管理窗口"""
        if self.window and self.window.winfo_exists():
            self.window.lift()
            return
            
        self.load_config()
        self.create_config_window()
    
    def create_config_window(self):
        """创建配置管理窗口"""
        self.window = tk.Toplevel(self.parent) if self.parent else tk.Tk()
        self.window.title("配置管理器 - CalcAny")
        self.window.geometry("800x600")
        self.window.resizable(True, True)
        
        # 创建主框架
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建工具栏
        self.create_toolbar(main_frame)
        
        # 创建配置编辑区域
        self.create_config_editor(main_frame)
        
        # 创建按钮区域
        self.create_button_area(main_frame)
        
        # 居中显示窗口
        self.center_window()
    
    def create_toolbar(self, parent):
        """创建工具栏"""
        toolbar_frame = ttk.Frame(parent)
        toolbar_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 导入配置按钮
        ttk.Button(toolbar_frame, text="📁 导入配置", 
                  command=self.import_config).pack(side=tk.LEFT, padx=(0, 5))
        
        # 导出配置按钮
        ttk.Button(toolbar_frame, text="💾 导出配置", 
                  command=self.export_config).pack(side=tk.LEFT, padx=(0, 5))
        
        # 重置为默认配置按钮
        ttk.Button(toolbar_frame, text="🔄 重置默认", 
                  command=self.reset_to_default).pack(side=tk.LEFT, padx=(0, 5))
        
        # 分隔符
        ttk.Separator(toolbar_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        # 帮助按钮
        ttk.Button(toolbar_frame, text="❓ 帮助", 
                  command=self.show_help).pack(side=tk.RIGHT)
    
    def create_config_editor(self, parent):
        """创建配置编辑区域"""
        # 创建笔记本控件
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # 为每个主要配置项创建标签页
        self.config_frames = {}
        self.config_widgets = {}
        
        for key, info in self.config_descriptions.items():
            frame = ttk.Frame(self.notebook)
            self.notebook.add(frame, text=info["name"])
            self.config_frames[key] = frame
            self.create_config_section(frame, key, info)
        
        # 添加因子配置标签页
        factor_frame = ttk.Frame(self.notebook)
        self.notebook.add(factor_frame, text="因子配置")
        self.config_frames["factors"] = factor_frame
        self.create_factor_config_section(factor_frame)
    
    def create_config_section(self, parent, config_key, config_info):
        """创建配置项编辑区域"""
        # 创建滚动框架
        canvas = tk.Canvas(parent)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 添加描述
        desc_label = ttk.Label(scrollable_frame, text=config_info["description"], 
                              font=('微软雅黑', 9, 'italic'))
        desc_label.pack(anchor=tk.W, padx=10, pady=(10, 20))
        
        # 根据配置类型创建编辑控件
        self.config_widgets[config_key] = {}
        config_value = self.config_data.get(config_key, {})
        
        if config_info["type"] == "dict":
            self.create_dict_editor(scrollable_frame, config_key, config_value)
        elif config_info["type"] == "string":
            self.create_string_editor(scrollable_frame, config_key, config_value)
    
    def create_dict_editor(self, parent, config_key, config_value):
        """创建字典类型配置编辑器"""
        frame = ttk.LabelFrame(parent, text=f"{self.config_descriptions[config_key]['name']}设置")
        frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.config_widgets[config_key]['entries'] = {}
        
        for key, value in config_value.items():
            row_frame = ttk.Frame(frame)
            row_frame.pack(fill=tk.X, padx=10, pady=5)
            
            ttk.Label(row_frame, text=f"{key}:", width=20).pack(side=tk.LEFT)
            
            if isinstance(value, (str, int, float)):
                entry = ttk.Entry(row_frame, width=30)
                entry.insert(0, str(value))
                entry.pack(side=tk.LEFT, padx=(10, 0))
                self.config_widgets[config_key]['entries'][key] = entry
            elif isinstance(value, dict):
                # 对于嵌套字典，创建子编辑器
                self.create_nested_dict_editor(row_frame, key, value, config_key)
    
    def create_nested_dict_editor(self, parent, dict_key, dict_value, config_key):
        """创建嵌套字典编辑器"""
        sub_frame = ttk.LabelFrame(parent, text=dict_key)
        sub_frame.pack(fill=tk.X, pady=5)
        
        if config_key not in self.config_widgets:
            self.config_widgets[config_key] = {}
        if 'nested' not in self.config_widgets[config_key]:
            self.config_widgets[config_key]['nested'] = {}
        
        self.config_widgets[config_key]['nested'][dict_key] = {}
        
        for key, value in dict_value.items():
            row_frame = ttk.Frame(sub_frame)
            row_frame.pack(fill=tk.X, padx=10, pady=2)
            
            ttk.Label(row_frame, text=f"{key}:", width=15).pack(side=tk.LEFT)
            
            entry = ttk.Entry(row_frame, width=25)
            entry.insert(0, str(value))
            entry.pack(side=tk.LEFT, padx=(10, 0))
            
            self.config_widgets[config_key]['nested'][dict_key][key] = entry
    
    def create_string_editor(self, parent, config_key, config_value):
        """创建字符串类型配置编辑器"""
        frame = ttk.LabelFrame(parent, text=f"{self.config_descriptions[config_key]['name']}")
        frame.pack(fill=tk.X, padx=10, pady=5)
        
        entry = ttk.Entry(frame, width=50)
        entry.insert(0, str(config_value))
        entry.pack(padx=10, pady=10)
        
        self.config_widgets[config_key]['entry'] = entry
    
    def create_button_area(self, parent):
        """创建按钮区域"""
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X)
        
        # 应用按钮
        ttk.Button(button_frame, text="✅ 应用配置", 
                  command=self.apply_config).pack(side=tk.RIGHT, padx=(5, 0))
        
        # 取消按钮
        ttk.Button(button_frame, text="❌ 取消", 
                  command=self.cancel_config).pack(side=tk.RIGHT)
    
    def import_config(self):
        """导入配置文件"""
        file_path = filedialog.askopenfilename(
            title="选择配置文件",
            filetypes=[("JSON文件", "*.json"), ("所有文件", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    imported_config = json.load(f)
                
                # 验证配置格式
                if self.validate_config(imported_config):
                    self.config_data = imported_config
                    self.refresh_ui()
                    messagebox.showinfo("成功", "配置文件导入成功！")
                    self.logger.info(f"配置文件导入成功: {file_path}")
                else:
                    messagebox.showerror("错误", "配置文件格式不正确！")
                    
            except Exception as e:
                messagebox.showerror("错误", f"导入配置文件失败：{e}")
                self.logger.error(f"导入配置文件失败: {e}")
    
    def export_config(self):
        """导出配置文件"""
        file_path = filedialog.asksaveasfilename(
            title="保存配置文件",
            defaultextension=".json",
            filetypes=[("JSON文件", "*.json"), ("所有文件", "*.*")]
        )
        
        if file_path:
            try:
                # 收集当前UI中的配置
                current_config = self.collect_config_from_ui()
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(current_config, f, ensure_ascii=False, indent=2)
                
                messagebox.showinfo("成功", "配置文件导出成功！")
                self.logger.info(f"配置文件导出成功: {file_path}")
                
            except Exception as e:
                messagebox.showerror("错误", f"导出配置文件失败：{e}")
                self.logger.error(f"导出配置文件失败: {e}")
    
    def reset_to_default(self):
        """重置为默认配置"""
        if messagebox.askyesno("确认", "确定要重置为默认配置吗？这将丢失当前的所有配置！"):
            self.config_data = self.get_default_config()
            self.refresh_ui()
            messagebox.showinfo("成功", "已重置为默认配置！")
    
    def validate_config(self, config):
        """验证配置格式"""
        try:
            # 检查必要的配置项
            required_keys = ["data_hierarchy_names", "factor_categories", "display_names"]
            for key in required_keys:
                if key not in config:
                    return False
            
            # 验证factor_categories结构
            if "factor_categories" in config:
                factor_categories = config["factor_categories"]
                if isinstance(factor_categories, dict):
                    for category_name, category_data in factor_categories.items():
                        if isinstance(category_data, list):
                            # 新格式：数组结构
                            for factor in category_data:
                                if not isinstance(factor, dict) or "name" not in factor:
                                    return False
                                # 验证basic_info是列表
                                if "basic_info" in factor and not isinstance(factor["basic_info"], list):
                                    return False
            
            return True
        except:
            return False
    
    def collect_config_from_ui(self):
        """从UI收集配置数据"""
        config = {}
        
        for config_key, widgets in self.config_widgets.items():
            if config_key == "factors":
                # 处理因子配置
                config[config_key] = {"categories": {}}
                if "categories" in widgets:
                    for category_name, category_widgets in widgets["categories"].items():
                        config[config_key]["categories"][category_name] = {
                            "description": category_widgets["description"].get(),
                            "factors": {}
                        }
                        
                        for factor_name, factor_widgets in category_widgets["factors"].items():
                            # 收集列信息
                            columns = []
                            data_types = []
                            for col_entry, type_entry in zip(factor_widgets["columns"], factor_widgets["data_types"]):
                                col_value = col_entry.get().strip()
                                type_value = type_entry.get().strip()
                                if col_value:  # 只添加非空列
                                    columns.append(col_value)
                                    data_types.append(type_value if type_value else "string")
                            
                            config[config_key]["categories"][category_name]["factors"][factor_name] = {
                                "name": factor_widgets["name"].get(),
                                "unit": factor_widgets["unit"].get(),
                                "description": factor_widgets["description"].get(),
                                "table_info": {
                                    "columns": columns,
                                    "data_types": data_types
                                }
                            }
            elif 'entry' in widgets:
                # 字符串类型
                config[config_key] = widgets['entry'].get()
            elif 'entries' in widgets:
                # 字典类型
                config[config_key] = {}
                for key, entry in widgets['entries'].items():
                    value = entry.get()
                    # 尝试转换为适当的类型
                    try:
                        if value.isdigit():
                            value = int(value)
                        elif value.replace('.', '').isdigit():
                            value = float(value)
                        elif value.lower() in ['true', 'false']:
                            value = value.lower() == 'true'
                    except:
                        pass
                    config[config_key][key] = value
                
                # 处理嵌套字典
                if 'nested' in widgets:
                    for nested_key, nested_widgets in widgets['nested'].items():
                        config[config_key][nested_key] = {}
                        for key, entry in nested_widgets.items():
                            value = entry.get()
                            try:
                                if value.isdigit():
                                    value = int(value)
                                elif value.replace('.', '').isdigit():
                                    value = float(value)
                                elif value.lower() in ['true', 'false']:
                                    value = value.lower() == 'true'
                            except:
                                pass
                            config[config_key][nested_key][key] = value
        
        return config
    
    def refresh_ui(self):
        """刷新UI显示"""
        # 销毁现有的笔记本控件
        if hasattr(self, 'notebook'):
            self.notebook.destroy()
        
        # 重新创建配置编辑区域
        parent = self.notebook.master
        self.create_config_editor(parent)
    
    def apply_config(self):
        """应用配置"""
        try:
            # 收集UI中的配置
            new_config = self.collect_config_from_ui()
            
            # 验证配置
            if self.validate_config(new_config):
                self.config_data = new_config
                
                # 保存到文件
                if self.save_config():
                    messagebox.showinfo("成功", "配置已保存并应用！")
                    
                    # 如果有父窗口，通知配置已更新
                    if hasattr(self.parent, 'on_config_updated'):
                        self.parent.on_config_updated()
                    
                    self.window.destroy()
            else:
                messagebox.showerror("错误", "配置格式不正确，请检查输入！")
                
        except Exception as e:
            messagebox.showerror("错误", f"应用配置失败：{e}")
            self.logger.error(f"应用配置失败: {e}")
    
    def cancel_config(self):
        """取消配置"""
        self.window.destroy()
    
    def show_help(self):
        """显示帮助信息"""
        help_text = """
配置管理器使用说明：

1. 📁 导入配置：从JSON文件导入配置
2. 💾 导出配置：将当前配置导出为JSON文件
3. 🔄 重置默认：恢复为程序默认配置
4. ✅ 应用配置：保存并应用当前配置
5. ❌ 取消：放弃修改并关闭窗口

配置项说明：
• 数据层次名称：定义数据的层次结构显示名称
• 默认数据路径：程序启动时自动加载的数据文件
• 界面主题：程序界面的外观设置
• 性能设置：内存使用和性能优化相关配置
• 日志设置：日志记录的详细程度和文件管理

注意：修改配置后需要重启程序才能完全生效。
        """
        
        help_window = tk.Toplevel(self.window)
        help_window.title("帮助 - 配置管理器")
        help_window.geometry("500x400")
        help_window.resizable(False, False)
        
        text_widget = tk.Text(help_window, wrap=tk.WORD, padx=10, pady=10)
        text_widget.pack(fill=tk.BOTH, expand=True)
        text_widget.insert(tk.END, help_text)
        text_widget.config(state=tk.DISABLED)
        
        # 居中显示帮助窗口
        help_window.transient(self.window)
        help_window.grab_set()
        
        # 计算居中位置
        help_window.update_idletasks()
        x = (help_window.winfo_screenwidth() // 2) - (500 // 2)
        y = (help_window.winfo_screenheight() // 2) - (400 // 2)
        help_window.geometry(f"500x400+{x}+{y}")
    
    def create_factor_config_section(self, parent):
        """创建因子配置编辑区域"""
        # 创建滚动框架
        canvas = tk.Canvas(parent)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 添加描述
        desc_label = ttk.Label(scrollable_frame, text="配置计算因子的分类和详细信息", 
                              font=('微软雅黑', 9, 'italic'))
        desc_label.pack(anchor=tk.W, padx=10, pady=(10, 20))
        
        # 创建因子分类编辑器
        self.config_widgets["factors"] = {}
        factors_config = self.config_data.get("factors", {}).get("categories", {})
        
        for category_name, category_data in factors_config.items():
            self.create_factor_category_editor(scrollable_frame, category_name, category_data)
    
    def create_factor_category_editor(self, parent, category_name, category_data):
        """创建因子分类编辑器"""
        category_frame = ttk.LabelFrame(parent, text=f"分类: {category_name}")
        category_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # 分类描述
        desc_frame = ttk.Frame(category_frame)
        desc_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(desc_frame, text="描述:").pack(side=tk.LEFT)
        desc_entry = ttk.Entry(desc_frame, width=40)
        desc_entry.insert(0, category_data.get("description", ""))
        desc_entry.pack(side=tk.LEFT, padx=(10, 0))
        
        # 存储控件引用
        if "categories" not in self.config_widgets["factors"]:
            self.config_widgets["factors"]["categories"] = {}
        self.config_widgets["factors"]["categories"][category_name] = {
            "description": desc_entry,
            "factors": {}
        }
        
        # 因子列表
        factors = category_data.get("factors", {})
        for factor_name, factor_data in factors.items():
            self.create_factor_editor(category_frame, category_name, factor_name, factor_data)
    
    def create_factor_editor(self, parent, category_name, factor_name, factor_data):
        """创建单个因子编辑器"""
        factor_frame = ttk.LabelFrame(parent, text=f"因子: {factor_name}")
        factor_frame.pack(fill=tk.X, padx=20, pady=5)
        
        # 基本信息框架
        basic_frame = ttk.Frame(factor_frame)
        basic_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # 名称
        ttk.Label(basic_frame, text="名称:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        name_entry = ttk.Entry(basic_frame, width=20)
        name_entry.insert(0, factor_data.get("name", ""))
        name_entry.grid(row=0, column=1, padx=(0, 10))
        
        # 单位
        ttk.Label(basic_frame, text="单位:").grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        unit_entry = ttk.Entry(basic_frame, width=10)
        unit_entry.insert(0, factor_data.get("unit", ""))
        unit_entry.grid(row=0, column=3, padx=(0, 10))
        
        # 描述
        ttk.Label(basic_frame, text="描述:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5), pady=(5, 0))
        desc_entry = ttk.Entry(basic_frame, width=50)
        desc_entry.insert(0, factor_data.get("description", ""))
        desc_entry.grid(row=1, column=1, columnspan=3, sticky=tk.W+tk.E, pady=(5, 0))
        
        # 表格信息框架
        table_frame = ttk.LabelFrame(factor_frame, text="表格信息")
        table_frame.pack(fill=tk.X, padx=10, pady=5)
        
        table_info = factor_data.get("table_info", {})
        columns = table_info.get("columns", [])
        data_types = table_info.get("data_types", [])
        
        # 列配置
        columns_frame = ttk.Frame(table_frame)
        columns_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(columns_frame, text="列配置:").pack(anchor=tk.W)
        
        column_entries = []
        type_entries = []
        
        for i, (col, dtype) in enumerate(zip(columns + ["", "", ""], data_types + ["", "", ""])):
            col_frame = ttk.Frame(columns_frame)
            col_frame.pack(fill=tk.X, pady=2)
            
            ttk.Label(col_frame, text=f"列{i+1}:", width=8).pack(side=tk.LEFT)
            
            col_entry = ttk.Entry(col_frame, width=15)
            col_entry.insert(0, col)
            col_entry.pack(side=tk.LEFT, padx=(0, 5))
            column_entries.append(col_entry)
            
            ttk.Label(col_frame, text="类型:").pack(side=tk.LEFT, padx=(10, 5))
            
            type_combo = ttk.Combobox(col_frame, values=["string", "float", "int", "bool"], width=10)
            type_combo.set(dtype)
            type_combo.pack(side=tk.LEFT)
            type_entries.append(type_combo)
        
        # 存储控件引用
        self.config_widgets["factors"]["categories"][category_name]["factors"][factor_name] = {
            "name": name_entry,
            "unit": unit_entry,
            "description": desc_entry,
            "columns": column_entries,
            "data_types": type_entries
        }
    
    def center_window(self):
        """居中显示窗口"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")


if __name__ == "__main__":
    # 测试配置管理器
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    
    config_manager = ConfigManagerUI()
    config_manager.open_config_window()
    
    root.mainloop()