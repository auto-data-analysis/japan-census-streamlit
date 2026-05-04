"""Streamlitエントリーポイント。"""

import streamlit as st

st.set_page_config(
    page_title="国勢調査ダッシュボード",
    page_icon="📊",
    layout="wide",
)

st.title("📊 国勢調査ダッシュボード")
st.markdown(
    """
    e-Stat（政府統計の総合窓口）が公開している国勢調査データを集計・可視化します。

    左のサイドバーからページを選んでください。
    """
)
