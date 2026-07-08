"""
总控智能体：协调各子智能体完成完整工作流
"""
import os
import numpy as np
import pandas as pd
from src.agents.base_agent import BaseAgent
from src.agents.planner import PlannerAgent
from src.agents.data_fetcher import DataFetcherAgent
from src.agents.coder import CoderAgent
from src.agents.reporter import ReporterAgent
from src.utils.llm_client import DeepSeekClient
from src.tools.utils import ensure_dir
from typing import Dict, Any


class OrchestratorAgent(BaseAgent):
    def __init__(self, llm_client: DeepSeekClient):
        super().__init__(
            name="Orchestrator",
            system_prompt="你是总协调员，负责调度子智能体完成任务。",
            llm_client=llm_client
        )
        self.planner = PlannerAgent("Planner", "你是一个规划专家", llm_client)
        self.data_fetcher = DataFetcherAgent("DataFetcher", "你是一个数据获取专家", llm_client)
        self.coder = CoderAgent("Coder", "你是一个编程专家", llm_client)
        self.reporter = ReporterAgent("Reporter", "你是一个报告专家", llm_client)

    def _generate_simulated_data(self) -> str:
        """生成模拟气温数据"""
        self.logger.info("📊 生成模拟气温数据...")
        dates = pd.date_range('2014-01-01', '2024-12-31', freq='MS')  # 使用 'MS' 代替 'M'
        n_points = len(dates)
        np.random.seed(42)
        base_temp = 15.0
        trend = 0.028 * np.arange(n_points)
        seasonal = 2.5 * np.sin(2 * np.pi * np.arange(n_points) / 12 - np.pi/2)
        interannual = 0.3 * np.sin(2 * np.pi * np.arange(n_points) / 40 + 0.5)
        noise = np.random.randn(n_points) * 0.15
        temperature = base_temp + trend + seasonal + interannual + noise
        df = pd.DataFrame({
            'date': dates,
            'temperature': temperature,
            'anomaly': temperature - np.mean(temperature[:12]),
        })
        ensure_dir("outputs/data")
        file_path = "outputs/data/simulated_temperature.csv"
        df.to_csv(file_path, index=False)
        self.logger.info(f"✅ 模拟数据已生成: {file_path}")
        return file_path

    def _ensure_data_file(self, data_result: Dict[str, Any]) -> str:
        data_source = data_result.get("data_source_info", "")
        file_path = data_result.get("file_path", "")
        if "未指定" in data_source or not os.path.exists(file_path):
            self.logger.warning("⚠️ 数据获取失败或文件不存在，使用模拟数据替代")
            return self._generate_simulated_data()
        return file_path

    def process(self, input_text: str, **kwargs) -> Dict[str, Any]:
        self.logger.info(f"收到用户问题：{input_text}")

        # 1. 规划（如果失败，使用默认计划）
        try:
            plan_result = self.planner.process(input_text)
            plan = plan_result.get("plan", "")
            if not plan or plan == "无法生成计划":
                plan = "1. 获取气候数据\n2. 分析趋势\n3. 生成可视化\n4. 撰写报告"
                self.logger.warning("⚠️ 使用默认计划替代")
        except Exception as e:
            self.logger.error(f"规划失败: {e}")
            plan = "1. 获取气候数据\n2. 分析趋势\n3. 生成可视化\n4. 撰写报告"
        self.logger.info(f"计划完成：{plan}")

        # 2. 数据获取（并确保文件存在）
        try:
            data_result = self.data_fetcher.process(input_text)
        except Exception as e:
            self.logger.error(f"数据获取失败: {e}")
            data_result = {"data_source_info": "错误", "file_path": ""}
        data_file = self._ensure_data_file(data_result)
        self.logger.info(f"数据准备完成：{data_file}")

        # 3. 编码分析 - 使用纯英文提示词，与测试一致
        # 修改点：将中文提示改为纯英文，避免混淆模型
        analysis_prompt = f"Analyze the data file {data_file}, compute temperature trend, generate a line plot, and save it to outputs/figures/."
        try:
            code_result = self.coder.process(analysis_prompt)
            code_output = code_result.get('execution_result', '无代码执行结果')
        except Exception as e:
            self.logger.error(f"编码分析失败: {e}")
            code_output = f"编码分析失败: {e}"

        self.logger.info(f"代码执行结果：{code_output}")

        # 4. 生成报告
        context = f"""
用户问题：{input_text}

研究计划：
{plan}

数据来源：{data_result.get('data_source_info', '模拟数据')}
数据文件：{data_file}

分析结果：{code_output}
"""
        try:
            report_result = self.reporter.process(input_text, context=context)
        except Exception as e:
            self.logger.error(f"报告生成失败: {e}")
            # 手动生成简单报告
            report_text = f"""# 气候分析报告（应急生成）

## 问题
{input_text}

## 计划
{plan}

## 数据
{data_file}

## 分析结果
{code_output}

## 错误
报告生成过程中遇到异常，以上为部分信息。
"""
            report_dir = "outputs/reports"
            ensure_dir(report_dir)
            report_path = os.path.join(report_dir, "report.md")
            with open(report_path, "w", encoding='utf-8') as f:
                f.write(report_text)
            report_result = {"report": report_text, "saved_to": report_path}

        return {
            "plan": plan,
            "data": data_result,
            "data_file": data_file,
            "code": code_result if 'code_result' in locals() else {"execution_result": code_output},
            "report": report_result,
        }