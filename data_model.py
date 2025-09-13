import json
import pandas as pd
import os
import logging
import gc
import psutil
from functools import lru_cache

class ConfigManager:
    def __init__(self, config_path='config.json'):
        self.config = {}
        self.config_path = config_path
        self._load_config()
    
    def _load_config(self):
        """加载配置文件，包含错误处理"""
        try:
            # 检查配置文件是否存在
            if not os.path.exists(self.config_path):
                raise FileNotFoundError(f"配置文件不存在: {self.config_path}")
            
            # 检查文件是否可读
            if not os.access(self.config_path, os.R_OK):
                raise PermissionError(f"无法读取配置文件: {self.config_path}")
            
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
                
            # 验证配置文件的基本结构
            self._validate_config()
            
            logging.info(f"配置文件加载成功: {self.config_path}，包含 {len(self.config)} 个配置项")
            
        except FileNotFoundError as e:
            logging.error(f"配置文件加载失败: {e}")
            self._load_default_config()
        except json.JSONDecodeError as e:
            logging.error(f"配置文件JSON格式错误: {e}")
            self._load_default_config()
        except PermissionError as e:
            logging.error(f"配置文件权限错误: {e}")
            self._load_default_config()
        except Exception as e:
            logging.error(f"配置文件加载时发生未知错误: {e}")
            self._load_default_config()
    
    def _validate_config(self):
        """验证配置文件的基本结构"""
        required_keys = ['document_info_fields', 'factor_categories', 'display_names', 'data_hierarchy_names']
        for key in required_keys:
            if key not in self.config:
                logging.warning(f"配置文件缺少必需的键: {key}")
        
        # 验证factor_categories结构
        if 'factor_categories' in self.config:
            factor_categories = self.config['factor_categories']
            if isinstance(factor_categories, dict):
                for category_name, category_data in factor_categories.items():
                    if isinstance(category_data, list):
                        # 新格式：数组结构
                        for factor in category_data:
                            if not isinstance(factor, dict) or 'name' not in factor:
                                logging.warning(f"因子配置格式错误: {factor}")
                            # 验证basic_info是列表
                            if 'basic_info' in factor and not isinstance(factor['basic_info'], list):
                                logging.warning(f"basic_info应为列表格式: {factor['name']}")
    
    def _load_default_config(self):
        """加载默认配置"""
        logging.info("使用默认配置")
        self.config = {
            'document_info_fields': ['businessCode', 'description', 'unit'],
            'factor_categories': {
                '基础因子': [
                    {
                        'name': '收入因子',
                        'basic_info': ['businessCode', 'netSalesRevenue', 'description', 'unit', 'category'],
                        'table_info': [['total', 'boq', 'model', 'part'], ['businessCode', 'netSalesRevenue', 'description']]
                    },
                    {
                        'name': '成本因子',
                        'basic_info': ['businessCode', 'totalCost', 'description', 'unit', 'category'],
                        'table_info': [['total', 'boq', 'model', 'part'], ['businessCode', 'totalCost', 'description']]
                    }
                ]
            },
            'display_names': {
                'businessCode': '业务编码',
                'netSalesRevenue': '净销售收入',
                'totalCost': '总成本',
                'description': '描述',
                'unit': '单位',
                'category': '类别',
                '收入因子': '收入因子',
                '成本因子': '成本因子'
            },
            'data_hierarchy_names': {
                'total': '总计',
                'boq': '清单项',
                'model': '模型构件',
                'part': '零部件'
            },
            'enabled_hierarchy_levels': ['total', 'boq', 'model', 'part'],
            'default_hierarchy_level': 'part'
        }

    def get_document_info_fields(self):
        return self.config.get('document_info_fields', [])

    def get_factor_categories(self):
        return self.config.get('factor_categories', {})

    def get_sub_factor_basic_info(self, factor_name=None):
        # 返回配置中的basic_info字段列表
        if factor_name:
            factor_categories = self.config.get('factor_categories', {})
            for category, factors in factor_categories.items():
                for factor in factors:
                    if factor.get('name') == factor_name:
                        return factor.get('basic_info', [])
        # 否则返回空列表
        return []

    def get_data_table_columns(self, level, factor_name=None):
        # 如果提供了因子名称，在因子分类中查找
        if factor_name:
            factor_categories = self.config.get('factor_categories', {})
            for category, factors in factor_categories.items():
                for factor in factors:
                    if factor.get('name') == factor_name:
                        table_info = factor.get('table_info', {})
                        return table_info.get(level, [])
        # 否则返回空列表
        return []
        
    def get_display_name(self, name):
        """获取任意字段或因子的显示名称"""
        return self.config.get('display_names', {}).get(name, name)
        
    # 移除重复方法，统一使用get_display_name方法
        
    def get_data_hierarchy_name(self, level):
        """获取数据层次的显示名称"""
        return self.config.get('data_hierarchy_names', {}).get(level, level)
    
    def get_enabled_hierarchy_levels(self):
        """获取启用的数据层次级别"""
        return self.config.get('enabled_hierarchy_levels', ['total', 'boq', 'model', 'part'])
    
    def get_default_hierarchy_level(self):
        """获取默认的数据层次级别"""
        return self.config.get('default_hierarchy_level', 'total')

