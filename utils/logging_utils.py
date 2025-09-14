# -*- coding: utf-8 -*-
"""
日志工具函数模块
提供日志记录和错误处理功能
"""

import logging


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