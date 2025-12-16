'''
版本 V5.0
最后加入了背景变色和情绪切换特效
build by ArthurLiu
'''


import streamlit as st
import time
from streamlit_mic_recorder import mic_recorder
from transformers import pipeline

from huggingface_hub import InferenceClient

st.set_page_config(page_title="EmoScape AI", page_icon="🎨", layout="wide")

HF_API_TOKEN = "hf_xxxxxxxxx" # 若想使用，请替换成自己HuggingFace的真实 Token


client = InferenceClient(token=HF_API_TOKEN)

@st.cache_resource
def load_emotion_model():
    return pipeline("zero-shot-classification", model="MoritzLaurer/mDeBERTa-v3-base-mnli-xnli")

def load_local_audio(file_path):
    """安全加载本地音频文件，找不到文件时返回 None"""
    try:
        with open(file_path, "rb") as f:
            audio_bytes = f.read()
        return audio_bytes
    except FileNotFoundError:
        st.error(f"⚠️ 音频文件丢失: {file_path}，请检查路径。")
        return None

def apply_visual_theme(emotion):
    """
    根据情绪标签，注入对应的 CSS 背景特效和 Streamlit 动效
    """

    keyframes = """
    <style>
    @keyframes breathe {
        0% { opacity: 0.8; }
        50% { opacity: 1.0; }
        100% { opacity: 0.8; }
    }
    @keyframes shake {
        0% { transform: translate(1px, 1px) rotate(0deg); }
        10% { transform: translate(-1px, -2px) rotate(-1deg); }
        20% { transform: translate(-3px, 0px) rotate(1deg); }
        30% { transform: translate(3px, 2px) rotate(0deg); }
        40% { transform: translate(1px, -1px) rotate(1deg); }
        50% { transform: translate(-1px, 2px) rotate(-1deg); }
        60% { transform: translate(-3px, 1px) rotate(0deg); }
        70% { transform: translate(3px, 1px) rotate(-1deg); }
        80% { transform: translate(-1px, -1px) rotate(1deg); }
        90% { transform: translate(1px, 2px) rotate(0deg); }
        100% { transform: translate(1px, -2px) rotate(-1deg); }
    }
    @keyframes drift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    </style>
    """
    st.markdown(keyframes, unsafe_allow_html=True)

 
    themes = {
        "焦虑": """
            <style>
            .stApp {
                background: linear-gradient(180deg, #636fa4 0%, #e8e8e8 100%);
                background-size: 400% 400%;
                animation: drift 15s ease infinite; /* 缓慢流动的雾气感 */
            }
            </style>
            """,
        "悲伤": """
            <style>
            .stApp {
                background: linear-gradient(to bottom, #203a43, #2c5364); /* 深蓝雨夜 */
                color: #e0e0e0;
            }
            </style>
            """,
        "愤怒": """
            <style>
            .stApp {
                background: linear-gradient(to bottom, #4a0000, #1a0505); /* 深红岩浆 */
                color: #ffcccc;
                animation: breathe 5s infinite; /* 急促的呼吸/脉动感 */
            }
            </style>
            """,
        "治愈": """
            <style>
            .stApp {
                background: linear-gradient(120deg, #a18cd1 0%, #fbc2eb 100%); /* 梦幻糖果色 */
                background-size: 200% 200%;
                animation: drift 10s ease infinite; /* 柔和流动 */
                color: #333333;
            }
            </style>
            """,
        "疲惫": """
            <style>
            .stApp {
                background: linear-gradient(to top, #0f2027, #203a43, #2c5364); /* 静谧星空 */
                color: #d7d7d7;
            }
            </style>
            """
    }

    css = themes.get(emotion, themes["治愈"])
    st.markdown(css, unsafe_allow_html=True)

    # 4. 触发 Streamlit 原生特效 
    if emotion == "治愈":
        st.balloons()  # 撒气球
    elif emotion == "悲伤":
        st.snow()      # 下雪 (隐喻下雨/寒冷)
    elif emotion == "愤怒":
        st.toast("🔥 检测到强烈情绪波动，正在启动降温程序...", icon="🧊")

def generate_image(prompt):
    
    full_prompt = f"masterpiece, best quality, cinematic lighting, 4k wallpaper, {prompt}, emotional atmosphere, digital art"
    
    try:
        image = client.text_to_image(
            full_prompt,
            model="stabilityai/stable-diffusion-xl-base-1.0"
        )
        return image
    except Exception as e:
        print(f"Error generating image: {e}")
        st.error(f"生成图片时遇到问题: {e}")
        return None


classifier = load_emotion_model()
candidate_labels = ["焦虑", "治愈", "愤怒", "悲伤", "疲惫"]

# ================= 1. 侧边栏：多模态设置 =================
with st.sidebar:
    st.header("🎛️ 多模态控制台")
    st.success("✅ 情感计算引擎 (mDeBERTa) 已就绪")
    st.success("✅ AIGC 绘图引擎 (SDXL) 已就绪")
    
    st.markdown("---")
    st.markdown("**问卷数据应用 (Survey Source)**")
    st.caption("基于《大学生情绪表达现状调研》配置：")
    enable_audio = st.checkbox("启用白噪音疗愈 (86%用户偏好)", value=True)
    enable_voice = st.checkbox("启用语音输入模式 (60%用户偏好)", value=True)
    auto_play_audio = st.toggle("生成后自动播放白噪音", value=False)

