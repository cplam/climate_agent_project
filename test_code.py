from src.utils.llm_client import DeepSeekClient
c = DeepSeekClient()
prompt = "Write Python code to read a CSV and plot a line."
msg = [{"role": "user", "content": prompt}]
resp = c.chat(msg)
print("长度:", len(resp["content"]))
print("内容:", repr(resp["content"][:200]))