# -*- mode: python ; coding: utf-8 -*-
# 优化的PyInstaller配置 - 提升启动速度并避免杀毒软件误杀

import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# 排除不必要的模块以减少体积和提升启动速度
excluded_modules = [
    # 网络相关模块（保留socket和ssl，psutil需要）
    'urllib3', 'requests', 'http', 'email', 'ftplib', 'smtplib', 'poplib', 'imaplib',
    'socketserver', 'http.client', 'http.server',
    
    # 测试框架（生产环境不需要）
    'unittest', 'pytest', 'nose', 'doctest', 'test',
    
    # 开发调试工具（生产环境不需要）
    'pdb', 'pydoc', 'trace', 'profile', 'cProfile', 'pstats',
    
    # 数据库相关（项目不使用数据库）
    'sqlite3', 'dbm', 'shelve',
    
    # 文档和标记语言处理（项目不需要）
    'xml', 'html', 'xmlrpc', 'html.parser', 'xml.etree', 'xml.dom', 'xml.sax',
    
    # 构建和分发工具（运行时不需要）
    'distutils', 'setuptools', 'pip', 'pkg_resources',
    
    # 图像和科学计算库（项目已移除这些依赖）
    'PIL', 'matplotlib', 'numpy', 'pandas', 'scipy', 'sklearn',
    'cv2', 'skimage', 'imageio',
    
    # 多媒体处理（项目不需要）
    'wave', 'audioop', 'sunau', 'aifc',
    
    # 加密和安全（项目不需要高级加密）
    'cryptography', 'hashlib', 'hmac', 'secrets',
    
    # 并发和异步（项目使用简单的线程模型）
    'asyncio', 'concurrent', 'multiprocessing', 'queue',
    
    # 国际化（保留locale，subprocess需要）
    'gettext',
    
    # 其他不常用的标准库模块
    'turtle', 'tkinter.dnd', 'tkinter.colorchooser', 'tkinter.font',
    'calendar', 'cmd', 'code', 'codeop', 'compileall',
]

a = Analysis(
    ['../main.py'],
    pathex=[os.path.abspath('..')],  # 添加项目根路径
    binaries=[],
    datas=[
        # 核心配置文件（必须包含）
        ('../config/config.json', '.'),
        ('../sample.json', '.'),
        ('../config/version_info.txt', '.'),
        
        # 日志配置文件（生产环境使用）
        ('../config/logging_config_production.json', '.'),
        
        # 开发环境日志配置（可选，用于调试）
        ('../config/logging_config.json', '.'),
    ],
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
    noarchive=False,  # 保持False以获得更好的启动性能和内存使用
    optimize=2,  # 启用最高级别的Python字节码优化（-OO）
    
    # 启动性能优化配置
    cipher=None,  # 不使用加密以提升启动速度
    
    # 模块加载优化
    collect_all=False,  # 不收集所有子模块，只加载必需的
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
    version_file='../config/version_info.txt',  # 详细版本信息，提升杀毒软件信任度
    
    # 防误杀和兼容性配置
    manifest='../CalcAny.exe.manifest',  # 使用manifest文件提升系统兼容性
    uac_admin=False,  # 不需要管理员权限，降低安全风险
    uac_uiaccess=False,  # 不需要UI访问权限
    
    # 启动和显示优化
    hide_console='hide-early',  # 早期隐藏控制台窗口，提升用户体验
    
    # 代码签名配置（可选，用于进一步提升信任度）
    # codesign_identity='Developer ID Application: Your Name',
    # entitlements_file='entitlements.plist',
)