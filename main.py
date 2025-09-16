#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CalcAny - 专业数据计算分析工具
主程序入口
"""

# 首先应用启动优化
from startup_optimizer import apply_startup_optimizations, print_startup_summary

# 应用启动优化
optimizer = apply_startup_optimizations()

# 导入主控制器
from controllers import AppController

def main():
    """主函数"""
    try:
        # 打印启动信息
        print_startup_summary()
        
        # 创建并运行应用
        app = AppController()
        app.run()
        
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    except Exception as e:
        print(f"程序运行出错: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # 清理资源
        import gc
        gc.collect()

if __name__ == "__main__":
    main()