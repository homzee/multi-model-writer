import streamlit as st
from models.chatglm import call_chatglm
from models.qwen import call_qwen
from models.baichuan import call_baichuan
from models.yi import call_yi
from models.gpt import call_gpt
from models.deepseek import call_deepseek
import json
import os

st.set_page_config(page_title="多模型中文写作助手", layout="wide")
st.title("📝 多模型中文写作助手")

st.markdown("""输入提纲后，将同时调用多个中文大模型生成写作内容，供你比对选择。""")

# 初始化状态
if "topic" not in st.session_state:
    st.session_state.topic = ""
if "custom_prefix" not in st.session_state:
    st.session_state.custom_prefix = ""
if "prompt_template" not in st.session_state:
    st.session_state.prompt_template = "通用"
if "force_generate" not in st.session_state:
    st.session_state.force_generate = False

template_prefix = {
    "通用": "请根据以下提纲生成一段连贯的中文内容：",
    "学术论文": "请根据以下提纲，生成一段符合学术论文风格的文字：",
    "工作汇报": "请根据以下提纲，生成一份结构清晰的工作汇报内容：",
    "心得总结": "请根据以下提纲，生成一段个人心得总结类型的内容："
}

# UI 控件
st.session_state.prompt_template = st.selectbox(
    "📋 选择写作模板：",
    list(template_prefix.keys()),
    index=list(template_prefix.keys()).index(st.session_state.prompt_template)
)
st.session_state.custom_prefix = st.text_area("✏️ 可选：自定义提示词前缀（留空则使用模板默认）", value=st.session_state.custom_prefix)
st.session_state.topic = st.text_area("✍️ 请输入写作提纲：", height=200, value=st.session_state.topic)

models_selected = st.multiselect(
    "🧠 选择要调用的大模型：",
    ["ChatGLM", "Qwen", "Baichuan", "Yi", "DeepSeek", "GPT"],
    default=["ChatGLM", "Qwen", "DeepSeek"]
)

gpt_model = "gpt-3.5-turbo"
if "GPT" in models_selected:
    gpt_model = st.radio("⚙️ GPT 版本：", ["gpt-3.5-turbo", "gpt-4o"], horizontal=True)

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
            if st.button(f"🔁 重新生成第 {len(history) - i} 条", key=f"regen_{i}"):
                st.session_state.topic = record['prompt'].split("\n", 1)[-1]
                st.session_state.custom_prefix = record['prompt'].split("\n", 1)[0]
                st.session_state.prompt_template = record['template']
                st.session_state.force_generate = True

else:
    st.info("暂无历史记录。")

# 提前触发生成（如来自历史记录）
if st.session_state.force_generate:
    st.session_state.force_generate = False
    st.experimental_rerun()

# 生成按钮
if st.button("🚀 开始生成") and st.session_state.topic.strip():
    st.info("正在生成内容，请稍候...")
    results = {}
    prefix = st.session_state.custom_prefix.strip() or template_prefix[st.session_state.prompt_template]
    full_prompt = f"{prefix}\n{st.session_state.topic}"

    if "ChatGLM" in models_selected:
        results["ChatGLM"] = call_chatglm(full_prompt)
    if "Qwen" in models_selected:
        results["Qwen"] = call_qwen(full_prompt)
    if "Baichuan" in models_selected:
        results["Baichuan"] = call_baichuan(full_prompt)
    if "Yi" in models_selected:
        results["Yi"] = call_yi(full_prompt)
    if "DeepSeek" in models_selected:
        results["DeepSeek"] = call_deepseek(full_prompt)
    if "GPT" in models_selected:
        content, usage = call_gpt(full_prompt, model=gpt_model, return_usage=True)
        results[f"GPT ({gpt_model})"] = content
        st.markdown(f"🔢 GPT Token 使用量：**{usage}** tokens")

    st.subheader("📌 模型生成内容对比")
    cols = st.columns(len(results))
    for idx, (model, content) in enumerate(results.items()):
        with cols[idx]:
            st.markdown(f"**{model}**")
            st.write(content)

    history.append({
        "prompt": full_prompt,
        "template": st.session_state.prompt_template,
        "results": results
    })
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

    st.success("✅ 写作完成，历史记录已保存。")
else:
    st.caption("请先输入提纲并选择模型")
