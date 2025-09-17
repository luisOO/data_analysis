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

def clean_build_dirs(project_root=None):
    """清理之前的构建目录"""
    if project_root is None:
        project_root = get_project_root()
    
    print(f"[INFO] 在项目根目录清理构建文件: {project_root}")
    
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        dir_path = project_root / dir_name
        if dir_path.exists():
            print(f"清理目录: {dir_path}")
            shutil.rmtree(str(dir_path))
    
    # 清理.pyc文件
    for root, dirs, files in os.walk(str(project_root)):
        for file in files:
            if file.endswith('.pyc'):
                pyc_path = os.path.join(root, file)
                try:
                    os.remove(pyc_path)
                    print(f"清理.pyc文件: {pyc_path}")
                except OSError as e:
                    print(f"[WARNING] 无法删除.pyc文件 {pyc_path}: {e}")

def optimize_python_cache(project_root=None):
    """优化Python字节码缓存"""
    if project_root is None:
        project_root = get_project_root()
    
    print(f"优化Python字节码缓存: {project_root}")
    result = subprocess.run([sys.executable, '-m', 'compileall', str(project_root)], 
                          capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"[WARNING] 字节码编译警告: {result.stderr}")
    else:
        print("[SUCCESS] 字节码缓存优化完成")

def create_manifest_file(project_root=None):
    """创建Windows应用程序清单文件，提升系统兼容性和防误杀"""
    manifest_content = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
  <assemblyIdentity
    version="1.2.13.0"
    processorArchitecture="*"
    name="CalcAny.DataAnalysisTool"
    type="win32"
  />
  <description>CalcAny - 专业数据分析可视化工具</description>
  
  <!-- 依赖Windows通用控件，提升界面兼容性 -->
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
  
  <!-- 安全权限配置，不需要管理员权限 -->
  <trustInfo xmlns="urn:schemas-microsoft-com:asm.v2">
    <security>
      <requestedPrivileges xmlns="urn:schemas-microsoft-com:asm.v3">
        <requestedExecutionLevel level="asInvoker" uiAccess="false"/>
      </requestedPrivileges>
    </security>
  </trustInfo>
  
  <!-- 系统兼容性声明，支持Windows 7到Windows 11 -->
  <compatibility xmlns="urn:schemas-microsoft-com:compatibility.v1">
    <application>
      <supportedOS Id="{35138b9a-5d96-4fbd-8e2d-a2440225f93a}"/>  <!-- Windows 7 -->
      <supportedOS Id="{4a2f28e3-53b9-4441-ba9c-d69d4a4a6e38}"/>  <!-- Windows 8 -->
      <supportedOS Id="{1f676c76-80e1-4239-95bb-83d0f6d0da78}"/>  <!-- Windows 8.1 -->
      <supportedOS Id="{8e0f7a12-bfb3-4fe8-b9a5-48fd50a15a9a}"/>  <!-- Windows 10 -->
      <supportedOS Id="{8e0f7a12-bfb3-4fe8-b9a5-48fd50a15a9b}"/>  <!-- Windows 11 -->
    </application>
  </compatibility>
  
  <!-- DPI感知配置，提升高分辨率显示效果 -->
  <application xmlns="urn:schemas-microsoft-com:asm.v3">
    <windowsSettings>
      <dpiAware xmlns="http://schemas.microsoft.com/SMI/2005/WindowsSettings">true</dpiAware>
      <dpiAwareness xmlns="http://schemas.microsoft.com/SMI/2016/WindowsSettings">PerMonitorV2</dpiAwareness>
      <longPathAware xmlns="http://schemas.microsoft.com/SMI/2016/WindowsSettings">true</longPathAware>
    </windowsSettings>
  </application>
