import json, re
from openai import OpenAI
from typing import List, Dict, Any, Optional

BASE_URL = "https://aihubmix.com/v1"
DEEPSEEK_API_KEY = "I47C7kQFfaBkYjFwB39c3f407d7d4a0e812414695657Be6e"
DEFAULT_MODEL = "gpt-5"

class DeepSeekClient:
    def __init__(self, model: str = DEFAULT_MODEL, temperature: float = 0.2):
        self.client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=BASE_URL, timeout=30.0)
        self.model = model
        self.temperature = temperature
        print(f"[LLM] init ok, model={model}")

    def chat(self, messages, tools=None, tool_choice="auto", max_tokens=2048, **kwargs):
        params = {"model": self.model, "messages": messages, "temperature": self.temperature, "max_tokens": max_tokens, **kwargs}
        if tools:
            params["tools"] = tools
            params["tool_choice"] = tool_choice
        try:
            response = self.client.chat.completions.create(**params)
            content = response.choices[0].message.content or ""
            print(f"[DEBUG] raw content (len {len(content)}):\n{repr(content)}")  # 关键调试
            return {"content": content, "tool_calls": None, "finish_reason": "done"}
        except Exception as e:
            print(f"[LLM] error: {e}")
            return {"content": "", "tool_calls": None, "finish_reason": "error"}

    def extract_code(self, text: str) -> str:
        pattern = r"```python\n(.*?)```"
        matches = re.findall(pattern, text, re.DOTALL)
        return "\n".join(matches) if matches else text