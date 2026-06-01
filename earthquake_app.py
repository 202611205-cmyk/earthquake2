import streamlit as st
import folium
from streamlit_folium import st_folium
import random
import math

st.set_page_config(page_title="세계 지진 위험도 분석 시스템", layout="centered")

st.markdown("""
<style>
    .main > div { padding-top: 2rem; }
    .risk-high { font-size: 1.4rem; font-weight: 700; color: #c53030; margin: 1rem 0; }
    .risk-mid  { font-size: 1.4rem; font-weight: 700; color: #c05621; margin: 1rem 0; }
    .risk-low  { font-size: 1.4rem; font-weight: 700; color: #276749; margin: 1rem 0; }
</style>
""", unsafe_allow_html=True)

st.title("세계 지진 위험도 분석 시스템")
st.caption("위도와 경도를 입력하면 주변 지진 데이터를 기반으로 위험도를 분석합니다.")

st.caption("위도 입력")
lat = st.number_input("위도", min_value=-90.0, max_value=90.0, value=37.50, step=0.5, label_visibility="collapsed")

st.caption("경도 입력")
lon = st.number_input("경도", min_value=-180.0, max_value=180.0, value=127.00, step=0.5, label_visibility="collapsed")

# 지진 다발 지역 데이터 (위도, 경도, 규모)
EARTHQUAKE_ZONES = [
    # 환태평양 불의 고리
    (35.6, 139.7, 6.5), (37.5, 141.0, 7.2), (33.0, 131.0, 5.8),
    (40.0, 143.0, 6.8), (28.0, 130.0, 5.5), (45.0, 150.0, 6.2),
    (50.0, 156.0, 5.9), (55.0, 160.0, 6.1), (60.0, 165.0, 5.7),
    (19.4, -155.3, 6.0), (21.0, -157.0, 5.5), (61.0, -150.0, 6.3),
    (58.0, -152.0, 5.8), (52.0, -175.0, 6.5), (48.0, -122.0, 5.2),
    (37.7, -122.4, 6.0), (34.0, -118.0, 5.8), (19.0, -99.0, 5.5),
    (13.0, -89.0, 6.2), (-12.0, -77.0, 5.9), (-33.0, -70.0, 6.1),
    (-18.0, -70.0, 5.7), (-41.0, 174.0, 5.5), (-43.0, 172.0, 6.0),
    (-8.0, 115.0, 5.8), (1.0, 124.0, 6.3), (14.0, 121.0, 5.6),
    (-6.0, 105.0, 6.5), (-8.0, 120.0, 5.9), (4.0, 96.0, 7.5),
    # 알프스-히말라야 지진대
    (28.0, 84.0, 6.8), (36.0, 70.0, 6.2), (38.0, 43.0, 5.8),
    (39.0, 35.0, 5.5), (38.0, 22.0, 6.0), (37.0, 15.0, 5.7),
    (43.0, 13.0, 5.3), (41.0, 29.0, 5.9), (40.0, 50.0, 6.1),
    (35.0, 60.0, 5.8), (30.0, 57.0, 6.3), (29.0, 52.0, 5.6),
    # 기타
    (-4.0, 15.0, 5.2), (0.0, 30.0, 5.5), (38.0, 15.0, 5.4),
    (-20.0, -175.0, 6.7), (-15.0, 167.0, 6.4), (17.0, -62.0, 5.1),
    (18.5, -72.0, 5.8), (10.0, -84.0, 5.3),
    # 추가 랜덤 분포
    (46.0, 13.0, 4.8), (47.0, 18.0, 4.5), (36.5, 25.0, 5.2),
    (32.0, 35.0, 4.9), (24.0, 121.0, 5.7), (23.0, 120.0, 6.0),
    (-37.0, -72.0, 5.5), (-25.0, -65.0, 5.0), (6.0, -77.0, 5.3),
    (10.0, 125.0, 5.6), (8.0, 126.0, 6.1), (16.0, 120.0, 5.4),
]

def get_risk(lat, lon):
    min_dist = float('inf')
    for eq_lat, eq_lon, mag in EARTHQUAKE_ZONES:
        dist = math.sqrt((lat - eq_lat)**2 + (lon - eq_lon)**2)
        weighted = dist / (mag / 5.0)
        if weighted < min_dist:
            min_dist = weighted
    if min_dist < 5:
        return "높음"
    elif min_dist < 12:
        return "중간"
    else:
        return "낮음"

def get_color(mag):
    if mag >= 6.5:
        return 'red'
    elif mag >= 5.5:
        return 'green'
    else:
        return 'blue'

if st.button("위험도 분석"):
    risk = get_risk(lat, lon)

    css_class = {"높음": "risk-high", "중간": "risk-mid", "낮음": "risk-low"}[risk]
    st.markdown(f'<div class="{css_class}">예상 위험도: {risk}</div>', unsafe_allow_html=True)

    m = folium.Map(location=[lat, lon], zoom_start=4, tiles="CartoDB positron")

    for eq_lat, eq_lon, mag in EARTHQUAKE_ZONES:
        folium.CircleMarker(
            location=[eq_lat, eq_lon],
            radius=6,
            color=get_color(mag),
            fill=True,
            fill_opacity=0.8,
            popup=f"규모: {mag}",
        ).add_to(m)

    folium.Marker(
        location=[lat, lon],
        icon=folium.Icon(color='black', icon='star', prefix='fa'),
        popup="입력 위치"
    ).add_to(m)

    st_folium(m, width=680, height=400)

    st.caption("🔴 규모 6.5 이상  🟢 규모 5.5~6.4  🔵 규모 5.5 미만  ★ 입력 위치")
