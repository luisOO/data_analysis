# -*- coding: utf-8 -*-
"""
剪贴板工具函数模块
提供剪贴板操作功能
"""

import logging


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