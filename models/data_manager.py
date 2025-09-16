import json
import os
import logging
import psutil
import gc
from functools import lru_cache
from utils.validation_utils import ValidationUtils
from utils.lightweight_data import pd


class DataManager:
    """数据管理器，负责加载和管理数据"""
    
    def __init__(self, config_manager=None):
        self.data = None
        self.data_path = None
        self.config_manager = config_manager
    
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
        if not self._validate_input(basic_info_fields, (list, tuple), "basic_info_fields"):
            return {}
        
        basic_info = {}
        
        # 根据字段列表从数据中提取值，配置了多少字段就显示多少字段
        for field in basic_info_fields:
            # 优先从最外层数据获取
            value = self._safe_get_value(self.data, field)
            if not value:
                # 从calculateItemVO中获取
                calculate_item = self._safe_get_value(self.data, 'calculateItemVO', {})
                value = self._safe_get_value(calculate_item, field)
            basic_info[field] = value
        
        return basic_info

    def get_calculate_item_vo(self):
        if not self.data:
            return None
        return self.data.get('calculateItemVO')

    def get_data_for_level(self, nodes, columns, chunk_size=1000):
        """获取指定层级的数据，包含输入验证和内存优化"""
        # 输入验证
        if not self._validate_input(nodes, (list, tuple), "节点列表"):
            return pd.DataFrame()
        
        if not self._validate_input(columns, (list, tuple), "列配置"):
            return pd.DataFrame()
        
        # 验证数据是否已加载
        if not self.data:
            logging.warning("数据未加载，无法创建DataFrame")
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
                    if isinstance(col, str):
                        record[col] = self._safe_get_value(node, col)
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
        logger = logging.getLogger('CalcAnyApp')
        logger.info(f"=== get_all_nodes_for_level方法开始执行 ===")
        logger.info(f"输入参数 - start_node类型: {type(start_node)}, target_level: {target_level}")
        
        # 输入验证
        if not self._validate_input(start_node, dict, "起始节点"):
            logger.error("起始节点验证失败")
            return []
        
        if not self._validate_input(target_level, str, "目标层级") or not target_level:
            logger.error("目标层级验证失败")
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
                logger = logging.getLogger('CalcAnyApp')
                current_level = current_node.get('calcLevel')
                logger.info(f"处理节点，深度{depth}，当前层级: {current_level}，目标层级: {target_level}")
                
                # 检查当前节点是否匹配目标层级
                if current_level == target_level:
                    logger.info(f"找到匹配节点，层级: {current_level}")
                    nodes.append(current_node)
                
                # 递归处理子节点
                sub_list = current_node.get('subList')
                if sub_list and isinstance(sub_list, list):
                    logger.info(f"当前节点有{len(sub_list)}个子节点")
                    for i, child in enumerate(sub_list):
                        if isinstance(child, dict):
                            logger.info(f"递归处理第{i+1}个子节点")
                            recurse(child, depth + 1)
                        else:
                            logger.warning(f"子节点不是字典类型，跳过: {type(child)}")
                else:
                    logger.info(f"当前节点没有子节点或subList不是列表")
                            
            except Exception as e:
                logger.error(f"处理节点时发生错误: {e}")
            finally:
                visited_nodes.discard(node_id)
        
        try:
            logger = logging.getLogger('CalcAnyApp')
            logger.info(f"开始递归查找层级为 '{target_level}' 的节点")
            logger.info(f"起始节点calcLevel: {start_node.get('calcLevel', 'unknown')}")
            logger.info(f"起始节点是否有subList: {'subList' in start_node}")
            if 'subList' in start_node:
                logger.info(f"起始节点subList长度: {len(start_node.get('subList', []))}")
            recurse(start_node)
            logger.info(f"找到 {len(nodes)} 个层级为 '{target_level}' 的节点")
            if len(nodes) == 0:
                logger.warning(f"未找到层级为 '{target_level}' 的节点，起始节点结构: {start_node.get('calcLevel', 'unknown')}")
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
        """优化DataFrame的内存使用（轻量化版本）"""
        try:
            if df.empty:
                return df
                
            initial_memory = df.memory_usage(deep=True).sum() / 1024 / 1024
            
            # 优化数值类型
            int_columns = df.select_dtypes(include=['int64']).columns
            for col in int_columns:
                df[col] = pd.to_numeric(df[col], downcast='integer')
            
            float_columns = df.select_dtypes(include=['float64']).columns
            for col in float_columns:
                df[col] = pd.to_numeric(df[col], downcast='float')
            
            # 简化的内存优化，不进行复杂的category转换
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
                        record = {col: self._safe_get_value(node, col) for col in columns if isinstance(col, str)}
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