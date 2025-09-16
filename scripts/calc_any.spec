# -*- mode: python ; coding: utf-8 -*-
# 优化的PyInstaller配置 - 提升启动速度并避免杀毒软件误杀

import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# 排除不必要的模块以减少体积和提升启动速度
excluded_modules = [
    # 网络相关（如果不需要）
    'urllib3', 'requests', 'http', 'email',
    # 测试框架
    'unittest', 'pytest', 'nose',
    # 开发工具
    'pdb', 'doctest', 'pydoc',
    # 不常用的标准库
    'sqlite3', 'xml', 'html', 'distutils',
    # 图像处理（如果不需要）
    'PIL', 'matplotlib', 'numpy',
    # 其他大型库
    'pandas', 'scipy', 'sklearn',
]

a = Analysis(
    ['../main.py'],
    pathex=[os.path.abspath('..')],  # 添加项目根路径
    binaries=[],
    datas=[
        ('../config/config.json', '.'),
        ('../sample.json', '.'),
    ] + ([('../logs', 'logs')] if os.path.exists('../logs') else []),
    hiddenimports=[
        # 核心GUI框架（按需加载）
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'tkinter.filedialog',
        'tkinter.simpledialog',
        
        # 必需的第三方依赖
        'psutil',
        'tksheet',
        
        # 核心标准库模块
        'json',
        'logging',
        'decimal',  # 高精度计算
        'functools',  # lru_cache等
        'typing',  # 类型注解
        
        # 项目核心模块
        'config_manager_ui',
        'controllers.app_controller',
        'controllers.logging_setup',
        'models.config_manager',
        'models.data_manager',
        'views.main_app_view',
        'views.document_info_view',
        'views.factor_view',
        'views.sub_factor_detail_view',
        'utils.validation_utils',
        'utils.data_utils',
        'utils.clipboard_utils',
        'utils.logging_utils',
        'utils.lightweight_data',
    ],
    hookspath=[],
    hooksconfig={
        # 优化tkinter加载
        'gi': {
            'module-versions': {},
        },
    },
    runtime_hooks=[],
    excludes=excluded_modules,  # 排除不必要的模块
    noarchive=False,  # 保持False以获得更好的启动性能
    optimize=2,  # 启用最高级别的Python字节码优化
)
# 优化PYZ配置
pyz = PYZ(
    a.pure,
    cipher=None,  # 不使用加密以提升启动速度
)

# 创建优化的EXE配置
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='CalcAny',
    debug=False,  # 生产环境关闭调试
    bootloader_ignore_signals=False,
    strip=True,  # 启用strip以减少文件大小
    upx=False,  # 关闭UPX压缩避免杀毒软件误报
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 窗口应用
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # 可添加图标: 'assets/icon.ico'
    version_file='../config/version_info.txt',  # 版本信息有助于避免误杀
    
    # 启动优化选项
    manifest=None,  # 可添加manifest文件提升兼容性
    uac_admin=False,  # 不需要管理员权限
    uac_uiaccess=False,  # 不需要UI访问权限
    
    # 安全和兼容性选项
    hide_console='hide-early',  # 早期隐藏控制台窗口
)