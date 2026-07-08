"""
报告生成智能体：汇总结果并撰写科学报告
"""
import os
from src.agents.base_agent import BaseAgent
from typing import Dict, Any


class ReporterAgent(BaseAgent):
    def process(self, input_text: str, **kwargs) -> Dict[str, Any]:
        """
        根据上下文生成Markdown格式的报告
        如果LLM无法生成，使用默认模板
        """
        context = kwargs.get("context", "无分析结果")
        
        # 提取关键信息（只取前1000字符，且尽量只保留英文和数字）
        # 由于context包含中文，但模型能理解，我们保留，但提示词只要求简短摘要
        prompt = f"""
Based on the following climate analysis results, write a concise summary in Markdown format.
Include the main findings, data source, and a brief conclusion. Keep it short (max 300 words).

Results:
{context[:1500]}
"""
        # 直接使用用户消息，不加系统提示
        messages = [{"role": "user", "content": prompt}]
        response = self.llm.chat(messages)
        report = response.get("content", "").strip()
        
        # 如果LLM返回空或错误信息，使用默认模板
        if not report or report.startswith("[LLM 错误"):
            self.logger.warning("⚠️ LLM未能生成有效报告，使用默认模板")
            report = self._generate_default_report(input_text, context)
        
        # 保存报告
        report_dir = os.path.join("outputs", "reports")
        os.makedirs(report_dir, exist_ok=True)
        report_path = os.path.join(report_dir, "report.md")
        with open(report_path, "w", encoding='utf-8') as f:
            f.write(report)
        
        self.logger.info(f"报告已保存至 {report_path}")
        return {"report": report, "saved_to": report_path}
    
    def _generate_default_report(self, question: str, context: str) -> str:
        """生成默认报告模板（当LLM失败时使用）"""
        return f"""# 气候分析报告

## 1. 摘要
本文档针对问题“{question}”进行了初步分析。由于AI模型暂时无法生成完整报告，本报告提供了基础框架和模拟数据结果。

## 2. 研究背景
用户提出的问题涉及气候科学领域，需要结合数据分析和可视化方法进行探索。

## 3. 数据与方法
- **数据来源**：使用模拟数据集（包含时间序列和温度变量）
- **分析方法**：线性趋势分析、时间序列可视化

## 4. 结果
分析结果如下：
{context[:500] if context else "（无具体分析结果）"}

## 5. 讨论与结论
- 模拟数据展示了典型的气候变化特征（如升温趋势）。
- 建议后续使用真实气候数据集（如ERA5、GISTEMP）进行更精确的分析。

## 6. 局限性
- 本报告基于模拟数据，不代表真实气候状况。
- 需要配置API密钥并连接真实数据源以获得可靠结论。

---
*报告生成时间: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""