class DataManager:
    def __init__(self, data_path=None, config_manager=None):
        self.data = None
        self.data_path = data_path
        self.config_manager = config_manager
        if data_path:
            self.load_data(data_path)
    
    def load_data(self, data_path):
        """加载数据文件，包含错误处理"""
        try:
            # 检查数据文件是否存在
            if not os.path.exists(data_path):
                raise FileNotFoundError(f"数据文件不存在: {data_path}")
            
            # 检查文件是否可读
            if not os.access(data_path, os.R_OK):
                raise PermissionError(f"无法读取数据文件: {data_path}")
            
            # 检查文件大小（避免加载过大文件）
            file_size = os.path.getsize(data_path)
            if file_size > 100 * 1024 * 1024:  # 100MB限制
                logging.warning(f"数据文件较大 ({file_size / 1024 / 1024:.1f}MB): {data_path}")
            
            with open(data_path, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
                
            # 验证数据结构
            self._validate_data()
            self.data_path = data_path
            logging.info(f"成功加载数据文件: {data_path}")
            
        except FileNotFoundError as e:
            logging.error(f"数据文件加载失败: {e}")
            self.data = None
            raise
        except json.JSONDecodeError as e:
            logging.error(f"数据文件JSON格式错误: {e}")
            self.data = None
            raise
        except PermissionError as e:
            logging.error(f"数据文件权限错误: {e}")
            self.data = None
            raise
        except MemoryError as e:
            logging.error(f"内存不足，无法加载数据文件: {e}")
            self.data = None
            raise
        except Exception as e:
            logging.error(f"数据文件加载时发生未知错误: {e}")
            self.data = None
            raise
    
    def _validate_data(self):
        """验证数据结构的基本完整性"""
        if not isinstance(self.data, (list, dict)):
            raise ValueError("数据格式错误：根节点必须是列表或字典")
        
        if isinstance(self.data, list) and len(self.data) == 0:
            logging.warning("数据文件为空列表")
        elif isinstance(self.data, dict) and len(self.data) == 0:
            logging.warning("数据文件为空字典")

    def load_json_data(self, file_path):
        """兼容旧接口"""
        self.load_data(file_path)

    def get_document_info(self, fields=None):
        """获取文档信息，包含错误处理"""
        try:
            if not self.data:
                logging.warning("尝试获取文档信息但数据未加载")
                return {}
            
            if fields is None:
                # 如果没有指定字段，返回整个文档信息
                doc_info = self.data.get('document_info', {})
                if not isinstance(doc_info, dict):
                    logging.warning("文档信息格式错误，应为字典类型")
                    return {}
                return doc_info
            else:
                # 如果指定了字段，返回指定字段的信息
                return {field: self.data.get(field) for field in fields}
        except Exception as e:
            logging.error(f"获取文档信息时发生错误: {e}")
            return {}
    
    def get_basic_info_from_data(self, factor_name, basic_info_fields):
        """根据basic_info字段列表从JSON数据中获取对应的值"""
        if not basic_info_fields:
            return {}
        
        basic_info = {}
        
        # 根据字段列表从数据中提取值，配置了多少字段就显示多少字段
        for field in basic_info_fields:
            if self.data and field in self.data:
                # 从最外层数据获取
                basic_info[field] = self.data[field]
            elif self.data and 'calculateItemVO' in self.data and field in self.data['calculateItemVO']:
                # 从calculateItemVO中获取
                basic_info[field] = self.data['calculateItemVO'][field]
            else:
                # 如果JSON中不存在该字段，显示为空值
                # 确保配置中的所有字段都会显示
                basic_info[field] = ""
        
        return basic_info

    def get_calculate_item_vo(self):
        if not self.data:
            return None
        return self.data.get('calculateItemVO')

    def get_data_for_level(self, nodes, columns, chunk_size=1000):
        """获取指定层级的数据，包含输入验证和内存优化"""
        # 输入验证
        if not nodes:
            logging.info("节点列表为空，返回空DataFrame")
            return pd.DataFrame()
        
        if not isinstance(nodes, (list, tuple)):
            logging.error("节点参数必须是列表或元组类型")
            return pd.DataFrame()
        
        if not columns:
            logging.warning("列配置为空，返回空DataFrame")
            return pd.DataFrame()
        
        if not isinstance(columns, (list, tuple)):
            logging.error("列参数必须是列表或元组类型")
            return pd.DataFrame()
        
        try:
            # 内存监控
            initial_memory = self._get_memory_usage()
            
            # 对于大数据集，使用分块处理
            if len(nodes) > chunk_size:
                logging.info(f"大数据集检测到 ({len(nodes)} 节点)，使用分块处理")
                return self._process_large_dataset(nodes, columns, chunk_size)
            
            # 小数据集直接处理
            records = []
            for i, node in enumerate(nodes):
                if not isinstance(node, dict):
                    logging.warning(f"节点 {i} 不是字典类型，跳过")
                    continue
                
                record = {}
                for col in columns:
                    if not isinstance(col, str):
                        logging.warning(f"列名 {col} 不是字符串类型，跳过")
                        continue
                    record[col] = node.get(col, '')
                records.append(record)
            
            if not records:
                logging.warning("没有有效的记录数据")
                return pd.DataFrame()
            
            df = pd.DataFrame(records)
            
            # 内存优化：优化数据类型
            df = self._optimize_dataframe_memory(df)
            
            # 记录内存使用情况
            final_memory = self._get_memory_usage()
            memory_diff = final_memory - initial_memory
            logging.info(f"成功创建DataFrame，包含 {len(df)} 行 {len(df.columns)} 列，内存使用: {memory_diff:.2f}MB")
            
            return df
            
        except Exception as e:
            logging.error(f"创建DataFrame时发生错误: {e}")
            return pd.DataFrame()

    def get_sub_factor_info(self, fields, sub_factor_name):
        if not self.data:
            return {}
        # This is a simplified example. In a real scenario, you might need to find the specific sub-factor node.
        return {field: self.data.get(field) for field in fields}

    def get_all_nodes_for_level(self, start_node, target_level):
        """递归查找指定层级的所有节点，包含输入验证和边界检查"""
        # 输入验证
        if not start_node:
            logging.warning("起始节点为空")
            return []
        
        if not isinstance(start_node, dict):
            logging.error("起始节点必须是字典类型")
            return []
        
        if not target_level or not isinstance(target_level, str):
            logging.error("目标层级必须是非空字符串")
            return []
        
        nodes = []
        visited_nodes = set()  # 防止循环引用
        max_depth = 100  # 防止无限递归
        
        def recurse(current_node, depth=0):
            # 深度检查
            if depth > max_depth:
                logging.warning(f"递归深度超过限制 ({max_depth})，停止递归")
                return
            
            # 循环引用检查
            node_id = id(current_node)
            if node_id in visited_nodes:
                logging.warning("检测到循环引用，跳过节点")
                return
            visited_nodes.add(node_id)
            
            try:
                # 检查当前节点是否匹配目标层级
                if current_node.get('calcLevel') == target_level:
                    nodes.append(current_node)
                
                # 递归处理子节点
                sub_list = current_node.get('subList')
                if sub_list and isinstance(sub_list, list):
                    for child in sub_list:
                        if isinstance(child, dict):
                            recurse(child, depth + 1)
                        else:
                            logging.warning(f"子节点不是字典类型，跳过: {type(child)}")
                            
            except Exception as e:
                logging.error(f"处理节点时发生错误: {e}")
            finally:
                visited_nodes.discard(node_id)
        
        try:
            recurse(start_node)
            logging.info(f"找到 {len(nodes)} 个层级为 '{target_level}' 的节点")
            return nodes
        except Exception as e:
            logging.error(f"递归查找节点时发生错误: {e}")
            return []
        
    def get_hierarchy_levels(self):
        """获取数据层次级别"""
        if self.config_manager:
            return self.config_manager.get_enabled_hierarchy_levels()
        # 如果没有配置管理器，返回默认的层次级别
        return ["total", "boq", "model", "part"]
    
    def _get_memory_usage(self):
        """获取当前内存使用量（MB）"""
        try:
            process = psutil.Process(os.getpid())
            return process.memory_info().rss / 1024 / 1024
        except Exception:
            return 0
    
    def _optimize_dataframe_memory(self, df):
        """优化DataFrame的内存使用"""
        try:
            initial_memory = df.memory_usage(deep=True).sum() / 1024 / 1024
            
            # 优化数值类型
            for col in df.select_dtypes(include=['int64']).columns:
                df[col] = pd.to_numeric(df[col], downcast='integer')
            
            for col in df.select_dtypes(include=['float64']).columns:
                df[col] = pd.to_numeric(df[col], downcast='float')
            
            # 优化字符串类型
            for col in df.select_dtypes(include=['object']).columns:
                if df[col].nunique() / len(df) < 0.5:  # 如果唯一值比例小于50%，转换为category
                    df[col] = df[col].astype('category')
            
            final_memory = df.memory_usage(deep=True).sum() / 1024 / 1024
            memory_saved = initial_memory - final_memory
            
            if memory_saved > 0:
                logging.info(f"DataFrame内存优化完成，节省 {memory_saved:.2f}MB ({memory_saved/initial_memory*100:.1f}%)")
            
            return df
        except Exception as e:
            logging.error(f"DataFrame内存优化失败: {e}")
            return df
    
    def _process_large_dataset(self, nodes, columns, chunk_size):
        """分块处理大数据集"""
        try:
            dataframes = []
            total_chunks = (len(nodes) + chunk_size - 1) // chunk_size
            
            for i in range(0, len(nodes), chunk_size):
                chunk_num = i // chunk_size + 1
                logging.info(f"处理数据块 {chunk_num}/{total_chunks}")
                
                chunk_nodes = nodes[i:i + chunk_size]
                chunk_records = []
                
                for node in chunk_nodes:
                    if isinstance(node, dict):
                        record = {col: node.get(col, '') for col in columns if isinstance(col, str)}
                        chunk_records.append(record)
                
                if chunk_records:
                    chunk_df = pd.DataFrame(chunk_records)
                    chunk_df = self._optimize_dataframe_memory(chunk_df)
                    dataframes.append(chunk_df)
                
                # 强制垃圾回收
                if chunk_num % 10 == 0:
                    gc.collect()
            
            if not dataframes:
                return pd.DataFrame()
            
            # 合并所有数据块
            logging.info("合并数据块...")
            result_df = pd.concat(dataframes, ignore_index=True)
            
            # 清理临时数据
            del dataframes
            gc.collect()
            
            logging.info(f"大数据集处理完成，最终包含 {len(result_df)} 行")
            return result_df
            
        except Exception as e:
            logging.error(f"大数据集处理失败: {e}")
            return pd.DataFrame()
    
    @lru_cache(maxsize=128)
    def get_cached_hierarchy_levels(self):
        """缓存的层次级别获取方法"""
        return self.get_hierarchy_levels()
    
    def clear_cache(self):
        """清理缓存"""
        self.get_cached_hierarchy_levels.cache_clear()
        gc.collect()
        logging.info("缓存已清理")