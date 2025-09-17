import logging
import os
import sys
import json
from datetime import datetime


def load_logging_config():
    """加载日志配置文件"""
    try:
        # 确定配置文件路径
        if getattr(sys, 'frozen', False):
            # EXE环境：配置文件在EXE同目录
            config_path = os.path.join(os.path.dirname(sys.executable), 'logging_config.json')
        else:
            # 开发环境：配置文件在config目录
            config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'logging_config.json')
        
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # 返回默认配置
            return {
                "enable_file_logging": True,
                "log_level": "INFO",
                "log_format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "console_logging": True,
                "log_file_name_format": "app_{date}.log"
            }
    except Exception as e:
        print(f"加载日志配置失败，使用默认配置: {e}")
        return {
            "enable_file_logging": True,
            "log_level": "INFO",
            "log_format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "console_logging": True,
            "log_file_name_format": "app_{date}.log"
        }


def setup_logging():
    """设置日志系统"""
    # 加载日志配置
    config = load_logging_config()
    
    # 获取根日志记录器并清除现有处理器
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.setLevel(getattr(logging, config['log_level']))
    
    # 创建格式化器
    formatter = logging.Formatter(config['log_format'])
    
    # 根据配置决定是否创建文件处理器
    if config['enable_file_logging']:
        # 创建logs目录 - 适配EXE环境
        if getattr(sys, 'frozen', False):
            # EXE环境：logs目录在EXE同目录
            log_dir = os.path.join(os.path.dirname(sys.executable), 'logs')
        else:
            # 开发环境：logs目录在项目根目录
            log_dir = 'logs'
        
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # 设置日志文件名（包含日期）
        log_filename = os.path.join(log_dir, config['log_file_name_format'].format(date=datetime.now().strftime("%Y%m%d")))
        
        # 创建文件处理器
        file_handler = logging.FileHandler(log_filename, encoding='utf-8')
        file_handler.setLevel(getattr(logging, config['log_level']))
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    
    # 根据配置决定是否创建控制台处理器
    if config.get('console_logging', True):
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, config['log_level']))
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)
    
    # 创建应用专用的logger
    logger = logging.getLogger('CalcAnyApp')
    return logger