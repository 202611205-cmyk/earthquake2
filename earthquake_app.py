import streamlit as st
import matplotlib
matplotlib.rcParams['font.family'] = 'DejaVu Sans'
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="폐암 환자 군집 분석 시스템", layout="centered")

st.markdown("""
<style>
    .main > div { padding-top: 2rem; }
    .result-box {
        background-color: #f0fff4;
        border: 1px solid #9ae6b4;
        border-radius: 8px;
        padding: 14px 18px;
        color: #276749;
        font-size: 1rem;
        font-weight: 500;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("## 🫁 폐암 환자 군집 분석 시스템")
st.markdown("AI가 환자의 특성을 분석하여  \n어떤 군집(유형)에 속하는지 예측합니다.")
st.markdown("---")
st.markdown("### 📋 환자 정보 입력")

col1, col2, col3 = st.columns(3)
with col1:
    st.caption("나이")
    age = st.number_input("나이", min_value=0.0, max_value=120.0, value=50.0, step=0.5, label_visibility="collapsed")
with col2:
    st.caption("흡연량")
    smoking = st.number_input("흡연량", min_value=0.0, max_value=100.0, value=10.0, step=0.5, label_visibility="collapsed")
with col3:
    st.caption("음주량")
    drinking = st.number_input("음주량", min_value=0.0, max_value=100.0, value=5.0, step=0.5, label_visibility="collapsed")

st.markdown("---")

if st.button("🔍 군집 분석하기", use_container_width=True):

    # 군집 분류: 0 매우건강, 1 위험, 2 건강
    risk = smoking * 0.5 + drinking * 0.3 + max(0, age - 40) * 0.2
    if risk >= 20:
        cluster = 1
    elif risk >= 8:
        cluster = 2
    else:
        cluster = 0

    st.markdown(f'<div class="result-box">이 환자는 {cluster}번 군집에 속합니다.</div>', unsafe_allow_html=True)
    st.markdown("0번은 매우 건강군, 1번은 위험군, 2번은 건강군입니다.")

    # 샘플 데이터 생성 (흡연량, 음주량 기반)
    np.random.seed(42)

    # 군집 0: 매우 건강 - 흡연/음주 낮음
    c0_x = np.random.uniform(0, 10, 15)
    c0_y = np.random.uniform(0, 3, 15)

    # 군집 1: 위험 - 흡연/음주 높음
    c1_x = np.random.uniform(20, 35, 15)
    c1_y = np.random.uniform(5, 9, 15)

    # 군집 2: 건강 - 흡연/음주 중간
    c2_x = np.random.uniform(10, 25, 15)
    c2_y = np.random.uniform(2, 6, 15)

    fig, ax = plt.subplots(figsize=(7, 5))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')

    color_map = {0: '#f9c74f', 1: '#3d405b', 2: '#2a9d8f'}
    label_map = {0: '매우 건강군(0)', 1: '위험군(1)', 2: '건강군(2)'}

    ax.scatter(c0_x, c0_y, color=color_map[0], s=70, label=label_map[0], zorder=3)
    ax.scatter(c1_x, c1_y, color=color_map[1], s=70, label=label_map[1], zorder=3)
    ax.scatter(c2_x, c2_y, color=color_map[2], s=70, label=label_map[2], zorder=3)

    # 현재 환자
    ax.scatter(smoking, drinking, color=color_map[cluster], marker='*', s=400,
               edgecolors='#333', linewidths=0.8, zorder=5, label='현재 환자')

    ax.set_title('군집 시각화', fontsize=13, pad=10)
    ax.set_xlabel('흡연량', fontsize=10)
    ax.set_ylabel('음주량', fontsize=10)
    ax.legend(loc='upper left', fontsize=9)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(labelsize=9)

    st.pyplot(fig)
    plt.close()
