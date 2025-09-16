#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
启动优化模块
提升应用程序启动速度和运行性能
"""

import os
import sys
import gc
import threading
import time
from functools import lru_cache
from typing import Optional

class StartupOptimizer:
    """启动优化器"""
    
    def __init__(self):
        self.optimization_enabled = True
        self.startup_time = time.time()
        
    def optimize_gc(self):
        """优化垃圾回收"""
        if not self.optimization_enabled:
            return
            
        # 设置垃圾回收阈值
        gc.set_threshold(700, 10, 10)
        
        # 禁用自动垃圾回收，手动控制
        gc.disable()
        
        # 执行一次完整的垃圾回收
        gc.collect()
        
    def optimize_imports(self):
        """优化模块导入"""
        if not self.optimization_enabled:
            return
            
        # 预加载核心模块
        try:
            import tkinter
            import json
            import logging
            import decimal
        except ImportError:
            pass
    
    def optimize_threading(self):
        """优化线程设置"""
        if not self.optimization_enabled:
            return
            
        # 设置线程栈大小
        threading.stack_size(1024 * 1024)  # 1MB
        
    def setup_memory_optimization(self):
        """设置内存优化"""
        if not self.optimization_enabled:
            return
            
        # 设置递归限制
        sys.setrecursionlimit(1500)
        
        # 优化字符串intern
        sys.intern('__main__')
        sys.intern('__file__')
        
    def optimize_path(self):
        """优化路径设置"""
        if not self.optimization_enabled:
            return
            
        # 确保当前目录在Python路径中
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
    
    @lru_cache(maxsize=128)
    def get_config_path(self, filename: str) -> str:
        """缓存配置文件路径"""
        return os.path.join(os.path.dirname(__file__), filename)
    
    def setup_logging_optimization(self):
        """优化日志设置"""
        if not self.optimization_enabled:
            return
            
        import logging
        
        # 设置日志级别以减少I/O（但保留INFO级别用于应用日志）
        # logging.getLogger().setLevel(logging.WARNING)  # 注释掉，让应用自己管理日志级别
        
        # 禁用不必要的日志记录器
        logging.getLogger('tkinter').setLevel(logging.ERROR)
        logging.getLogger('PIL').setLevel(logging.ERROR)
    
    def enable_fast_startup(self):
        """启用快速启动模式"""
        if not self.optimization_enabled:
            return
            
        # 设置环境变量以优化启动
        os.environ['PYTHONOPTIMIZE'] = '2'
        os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
        
        # 禁用一些不必要的功能
        if hasattr(sys, 'setdlopenflags'):
            import ctypes
            sys.setdlopenflags(ctypes.RTLD_LAZY)
    
    def delayed_gc_enable(self, delay: float = 2.0):
        """延迟启用垃圾回收"""
        def enable_gc():
            time.sleep(delay)
            gc.enable()
            gc.collect()
            
        thread = threading.Thread(target=enable_gc, daemon=True)
        thread.start()
    
    def apply_all_optimizations(self):
        """应用所有优化"""
        try:
            self.enable_fast_startup()
            self.optimize_path()
            self.optimize_gc()
            self.optimize_imports()
            self.optimize_threading()
            self.setup_memory_optimization()
            self.setup_logging_optimization()
            
            # 延迟启用垃圾回收
            self.delayed_gc_enable()
            
            startup_duration = time.time() - self.startup_time
            print(f"启动优化完成，耗时: {startup_duration:.3f}秒")
            
        except Exception as e:
            print(f"启动优化警告: {e}")
            # 即使优化失败也不影响程序运行
    
    def get_memory_usage(self) -> dict:
        """获取内存使用情况"""
        try:
            import psutil
            process = psutil.Process()
            memory_info = process.memory_info()
            
            return {
                'rss': memory_info.rss / 1024 / 1024,  # MB
                'vms': memory_info.vms / 1024 / 1024,  # MB
                'percent': process.memory_percent()
            }
        except ImportError:
            return {'error': 'psutil not available'}
    
    def print_startup_info(self):
        """打印启动信息"""
        startup_duration = time.time() - self.startup_time
        memory_usage = self.get_memory_usage()
        
        try:
            print(f"\n[启动] CalcAny 启动完成")
            print(f"[时间] 启动时间: {startup_duration:.3f}秒")
            
            if 'error' not in memory_usage:
                print(f"[内存] 内存使用: {memory_usage['rss']:.1f}MB ({memory_usage['percent']:.1f}%)")
            
            print(f"[系统] Python版本: {sys.version.split()[0]}")
            print(f"[路径] 工作目录: {os.getcwd()}")
            print("-" * 50)
        except UnicodeEncodeError:
            # 如果遇到编码问题，使用简化输出
            print("\nCalcAny startup completed")
            print(f"Startup time: {startup_duration:.3f}s")
            if 'error' not in memory_usage:
                print(f"Memory usage: {memory_usage['rss']:.1f}MB")
            print(f"Python version: {sys.version.split()[0]}")
            print("-" * 50)

# 全局优化器实例
_optimizer = None

def get_optimizer() -> StartupOptimizer:
    """获取优化器实例"""
    global _optimizer
    if _optimizer is None:
        _optimizer = StartupOptimizer()
    return _optimizer

def apply_startup_optimizations():
    """应用启动优化（入口函数）"""
    optimizer = get_optimizer()
    optimizer.apply_all_optimizations()
    return optimizer

def print_startup_summary():
    """打印启动摘要"""
    optimizer = get_optimizer()
    optimizer.print_startup_info()

if __name__ == '__main__':
    # 测试启动优化
    optimizer = apply_startup_optimizations()
    print_startup_summary()