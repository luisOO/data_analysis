#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
优化的EXE打包脚本
提升启动速度并避免杀毒软件误杀
"""

import os
import sys
import shutil
import subprocess
import time
from pathlib import Path

def clean_build_dirs():
    """清理之前的构建目录"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"清理目录: {dir_name}")
            shutil.rmtree(dir_name)
    
    # 清理.pyc文件
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.pyc'):
                os.remove(os.path.join(root, file))

def optimize_python_cache():
    """优化Python字节码缓存"""
    print("优化Python字节码缓存...")
    subprocess.run([sys.executable, '-m', 'compileall', '.'], 
                  capture_output=True)

def create_manifest_file():
    """创建Windows manifest文件以提升兼容性"""
    manifest_content = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
  <assemblyIdentity
    version="1.2.13.0"
    processorArchitecture="*"
    name="CalcAny.exe"
    type="win32"
  />
  <description>CalcAny Data Analysis Tool</description>
  <dependency>
    <dependentAssembly>
      <assemblyIdentity
        type="win32"
        name="Microsoft.Windows.Common-Controls"
        version="6.0.0.0"
        processorArchitecture="*"
        publicKeyToken="6595b64144ccf1df"
        language="*"
      />
    </dependentAssembly>
  </dependency>
  <trustInfo xmlns="urn:schemas-microsoft-com:asm.v2">
    <security>
      <requestedPrivileges>
        <requestedExecutionLevel level="asInvoker" uiAccess="false"/>
      </requestedPrivileges>
    </security>
  </trustInfo>
  <compatibility xmlns="urn:schemas-microsoft-com:compatibility.v1">
    <application>
      <supportedOS Id="{e2011457-1546-43c5-a5fe-008deee3d3f0}"/>  <!-- Vista -->
      <supportedOS Id="{35138b9a-5d96-4fbd-8e2d-a2440225f93a}"/>  <!-- Win7 -->
      <supportedOS Id="{4a2f28e3-53b9-4441-ba9c-d69d4a4a6e38}"/>  <!-- Win8 -->
      <supportedOS Id="{1f676c76-80e1-4239-95bb-83d0f6d0da78}"/>  <!-- Win8.1 -->
      <supportedOS Id="{8e0f7a12-bfb3-4fe8-b9a5-48fd50a15a9a}"/>  <!-- Win10 -->
    </application>
  </compatibility>
</assembly>'''
    
    with open('CalcAny.exe.manifest', 'w', encoding='utf-8') as f:
        f.write(manifest_content)
    print("已创建manifest文件")

def build_exe():
    """执行优化的EXE构建"""
    print("开始构建优化的EXE文件...")
    
    # 切换到项目根目录执行构建
    original_dir = os.getcwd()
    project_root = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(project_root)  # 回到项目根目录
    os.chdir(project_root)
    
    # PyInstaller命令参数
    cmd = [
        'pyinstaller',
        '--clean',  # 清理临时文件
        '--noconfirm',  # 不询问覆盖
        '--log-level=WARN',  # 减少日志输出
        'scripts/calc_any.spec'
    ]
    
    try:
        start_time = time.time()
        result = subprocess.run(cmd, capture_output=True, text=True)
        build_time = time.time() - start_time
        
        if result.returncode == 0:
            print(f"✅ 构建成功! 耗时: {build_time:.2f}秒")
            
            # 检查生成的文件
            exe_path = Path('dist/CalcAny.exe')
            if exe_path.exists():
                size_mb = exe_path.stat().st_size / (1024 * 1024)
                print(f"📦 EXE文件大小: {size_mb:.2f} MB")
                print(f"📍 文件位置: {exe_path.absolute()}")
            
            return True
        else:
            print("❌ 构建失败!")
            print("错误输出:")
            print(result.stderr)
            return False
    finally:
        # 恢复原始工作目录
        os.chdir(original_dir)

def post_build_optimization():
    """构建后优化"""
    exe_path = Path('dist/CalcAny.exe')
    if not exe_path.exists():
        return
    
    print("执行构建后优化...")
    
    # 复制必要的配置文件到dist目录
    config_files = [
        ('config/config.json', 'config.json'),
        ('sample.json', 'sample.json'),
        ('config/logging_config_production.json', 'logging_config.json')  # 使用生产环境日志配置
    ]
    for src_file, dst_file in config_files:
        if os.path.exists(src_file):
            shutil.copy2(src_file, f'dist/{dst_file}')
            print(f"已复制配置文件: {src_file} -> dist/{dst_file}")
    
    # 特别提示日志配置
    print("📝 已使用生产环境日志配置（默认禁用文件日志）")
    
    # 生产环境不创建logs目录（根据配置动态创建）
    print("📝 生产环境不预创建logs目录，将根据日志配置动态创建")
    
    # 清理临时文件
    if os.path.exists('CalcAny.exe.manifest'):
        os.remove('CalcAny.exe.manifest')

def main():
    """主函数"""
    print("🚀 开始优化EXE构建流程")
    print("=" * 50)
    
    try:
        # 1. 清理构建目录
        clean_build_dirs()
        
        # 2. 优化Python缓存
        optimize_python_cache()
        
        # 3. 创建manifest文件
        create_manifest_file()
        
        # 4. 构建EXE
        if build_exe():
            # 5. 构建后优化
            post_build_optimization()
            
            print("\n🎉 优化构建完成!")
            print("\n📋 优化特性:")
            print("  ✅ 启用最高级别字节码优化")
            print("  ✅ 排除不必要的模块")
            print("  ✅ 关闭UPX压缩避免误杀")
            print("  ✅ 添加详细版本信息")
            print("  ✅ 优化启动性能")
            print("  ✅ 提升杀毒软件兼容性")
            
            print("\n🔧 使用建议:")
            print("  1. 首次运行可能需要几秒钟初始化")
            print("  2. 建议添加到杀毒软件白名单")
            print("  3. 如遇到问题，请检查logs目录下的日志")
        else:
            print("\n❌ 构建失败，请检查错误信息")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ 构建过程中出现错误: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()