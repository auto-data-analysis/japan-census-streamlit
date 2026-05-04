"""matplotlibによる描画ロジック。"""

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.ticker import FuncFormatter, MaxNLocator

TEXT_COLOR = "#595959"
COLOR_MALE = "#9DB7F9"    # ブルー系
COLOR_FEMALE = "#FFA66D"  # オレンジ系
LABEL_MALE = "男性"
LABEL_FEMALE = "女性"


def _set_japanese_font() -> None:
    """利用可能な日本語フォントを設定する。"""
    candidates = ["Meiryo", "Hiragino Sans", "IPAexGothic", "Noto Sans CJK JP"]
    available = {f.name for f in fm.fontManager.ttflist}
    for font in candidates:
        if font in available:
            plt.rcParams["font.family"] = font
            return


def plot_gender_trend(
    df: pd.DataFrame,
    title: str = "就業者数の推移（男女別）",
    figsize: tuple[int, int] = (10, 4),
    dpi: int = 150,
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

    ax.plot(df["year_dt"], df["male"],   label=LABEL_MALE,   color=COLOR_MALE,   linewidth=3)
    ax.plot(df["year_dt"], df["female"], label=LABEL_FEMALE, color=COLOR_FEMALE, linewidth=3)

    # 右端ラベル
    x_last = df["year_dt"].iloc[-1]
    ax.text(x_last, df["male"].iloc[-1],   f" {LABEL_MALE}",   color=COLOR_MALE,   va="center", fontsize=12)
    ax.text(x_last, df["female"].iloc[-1], f" {LABEL_FEMALE}", color=COLOR_FEMALE, va="center", fontsize=12)

    # 装飾
    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.yaxis.set_major_locator(MaxNLocator(nbins=4))
    ax.tick_params(axis="both", length=0, colors=TEXT_COLOR)
    ax.yaxis.grid(True, color="lightgray", linewidth=0.5)
    ax.xaxis.grid(False)

    # y軸：万人単位
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{int(x / 10000):,}"))
    ax.text(-0.05, 1.02, "(万人)", transform=ax.transAxes,
            ha="left", va="bottom", fontsize=10, color=TEXT_COLOR)

    ax.set_title(title, fontsize=12, fontweight="bold", pad=8, color=TEXT_COLOR)
    plt.tight_layout()

    return fig
