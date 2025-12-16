'''
版本 V1.0
无多样交互界面实现，仅提供基础情绪分析功能。
build by ArthurLiu
'''

import streamlit as st
from snownlp import SnowNLP

st.title("情绪分析工具 V1.0")

text = st.text_input("输入日记：")

if st.button("分析"):
    s = SnowNLP(text)
    score = s.sentiments
    st.write(f"情感得分: {score}")
    
    if score < 0.5:
        st.write("判断结果：负面情绪")
    else:
        st.write("判断结果：正面情绪")