"""就業者数の推移ページ。"""

import streamlit as st

from src.query import (
    fetch_gender_trend,
    get_labor_status_list,
    get_year_range,
    get_pref_list,
)
from src.chart import plot_gender_trend

st.set_page_config(page_title="就業者数の推移", page_icon="📈", layout="wide")

st.title("📈 労働力状態別人口の推移（男女別）")

# --- サイドバー：操作パネル ---
with st.sidebar:
    st.header("絞り込み")

    labor_status_list = get_labor_status_list()
    labor_status = st.radio("労働力状態", labor_status_list, index=0)

    year_min, year_max = get_year_range()
    start_year, end_year = st.select_slider(
        "期間",
        options=list(range(year_min, year_max + 1, 5)),
        value=(1965, year_max),
    )

    pref_list = get_pref_list()
    selected_prefs = st.multiselect(
        "都道府県（未選択で全国）",
        pref_list,
        placeholder="都道府県を選択...",
    )

# --- 集計 ---
df = fetch_gender_trend(
    labor_status, start_year, end_year, prefs=selected_prefs or None
)

if df.empty:
    st.warning("該当するデータがありません。")
    st.stop()

# --- グラフ ---
pref_label = "・".join(selected_prefs) if selected_prefs else "全国"
title = f"{start_year}–{end_year}年　{pref_label}　{labor_status}数の推移（男女別）"
fig = plot_gender_trend(df, title=title)
st.pyplot(fig)

# --- データテーブル（折りたたみ） ---
with st.expander("集計データを表示"):
    display_df = df[["year", "male", "female"]].copy()
    display_df.columns = ["年", "男（人）", "女（人）"]
    st.dataframe(display_df.set_index("年"), use_container_width=True)
