import logging
import os
import sys
from datetime import datetime


def setup_logging():
    """设置日志系统"""
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
    log_filename = os.path.join(log_dir, f'app_{datetime.now().strftime("%Y%m%d")}.log')
    
    # 获取根日志记录器并清除现有处理器
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.setLevel(logging.INFO)
    
    # 创建格式化器
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # 创建文件处理器
    file_handler = logging.FileHandler(log_filename, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)
    
    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # 创建应用专用的logger
    logger = logging.getLogger('CalcAnyApp')
    return logger