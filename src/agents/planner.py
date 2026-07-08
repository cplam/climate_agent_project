"""
任务规划智能体：将用户问题分解为可执行的子任务列表
"""
from src.agents.base_agent import BaseAgent
from typing import Dict, Any


class PlannerAgent(BaseAgent):
    def process(self, input_text: str, **kwargs) -> Dict[str, Any]:
        """
        分解问题为步骤列表。如果 LLM 返回空，则使用默认计划。
        """
        prompt = f"""
用户问题：{input_text}

请将这个问题分解为 3~6 个清晰的步骤，每个步骤用一句话描述，并以编号列表输出。
步骤应涵盖：数据获取、数据分析、可视化、报告撰写。
只输出编号列表，不要额外解释。

示例：
1. 从指定数据源获取过去10年的全球温度数据。
2. 对数据进行趋势分析和统计检验。
3. 生成时间序列折线图展示变化趋势。
4. 撰写总结报告。

现在请针对用户问题给出步骤列表：
"""
        messages = self._build_messages(prompt)
        response = self.llm.chat(messages)
        plan_text = response.get("content", "").strip()

        # 如果 LLM 返回空或只有标点，使用默认计划
        if not plan_text or len(plan_text) < 10:
            self.logger.warning("⚠️ LLM 未生成有效计划，使用默认计划")
            plan_text = self._get_default_plan(input_text)

        self.logger.info(f"生成的计划：\n{plan_text}")
        return {"plan": plan_text}

    def _get_default_plan(self, question: str) -> str:
        """生成默认计划（当 LLM 失败时）"""
        return f"""1. 获取与问题相关的气候数据："{question}"。
2. 对数据进行预处理和质量控制。
3. 执行趋势分析和统计检验（如线性回归）。
4. 生成可视化图表（时间序列、空间分布等）。
5. 整理结果并撰写科学报告。"""