"""
智能体模块单元测试
"""
import unittest
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.llm_client import DeepSeekClient
from src.agents.planner import PlannerAgent
from src.agents.coder import CoderAgent


class TestAgents(unittest.TestCase):
    
    def setUp(self):
        """每个测试前的准备工作"""
        self.client = DeepSeekClient()
        self.planner = PlannerAgent("TestPlanner", "测试规划", self.client)
    
    def test_planner(self):
        """测试规划智能体"""
        result = self.planner.process("分析全球变暖趋势")
        self.assertIsNotNone(result.get("plan"))
        self.assertGreater(len(result["plan"]), 10)
    
    def test_coder_code_extraction(self):
        """测试代码提取"""
        coder = CoderAgent("TestCoder", "测试编码", self.client)
        # 模拟响应
        mock_response = {
            "content": "```python\nprint('hello')\n```"
        }
        # 直接测试提取逻辑
        code = self.client.extract_code(mock_response["content"])
        self.assertEqual(code, "print('hello')")


if __name__ == "__main__":
    unittest.main()