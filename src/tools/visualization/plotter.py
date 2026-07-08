"""
气候数据可视化工具：时间序列、空间地图、异常图
"""
import os
import matplotlib.pyplot as plt
import numpy as np
from src.tools.utils import ensure_dir  # 确保导入


def plot_timeseries(
    dates: list,
    values: np.ndarray,
    title: str = "Time Series",
    xlabel: str = "Time",
    ylabel: str = "Value",
    save_path: str = None,
    show: bool = False
) -> str:
    """
    绘制时间序列折线图
    :param dates: 日期列表（或 x 轴数值）
    :param values: 数据值
    :param title, xlabel, ylabel: 图表标签
    :param save_path: 保存路径，若为空则自动生成
    :param show: 是否显示图表
    :return: 保存的文件路径
    """
    if save_path is None:
        save_path = os.path.join("outputs", "figures", "timeseries.png")
    
    # 🔧 确保目录存在（无论是用户传入的还是自动生成的）
    ensure_dir(os.path.dirname(save_path))

    plt.figure(figsize=(12, 6))
    plt.plot(dates, values, linewidth=2, color="royalblue")
    plt.title(title, fontsize=14)
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.grid(True, linestyle="--", alpha=0.6)

    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    if show:
        plt.show()
    plt.close()

    print(f"📊 图表已保存: {save_path}")
    return save_path


def plot_map(
    data: np.ndarray,
    lons: np.ndarray,
    lats: np.ndarray,
    title: str = "Spatial Map",
    save_path: str = None,
    show: bool = False
) -> str:
    """
    绘制空间分布图（使用 Cartopy 支持地图投影）
    若未安装 Cartopy，回退到标准 contourf
    """
    if save_path is None:
        save_path = os.path.join("outputs", "figures", "spatial_map.png")
    
    ensure_dir(os.path.dirname(save_path))

    try:
        import cartopy.crs as ccrs
        import cartopy.feature as cfeature

        fig = plt.figure(figsize=(12, 8))
        ax = plt.axes(projection=ccrs.PlateCarree())
        ax.add_feature(cfeature.LAND, facecolor="lightgray")
        ax.add_feature(cfeature.COASTLINE)
        ax.add_feature(cfeature.BORDERS, linestyle=":")

        cf = ax.contourf(lons, lats, data, transform=ccrs.PlateCarree(),
                         cmap="RdBu_r", extend="both")
        plt.colorbar(cf, orientation="horizontal", pad=0.05, shrink=0.8)
        ax.set_title(title, fontsize=14)
    except ImportError:
        print("⚠️ Cartopy 未安装，使用普通 matplotlib 绘制（无地图投影）")
        fig, ax = plt.subplots(figsize=(12, 8))
        cf = ax.contourf(lons, lats, data, cmap="RdBu_r", extend="both")
        plt.colorbar(cf, orientation="horizontal", pad=0.05, shrink=0.8)
        ax.set_title(title, fontsize=14)

    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    if show:
        plt.show()
    plt.close()

    print(f"🗺️ 地图已保存: {save_path}")
    return save_path


def plot_anomaly(
    anomaly_data: np.ndarray,
    time: list,
    title: str = "Anomaly Time Series",
    save_path: str = None,
    show: bool = False
) -> str:
    """
    绘制距平时间序列（含零线标注）
    """
    if save_path is None:
        save_path = os.path.join("outputs", "figures", "anomaly.png")
    
    ensure_dir(os.path.dirname(save_path))

    plt.figure(figsize=(12, 6))
    plt.bar(time, anomaly_data, color=np.where(anomaly_data >= 0, "red", "blue"), alpha=0.7)
    plt.axhline(y=0, color="black", linestyle="-", linewidth=1)
    plt.title(title, fontsize=14)
    plt.xlabel("Time", fontsize=12)
    plt.ylabel("Anomaly", fontsize=12)
    plt.grid(True, linestyle="--", alpha=0.3)

    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    if show:
        plt.show()
    plt.close()

    print(f"📊 距平图已保存: {save_path}")
    return save_path