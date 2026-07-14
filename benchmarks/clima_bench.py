"""
ClimaBench: 气候科学 AI Agent 基准测试
用于评估智能体的任务完成能力
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import time
from typing import Dict, List, Any
from src.utils.llm_client import DeepSeekClient
from src.agents.orchestrator import OrchestratorAgent


class ClimaBench:
    """
    基准测试套件，包含一系列气候科学问题
    评估指标：任务完成率、响应时间、报告质量
    """
    def __init__(self):
        self.client = DeepSeekClient()
        self.agent = OrchestratorAgent(self.client)
        self.results = []
        
        # 测试问题集
        self.test_questions = [
            {
                "id": "temp_trend",
                "question": "分析过去10年全球平均气温的变化趋势，并生成趋势图。",
                "expected": ["趋势", "温度", "图"]
            },
            {
                "id": "sea_ice",
                "question": "分析北极海冰面积在夏季的变化规律。",
                "expected": ["海冰", "北极", "变化"]
            },
            {
                "id": "precipitation",
                "question": "分析中国东部地区降水量的季节性变化特征。",
                "expected": ["降水", "季节性", "中国"]
            },
            {
                "id": "enso",
                "question": "分析ENSO事件对全球温度异常的影响。",
                "expected": ["ENSO", "温度异常", "影响"]
            }
        ]

    def run_all(self) -> List[Dict[str, Any]]:
        """运行所有测试"""
        print("=" * 60)
        print("🧪 开始运行 ClimaBench 基准测试")
        print("=" * 60)
        
        for test in self.test_questions:
            result = self.run_single(test)
            self.results.append(result)
            self._print_result(result)
        
        self._print_summary()
        return self.results

    def run_single(self, test: Dict) -> Dict[str, Any]:
        """运行单个测试"""
        question_id = test["id"]
        question = test["question"]
        expected_keywords = test["expected"]
        
        print(f"\n📝 测试 [{question_id}]: {question}")
        
        start_time = time.time()
        
        try:
            # 运行智能体
            response = self.agent.process(question)
            elapsed_time = time.time() - start_time
            
            # 评估结果
            report = response.get("report", {}).get("report", "")
            
            # 检查关键词是否出现
            keyword_match = all(kw in report for kw in expected_keywords)
            
            # 检查是否生成了图表
            has_figure = "figure" in report.lower() or "图" in report
            
            return {
                "id": question_id,
                "question": question,
                "success": keyword_match and has_figure,
                "elapsed_time": elapsed_time,
                "keyword_match": keyword_match,
                "has_figure": has_figure,
                "report_length": len(report),
                "report_preview": report[:200] + "..." if len(report) > 200 else report
            }
            
        except Exception as e:
            return {
                "id": question_id,
                "question": question,
                "success": False,
                "elapsed_time": time.time() - start_time,
                "error": str(e)
            }

    def _print_result(self, result: Dict):
        """打印单个测试结果"""
        status = "✅ PASS" if result.get("success") else "❌ FAIL"
        print(f"  {status} - 耗时: {result.get('elapsed_time', 0):.2f}s")
        if not result.get("success") and result.get("error"):
            print(f"  错误: {result['error']}")

    def _print_summary(self):
        """打印测试总结"""
        total = len(self.results)
        passed = sum(1 for r in self.results if r.get("success", False))
        
        print("\n" + "=" * 60)
        print("📊 基准测试总结")
        print("=" * 60)
        print(f"通过: {passed}/{total} ({passed/total*100:.1f}%)")
        print(f"平均耗时: {sum(r.get('elapsed_time', 0) for r in self.results)/total:.2f}s")
        print(f"详细结果已保存至: outputs/benchmarks/results.json")
        
        # 保存结果
        os.makedirs("outputs/benchmarks", exist_ok=True)
        with open("outputs/benchmarks/results.json", "w") as f:
            json.dump(self.results, f, indent=2)


if __name__ == "__main__":
    bench = ClimaBench()
    bench.run_all()