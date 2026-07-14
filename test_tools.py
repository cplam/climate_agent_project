from src.tools.analysis.statistics import compute_trend
from src.tools.visualization.plotter import plot_timeseries
import numpy as np

# 模拟数据
x = np.arange(100)
y = np.random.randn(100) + x * 0.02

# 计算趋势
result = compute_trend(x, y)
print(f"趋势斜率: {result['slope']:.4f}")

# 绘图
plot_timeseries(x, y, title="Climate Trend", save_path="outputs/figures/my_trend.png")