'''
版本 V5.1 (配色增强版)
- 修复了深色背景下文字看不清的问题
- 针对不同情绪优化了文字对比度
- 增强了 CSS 选择器的权重
'''

import streamlit as st
import time
from streamlit_mic_recorder import mic_recorder
from transformers import pipeline
from huggingface_hub import InferenceClient

# 页面基础配置
st.set_page_config(page_title="EmoScape AI", page_icon="🎨", layout="wide")

# 注意：生产环境中建议将 Token 放入 st.secrets，不要直接写在代码里
HF_API_TOKEN = "" 
client = InferenceClient(token=HF_API_TOKEN)

@st.cache_resource
def load_emotion_model():
    return pipeline("zero-shot-classification", model="MoritzLaurer/mDeBERTa-v3-base-mnli-xnli")

def load_local_audio(file_path):
    """安全加载本地音频文件"""
    try:
        with open(file_path, "rb") as f:
            audio_bytes = f.read()
        return audio_bytes
    except FileNotFoundError:
        # 为了不破坏界面美观，这里用 toast 提示而不是 error
        st.toast(f"⚠️ 音频文件未找到: {file_path}", icon="🔇")
        return None

def apply_visual_theme(emotion):
    """
    根据情绪标签，注入高对比度的 CSS 配色
    """
    
    # 基础动效（保持不变）
    keyframes = """
    <style>
    @keyframes breathe { 0% { opacity: 0.8; } 50% { opacity: 1.0; } 100% { opacity: 0.8; } }
    @keyframes drift { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
    </style>
    """
    st.markdown(keyframes, unsafe_allow_html=True)

    # 核心配色逻辑：明确指定背景色(Background)和前景色(Color)
    # !important 确保覆盖 Streamlit 的默认黑白主题
    themes = {
        "焦虑": """
            <style>
            .stApp {
                background: linear-gradient(180deg, #636fa4 0%, #e8e8e8 100%);
                background-size: 400% 400%;
                animation: drift 15s ease infinite;
            }
            /* 浅色底部，必须用深色文字 */
            h1, h2, h3, p, div, span, label, .stMarkdown {
                color: #1a1a2e !important; 
            }
            /* 输入框背景微调，防止太亮刺眼 */
            .stTextArea textarea {
                background-color: rgba(255, 255, 255, 0.8) !important;
                color: #000 !important;
            }
            </style>
            """,
            
        "悲伤": """
            <style>
            .stApp {
                background: linear-gradient(to bottom, #203a43, #2c5364);
            }
            /* 深蓝背景，使用银灰色文字 */
            h1, h2, h3, p, div, span, label, .stMarkdown {
                color: #e0e0e0 !important;
            }
            .stCaption { color: #b0bec5 !important; }
            </style>
            """,
            
        "愤怒": """
            <style>
            .stApp {
                background: linear-gradient(to bottom, #4a0000, #1a0505);
                animation: breathe 5s infinite;
            }
            /* 深红背景，使用浅粉/白色文字 */
            h1, h2, h3, p, div, span, label, .stMarkdown {
                color: #ffcccc !important;
            }
            /* 按钮特殊处理：红色背景通常配白色按钮边框 */
            .stButton button {
                border-color: #ff9999 !important;
                color: #ff9999 !important;
            }
            </style>
            """,
            
        "治愈": """
            <style>
            .stApp {
                background: linear-gradient(120deg, #a18cd1 0%, #fbc2eb 100%);
                background-size: 200% 200%;
                animation: drift 10s ease infinite;
            }
            /* 糖果色背景较亮，使用深灰/深紫色文字 */
            h1, h2, h3, p, div, span, label, .stMarkdown {
                color: #4a4a4a !important;
            }
            </style>
            """,
            
        "疲惫": """
            <style>
            .stApp {
                background: linear-gradient(to top, #0f2027, #203a43, #2c5364);
            }
            /* 星空深色背景，使用暖金色/亮白色文字，增加易读性 */
            h1, h2, h3, p, div, span, label, .stMarkdown {
                color: #f0f0f0 !important;
                text-shadow: 0px 0px 5px rgba(0,0,0,0.5); /* 增加文字阴影，防止背景太花看不清 */
            }
            /* 特别强调高亮文字 */
            .highlight-text {
                color: #FFD700 !important;
                font-weight: bold;
            }
            </style>
            """
    }

    css = themes.get(emotion, themes["治愈"])
    st.markdown(css, unsafe_allow_html=True)

    # 触发特效
    if emotion == "治愈":
        st.balloons()
    elif emotion == "悲伤":
        st.snow()
    elif emotion == "愤怒":
        st.toast("🔥 正在进行情绪降温...", icon="🧊")

def generate_image(prompt):
    full_prompt = f"masterpiece, best quality, cinematic lighting, 4k wallpaper, {prompt}, emotional atmosphere, digital art"
    try:
        image = client.text_to_image(
            full_prompt,
            model="stabilityai/stable-diffusion-xl-base-1.0"
        )
        return image
    except Exception as e:
        st.error(f"画图出错了: {e}")
        return None

# 初始化模型
classifier = load_emotion_model()
candidate_labels = ["焦虑", "治愈", "愤怒", "悲伤", "疲惫"]

