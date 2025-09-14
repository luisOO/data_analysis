import tkinter as tk
from tkinter import filedialog, messagebox
import logging
import os
from models import ConfigManager, DataManager
from views import MainAppView
from utils import DataUtils
from .logging_setup import setup_logging


class AppController:
    def __init__(self):
        # 设置日志系统
        self.logger = setup_logging()
        self.logger.info("应用程序启动")
        
        try:
            # 加载配置文件
            config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')
            self.config_manager = ConfigManager(config_path)
            self.data_manager = DataManager(config_manager=self.config_manager)
            self.view = MainAppView(self)
            self.current_sub_factor = None
            self.logger.info("应用程序初始化完成")
        except Exception as e:
            self.logger.error(f"应用程序初始化失败: {e}")
            raise
        
        # 显示空白的单据基本信息
        self.view.doc_info_view.show_default_info()
        
        # 初始化因子分类框架
        self.setup_initial_factor_tabs()
    
    def _convert_to_display_info(self, data_dict):
        """将数据字典转换为显示信息字典的通用方法"""
        return DataUtils.convert_to_display_info(data_dict, self.config_manager)
    
    def _convert_to_display_columns(self, columns):
        """将列名转换为显示列名的通用方法"""
        return DataUtils.convert_to_display_columns(columns, self.config_manager)

    def setup_initial_factor_tabs(self):
        """根据配置初始化因子分类框架"""
        try:
            # 获取配置的因子分类
            factor_categories = self.config_manager.get_factor_categories()
            
            if factor_categories:
                # 设置因子分类标签页
                self.view.factor_view.setup_tabs(factor_categories)
                
                # 为每个分类设置空白框架
                for category, factors in factor_categories.items():
                    if factors:
                        # 设置第一个子因子的空白框架
                        first_sub_factor = factors[0]['name']
                        self.view.factor_view.setup_sub_factor_framework(category, first_sub_factor)
                        
        except Exception as e:
            self.logger.error(f"初始化因子分类框架失败: {e}")
    
    def run(self):
        self.view.mainloop()
        
    def load_default_data(self):
        """程序启动时加载默认示例数据"""
        try:
            import os
            sample_file = os.path.join(os.path.dirname(__file__), 'sample.json')
            if os.path.exists(sample_file):
                self.data_manager.load_json_data(sample_file)
                
                # Update document info
                doc_info_fields = self.config_manager.get_document_info_fields()
                doc_info = self.data_manager.get_document_info(doc_info_fields)
                
                # 获取字段显示名称
                display_info = {}
                for field, value in doc_info.items():
                    display_name = self.config_manager.get_display_name(field)
                    display_info[display_name] = value
                
                self.view.doc_info_view.display_info(display_info)

                # Setup factor tabs
                factor_categories = self.config_manager.get_factor_categories()
                self.view.factor_view.setup_tabs(factor_categories)
        except Exception as e:
            self.logger.error(f"加载默认数据时出错: {e}")
            # 如果加载失败，显示默认提示信息
            default_info = {
                "单据编号": "请加载数据文件",
                "状态": "未加载数据",
                "提示": "请通过菜单选择JSON文件加载数据"
            }
            self.view.doc_info_view.display_info(default_info)

    def load_data_action(self):
        """加载用户选择的数据文件"""
        file_path = filedialog.askopenfilename(
            title="选择JSON文件",
            filetypes=(("JSON files", "*.json"), ("All files", "*.*"))
        )
        if not file_path:
            return

        try:
            self.logger.info(f"开始加载用户数据文件: {file_path}")
            self.data_manager.load_json_data(file_path)
            
            # Update document info
            self.logger.info("获取文档信息字段")
            doc_info_fields = self.config_manager.get_document_info_fields()
            self.logger.info(f"文档信息字段: {doc_info_fields}")
            
            doc_info = self.data_manager.get_document_info(doc_info_fields)
            self.logger.info(f"文档信息: {doc_info}")
            
            # 使用通用方法转换显示信息
            display_info = self._convert_to_display_info(doc_info)
            self.logger.info(f"显示信息: {display_info}")
            self.view.doc_info_view.display_info(display_info)

            # Setup factor tabs
            self.logger.info("设置因子标签页")
            factor_categories = self.config_manager.get_factor_categories()
            self.logger.info(f"因子分类: {factor_categories}")
            self.view.factor_view.setup_tabs(factor_categories)
            
            self.logger.info("用户数据文件加载成功")
            
        except Exception as e:
            import traceback
            self.logger.error(f"加载数据文件时出错: {e}")
            self.logger.error(f"错误堆栈: {traceback.format_exc()}")
            messagebox.showerror("错误", f"加载数据文件失败:\n{str(e)}")

    def on_sub_factor_select(self, sub_factor_name):
        """处理子因素选择事件"""
        self.current_sub_factor = sub_factor_name
        self.logger.info(f"选中子因素: {sub_factor_name}")
        
        # 获取basic_info字段配置
        basic_info_fields = self.config_manager.get_sub_factor_basic_info(sub_factor_name)
        # 从实际数据中获取basic info
        sub_factor_basic_info = self.data_manager.get_basic_info_from_data(sub_factor_name, basic_info_fields)
        
        # 使用通用方法转换显示信息
        display_info = self._convert_to_display_info(sub_factor_basic_info)
        
        # 更新右侧详情视图
        if hasattr(self.view.factor_view, 'detail_view') and self.view.factor_view.detail_view:
            self.view.factor_view.detail_view.display_basic_info(display_info)
            
            # 初始化数据层次选择
            self.view.factor_view.detail_view.setup_data_hierarchy_selection()
            
            # 默认选择配置的层次并显示数据
            default_level = self.config_manager.get_default_hierarchy_level()
            self.on_hierarchy_node_select(default_level)

    def on_hierarchy_node_select(self, level):
        """处理层级节点选择事件"""
        if not self.current_sub_factor:
            return
            
        self.logger.info(f"选中层级节点: {level}")
        
        try:
            root_node = self.data_manager.get_calculate_item_vo()
            self.logger.info(f"获取到的root_node: {type(root_node)}, 是否为None: {root_node is None}")
            if root_node is None:
                self.logger.error("root_node为None，数据可能未正确加载")
                return
            self.logger.info(f"准备调用get_all_nodes_for_level，参数: level={level}")
            nodes_at_level = self.data_manager.get_all_nodes_for_level(root_node, level)
            self.logger.info(f"get_all_nodes_for_level返回结果: {len(nodes_at_level) if nodes_at_level else 0}个节点")
            
            # 使用当前选中的因子名称获取列配置
            columns = self.config_manager.get_data_table_columns(level, self.current_sub_factor)
            df = self.data_manager.get_data_for_level(nodes_at_level, columns)
            
            # 保存当前数据帧，用于搜索过滤
            self.current_df = df
            
            # 使用通用方法转换显示列名
            display_columns = self._convert_to_display_columns(columns)
            
            # 更新右侧详情视图的数据表格
            if hasattr(self.view.factor_view, 'detail_view') and self.view.factor_view.detail_view:
                self.view.factor_view.detail_view.display_data_table(df, display_columns, columns)
                self.logger.info(f"成功更新表格数据，共 {len(df)} 行")
                
        except Exception as e:
            self.logger.error(f"处理层级节点选择时出错: {e}")
            
    def apply_search_filter(self, level, search_text):
        """应用搜索过滤"""
        self.logger.info(f"应用搜索过滤: {search_text}")
        
        # 检查是否有当前数据帧
        if not hasattr(self, 'current_df') or self.current_df is None or self.current_df.empty:
            return
            
        # 更严格的重复检查 - 包括搜索文本、层级和数据版本
        current_data_hash = hash(str(self.current_df.values.tobytes())) if hasattr(self.current_df, 'values') else 0
        search_key = f"{level}_{search_text}_{current_data_hash}"
        
        if hasattr(self, '_last_search_key') and self._last_search_key == search_key:
            return
            
        # 保存当前搜索键
        self._last_search_key = search_key
        self._last_search_text = search_text
        self._last_search_level = level
            
        try:
            # 如果搜索文本为空，显示所有数据
            if not search_text:
                # 使用通用方法转换显示列名
                display_columns = self._convert_to_display_columns(self.current_df.columns)
                    
                # 更新表格显示
                if hasattr(self.view.factor_view, 'detail_view') and self.view.factor_view.detail_view:
                    # 获取当前层级的列配置
                    current_level = getattr(self.view.factor_view.detail_view, 'current_level', 'part')
                    columns = self.config_manager.get_data_table_columns(current_level, self.current_sub_factor)
                    self.view.factor_view.detail_view.display_data_table(self.current_df, display_columns, columns)
                return
            
            # 过滤数据
            filtered_df = self.current_df.copy()
            mask = None
            
            # 在所有列中搜索
            for col in filtered_df.columns:
                col_mask = filtered_df[col].astype(str).str.lower().str.contains(search_text, na=False)
                if mask is None:
                    mask = col_mask
                else:
                    mask = mask | col_mask
                    
            filtered_df = filtered_df[mask]
            
            # 使用通用方法转换显示列名
            display_columns = self._convert_to_display_columns(filtered_df.columns)
                
            # 更新表格显示
            if hasattr(self.view.factor_view, 'detail_view') and self.view.factor_view.detail_view:
                # 获取当前层级的列配置
                current_level = getattr(self.view.factor_view.detail_view, 'current_level', 'part')
                columns = self.config_manager.get_data_table_columns(current_level, self.current_sub_factor)
                self.view.factor_view.detail_view.display_data_table(filtered_df, display_columns, columns)
                self.logger.info(f"搜索过滤完成，找到 {len(filtered_df)} 条匹配记录")
                
        except Exception as e:
            self.logger.error(f"应用搜索过滤时出错: {e}")
    
    def reload_config(self):
        """重新加载配置文件"""
        try:
            # 重新创建配置管理器
            old_config = self.config_manager.config.copy() if hasattr(self.config_manager, 'config') else {}
            self.config_manager = ConfigManager()
            
            # 记录配置变化
            new_config = self.config_manager.config
            self.logger.info("配置文件已重新加载")
            
            # 检查是否有重要配置变化
            config_changed = False
            if old_config.get('default_data_path') != new_config.get('default_data_path'):
                config_changed = True
                self.logger.info("默认数据路径已更改")
            
            if old_config.get('ui_theme') != new_config.get('ui_theme'):
                config_changed = True
                self.logger.info("UI主题配置已更改")
            
            if config_changed:
                self.logger.info("检测到重要配置变化，建议重启程序以完全应用新配置")
            
            return True
            
        except Exception as e:
            self.logger.error(f"重新加载配置失败: {e}")
            return False
    
    def refresh_view(self):
        """刷新视图 - 重新加载当前数据和配置"""
        try:
            self.logger.info("开始刷新视图")
            
            # 重新加载配置
            self.reload_config()
            
            # 如果有当前选中的子因子，重新加载其数据
            if self.current_sub_factor:
                self.logger.info(f"重新加载子因子数据: {self.current_sub_factor}")
                self.on_sub_factor_select(self.current_sub_factor)
            
            # 重新显示单据基本信息
            if hasattr(self.data_manager, 'data') and self.data_manager.data:
                doc_info_fields = self.config_manager.get_document_info_fields()
                doc_info = self.data_manager.get_document_info(doc_info_fields)
                
                # 获取字段显示名称
                display_info = {}
                for field, value in doc_info.items():
                    display_name = self.config_manager.get_display_name(field)
                    display_info[display_name] = value
                
                self.view.doc_info_view.display_info(display_info)
            else:
                # 如果没有数据，显示默认信息
                self.view.doc_info_view.show_default_info()
            
            self.logger.info("视图刷新完成")
            
        except Exception as e:
            self.logger.error(f"刷新视图时出错: {e}")
            messagebox.showerror("错误", f"刷新视图失败:\n{str(e)}")