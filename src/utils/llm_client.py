"""
大语言模型（LLM）客户端封装
基于 DeepSeek V3 API（通过 Aihubmix 代理）
"""
import os
import json
import re
from openai import OpenAI
from typing import List, Dict, Any, Optional

# ==========================================
# 🔐 使用您在 LLM.py 中验证过的配置
# ==========================================
BASE_URL = "https://aihubmix.com/v1"
DEEPSEEK_API_KEY = "**********"  # 请替换为实际的 DeepSeek API Key
DEFAULT_MODEL = "gpt-5"   # 或 "deepseek-chat"，请根据实际可用模型调整


class DeepSeekClient:
    def __init__(self, model: str = DEFAULT_MODEL, temperature: float = 0.2):
        """
        初始化 DeepSeek V3 客户端（通过 Aihubmix 代理）
        :param model: 模型名称（根据代理支持的模型列表选择）
        :param temperature: 温度参数（0.0-1.0）
        """
        self.client = OpenAI(
            api_key=DEEPSEEK_API_KEY,
            base_url=BASE_URL,
            timeout=30.0
        )
        self.model = model
        self.temperature = temperature
        print(f"[LLM] 初始化成功，模型: {model}, 代理: {BASE_URL}")

    def chat(
        self,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict]] = None,
        tool_choice: str = "auto",
        max_tokens: int = 2048,
        **kwargs
    ) -> Dict[str, Any]:
        """
        调用 LLM 聊天接口
        :param messages: 消息列表
        :param tools: 工具定义（Function Calling）
        :param tool_choice: 工具选择策略
        :param max_tokens: 最大输出 token 数
        :return: 响应结果字典
        """
        try:
            # 🔧 关键修复：只在 tools 非空时才添加 tool_choice
            params = {
                "model": self.model,
                "messages": messages,
                "temperature": self.temperature,
                "max_tokens": max_tokens,
                **kwargs
            }
            if tools:
                params["tools"] = tools
                params["tool_choice"] = tool_choice

            response = self.client.chat.completions.create(**params)
            
            choice = response.choices[0]
            result = {
                "content": choice.message.content,
                "tool_calls": choice.message.tool_calls,
                "finish_reason": choice.finish_reason,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            }
            return result
            
        except Exception as e:
            print(f"[LLM] API 调用失败: {type(e).__name__}: {e}")
            # 返回空结果，让上层处理
            return {"content": "", "tool_calls": None, "finish_reason": "error"}

    def extract_code(self, text: str) -> str:
        """
        从 LLM 回复中提取 Python 代码块
        :param text: LLM 返回的文本
        :return: 提取的代码字符串
        """
        pattern = r"```python\n(.*?)```"
        matches = re.findall(pattern, text, re.DOTALL)
        return "\n".join(matches) if matches else text

    def extract_json(self, text: str) -> Optional[dict]:
        """
        从 LLM 回复中提取 JSON 对象
        :param text: LLM 返回的文本
        :return: 解析后的字典，若失败则返回 None
        """
        pattern = r"```json\n(.*?)```"
        matches = re.findall(pattern, text, re.DOTALL)
        if matches:
            try:
                return json.loads(matches[0])
            except:
                pass
        
        # 尝试直接解析
        try:
            return json.loads(text)
        except:
            return None