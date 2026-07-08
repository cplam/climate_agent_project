"""
编码智能体：生成并（可选）执行 Python 代码
"""
import subprocess
import tempfile
import os
from src.agents.base_agent import BaseAgent
from typing import Dict, Any


class CoderAgent(BaseAgent):
    def process(self, input_text: str, **kwargs) -> Dict[str, Any]:
        """
        根据需求生成 Python 代码。如果 LLM 无法生成，返回默认模板。
        """
        # 使用简短、明确的提示词（已验证能正常返回代码）
        prompt = f"Write Python code to analyze temperature trend from a CSV file with columns 'date' and 'temperature'. Compute linear trend, plot it, and save the figure. Only output the code. Task: {input_text}"
        
        # 关键修改：直接使用用户消息，不加系统提示
        messages = [{"role": "user", "content": prompt}]
        response = self.llm.chat(messages)
        raw = response.get("content", "").strip()
        
        # 尝试提取代码块，若没有则直接使用原始内容
        code = self.llm.extract_code(raw)
        if not code and raw:
            code = raw
        
        # 如果仍为空，使用默认模板
        if not code:
            self.logger.warning("⚠️ LLM 未生成有效代码，使用默认代码模板")
            code = self._get_default_code()

        self.logger.info(f"生成的代码（前200字符）：\n{code[:200]}...")

        exec_result = "代码未执行（可设置环境变量 EXECUTE_CODE=1 以启用执行）"
        if os.environ.get("EXECUTE_CODE") == "1":
            try:
                os.makedirs("outputs/figures", exist_ok=True)
                with tempfile.NamedTemporaryFile(suffix=".py", delete=False, mode='w', encoding='utf-8') as f:
                    f.write(code)
                    f.flush()
                    result = subprocess.run(
                        ["python", f.name],
                        capture_output=True,
                        text=True,
                        timeout=60
                    )
                    exec_result = result.stdout + result.stderr
                    os.unlink(f.name)
            except Exception as e:
                exec_result = f"执行失败：{str(e)}"

        return {"code": code, "execution_result": exec_result}

    def _get_default_code(self) -> str:
        """生成默认分析代码（当 LLM 失败时）"""
        return '''import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import os

# 读取模拟数据
df = pd.read_csv('outputs/data/simulated_temperature.csv')
df['date'] = pd.to_datetime(df['date'])

# 计算年度平均值
df['year'] = df['date'].dt.year
annual = df.groupby('year')['temperature'].mean().reset_index()

# 线性回归
x = annual['year'].values
y = annual['temperature'].values
slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
trend_line = slope * x + intercept

print(f"温度趋势斜率: {slope:.4f} °C/年")
print(f"R²: {r_value**2:.4f}")
print(f"p值: {p_value:.4f}")

# 绘图
plt.figure(figsize=(12, 6))
plt.plot(annual['year'], y, 'o-', label='年度平均温度', linewidth=2, markersize=8)
plt.plot(x, trend_line, 'r--', label=f'趋势线 (斜率={slope:.4f}°C/年)', linewidth=2)
plt.xlabel('年份', fontsize=12)
plt.ylabel('温度 (°C)', fontsize=12)
plt.title('全球平均气温变化趋势（模拟数据）', fontsize=14)
plt.legend()
plt.grid(True, alpha=0.3)
os.makedirs('outputs/figures', exist_ok=True)
plt.savefig('outputs/figures/temperature_trend.png', dpi=150, bbox_inches='tight')
plt.close()
print('✅ 图表已保存到 outputs/figures/temperature_trend.png')
'''