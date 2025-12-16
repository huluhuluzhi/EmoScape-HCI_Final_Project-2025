# EmoScape-HCI_Final_Project-2025
# 技术实现与迭代文档
### 🌦️ 情绪气象台 (EmoScape) - A multimodal AI system that visualizes emotions as generative weather. Powered by Transformers (Zero-Shot) &amp; Stable Diffusion. [HCI Final Project]


> **项目名称**：人机交互期末团队项目 - 多模态情绪可视化系统
> 
> **技术负责人**：Arthur Liu

-----

## 📖 项目简介

本项目是一个基于 **生成式 AI (AIGC)** 与 **多模态交互** 的情绪可视化系统。旨在解决大学生“隐性焦虑”与表达障碍痛点，通过将抽象情绪转化为具象的“天气”与“风景”，提供兼具**沉浸感**与**治愈感**的交互体验。

-----

## 🛠️ 核心技术栈 (Tech Stack)

  * **前端交互**: Python Streamlit + Custom CSS Injection (动态视觉引擎)
  * **核心推理**: HuggingFace Transformers (`mDeBERTa-v3-base`) - **Zero-Shot Classification**
  * **视觉生成**: Stable Diffusion XL (via HuggingFace Inference API)
  * **数据可视化**: Plotly (情绪成分雷达图)
  * **音频处理**: Streamlit Audio / Local Soundscapes

-----

## 🚀 设计迭代过程 (Design Iteration Log)


### 🟢 阶段一：功能验证原型 (v1.0 Proof of Concept)

  * **目标**: 快速验证“情绪转数值”的可行性。
  * **实现**: 采用了基础的 `SnowNLP` 库进行中文情感倾向分析。
  * **局限**: 只能识别简单的“积极/消极”二元对立，无法捕捉复杂情绪，且准确率较低。

### 🟡 阶段二：沉浸式体验原型 (v2.0 High-fidelity Prototype)

  * **改进点**: 引入了\*\*“多模态隐喻”\*\*概念，尝试加入视觉（动态背景色/天气图标）+ 听觉（治愈白噪音/音效）。
  * **演示场景**:
      * **场景A (焦虑)**: 输入“作业多好累” -\> 背景变暗/下雨图标/雨声 -\> 弹出深呼吸建议。
      * **场景B (开心)**: 输入“代码跑通了” -\> 背景亮蓝/晴天图标/气球动画。

### 🟠 阶段三：AI 内核重构 (v3.0 The AI Overhaul)

  * **痛点解决**: 彻底解决 v1.0 中 SnowNLP 识别不准的问题。
  * **核心升级**: 引入 **HuggingFace Transformers** 架构。
      * **模型替换**: 弃用贝叶斯算法，改用 **`MoritzLaurer/mDeBERTa-v3-base-mnli-xnli`**。
      * **技术亮点 (Zero-Shot Classification)**: 基于 Transformer 的零样本分类技术，无需特定训练即可理解“焦虑”、“疲惫”、“愤怒”等复杂标签。
  * **HCI 深度体现**:
      * **细粒度情感**: 将情绪从 2 类扩展至 5 类具体情感。
      * **可解释性 (Explainability)**: 新增 **“情绪成分分析雷达图”**。
          * *话术*: “虽然用户觉得是生气，但 AI 发现其中 30% 是焦虑。这体现了 HCI 中帮助用户‘自我认知’的深度。”

#### 📊 情绪-天气映射表 (Emotion-Weather Mapping)

| 情绪标签 | 天气隐喻 | 视觉设计 (CSS) | HCI 关怀策略 |
| :--- | :--- | :--- | :--- |
| **开心 (Joy)** | ☀️ 晴空万里 | 暖橙色渐变 + 阳光动效 | 正向强化，撒花特效 |
| **焦虑 (Anxiety)** | 🌫️ 大雾弥漫 | 灰白色渐变 + 模糊滤镜 | 降低信息密度，提供清晰指引 |
| **悲伤 (Sadness)** | 🌧️ 连绵阴雨 | 蓝紫色渐变 + 雨滴动效 | 陪伴感，播放白噪音 |
| **愤怒 (Anger)** | ⛈️ 雷暴天气 | 深红/黑渐变 + 闪电特效 | 引导深呼吸，宣泄出口 |
| **疲惫 (Fatigue)** | 🌌 静谧星空 | 深蓝夜空 + 星星闪烁 | 助眠引导，暗示“该休息了” |

### 🔵 阶段四：AIGC 多模态生成 (v4.0 Generative Era)

  * **用户研究驱动开发**:
      * *数据引用*: 调研显示 **78%** 用户偏好听觉安抚，**86%** 用户认为“可视化图片”比分数更治愈。
  * **技术升级**: 构建**多模态生成式情感交互架构**。
      * **AIGC 画师**: 接入 **Stable Diffusion**。
          * *旧方案*: 固定贴图。
          * *新方案*: **千人千面**。用户输入“失恋难过”和“挂科难过”，AI 会生成截然不同的雨景画作。
      * **沉浸式声景**: 响应问卷需求，建立情感-音频映射矩阵（本地加载海浪、壁炉、钢琴声），实现全感官包围。
      * **语音计算**: 集成语音输入模块（模拟 Whisper 流程），响应 **60%** 用户“语音碎碎念”的需求。

### 🟣 阶段五：终极交互打磨 (v5.0 Final Polish)

  * **核心理念**: **系统状态的可视化反馈 (Visual Feedback)**。
  * **实现细节**: 通过动效让用户潜意识“感觉”到系统的情绪理解。

#### 🎨 视觉隐喻与交互动效表

| 情绪类别 | 视觉隐喻 | 交互动效 (Micro-interaction) | HCI 设计意图 |
| :--- | :--- | :--- | :--- |
| **治愈** | 暖色渐变 | **漂浮 (Drift) + 撒花** | 庆祝式动画，提供正向强化 |
| **悲伤** | 冷色深渊 | **下落 (Snow/Rain)** | 模拟物理规律，提供情感共鸣 |
| **愤怒** | 警示深红 | **急促脉动 (Pulse)** | 模拟心跳加速，暗示需要平复 |
| **焦虑** | 迷雾灰 | **缓慢流动 (Slow Flow)** | 低对比度降噪，减少视觉刺激 |

-----

## 💻 本地运行指南 (How to Run)

如果你需要在本地复现演示效果，请按以下步骤操作：

1.  **克隆仓库**

    ```bash
    git clone https://github.com/huluhuluzhi/EmoScape-HCI_Final_Project-2025.git
    ```

2.  **安装依赖**

    ```bash
    pip install streamlit transformers torch plotly huggingface_hub streamlit-mic-recorder
    ```

3.  **配置 Token (重要)**
    打开 `prototype_v5.py`，找到 `HF_API_TOKEN`，填入你的 Hugging Face Token (Write权限)。

4.  **准备音频文件**
    确保 `sounds/` 目录下包含 `ocean.mp3`, `rain.mp3`, `fire.mp3`, `piano.mp3`, `silence.mp3`。

5.  **启动系统**

    ```bash
    streamlit run prototype_v5.py
    ```

-----

> **Note for Team**: 演示视频录制建议使用 v5.0 版本，并开启侧边栏的“自动播放”功能以获得最佳效果。如有 Bug 请联系技术负责人。