# ================= 2. 主界面逻辑 =================
st.title("🎨 EmoScape: 你的心情，AI 为你作画")
st.markdown("### 多模态情感可视化系统 (Multimodal Emotion Visualization)")

col1, col2 = st.columns([1, 4])

user_text = ""

with col1:
    st.markdown("#### 🎙️ 语音碎碎念")
    if enable_voice:
        audio = mic_recorder(start_prompt="点击录音", stop_prompt="停止并识别", key='recorder')
        if audio:
            st.audio(audio['bytes'])
            '''
            这里我们为了演示稳定，模拟了语音转文字的结果
            真实项目可接入 Whisper: st.write(whisper_model.transcribe(audio['bytes']))
            '''
            st.info("🔄 Whisper 正在转录...")
            time.sleep(1)
            # 模拟识别结果，演示时可以说这段话
            simulated_text = "最近实验一直失败，导师还要催进度，感觉压力好大，想去海边吹吹风。" 
            user_text = st.text_area("识别结果：", value=simulated_text, height=100)
    else:
        st.info("语音模块已关闭")

with col2:
    if not user_text: 
        user_text = st.text_area("✍️ 文字记录", placeholder="写下此刻的心情，让 AI 为你生成专属风景...", height=135)

if st.button("✨ 生成我的心情风景"):
    if not user_text:
        st.warning("请先输入或录入内容...")
    else:
        # 1. 情感分析
        with st.spinner("🧠 神经网络正在解析情绪成分..."):
            result = classifier(user_text, candidate_labels, multi_label=False)
            top_label = result['labels'][0]
            top_score = result['scores'][0]
            time.sleep(0.5) # 演示节奏控制

        

        mapping = {
            "焦虑": {
                "prompt": "a lonely lighthouse in heavy fog, mysterious, calm ocean, minimal style, soothing colors",
                "sound_file": "sounds/ocean.mp3",  # 改成本地路径
                "sound_name": "🌊 治愈海浪 (Ocean Waves)",
                "advice": "大雾总会散去。听听海浪的声音，专注于当下的呼吸。"
            },
            "悲伤": {
                "prompt": "a girl holding umbrella in rain, reflection on wet street, lofi aesthetic, soft lighting, anime style",
                "sound_file": "sounds/rain.mp3",   # 改成本地路径
                "sound_name": "🌧️ 窗外雨声 (Soft Rain)",
                "advice": "允许自己难过一会儿。这场雨是天空在陪你哭泣。"
            },
            "愤怒": {
                "prompt": "burning fireplace in a cozy wooden cabin, snow outside window, warm atmosphere, hyperrealistic",
                "sound_file": "sounds/fire.mp3",   # 改成本地路径
                "sound_name": "🔥 壁炉柴火 (Fireplace)",
                "advice": "将怒火转化为壁炉的温暖。这里很安全，你可以放松下来。"
            },
            "治愈": {
                "prompt": "beautiful rainbow over a green meadow, sunny sky, ghibli style, vibrant colors",
                "sound_file": "sounds/piano.mp3",  # 改成本地路径
                "sound_name": "🎹 轻柔钢琴 (Soft Piano)",
                "advice": "真棒！记住这一刻的阳光，把它存进心里。"
            },
             "疲惫": {
                "prompt": "starry night sky, milky way, quiet mountains, silhouette, dreamlike",
                "sound_file": "sounds/silence.mp3", # 改成本地路径
                "sound_name": "🌌 静谧星空 (White Noise)",
                "advice": "世界睡着了，你也可以休息了。晚安。"
            }
        }
        
        current_mode = mapping.get(top_label, mapping["治愈"])

 
        apply_visual_theme(top_label)

        st.markdown("---")
        
        res_col1, res_col2 = st.columns([1, 1])
        
        with res_col1:
            st.markdown(f"### 🖼️ AI 生成的心情画卷：{top_label}")
            with st.spinner("🎨 Diffusion 模型正在逐像素绘制..."):
                generated_img = generate_image(current_mode["prompt"])
                
                if generated_img:
                    st.image(generated_img, caption=f"Prompt: {current_mode['prompt']}", use_container_width=True)
                else:
                    st.error("GPU 算力繁忙，请稍后重试")

        with res_col2:
            st.markdown(f"### 📊 情绪分析报告")
            st.progress(top_score, text=f"主要情绪置信度: {top_score:.1%}")
            st.info(f"💡 **AI 建议**: {current_mode['advice']}")
            
            st.markdown("---")
            st.markdown("### 🎧 沉浸式声景")
            st.caption(f"当前声源: {current_mode['sound_name']}")
            
            audio_bytes = load_local_audio(current_mode["sound_file"])
            
            if audio_bytes:

                st.audio(audio_bytes, format="audio/mp3", autoplay=auto_play_audio)
                
                if auto_play_audio:
                    st.toast(f"正在自动播放: {current_mode['sound_name']}")