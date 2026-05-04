# japan-census-streamlit

国勢調査（e-Stat）データをインタラクティブに探索できるStreamlitアプリです。

## 記事

https://zenn.dev/cool_crocus678/articles/japan-census-streamlit

## セットアップ

```bash
uv sync
uv run streamlit run app.py
```

## フォルダ構成

```
.
├── .streamlit/
│   └── config.toml       # テーマ設定
├── data/
│   └── raw/              # CSVファイル（変更しない）
├── src/
│   ├── query.py          # DuckDBによる集計ロジック
│   └── chart.py          # matplotlibによる描画ロジック
├── pages/
│   ├── 1_就業者数推移.py
│   └── 2_都道府県別ランキング.py
├── app.py                # エントリーポイント
├── packages.txt          # Streamlit Community Cloud用フォント設定
└── pyproject.toml
```

## データソース

本リポジトリで使用したデータは、e-Stat（政府統計の総合窓口）が公開している国勢調査データです。

- 出典：政府統計の総合窓口（e-Stat） https://www.e-stat.go.jp/
- 利用規約：https://www.e-stat.go.jp/terms-of-use
- 統計名：国勢調査 時系列データ 人口の労働力状態，就業者の産業・職業
- 表番号：2
- 表題：労働力状態（3区分），男女別人口及び労働力率（15歳以上）－ 都道府県（昭和25年～令和2年）
- データセットURL：https://www.e-stat.go.jp/dbview?sid=0003412176

地域コード（都道府県マスタ）は別データセットを使用しています。

- データセットURL：https://www.e-stat.go.jp/regional-statistics/ssdsview/prefectures

## ライセンス

本リポジトリのコードはMIT Licenseです。データの利用については上記e-Statの利用規約に従ってください。