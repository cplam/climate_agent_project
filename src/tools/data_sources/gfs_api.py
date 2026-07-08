"""
Global Forecast System (GFS) 数据获取接口
由于 GFS 数据通常通过 NOMADS 或 Amazon S3 公开，此处提供模拟/占位实现
"""
import os
import requests
from src.tools.utils import get_output_path


def fetch_gfs_data(
    variable: str = "TMP",
    level: str = "surface",
    forecast_hour: str = "000",
    date: str = "20200101",
    output_filename: str = None
) -> str:
    """
    模拟 GFS 数据获取（实际使用时需替换为真实 API）
    :return: 本地文件路径
    """
    if output_filename is None:
        output_filename = f"gfs_{variable}_{date}_{forecast_hour}.grib2"

    output_path = get_output_path("data", output_filename)

    if os.path.exists(output_path):
        print(f"✅ GFS 数据文件已存在: {output_path}")
        return output_path

    # 真实 GFS 可通过 NOMADS 下载，例如:
    # url = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.{date}/{forecast_hour}/atmos/gfs.t{forecast_hour}z.pgrb2.0p25.f{forecast_hour}"

    print(f"⚠️ GFS 数据获取未完整实现，请参考官方文档配置真实源。")
    print(f"📝 模拟返回路径: {output_path}")

    # 创建一个空文件作为占位
    with open(output_path, "w") as f:
        f.write("# GFS placeholder data\n")

    return output_path