import sys
import os

# 获取项目根目录（假设 test_agents.py 位于 src/agents/ 下）
current_dir = os.path.dirname(os.path.abspath(__file__))          # src/agents
project_root = os.path.dirname(os.path.dirname(current_dir))      # 项目根目录
sys.path.insert(0, project_root)

from src.utils.llm_client import DeepSeekClient
from src.agents.orchestrator import OrchestratorAgent

def main():
    client = DeepSeekClient()
    orchestrator = OrchestratorAgent(client)
    result = orchestrator.process("分析北极海冰面积变化趋势")
    print("\n" + "="*50)
    print("最终报告：")
    print("="*50)
    print(result["report"]["report"])

if __name__ == "__main__":
    main()