# ================= 1. 侧边栏：多模态设置 =================
with st.sidebar:
    st.header("🎛️ 多模态控制台")
    st.success("✅ 情感计算引擎 (mDeBERTa) Ready")
    st.success("✅ AIGC 绘图引擎 (SDXL) Ready")
    
    st.markdown("---")
    st.markdown("**偏好设置**")
    enable_audio = st.checkbox("启用白噪音疗愈", value=True)
    enable_voice = st.checkbox("启用语音输入模式", value=True)
    auto_play_audio = st.toggle("生成后自动播放音频", value=False)

# ================= 2. 主界面逻辑 =================
st.title("🎨 EmoScape: 你的心情，AI 为你作画")
st.markdown("### 多模态情感可视化系统")

col1, col2 = st.columns([1, 4])
user_text = ""

with col1:
    st.markdown("#### 🎙️ 语音输入")
    if enable_voice:
        audio = mic_recorder(start_prompt="🔴 录音", stop_prompt="⏹️ 停止", key='recorder')
        if audio:
            st.audio(audio['bytes'])
            st.info("🔄 正在转录...")
            time.sleep(1)
            # 模拟识别结果
            simulated_text = "最近实验一直失败，导师还要催进度，感觉压力好大，想去海边吹吹风。" 
            user_text = st.text_area("识别结果", value=simulated_text, height=100)
    else:
        st.info("语音模块已关闭")

with col2:
    if not user_text: 
        user_text = st.text_area("✍️ 文字记录", placeholder="在此输入你的心情，例如：'今天加班太晚了，感觉身体被掏空'...", height=135)

if st.button("✨ 生成我的心情风景", type="primary"):
    if not user_text:
        st.warning("请先输入内容...")
    else:
        # 1. 情感分析
        with st.spinner("🧠 AI 正在共情你的文字..."):
            result = classifier(user_text, candidate_labels, multi_label=False)
            top_label = result['labels'][0]
            top_score = result['scores'][0]
            time.sleep(0.8) 

        # 映射配置
        mapping = {
            "焦虑": {
                "prompt": "a lonely lighthouse in heavy fog, mysterious, calm ocean, minimal style, soothing colors",
                "sound_file": "sounds/ocean.mp3",
                "sound_name": "🌊 治愈海浪",
                "advice": "大雾总会散去。听听海浪的声音，专注于当下的呼吸。"
            },
            "悲伤": {
                "prompt": "a girl holding umbrella in rain, reflection on wet street, lofi aesthetic, soft lighting, anime style",
                "sound_file": "sounds/rain.mp3",
                "sound_name": "🌧️ 窗外雨声",
                "advice": "允许自己难过一会儿。这场雨是天空在陪你哭泣，我相信你会和自我和解的，加油！"
            },
            "愤怒": {
                "prompt": "burning fireplace in a cozy wooden cabin, snow outside window, warm atmosphere, hyperrealistic",
                "sound_file": "sounds/fire.mp3",
                "sound_name": "🔥 壁炉柴火",
                "advice": "将怒火转化为壁炉的温暖。这里很安全，你可以放松下来。"
            },
            "治愈": {
                "prompt": "beautiful rainbow over a green meadow, sunny sky, ghibli style, vibrant colors",
                "sound_file": "sounds/piano.mp3",
                "sound_name": "🎹 轻柔钢琴",
                "advice": "真棒！记住这一刻的阳光，把它存进心里。"
            },
             "疲惫": {
                "prompt": "starry night sky, milky way, quiet mountains, silhouette, dreamlike, 8k",
                "sound_file": "sounds/silence.mp3",
                "sound_name": "🌌 静谧星空",
                "advice": "世界睡着了，你也可以休息了。晚安。"
            }
        }
        
        current_mode = mapping.get(top_label, mapping["治愈"])

        # 2. 应用视觉主题（在所有计算完成后切换背景）
        apply_visual_theme(top_label)

        st.divider()
        
        # 3. 结果展示区
        res_col1, res_col2 = st.columns([1.2, 1])
        
        with res_col1:
            st.markdown(f"### 🖼️ 心情画卷：{top_label}")
            with st.spinner("🎨 AI 正在挥毫泼墨..."):
                generated_img = generate_image(current_mode["prompt"])
                if generated_img:
                    st.image(generated_img, use_container_width=True)
                else:
                    st.error("GPU 通道拥堵，请稍后重试")

        with res_col2:
            st.markdown(f"### 📊 情绪分析报告")
            
            # 使用原生进度条，但颜色会被全局 CSS 影响，通常没问题
            st.progress(top_score, text=f"情绪置信度: {top_score:.1%}")
            
            # 使用 info 框来突出建议，因为 info 框有自己的背景色，通常比较清晰
            st.info(f"💡 **AI 建议**: \n\n{current_mode['advice']}")
            
            st.markdown("### 🎧 沉浸声景")
            st.caption(f"正在播放: {current_mode['sound_name']}")
            
            audio_bytes = load_local_audio(current_mode["sound_file"])
            if audio_bytes:
                st.audio(audio_bytes, format="audio/mp3", autoplay=auto_play_audio)
                if auto_play_audio:
                    st.toast(f"🎵 已开始播放背景音")
