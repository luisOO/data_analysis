# -*- coding: utf-8 -*-
"""
数据处理工具函数模块
提供数据转换和处理功能
"""

import logging
import pandas as pd
from typing import Dict, Any, List, Optional


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