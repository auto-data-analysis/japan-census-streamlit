"""matplotlibによる描画ロジック。"""

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import pandas as pd
import matplotlib.dates as mdates
from matplotlib.figure import Figure
from matplotlib.ticker import FuncFormatter, MaxNLocator

TEXT_COLOR = "#595959"
COLOR_MALE = "#9DB7F9"  # ブルー系
COLOR_FEMALE = "#FFA66D"  # オレンジ系
LABEL_MALE = "男性"
LABEL_FEMALE = "女性"


def _set_japanese_font() -> None:
    """日本語フォントを設定する。"""
    import matplotlib.font_manager as fm

    # フォントキャッシュを再構築
    fm._load_fontmanager(try_read_cache=False)

    # フォントファイルを直接指定（Linux環境用）
    font_paths = [
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc",
    ]
    for path in font_paths:
        import os

        if os.path.exists(path):
            fm.fontManager.addfont(path)
            prop = fm.FontProperties(fname=path)
            plt.rcParams["font.family"] = prop.get_name()
            return

    # フォールバック：名前で検索
    candidates = ["Noto Sans CJK JP", "Noto Sans CJK", "Meiryo", "IPAexGothic"]
    available = {f.name for f in fm.fontManager.ttflist}
    for font in candidates:
        if font in available:
            plt.rcParams["font.family"] = font
            return


def plot_gender_trend(
    df: pd.DataFrame,
    title: str = "就業者数の推移（男女別）",
    figsize: tuple[int, int] = (10, 4),
    dpi: int = 200,
) -> Figure:
    """
    男女別の折れ線グラフを返す。

    Parameters
    ----------
    df : DataFrame
        columns = [year, male, female]
    title : str
    figsize : tuple
    dpi : int

    Returns
    -------
    matplotlib.figure.Figure
    """
    _set_japanese_font()
    df = df.copy().sort_values("year")
    df["year_dt"] = pd.to_datetime(df["year"], format="%Y")

    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)

    ax.plot(df["year_dt"], df["male"], label=LABEL_MALE, color=COLOR_MALE, linewidth=3)
    ax.plot(
        df["year_dt"], df["female"], label=LABEL_FEMALE, color=COLOR_FEMALE, linewidth=3
    )

    # 右端ラベル
    x_last = df["year_dt"].iloc[-1]
    ax.text(
        x_last,
        df["male"].iloc[-1],
        f" {LABEL_MALE}",
        color=COLOR_MALE,
        va="center",
        fontsize=12,
    )
    ax.text(
        x_last,
        df["female"].iloc[-1],
        f" {LABEL_FEMALE}",
        color=COLOR_FEMALE,
        va="center",
        fontsize=12,
    )

    # 装飾
    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.yaxis.set_major_locator(MaxNLocator(nbins=4))
    ax.tick_params(axis="both", length=0, colors=TEXT_COLOR)
    ax.yaxis.grid(True, color="lightgray", linewidth=0.5)
    ax.xaxis.grid(False)
    ax.set_xticks(df["year_dt"])
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

    # y軸：万人単位
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{int(x / 10000):,}"))
    ax.text(
        -0.05,
        1.02,
        "(万人)",
        transform=ax.transAxes,
        ha="left",
        va="bottom",
        fontsize=10,
        color=TEXT_COLOR,
    )

    ax.set_title(title, fontsize=12, fontweight="bold", pad=8, color=TEXT_COLOR)
    plt.tight_layout()

    return fig


def plot_pref_ranking(
    df: pd.DataFrame,
    title: str = "都道府県別ランキング",
    bar_color: str = "#E6ECFA",
    dpi: int = 200,
) -> Figure:
    """
    都道府県別の横棒グラフを返す。

    Parameters
    ----------
    df : DataFrame
        columns = [pref, value]  降順ソート済み
    title : str
    bar_color : str
        全棒の色。デフォルトは薄いブルー（#E6ECFA）。
        色を変えたい場合は明示的に渡す。
    dpi : int

    Returns
    -------
    matplotlib.figure.Figure
    """
    _set_japanese_font()
    df = df.copy()

    # 上から多い順に表示するため反転
    df = df.iloc[::-1].reset_index(drop=True)

    # 全棒を同色
    colors = [bar_color] * len(df)

    # 件数に応じて縦サイズを動的に決定（1件あたり0.45インチ、最低4インチ）
    fig_height = max(4, len(df) * 0.45)
    fig, ax = plt.subplots(figsize=(9, fig_height), dpi=dpi)
    bars = ax.barh(df["pref"], df["value"], color=colors)

    # 数値ラベル
    max_val = df["value"].max()
    for bar in bars:
        width = bar.get_width()
        ax.text(
            width + max_val * 0.01,
            bar.get_y() + bar.get_height() / 2,
            f"{int(width):,}",
            va="center",
            fontsize=10,
            color=TEXT_COLOR,
        )

    # 装飾
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(left=False, bottom=False, colors=TEXT_COLOR)
    ax.set_xticks([])
    ax.set_xlim(0, max_val * 1.18)

    ax.text(
        0.94,
        1.02,
        "(人)",
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        fontsize=10,
        color=TEXT_COLOR,
    )

    ax.set_title(title, fontsize=12, fontweight="bold", pad=8, color=TEXT_COLOR)
    plt.tight_layout()

    return fig
