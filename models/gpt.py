def call_gpt(prompt: str, model: str = "gpt-3.5-turbo", return_usage=False):
    output = "（模拟）GPT 生成内容：" + prompt
    return (output, 123) if return_usage else output
