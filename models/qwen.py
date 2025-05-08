import requests, os
API_URL = "https://api-inference.huggingface.co/models/Qwen/Qwen-7B-Chat"
headers = {"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"}
def call_qwen(prompt: str) -> str:
    try:
        res = requests.post(API_URL, headers=headers, json={"inputs": prompt}, timeout=30)
        result = res.json()
        if isinstance(result, list): return result[0].get("generated_text", "[无返回结果]")
        if isinstance(result, dict): return result.get("generated_text", result.get("error", "[无生成文本]"))
        return "[未知响应格式]"
    except Exception as e: return f"[调用失败: {str(e)}]"
