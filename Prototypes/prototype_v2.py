'''
版本 V2.0
新增多样化交互界面，实现“情绪气象台”概念，通过天气隐喻展现情绪状态。
build by ArthurLiu
'''


import streamlit as st
from snownlp import SnowNLP
import time

st.set_page_config(page_title="情绪气象台", page_icon="🌦️", layout="centered")

# 晴天样式
sunny_css = """
<style>
.stApp {
    background: linear-gradient(120deg, #a1c4fd 0%, #c2e9fb 100%);
    transition: background 1s ease;
}
.weather-icon { font-size: 80px; text-align: center; animation: float 3s infinite ease-in-out; }
@keyframes float { 0% { transform: translateY(0px); } 50% { transform: translateY(-20px); } 100% { transform: translateY(0px); } }
</style>
"""

# 雨天样式
rain_css = """
<style>
.stApp {
    background: linear-gradient(to bottom, #232526, #414345);
    color: white;
    transition: background 1s ease;
}
.weather-icon { font-size: 80px; text-align: center; }
</style>
"""

# ================= 侧边栏 =================
with st.sidebar:
    st.markdown("### 🛠️ 开发者调试面板")
    st.info("本栏仅在演示时辅助使用，真实用户不可见")
    force_mood = st.radio("强制干预模式 (Wizard of Oz)", ["Auto (AI分析)", "强制-雨天", "强制-晴天"])

# ================= 主界面 =================
st.markdown("<h1 style='text-align: center; font-family: serif;'>情绪气象台</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; opacity: 0.7;'>将你的心事告诉天空...</p>", unsafe_allow_html=True)

user_text = st.text_area("", height=100, placeholder="最近压力好大，感觉喘不过气...")

if st.button("生成今日天气 ☁️"):
    if not user_text:
        st.warning("请先输入内容...")
    else:
        with st.spinner("AI正在感知你的情绪气压..."):
            time.sleep(1.5)
        
        score = 0.5
        if force_mood == "Auto (AI分析)":
            s = SnowNLP(user_text)
            score = s.sentiments
        elif force_mood == "强制-雨天":
            score = 0.1
        else:
            score = 0.9
            
        st.markdown("---")
        
        if score < 0.4:
            st.markdown(rain_css, unsafe_allow_html=True)
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown('<div class="weather-icon">🌧️</div>', unsafe_allow_html=True)
            with col2:
                st.markdown(f"### 局部雷雨 (情绪指数: {score:.2f})")
                st.write("检测到高压区。不要急着赶路，先避避雨吧。")
                st.info("💡 建议：已为您开启白噪音模式，请深呼吸 3 次。")
                # 播放雨声 (这里放一个免费的雨声外链)
                st.audio("https://actions.google.com/sounds/v1/weather/rain_heavy_loud.ogg")
                
        else:
            st.markdown(sunny_css, unsafe_allow_html=True)
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown('<div class="weather-icon">☀️</div>', unsafe_allow_html=True)
            with col2:
                st.markdown(f"### 晴空万里 (情绪指数: {score:.2f})")
                st.write("你的心情就像今天的阳光一样明媚！")
                st.balloons() 