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
    
    # 配置日志格式
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename, encoding='utf-8'),
            logging.StreamHandler()  # 同时输出到控制台
        ]
    )
    
    # 创建应用专用的logger
    logger = logging.getLogger('CalcAnyApp')
    return logger