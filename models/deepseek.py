import requests
import os

API_URL = "https://api-inference.huggingface.co/models/deepseek-ai/deepseek-llm-7b-chat"
headers = {"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"}

def call_deepseekllm7bchat(prompt: str) -> str:
    payload = {"inputs": prompt, "parameters": {"max_new_tokens": 512, "temperature": 0.7}}
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        result = response.json()
        if isinstance(result, list):
            return result[0].get("generated_text", "[无返回结果]")
        elif isinstance(result, dict):
            return result.get("generated_text", result.get("error", "[无生成文本]"))
        else:
            return "[未知响应格式]"
    except Exception as e:
        return f"[调用失败: {str(e)}]"
