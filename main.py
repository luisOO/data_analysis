#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CalcAny - 专业数据计算分析工具
主程序入口
"""

# 首先应用启动优化
from scripts.startup_optimizer import apply_startup_optimizations, print_startup_summary

# 应用启动优化
optimizer = apply_startup_optimizations()

# 导入主控制器
from controllers import AppController

def main():
    """主函数"""
    try:
        print("CalcAny 程序启动中...")
        
        # 打印启动信息
        print_startup_summary()
        print("启动信息打印完成")
        
        # 创建并运行应用
        print("正在创建应用控制器...")
        app = AppController()
        print("应用控制器创建成功，开始运行...")
        app.run()
        print("应用程序正常退出")
        
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    except Exception as e:
        print(f"程序运行出错: {e}")
        import traceback
        traceback.print_exc()
        # 将错误写入文件
        try:
            import os
            error_file = os.path.join(os.path.dirname(__file__), 'error.log')
            with open(error_file, 'w', encoding='utf-8') as f:
                f.write(f"程序运行出错: {e}\n")
                f.write(traceback.format_exc())
            print(f"错误信息已写入: {error_file}")
        except:
            pass
    finally:
        # 清理资源
        import gc
        gc.collect()

if __name__ == "__main__":
    main()