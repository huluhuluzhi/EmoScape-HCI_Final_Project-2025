'''
版本 V3.0
基于 Transformer 的 Zero-Shot Learning，实现多维情绪感知与高级交互界面设计。
build by ArthurLiu
'''

import streamlit as st
from transformers import pipeline
import pandas as pd
import plotly.express as px
import time

@st.cache_resource
def load_model():
    # 使用支持多语言(含中文)的 Zero-Shot 模型
    # 这个模型比 SnowNLP 强大概 100 倍，能理解复杂的语义
    classifier = pipeline("zero-shot-classification", 
                          model="MoritzLaurer/mDeBERTa-v3-base-mnli-xnli")
    return classifier

candidate_labels = ["开心", "焦虑", "悲伤", "愤怒", "疲惫"]

with st.spinner('正在初始化 Transformer 神经引擎...'):
    classifier = load_model()

st.set_page_config(page_title="AI 情绪气象台 Pro", page_icon="🧠", layout="centered")

def inject_css(weather_type):
    css = ""
    if weather_type == "开心":
        css = """<style>.stApp {background: linear-gradient(120deg, #f6d365 0%, #fda085 100%);}</style>"""
    elif weather_type == "焦虑":
        css = """<style>.stApp {background: linear-gradient(to top, #cfd9df 0%, #e2ebf0 100%); opacity: 0.9;}</style>"""
    elif weather_type == "悲伤":
        css = """<style>.stApp {background: linear-gradient(to bottom, #5f72bd 0%, #9b23ea 100%); color: white;}</style>"""
    elif weather_type == "愤怒":
        css = """<style>.stApp {background: linear-gradient(to bottom, #870000, #190a05); color: white;}</style>"""
    elif weather_type == "疲惫":
        css = """<style>.stApp {background: linear-gradient(to top, #30cfd0 0%, #330867 100%); color: white;}</style>"""
    
    st.markdown(css, unsafe_allow_html=True)

st.title("🧠 情绪气象台 (AI Pro版)")
st.markdown("基于 **Transformer Zero-Shot Learning** 的多维情绪感知系统")

user_text = st.text_area("此刻的想法...", height=100, placeholder="试着输入：'项目快截止了，但我代码还没跑通，真的好烦躁！'")

if st.button("开始感知"):
    if not user_text:
        st.warning("请输入内容")
    else:
        start_time = time.time()
        with st.spinner("神经网络正在计算 Attention 权重..."):
            result = classifier(user_text, candidate_labels, multi_label=False)
            
            top_label = result['labels'][0]
            top_score = result['scores'][0]
            
            time.sleep(0.8)
        
        inject_css(top_label)
        
        weather_map = {
            "开心": "☀️ 晴空万里", "焦虑": "🌫️ 大雾弥漫", 
            "悲伤": "🌧️ 局部阵雨", "愤怒": "⛈️ 强雷暴", "疲惫": "🌌 静谧星空"
        }
        
        st.header(f"{weather_map[top_label]}")
        st.caption(f"主要情绪成分：{top_label} (置信度: {top_score:.1%})")
        

        st.markdown("### 📊 AI 情绪成分解析")
        st.write("人类的情绪往往不是单一的。看看 AI 在你的文字中读出了什么：")
        
        df = pd.DataFrame({
            "情绪维度": result['labels'],
            "强度": result['scores']
        })
        
        fig = px.bar(df, x="强度", y="情绪维度", orientation='h', 
                     color="强度", color_continuous_scale='Bluered')
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")
        if top_label == "焦虑":
            st.info("💡 **AI 建议**：检测到高焦虑水平。大雾天看不清路没关系，试着只关注脚下这一步。")
        elif top_label == "愤怒":
            st.error("💡 **AI 建议**：雷暴能量过大。建议立刻离开当前环境 3 分钟，去喝杯凉水。")
        elif top_label == "疲惫":
            st.success("💡 **AI 建议**：星星都亮了。虽然事情没做完，但你的大脑需要重启了。晚安。")
            
        st.write(f"推理耗时: {time.time()-start_time:.2f}s | Model: mDeBERTa-v3-base")