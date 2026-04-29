import streamlit as st
import duckdb


@st.cache_data
def load_data():
    return duckdb.sql("""
        SELECT f.*, m.地域, m.階層, m.面積（平方キロメートル）
        FROM 'fact_人口.csv' f
        JOIN 'master_地域.csv' m ON f.地域コード = m.地域コード
    """).df()


df = load_data()

st.title("東京都 昼間人口ダッシュボード")

# 階層フィルター
階層 = st.selectbox("階層を選択", sorted(df["階層"].unique()))
filtered = df[df["階層"] == 階層]

# テーブル表示
st.dataframe(filtered)

# 昼間人口棒グラフ
st.subheader("昼間人口ランキング")
chart_data = filtered.set_index("地域")["昼間人口／総数（人）"].sort_values(
    ascending=True
)
st.bar_chart(chart_data, horizontal=True)
