# -*- coding: utf-8 -*-
"""
通用工具函数模块
提供项目中常用的工具函数和辅助方法
"""

import logging
import pandas as pd
from typing import Dict, Any, List, Optional


class ValidationUtils:
    """验证工具类"""
    
    @staticmethod
    def validate_input(value, param_name, expected_type=None, allow_none=False):
        """通用输入验证方法
        
        Args:
            value: 要验证的值
            param_name: 参数名称
            expected_type: 期望的类型
            allow_none: 是否允许None值
            
        Raises:
            ValueError: 当验证失败时
        """
        if value is None and not allow_none:
            raise ValueError(f"{param_name} 不能为空")
            
        if expected_type and value is not None and not isinstance(value, expected_type):
            raise ValueError(f"{param_name} 必须是 {expected_type.__name__} 类型")
    
    @staticmethod
    def safe_get_value(data_dict, key, default=''):
        """安全获取字典值的方法
        
        Args:
            data_dict: 数据字典
            key: 键名
            default: 默认值
            
        Returns:
            获取到的值或默认值
        """
        if not isinstance(data_dict, dict):
            return default
        return data_dict.get(key, default)


class DataUtils:
    """数据处理工具类"""
    
    @staticmethod
    def convert_to_display_info(data_dict, config_manager):
        """将数据字典转换为显示信息字典
        
        Args:
            data_dict: 原始数据字典
            config_manager: 配置管理器
            
        Returns:
            转换后的显示信息字典
        """
        display_info = {}
        for field, value in data_dict.items():
            display_name = config_manager.get_display_name(field)
            display_info[display_name] = value
        return display_info
    
    @staticmethod
    def convert_to_display_columns(columns, config_manager):
        """将列名转换为显示列名
        
        Args:
            columns: 原始列名列表
            config_manager: 配置管理器
            
        Returns:
            列名到显示名称的映射字典
        """
        display_columns = {}
        for col in columns:
            display_name = config_manager.get_display_name(col)
            display_columns[col] = display_name
        return display_columns
    
    @staticmethod
    def optimize_dataframe_memory(df):
        """优化DataFrame内存使用
        
        Args:
            df: 要优化的DataFrame
            
        Returns:
            优化后的DataFrame
        """
        if df is None or df.empty:
            return df
            
        # 优化数值类型
        for col in df.select_dtypes(include=['int64']).columns:
            df[col] = pd.to_numeric(df[col], downcast='integer')
            
        for col in df.select_dtypes(include=['float64']).columns:
            df[col] = pd.to_numeric(df[col], downcast='float')
            
        # 优化字符串类型
        for col in df.select_dtypes(include=['object']).columns:
            if df[col].dtype == 'object':
                try:
                    df[col] = df[col].astype('category')
                except:
                    pass
                    
        return df


class ClipboardUtils:
    """剪贴板工具类"""
    
    @staticmethod
    def copy_to_clipboard(content, success_message="内容已复制到剪贴板"):
        """通用复制到剪贴板方法
        
        Args:
            content: 要复制的内容
            success_message: 成功提示信息
            
        Returns:
            bool: 是否复制成功
        """
        try:
            import tkinter as tk
            root = tk.Tk()
            root.withdraw()  # 隐藏主窗口
            root.clipboard_clear()
            root.clipboard_append(str(content))
            root.update()  # 确保剪贴板更新
            root.destroy()
            
            # 显示成功提示
            from tkinter import messagebox
            messagebox.showinfo("复制成功", success_message)
            return True
            
        except Exception as e:
            logging.error(f"复制到剪贴板失败: {e}")
            from tkinter import messagebox
            messagebox.showerror("复制失败", f"无法复制到剪贴板: {e}")
            return False


class LoggingUtils:
    """日志工具类"""
    
    @staticmethod
    def setup_logger(name, level=logging.INFO):
        """设置日志记录器
        
        Args:
            name: 日志记录器名称
            level: 日志级别
            
        Returns:
            配置好的日志记录器
        """
        logger = logging.getLogger(name)
        logger.setLevel(level)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            
        return logger
    
    @staticmethod
    def log_error_with_context(logger, error, context=""):
        """记录带上下文的错误信息
        
        Args:
            logger: 日志记录器
            error: 错误对象
            context: 上下文信息
        """
        error_msg = f"错误: {str(error)}"
        if context:
            error_msg = f"{context} - {error_msg}"
        logger.error(error_msg, exc_info=True)