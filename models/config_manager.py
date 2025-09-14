import json
import os
import logging
from utils.validation_utils import ValidationUtils


class ConfigManager:
    """配置管理器，负责加载和管理应用配置"""
    
    def __init__(self, config_path=None):
        self.config = None
        self.config_path = config_path
        if config_path:
            self.load_config(config_path)
    
    def load_config(self, config_path):
        """加载配置文件，包含错误处理"""
        try:
            # 检查配置文件是否存在
            if not os.path.exists(config_path):
                logging.warning(f"配置文件不存在: {config_path}，将使用默认配置")
                self._load_default_config()
                return
            
            # 检查文件是否可读
            if not os.access(config_path, os.R_OK):
                logging.error(f"无法读取配置文件: {config_path}")
                self._load_default_config()
                return
            
            with open(config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            
            # 验证配置结构
            self._validate_config()
            self.config_path = config_path
            logging.info(f"成功加载配置文件: {config_path}")
            
        except json.JSONDecodeError as e:
            logging.error(f"配置文件JSON格式错误: {e}")
            self._load_default_config()
        except Exception as e:
            logging.error(f"配置文件加载时发生未知错误: {e}")
            self._load_default_config()
    
    def _validate_config(self):
        """验证配置文件的基本结构"""
        if not isinstance(self.config, dict):
            raise ValueError("配置文件格式错误：根节点必须是字典")
        
        # 检查必需的配置项
        required_keys = ['document_info_fields', 'factor_categories', 'display_names']
        for key in required_keys:
            if key not in self.config:
                logging.warning(f"配置文件缺少必需项: {key}")
    
    def _load_default_config(self):
        """加载默认配置"""
        self.config = {
            "document_info_fields": [
                "calcItemName",
                "calcItemCode",
                "calcItemType",
                "calcItemUnit",
                "calcItemDesc"
            ],
            "factor_categories": {
                "人工": ["人工费"],
                "材料": ["材料费"],
                "机械": ["机械费"],
                "其他": ["其他费用"]
            },
            "display_names": {
                "calcItemName": "项目名称",
                "calcItemCode": "项目编码",
                "calcItemType": "项目类型",
                "calcItemUnit": "计量单位",
                "calcItemDesc": "项目描述"
            },
            "hierarchy_levels": {
                "total": {"name": "合计", "enabled": True},
                "boq": {"name": "清单", "enabled": True},
                "model": {"name": "模型", "enabled": True},
                "part": {"name": "构件", "enabled": True}
            },
            "table_columns": [
                {"field": "calcItemName", "display_name": "项目名称", "width": 200},
                {"field": "calcItemCode", "display_name": "项目编码", "width": 150},
                {"field": "calcItemType", "display_name": "项目类型", "width": 100},
                {"field": "calcItemUnit", "display_name": "计量单位", "width": 100}
            ]
        }
        logging.info("已加载默认配置")
    
    def get_document_info_fields(self):
        """获取文档信息字段列表"""
        if not self.config:
            return []
        return self.config.get('document_info_fields', [])
    
    def get_factor_categories(self):
        """获取因子分类配置"""
        if not self.config:
            return {}
        return self.config.get('factor_categories', {})
    
    def get_display_names(self):
        """获取字段显示名称映射"""
        if not self.config:
            return {}
        return self.config.get('display_names', {})
    
    def get_display_name(self, field_name):
        """获取单个字段的显示名称"""
        display_names = self.get_display_names()
        return display_names.get(field_name, field_name)
    
    def get_sub_factor_basic_info(self, sub_factor_name):
        """获取子因子的基本信息字段"""
        if not self.config:
            return []
        
        # 从因子分类中查找子因子的配置
        factor_categories = self.get_factor_categories()
        for category, factors in factor_categories.items():
            for factor in factors:
                if factor.get('name') == sub_factor_name:
                    return factor.get('basic_info', [])
        
        return []
    
    def get_default_hierarchy_level(self):
        """获取默认层次级别"""
        if not self.config:
            return 'total'
        return self.config.get('default_hierarchy_level', 'total')
    
    def get_data_table_columns(self, level=None, factor_name=None):
        """获取数据表格列配置"""
        if not self.config:
            return []
        
        # 如果指定了因子名称和层级，尝试获取因子特定的列配置
        if factor_name and level:
            factor_categories = self.get_factor_categories()
            for category, factors in factor_categories.items():
                for factor in factors:
                    if factor.get('name') == factor_name:
                        table_info = factor.get('table_info', {})
                        if isinstance(table_info, dict) and level in table_info:
                            return table_info[level]
        
        # 返回默认表格列配置
        return self.config.get('table_columns', [])
    
    def get_hierarchy_levels(self):
        """获取层次级别配置"""
        if not self.config:
            return {}
        return self.config.get('hierarchy_levels', {})
    
    def get_enabled_hierarchy_levels(self):
        """获取启用的层次级别列表"""
        if not self.config:
            return []
        return self.config.get('enabled_hierarchy_levels', [])
    
    def get_data_hierarchy_name(self, level):
        """获取数据层次对应的中文显示名称"""
        if not self.config:
            return level
        
        hierarchy_names = self.config.get('data_hierarchy_names', {})
        return hierarchy_names.get(level, level)
    
    def get_table_columns(self):
        """获取表格列配置"""
        if not self.config:
            return []
        return self.config.get('table_columns', [])
    
    def reload_config(self):
        """重新加载配置文件"""
        if self.config_path:
            self.load_config(self.config_path)
        else:
            logging.warning("无法重新加载配置：配置文件路径未设置")
    
    def _validate_input(self, value, expected_type, name="参数"):
        """通用输入验证方法"""
        try:
            ValidationUtils.validate_input(value, name, expected_type)
            return True
        except (ValueError, TypeError) as e:
            logger = logging.getLogger('CalcAnyApp')
            logger.error(f"输入验证失败 - {name}: {e}")
            return False
    
    def _safe_get_value(self, data, key, default=""):
        """安全获取字典值的通用方法"""
        return ValidationUtils.safe_get_value(data, key, default)