</assembly>'''
    
    if project_root is None:
        project_root = get_project_root()
    
    manifest_path = project_root / 'CalcAny.exe.manifest'
    with open(str(manifest_path), 'w', encoding='utf-8') as f:
        f.write(manifest_content)
    print(f"[SUCCESS] 已创建优化的manifest文件: {manifest_path}")

def get_project_root():
    """获取项目根目录的绝对路径"""
    # 从当前脚本位置向上查找，直到找到包含main.py的目录
    current_path = Path(__file__).resolve().parent
    
    # 向上查找项目根目录（包含main.py的目录）
    while current_path.parent != current_path:  # 避免到达文件系统根目录
        if (current_path / 'main.py').exists():
            return current_path
        current_path = current_path.parent
    
    # 如果没找到，使用脚本所在目录的上级目录作为默认值
    script_dir = Path(__file__).resolve().parent
    return script_dir.parent

def validate_project_structure(project_root):
    """验证项目结构是否完整"""
    required_files = [
        'main.py',
        'scripts/calc_any.spec',
        'config/config.json'
    ]
    
    missing_files = []
    for file_path in required_files:
        full_path = project_root / file_path
        if not full_path.exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"[ERROR] 项目结构不完整，缺少以下文件:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        print(f"[INFO] 当前项目根目录: {project_root}")
        return False
    
    return True

def build_exe():
    """执行优化的EXE构建"""
    print("开始构建优化的EXE文件...")
    
    # 获取项目根目录
    project_root = get_project_root()
    print(f"[INFO] 项目根目录: {project_root}")
    
    # 验证项目结构
    if not validate_project_structure(project_root):
        return False
    
    # 切换到项目根目录执行构建
    original_dir = os.getcwd()
    os.chdir(project_root)
    
    # 构建spec文件的绝对路径
    spec_file = project_root / 'scripts' / 'calc_any.spec'
    
    # PyInstaller命令参数
    cmd = [
        'pyinstaller',
        '--clean',  # 清理临时文件
        '--noconfirm',  # 不询问覆盖
        '--log-level=WARN',  # 减少日志输出
        str(spec_file)  # 使用绝对路径
    ]
    
    try:
        start_time = time.time()
        result = subprocess.run(cmd, capture_output=True, text=True)
        build_time = time.time() - start_time
        
        if result.returncode == 0:
            print(f"[SUCCESS] 构建成功! 耗时: {build_time:.2f}秒")
            
            # 检查生成的文件
            exe_path = Path('dist/CalcAny.exe')
            if exe_path.exists():
                size_mb = exe_path.stat().st_size / (1024 * 1024)
                print(f"[INFO] EXE文件大小: {size_mb:.2f} MB")
                print(f"[INFO] 文件位置: {exe_path.absolute()}")
            
            return True
        else:
            print("[ERROR] 构建失败!")
            print("错误输出:")
            print(result.stderr)
            return False
    finally:
        # 恢复原始工作目录
        os.chdir(original_dir)

def post_build_optimization():
    """构建后优化"""
    # 获取项目根目录
    project_root = get_project_root()
    
    # 检查dist目录和exe文件
    dist_dir = project_root / 'dist'
    exe_path = dist_dir / 'CalcAny.exe'
    
    if not exe_path.exists():
        print(f"[ERROR] EXE文件不存在: {exe_path}")
        return
    
    print("执行构建后优化...")
    
    # 确保dist目录存在
    dist_dir.mkdir(exist_ok=True)
    
    # 复制必要的配置文件到dist目录
    config_files = [
        # 核心配置文件（必须存在）
        ('config/config.json', 'config.json'),
        ('sample.json', 'sample.json'),
        ('config/version_info.txt', 'version_info.txt'),
        
        # 日志配置文件（生产环境优先）
        ('config/logging_config_production.json', 'logging_config.json'),
        
        # 开发环境日志配置（备用，用于调试）
        ('config/logging_config.json', 'logging_config_dev.json'),
    ]
    
    copied_files = []
    for src_file, dst_file in config_files:
        src_path = project_root / src_file
        dst_path = dist_dir / dst_file
        
        if src_path.exists():
            shutil.copy2(str(src_path), str(dst_path))
            copied_files.append(f"{src_file} -> dist/{dst_file}")
            print(f"[SUCCESS] 已复制配置文件: {src_file} -> dist/{dst_file}")
        else:
            print(f"[WARNING] 配置文件不存在，跳过: {src_file}")
            print(f"   完整路径: {src_path}")
    
    print(f"\n[INFO] 共复制 {len(copied_files)} 个配置文件")
    
    # 特别提示日志配置
    print("[INFO] 已使用生产环境日志配置（默认禁用文件日志）")
    
    # 生产环境不创建logs目录（根据配置动态创建）
    print("[INFO] 生产环境不预创建logs目录，将根据日志配置动态创建")
    
    # 清理临时文件
    manifest_path = project_root / 'CalcAny.exe.manifest'
    if manifest_path.exists():
        os.remove(str(manifest_path))
        print(f"[SUCCESS] 已清理临时manifest文件: {manifest_path}")

def main():
    """主函数"""
    print("[INFO] 开始优化EXE构建流程")
    print("=" * 50)
    
    try:
        # 获取项目根目录
        project_root = get_project_root()
        print(f"[INFO] 项目根目录: {project_root}")
        
        # 验证项目结构
        if not validate_project_structure(project_root):
            print("[ERROR] 项目结构验证失败，无法继续构建")
            sys.exit(1)
        
        # 1. 清理构建目录
        clean_build_dirs(project_root)
        
        # 2. 优化Python缓存
        optimize_python_cache(project_root)
        
        # 3. 创建manifest文件
        create_manifest_file(project_root)
        
        # 4. 构建EXE
        if build_exe():
            # 5. 构建后优化
            post_build_optimization()
            
            print("\n[SUCCESS] 优化构建完成!")
            print("\n[INFO] 优化特性:")
            print("  [+] 启用最高级别字节码优化")
            print("  [+] 排除不必要的模块")
            print("  [+] 关闭UPX压缩避免误杀")
            print("  [+] 添加详细版本信息")
            print("  [+] 优化启动性能")
            print("  [+] 提升杀毒软件兼容性")
            
            print("\n[INFO] 使用建议:")
            print("  1. 首次运行可能需要几秒钟初始化")
            print("  2. 建议添加到杀毒软件白名单")
            print("  3. 如遇到问题，请检查logs目录下的日志")
        else:
            print("\n[ERROR] 构建失败，请检查错误信息")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n[ERROR] 构建过程中出现错误: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()