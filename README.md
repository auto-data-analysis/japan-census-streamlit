# my-streamlit

東京都の昼間人口データを Streamlit + DuckDB で可視化する練習プロジェクト。

## 概要

- `@st.cache_data` を使ったデータキャッシング
- DuckDB の JOIN で fact + master を結合
- selectbox によるフィルタリング
- bar_chart で簡易可視化

## 経緯

streamlit の動作確認用に作成。
本格的な分析と Zenn 記事化は `tokyo-daytime-population-analysis` リポジトリで実施しています。

## 注意事項

- streamlit のバージョン互換性を理由に、メインの開発環境とは別の仮想環境を用意しています
- 動作確認のみで、本格的な機能拡張は行っていません

## 削除可否

このプロジェクトは独立しており、他のプロジェクトから参照されていません。
不要になればフォルダごと削除可能です。