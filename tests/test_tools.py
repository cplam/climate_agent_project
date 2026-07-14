"""
工具模块单元测试
"""
import unittest
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from src.tools.analysis.statistics import compute_trend, calculate_anomaly
from src.tools.visualization.plotter import plot_timeseries
from src.tools.utils import ensure_dir, get_output_path


class TestTools(unittest.TestCase):
    
    def test_ensure_dir(self):
        """测试目录创建"""
        test_dir = "outputs/test_temp"
        ensure_dir(test_dir)
        self.assertTrue(os.path.exists(test_dir))
    
    def test_compute_trend(self):
        """测试趋势计算"""
        x = np.arange(10)
        y = x * 2 + 1
        result = compute_trend(x, y)
        self.assertAlmostEqual(result["slope"], 2.0, places=5)
        self.assertAlmostEqual(result["r_squared"], 1.0, places=5)
    
    def test_calculate_anomaly(self):
        """测试距平计算"""
        data = np.array([1, 2, 3, 4, 5])
        anomaly = calculate_anomaly(data)
        self.assertAlmostEqual(np.mean(anomaly), 0.0, places=5)
    
    def test_plot_timeseries(self):
        """测试图表生成"""
        x = np.arange(10)
        y = np.random.randn(10)
        save_path = "outputs/figures/test_plot.png"
        
        # 确保目录存在
        ensure_dir("outputs/figures")
        
        result = plot_timeseries(x, y, title="Test Plot", save_path=save_path)
        self.assertTrue(os.path.exists(result))
        
        # 清理测试文件
        if os.path.exists(result):
            os.remove(result)


if __name__ == "__main__":
    unittest.main()