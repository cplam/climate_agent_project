"""
数据获取智能体：确定数据源并返回数据文件路径（模拟或真实）
支持自动检测失败时生成模拟数据
"""
import os
import yaml
import numpy as np
import pandas as pd
from src.agents.base_agent import BaseAgent
from src.tools.utils import ensure_dir
from typing import Dict, Any, Optional


class DataFetcherAgent(BaseAgent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 加载数据源配置文件
        try:
            config_path = os.path.join("config", "data_sources.yaml")
            with open(config_path, "r") as f:
                self.sources = yaml.safe_load(f)
            self.logger.info(f"✅ 已加载数据源配置: {list(self.sources.keys())}")
        except Exception as e:
            self.logger.warning(f"⚠️ 加载数据源配置失败: {e}")
            self.sources = {}

    def _generate_realistic_simulated_data(self, input_text: str) -> Dict[str, Any]:
        """
        根据用户输入生成逼真的模拟气候数据
        """
        self.logger.info("📊 生成模拟气候数据...")
        
        # 从用户输入中提取年份信息
        import re
        years_match = re.search(r'(\d{4})\s*[-—到]\s*(\d{4})', input_text)
        if years_match:
            start_year = int(years_match.group(1))
            end_year = int(years_match.group(2))
        else:
            # 默认过去10年
            start_year = 2014
            end_year = 2024
        
        # 生成日期序列（月度数据）
        dates = pd.date_range(f'{start_year}-01-01', f'{end_year}-12-31', freq='M')
        n_points = len(dates)
        
        # 设置随机种子保证可重复性
        np.random.seed(42)
        
        # 判断是否是温度相关的问题
        is_temperature = '温度' in input_text or '气温' in input_text or 'temp' in input_text.lower()
        is_sea_ice = '海冰' in input_text or 'ice' in input_text.lower()
        is_precip = '降水' in input_text or 'rain' in input_text.lower()
        
        if is_sea_ice:
            # 海冰面积模拟（百万平方公里）
            base_value = 6.0
            trend = -0.08 * np.arange(n_points)  # 下降趋势
            seasonal = 1.5 * np.sin(2 * np.pi * np.arange(n_points) / 12 - np.pi/2)
            noise = np.random.randn(n_points) * 0.2
            data = base_value + trend + seasonal + noise
            unit = "百万平方公里"
            var_name = "sea_ice_area"
            label = "北极海冰面积"
        elif is_precip:
            # 降水量模拟（mm/月）
            base_value = 80
            seasonal = 40 * np.sin(2 * np.pi * np.arange(n_points) / 12 + np.pi/4)
            noise = np.random.randn(n_points) * 10
            data = base_value + seasonal + noise
            unit = "mm"
            var_name = "precipitation"
            label = "月降水量"
        else:
            # 默认：温度模拟（°C）
            base_temp = 15.0
            trend = 0.028 * np.arange(n_points)  # ~0.28°C/10年升温
            seasonal = 2.5 * np.sin(2 * np.pi * np.arange(n_points) / 12 - np.pi/2)
            interannual = 0.3 * np.sin(2 * np.pi * np.arange(n_points) / 40 + 0.5)
            noise = np.random.randn(n_points) * 0.15
            data = base_temp + trend + seasonal + interannual + noise
            unit = "°C"
            var_name = "temperature"
            label = "温度"
        
        # 创建DataFrame
        df = pd.DataFrame({
            'date': dates,
            var_name: data,
            'anomaly': data - np.mean(data[:12]),  # 相对于第一年基准
        })
        
        # 保存到文件
        ensure_dir("outputs/data")
        file_path = f"outputs/data/simulated_{var_name}_{start_year}_{end_year}.csv"
        df.to_csv(file_path, index=False)
        
        self.logger.info(f"✅ 模拟数据已生成: {file_path} (共 {n_points} 个数据点)")
        
        return {
            "data_source_info": f"模拟数据（{label}，{start_year}-{end_year}，{len(dates)}个时间点）",
            "file_path": file_path,
            "status": "simulated",
            "variable": var_name,
            "label": label,
            "unit": unit,
            "time_range": f"{start_year}-{end_year}",
            "n_points": n_points,
        }

    def _try_parse_llm_response(self, response_text: str) -> Optional[Dict[str, Any]]:
        """
        尝试从LLM响应中解析数据源信息
        """
        lines = response_text.strip().split('\n')
        result = {"data_source": "unknown", "dataset": None, "params": {}}
        
        for line in lines:
            line = line.strip()
            if line.startswith('数据源:') or line.startswith('数据源：'):
                result["data_source"] = line.split(':', 1)[1].strip()
            elif line.startswith('数据集:') or line.startswith('数据集：'):
                result["dataset"] = line.split(':', 1)[1].strip()
            elif line.startswith('参数:') or line.startswith('参数：'):
                param_str = line.split(':', 1)[1].strip()
                try:
                    import json
                    result["params"] = json.loads(param_str)
                except:
                    result["params"] = {"raw": param_str}
        
        # 检查是否成功解析
        if result["data_source"] != "unknown" and result["data_source"] != "未指定":
            return result
        return None

    def process(self, input_text: str, **kwargs) -> Dict[str, Any]:
        """
        根据需求解析数据源和参数，并获取数据
        如果LLM无法指定数据源，自动生成模拟数据
        """
        # 构建提示，让LLM从输入中提取数据源和参数
        prompt = f"""
        根据以下需求，确定需要从哪个数据源获取什么数据。
        可用数据源：{list(self.sources.keys()) if self.sources else ['CDS (ERA5)', 'GFS', '本地数据']}
        需求：{input_text}
        
        请按以下格式回答：
        数据源: <source>
        数据集: <dataset>  (仅对CDS有效)
        参数: <param_dict> (用JSON格式)
        
        如果无法确定，请只说"使用模拟数据"。
        """
        
        messages = self._build_messages(prompt)
        response = self.llm.chat(messages)
        raw_content = response.get("content", "")
        
        self.logger.info(f"LLM 原始响应: {raw_content[:200]}...")
        
        # 尝试解析LLM响应
        parsed = self._try_parse_llm_response(raw_content)
        
        if parsed:
            info = f"数据源: {parsed['data_source']}"
            if parsed.get('dataset'):
                info += f", 数据集: {parsed['dataset']}"
            if parsed.get('params'):
                info += f", 参数: {parsed['params']}"
            
            # 这里可以扩展真实数据下载逻辑
            # 例如调用 cdsapi 下载数据
            
            # 目前仍使用模拟数据，但记录更详细的来源信息
            simulated_file = os.path.join("outputs", "data", f"{parsed['data_source']}_sample.nc")
            os.makedirs(os.path.dirname(simulated_file), exist_ok=True)
            
            return {
                "data_source_info": info,
                "file_path": simulated_file,
                "status": "llm_specified",
                "parsed": parsed,
            }
        else:
            # LLM未成功指定数据源，生成模拟数据
            self.logger.info("🔄 LLM未指定具体数据源，自动生成模拟数据...")
            return self._generate_realistic_simulated_data(input_text)