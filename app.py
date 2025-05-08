
import streamlit as st
from models.gpt import call_gpt
import json
import os

st.set_page_config(page_title="GPT 中文写作助手", layout="wide")
st.title("✍️ GPT 中文写作助手")

st.markdown("输入提纲后，将调用 OpenAI 的 GPT 模型生成写作内容。")

# 初始化 session 状态
if "topic" not in st.session_state:
    st.session_state.topic = ""
if "custom_prefix" not in st.session_state:
    st.session_state.custom_prefix = ""
if "prompt_template" not in st.session_state:
    st.session_state.prompt_template = "通用"

template_prefix = {
    "通用": "请根据以下提纲生成一段连贯的中文内容：",
    "学术论文": "请根据以下提纲，生成一段符合学术论文风格的文字：",
    "工作汇报": "请根据以下提纲，生成一份结构清晰的工作汇报内容：",
    "心得总结": "请根据以下提纲，生成一段个人心得总结类型的内容："
}

st.session_state.prompt_template = st.selectbox("📋 写作模板", list(template_prefix.keys()), index=list(template_prefix.keys()).index(st.session_state.prompt_template))
st.session_state.custom_prefix = st.text_area("✏️ 自定义提示词前缀（可选）", value=st.session_state.custom_prefix)
st.session_state.topic = st.text_area("📝 输入写作提纲", height=200, value=st.session_state.topic)

gpt_model = st.radio("⚙️ GPT 模型版本", ["gpt-3.5-turbo", "gpt-4o"], horizontal=True)

# 历史记录
history_file = "history.json"
history = []
if os.path.exists(history_file):
    with open(history_file, "r", encoding="utf-8") as f:
        history = json.load(f)

st.markdown("---")
st.subheader("📜 历史记录")
if history:
    for i, record in enumerate(reversed(history[-5:])):
        with st.expander(f"📄 第 {len(history) - i} 条记录（模板：{record['template']}）"):
            st.code(record['prompt'], language="markdown")
            st.markdown(record['results'].get("content", "（无内容）"))
else:
    st.info("暂无历史记录。")

# 生成按钮
if st.button("🚀 开始生成") and st.session_state.topic.strip():
    st.info("正在调用 GPT 生成内容...")
    prefix = st.session_state.custom_prefix.strip() or template_prefix[st.session_state.prompt_template]
    full_prompt = f"{prefix}\n{st.session_state.topic}"
    content, usage = call_gpt(full_prompt, model=gpt_model, return_usage=True)

    st.markdown("### 📌 GPT 生成内容")
    st.write(content)
    st.markdown(f"🔢 Token 使用量：**{usage}**")

    # 存历史
    history.append({
        "prompt": full_prompt,
        "template": st.session_state.prompt_template,
        "results": {"content": content}
    })
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
    st.success("✅ 写作完成，历史记录已保存。")
else:
    st.caption("请输入提纲并点击生成")

