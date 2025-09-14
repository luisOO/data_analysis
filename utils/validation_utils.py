# -*- coding: utf-8 -*-
"""
验证工具函数模块
提供输入验证和数据安全获取功能
"""


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