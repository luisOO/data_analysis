"""轻量化数据处理模块
替代pandas的基本功能，减少依赖
"""

import json
import logging
from typing import List, Dict, Any, Optional, Union


class LightweightDataFrame:
    """轻量化DataFrame实现，替代pandas.DataFrame"""
    
    def __init__(self, data: Optional[Union[List[Dict], Dict]] = None):
        """初始化DataFrame
        
        Args:
            data: 数据，可以是字典列表或空
        """
        if data is None:
            self.data = []
            self.columns = []
        elif isinstance(data, list):
            self.data = data
            self.columns = list(data[0].keys()) if data else []
        elif isinstance(data, dict):
            self.data = [data]
            self.columns = list(data.keys())
        else:
            self.data = []
            self.columns = []
    
    def __len__(self):
        """返回行数"""
        return len(self.data)
    
    def __getitem__(self, key):
        """获取列数据"""
        if isinstance(key, str):
            return [row.get(key) for row in self.data]
        elif isinstance(key, int):
            return self.data[key] if 0 <= key < len(self.data) else {}
        return None
    
    def __setitem__(self, key, value):
        """设置列数据"""
        if isinstance(key, str):
            if key not in self.columns:
                self.columns.append(key)
            for i, row in enumerate(self.data):
                if i < len(value):
                    row[key] = value[i]
    
    @property
    def empty(self):
        """检查是否为空"""
        return len(self.data) == 0
    
    def iterrows(self):
        """迭代行数据"""
        for i, row in enumerate(self.data):
            yield i, row
    
    def to_dict(self, orient='records'):
        """转换为字典"""
        if orient == 'records':
            return self.data
        elif orient == 'list':
            return {col: self[col] for col in self.columns}
        return self.data
    
    def select_dtypes(self, include=None):
        """选择特定数据类型的列（简化版）"""
        result_columns = []
        if not self.data:
            return LightweightDataFrame()
        
        sample_row = self.data[0]
        for col in self.columns:
            if col in sample_row:
                value = sample_row[col]
                if include:
                    if 'int64' in include and isinstance(value, int):
                        result_columns.append(col)
                    elif 'float64' in include and isinstance(value, float):
                        result_columns.append(col)
                    elif 'object' in include and isinstance(value, str):
                        result_columns.append(col)
        
        class ColumnSelector:
            def __init__(self, columns):
                self.columns = columns
        
        return ColumnSelector(result_columns)
    
    def memory_usage(self, deep=True):
        """计算内存使用（简化版）"""
        import sys
        total_size = 0
        for row in self.data:
            total_size += sys.getsizeof(row)
            if deep:
                for value in row.values():
                    total_size += sys.getsizeof(value)
        
        class MemoryUsage:
            def __init__(self, size):
                self.size = size
            def sum(self):
                return self.size
        
        return MemoryUsage(total_size)
    
    def copy(self, deep=True):
        """复制DataFrame"""
        import copy as copy_module
        if deep:
            new_data = copy_module.deepcopy(self.data)
        else:
            new_data = self.data.copy()
        
        new_df = LightweightDataFrame(new_data)
        new_df.columns = self.columns.copy()
        return new_df
    
    def equals(self, other):
        """比较两个DataFrame是否相等"""
        if not isinstance(other, LightweightDataFrame):
            return False
        
        if len(self.data) != len(other.data):
            return False
        
        if set(self.columns) != set(other.columns):
            return False
        
        for i, row in enumerate(self.data):
            other_row = other.data[i]
            for col in self.columns:
                if row.get(col) != other_row.get(col):
                    return False
        
        return True


class LightweightDataUtils:
    """轻量化数据处理工具类"""
    
    @staticmethod
    def DataFrame(data=None):
        """创建DataFrame"""
        return LightweightDataFrame(data)
    
    @staticmethod
    def concat(dataframes, ignore_index=True):
        """合并多个DataFrame"""
        if not dataframes:
            return LightweightDataFrame()
        
        all_data = []
        all_columns = set()
        
        for df in dataframes:
            if isinstance(df, LightweightDataFrame):
                all_data.extend(df.data)
                all_columns.update(df.columns)
        
        # 确保所有行都有相同的列
        for row in all_data:
            for col in all_columns:
                if col not in row:
                    row[col] = None
        
        result = LightweightDataFrame(all_data)
        result.columns = list(all_columns)
        return result
    
    @staticmethod
    def to_numeric(series, downcast=None):
        """转换为数值类型"""
        result = []
        for value in series:
            try:
                if isinstance(value, str):
                    if '.' in value:
                        num_value = float(value)
                    else:
                        num_value = int(value)
                else:
                    num_value = value
                
                # 简化的downcast逻辑
                if downcast == 'integer' and isinstance(num_value, (int, float)):
                    result.append(int(num_value))
                elif downcast == 'float' and isinstance(num_value, (int, float)):
                    result.append(float(num_value))
                else:
                    result.append(num_value)
            except (ValueError, TypeError):
                result.append(value)
        
        return result
    
    @staticmethod
    def notna(value):
        """检查值是否不为空"""
        return value is not None and value != '' and str(value).lower() != 'nan'
    
    @staticmethod
    def isna(value):
        """检查值是否为空"""
        return not LightweightDataUtils.notna(value)


# 创建全局实例以模拟pandas接口
pd = LightweightDataUtils()