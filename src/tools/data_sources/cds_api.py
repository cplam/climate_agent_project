"""
Copernicus Climate Data Store (CDS) API 接口
支持 ERA5 等数据集的下载
"""
import os
import cdsapi
from src.tools.utils import ensure_dir, get_output_path


def fetch_cds_data(
    dataset: str = "reanalysis-era5-single-levels",
    variables: list = ["2m_temperature"],
    year: str = "2020",
    month: str = "01",
    day: str = "01",
    time: str = "00:00",
    area: list = [70, -20, 30, 40],  # [North, West, South, East]
    output_filename: str = None,
    use_api_key: str = None
) -> str:
    """
    从 CDS 下载气候数据
    :param dataset: 数据集名称，如 'reanalysis-era5-single-levels'
    :param variables: 变量列表
    :param year, month, day, time: 时间参数
    :param area: 区域 [北, 西, 南, 东]
    :param output_filename: 输出文件名，若为空则自动生成
    :param use_api_key: 可选，若提供则覆盖环境变量
    :return: 下载文件路径
    """
    # 若没有提供 key，尝试从环境变量读取
    api_key = use_api_key or os.getenv("CDS_API_KEY")
    if not api_key:
        print("⚠️ 警告: 未设置 CDS_API_KEY，将使用匿名访问（可能受限）。")
        # cdsapi 支持匿名访问，但会提示

    # 生成输出文件名
    if output_filename is None:
        output_filename = f"{dataset}_{year}_{month}_{day}_{variables[0]}.nc"
    
    output_path = get_output_path("data", output_filename)

    # 如果文件已存在，直接返回
    if os.path.exists(output_path):
        print(f"✅ 数据文件已存在: {output_path}")
        return output_path

    # 构建请求参数
    request = {
        "product_type": "reanalysis",
        "format": "netcdf",
        "variable": variables,
        "year": year,
        "month": month,
        "day": day,
        "time": time,
        "area": area,
    }

    # 针对压力层数据集增加 pressure_level 参数
    if "pressure" in dataset:
        request["pressure_level"] = "500"

    print(f"🌐 正在从 CDS 下载数据: {dataset}")
    try:
        client = cdsapi.Client(api_key=api_key)
        client.retrieve(dataset, request, output_path)
        print(f"✅ 数据下载完成: {output_path}")
        return output_path
    except Exception as e:
        print(f"❌ 下载失败: {e}")
        raise