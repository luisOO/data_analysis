# -*- coding: utf-8 -*-
"""
数据处理工具函数模块
提供数据转换和处理功能
"""

import logging
from typing import Dict, Any, List, Optional
from .lightweight_data import pd


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
        """优化DataFrame内存使用（轻量化版本）
        
        Args:
            df: 要优化的DataFrame
            
        Returns:
            优化后的DataFrame
        """
        if df is None or df.empty:
            return df
            
        # 使用LightweightDataFrame的优化方法
        try:
            # 优化数值类型
            int_columns = df.select_dtypes(include=['int64']).columns
            for col in int_columns:
                column_data = df[col]
                optimized_data = pd.to_numeric(column_data, downcast='integer')
                # 更新列数据
                for i, value in enumerate(optimized_data):
                    if i < len(df.data):
                        df.data[i][col] = value
                        
            float_columns = df.select_dtypes(include=['float64']).columns
            for col in float_columns:
                column_data = df[col]
                optimized_data = pd.to_numeric(column_data, downcast='float')
                # 更新列数据
                for i, value in enumerate(optimized_data):
                    if i < len(df.data):
                        df.data[i][col] = value
        except Exception as e:
            logging.warning(f"优化DataFrame内存时出错: {e}")
            
        # 简化的字符串处理，不进行复杂的category转换
        return df