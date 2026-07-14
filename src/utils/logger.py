"""
统一日志配置模块
"""
import logging
import sys
from datetime import datetime


def setup_logger(name: str, level=logging.INFO, log_to_file: bool = True) -> logging.Logger:
    """
    创建并配置日志记录器
    :param name: 日志记录器名称
    :param level: 日志级别
    :param log_to_file: 是否写入日志文件
    :return: 配置好的 Logger 实例
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # 避免重复添加 Handler
    if logger.handlers:
        return logger
    
    # 控制台 Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)
    
    # 文件 Handler
    if log_to_file:
        try:
            import os
            log_dir = "outputs/logs"
            os.makedirs(log_dir, exist_ok=True)
            log_file = os.path.join(log_dir, f"{name}_{datetime.now().strftime('%Y%m%d')}.log")
            
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(level)
            file_format = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(file_format)
            logger.addHandler(file_handler)
        except Exception as e:
            print(f"⚠️ 无法创建日志文件: {e}")
    
    return logger


# 默认日志记录器
default_logger = setup_logger("ClimateAgent")

# 便捷函数
def get_logger(name: str) -> logging.Logger:
    """获取日志记录器（用于模块中）"""
    return setup_logger(name)