# census-dashboard

国勢調査（e-Stat）データをDuckDB×Pythonで集計・可視化するStreamlitダッシュボード。

## データソース

政府統計の総合窓口（e-Stat）が公開している国勢調査データを使用しています。

- 出典：政府統計の総合窓口（e-Stat） https://www.e-stat.go.jp/
- 利用規約：https://www.e-stat.go.jp/terms-of-use

## セットアップ

```bash
uv sync
uv run streamlit run app.py
```

## フォルダ構成

```
.
├── data/
│   └── raw/          # CSVファイル（変更しない）
├── src/
│   ├── query.py      # DuckDBによる集計ロジック
│   └── chart.py      # matplotlibによる描画ロジック
├── pages/
│   └── 1_就業者数推移.py
├── app.py            # エントリーポイント
└── pyproject.toml
```
