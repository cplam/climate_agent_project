"""
通用工具函数：文件处理、路径管理、日期解析等
"""
import os
import pandas as pd
from datetime import datetime


def ensure_dir(path: str) -> None:
    """确保目录存在，若不存在则创建"""
    os.makedirs(path, exist_ok=True)


def parse_date(date_str: str) -> datetime:
    """解析常见日期格式"""
    try:
        return pd.to_datetime(date_str).to_pydatetime()
    except Exception:
        raise ValueError(f"无法解析日期格式: {date_str}")


def get_output_path(subdir: str, filename: str) -> str:
    """生成标准输出路径（如 outputs/data/xxx.nc）"""
    base = os.path.join("outputs", subdir)
    ensure_dir(base)
    return os.path.join(base, filename)


def load_data_file(file_path: str):
    """根据文件扩展名自动加载数据（支持 netCDF, CSV, 等）"""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".nc":
        import xarray as xr
        return xr.open_dataset(file_path)
    elif ext == ".csv":
        return pd.read_csv(file_path)
    elif ext in [".grib", ".grib2"]:
        # 需要 cfgrib 或 eccodes
        import xarray as xr
        return xr.open_dataset(file_path, engine="cfgrib")
    else:
        raise ValueError(f"不支持的文件格式: {ext}")