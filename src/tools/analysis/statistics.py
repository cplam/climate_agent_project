"""
气候统计分析工具：趋势、异常、统计检验
"""
import numpy as np
from scipy import stats
from typing import Tuple, Optional


def compute_trend(x: np.ndarray, y: np.ndarray) -> dict:
    """
    计算线性趋势（最小二乘法）
    :param x: 自变量（如时间序列索引）
    :param y: 因变量（如温度）
    :return: 包含斜率、截距、R² 的字典
    """
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    return {
        "slope": slope,
        "intercept": intercept,
        "r_squared": r_value ** 2,
        "p_value": p_value,
        "std_err": std_err,
    }


def mann_kendall_test(data: np.ndarray) -> dict:
    """
    Mann-Kendall 趋势检验（用于判断是否有显著单调趋势）
    :param data: 时间序列数据
    :return: 趋势方向、p值、统计量
    """
    try:
        from pymannkendall import original_test
        result = original_test(data)
        return {
            "trend": result.trend,
            "p_value": result.p,
            "z_score": result.z,
            "slope": result.slope,
        }
    except ImportError:
        # 若未安装 pymannkendall，使用简单替代方法
        print("⚠️ 未安装 pymannkendall，使用 Spearman 相关系数替代")
        x = np.arange(len(data))
        corr, p_val = stats.spearmanr(x, data)
        return {
            "trend": "increasing" if corr > 0 else "decreasing",
            "p_value": p_val,
            "z_score": corr,
            "slope": None,
        }


def calculate_anomaly(data: np.ndarray, climatology: Optional[np.ndarray] = None) -> np.ndarray:
    """
    计算距平（异常值）
    :param data: 原始数据
    :param climatology: 气候态平均值，若为空则使用 data 的均值
    :return: 距平值
    """
    if climatology is None:
        climatology = np.mean(data)
    return data - climatology