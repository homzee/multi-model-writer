# app.py
import streamlit as st
from models.chatglm import call_chatglm
from models.qwen import call_qwen
from models.baichuan import call_baichuan
from models.yi import call_yi
from models.gpt import call_gpt
from models.deepseek import call_deepseek
import io
from docx import Document
from fpdf import FPDF
import json
import os

st.set_page_config(page_title="多模型中文写作助手", layout="wide")
# ...（以下略，内容与 Canvas 相同，为节省篇幅此处不重复展示）

# 请补全 Canvas 中全部代码...