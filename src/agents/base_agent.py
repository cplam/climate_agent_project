"""
智能体基类，所有专业智能体均继承自此类。
提供统一的LLM客户端、日志和消息构建方法。
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from src.utils.llm_client import DeepSeekClient
from src.utils.logger import setup_logger


class BaseAgent(ABC):
    def __init__(self, name: str, system_prompt: str, llm_client: DeepSeekClient):
        """
        初始化智能体
        :param name: 智能体名称
        :param system_prompt: 系统提示词，定义角色和行为
        :param llm_client: DeepSeek V3 客户端实例
        """
        self.name = name
        self.system_prompt = system_prompt
        self.llm = llm_client
        self.logger = setup_logger(name)

    def _build_messages(self, user_input: str, history: Optional[List[Dict]] = None) -> List[Dict]:
        """
        构建发送给LLM的消息列表，包含系统提示、历史记录和当前用户输入
        """
        messages = [{"role": "system", "content": self.system_prompt}]
        if history:
            messages.extend(history)
        messages.append({"role": "user", "content": user_input})
        return messages

    @abstractmethod
    def process(self, input_text: str, **kwargs) -> Dict[str, Any]:
        """
        每个智能体的核心处理逻辑，子类必须实现
        :param input_text: 输入文本（问题或任务描述）
        :param kwargs: 额外参数（如上下文数据）
        :return: 处理结果字典
        """
        pass