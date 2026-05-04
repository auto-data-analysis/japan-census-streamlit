"""都道府県別ランキングページ。"""

import streamlit as st

from src.query import fetch_pref_ranking, get_labor_status_list, get_year_list
from src.chart import plot_pref_ranking, COLOR_MALE, COLOR_FEMALE

st.set_page_config(page_title="都道府県別ランキング", page_icon="🏅", layout="wide")

st.title("🏅 都道府県別ランキング")

# --- サイドバー：操作パネル ---
with st.sidebar:
    st.header("絞り込み")

    labor_status_list = get_labor_status_list()
    labor_status = st.radio("労働力状態", labor_status_list, index=0)

    gender = st.radio("性別", ["男性", "女性"], index=0)

    year_list = get_year_list()
    year = st.selectbox("年", year_list, index=0)

    top_n = st.slider("表示件数", min_value=5, max_value=47, value=10, step=1)

# --- 集計 ---
df = fetch_pref_ranking(labor_status, gender, year, top_n)

if df.empty:
    st.warning("該当するデータがありません。")
    st.stop()

# --- グラフ ---
highlight_color = COLOR_MALE if gender == "男性" else COLOR_FEMALE
title = f"{year}年　{gender}　{labor_status}　上位{top_n}都道府県"
fig = plot_pref_ranking(df, title=title, highlight_color=highlight_color)
st.pyplot(fig)

# --- データテーブル（折りたたみ） ---
with st.expander("集計データを表示"):
    display_df = df.copy()
    display_df.columns = ["都道府県", "人数（人）"]
    display_df.index = range(1, len(display_df) + 1)
    display_df.index.name = "順位"
    st.dataframe(display_df, use_container_width=True)
