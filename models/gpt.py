import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY") or "sk-你的key"

def call_gpt(prompt: str, model: str = "gpt-3.5-turbo", return_usage=False):
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "你是一位擅长中文写作的助手"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=800
        )
        content = response.choices[0].message.content.strip()
        usage = response.usage.total_tokens if return_usage else None
        return (content, usage) if return_usage else content
    except Exception as e:
        return (f"[GPT 调用失败: {str(e)}]", 0) if return_usage else f"[GPT 调用失败: {str(e)}]"
