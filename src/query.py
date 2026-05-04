"""DuckDBを使った集計ロジック。"""

from pathlib import Path

import duckdb
import pandas as pd

DATA_DIR = Path(__file__).parent.parent / "data" / "raw"

FACT_PATH = str(DATA_DIR / "fact_Population_Census_of_Japan.csv")
MASTER_YEAR_PATH = str(DATA_DIR / "master_year.csv")
MASTER_LABOR_PATH = str(DATA_DIR / "master_labor_status.csv")
MASTER_GENDER_PATH = str(DATA_DIR / "master_gender.csv")
MASTER_PREF_PATH = str(DATA_DIR / "master_pref.csv")
MASTER_REGION_PATH = str(DATA_DIR / "master_region.csv")


def get_region_list() -> list[str]:
    """地方名の一覧を返す（region_code順）。"""
    sql = "SELECT region FROM read_csv_auto(?) ORDER BY region_code"
    rows = duckdb.execute(sql, [MASTER_REGION_PATH]).fetchall()
    return [r[0] for r in rows]


def get_pref_by_region(region: str | None = None) -> list[str]:
    """
    地方名に対応する都道府県名の一覧を返す。
    regionがNoneまたは空の場合は全47都道府県を返す。
    """
    if region:
        sql = f"""
        SELECT p.pref
        FROM read_csv_auto('{MASTER_PREF_PATH}') AS p
        JOIN read_csv_auto('{MASTER_REGION_PATH}') AS r
            ON p.region_code = r.region_code
        WHERE r.region = '{region}'
        ORDER BY p.area_code
        """
    else:
        sql = f"SELECT pref FROM read_csv_auto('{MASTER_PREF_PATH}') ORDER BY area_code"
    rows = duckdb.execute(sql).fetchall()
    return [r[0] for r in rows]


def get_labor_status_list() -> list[str]:
    """労働力状態の選択肢を返す。"""
    sql = "SELECT labor_status FROM read_csv_auto(?) ORDER BY cat01_code"
    rows = duckdb.execute(sql, [MASTER_LABOR_PATH]).fetchall()
    return [r[0] for r in rows]


def get_year_range() -> tuple[int, int]:
    """利用可能な年の最小・最大を返す。"""
    sql = "SELECT MIN(year), MAX(year) FROM read_csv_auto(?)"
    row = duckdb.execute(sql, [MASTER_YEAR_PATH]).fetchone()
    return row[0], row[1]


def get_year_list() -> list[int]:
    """利用可能な年の一覧を返す（降順）。"""
    sql = "SELECT year FROM read_csv_auto(?) WHERE MOD(year, 5) = 0 ORDER BY year DESC"
    rows = duckdb.execute(sql, [MASTER_YEAR_PATH]).fetchall()
    return [r[0] for r in rows]


def fetch_pref_ranking(
    labor_status: str,
    gender: str,
    year: int,
    top_n: int,
) -> pd.DataFrame:
    """
    都道府県別の人口ランキングを返す。

    Parameters
    ----------
    labor_status : str
        労働力状態（例：就業者）
    gender : str
        性別（男性 or 女性）
    year : int
        対象年
    top_n : int
        上位何件を返すか

    Returns
    -------
    DataFrame: columns = [pref, value]  降順ソート済み
    """
    # UIは「男性・女性」、データは「男・女」
    gender_code = "男" if gender == "男性" else "女"

    sql = f"""
    SELECT
        p.pref,
        SUM(f.value) AS value
    FROM
        read_csv_auto('{FACT_PATH}') AS f
        JOIN read_csv_auto('{MASTER_LABOR_PATH}') AS l
            ON RTRIM(CAST(f.cat01_code AS VARCHAR)) = RTRIM(CAST(l.cat01_code AS VARCHAR))
        JOIN read_csv_auto('{MASTER_GENDER_PATH}') AS g
            ON RTRIM(CAST(f.cat02_code AS VARCHAR)) = RTRIM(CAST(g.cat02_code AS VARCHAR))
        JOIN read_csv_auto('{MASTER_YEAR_PATH}') AS y
            ON RTRIM(CAST(f.time_code AS VARCHAR)) = RTRIM(CAST(y.time_code AS VARCHAR))
        JOIN read_csv_auto('{MASTER_PREF_PATH}') AS p
            ON RTRIM(CAST(f.area_code AS VARCHAR)) = RTRIM(CAST(p.area_code AS VARCHAR))
    WHERE
        y.year = {year}
        AND l.labor_status = '{labor_status}'
        AND g.gender = '{gender_code}'
    GROUP BY p.pref
    ORDER BY value DESC
    LIMIT {top_n}
    """
    return duckdb.execute(sql).df()


def fetch_gender_trend(
    labor_status: str,
    start_year: int,
    end_year: int,
    prefs: list[str] | None = None,
) -> pd.DataFrame:
    """
    男女別の人口推移を返す。

    Parameters
    ----------
    prefs : list[str] | None
        都道府県名のリスト。Noneまたは空リストの場合は全国集計。

    Returns
    -------
    DataFrame: columns = [year, male, female]
    """
    # 都道府県フィルタの組み立て
    if prefs:
        pref_list = ", ".join(f"'{p}'" for p in prefs)
        pref_filter = f"AND p.pref IN ({pref_list})"
    else:
        pref_filter = ""

    sql = f"""
    SELECT
        y.year,
        SUM(CASE WHEN g.gender = '男' THEN COALESCE(f.value, 0) ELSE 0 END) AS male,
        SUM(CASE WHEN g.gender = '女' THEN COALESCE(f.value, 0) ELSE 0 END) AS female
    FROM
        read_csv_auto('{FACT_PATH}') AS f
        JOIN read_csv_auto('{MASTER_LABOR_PATH}') AS l
            ON RTRIM(CAST(f.cat01_code AS VARCHAR)) = RTRIM(CAST(l.cat01_code AS VARCHAR))
        JOIN read_csv_auto('{MASTER_GENDER_PATH}') AS g
            ON RTRIM(CAST(f.cat02_code AS VARCHAR)) = RTRIM(CAST(g.cat02_code AS VARCHAR))
        JOIN read_csv_auto('{MASTER_YEAR_PATH}') AS y
            ON RTRIM(CAST(f.time_code AS VARCHAR)) = RTRIM(CAST(y.time_code AS VARCHAR))
        JOIN read_csv_auto('{MASTER_PREF_PATH}') AS p
            ON RTRIM(CAST(f.area_code AS VARCHAR)) = RTRIM(CAST(p.area_code AS VARCHAR))
    WHERE
        y.year BETWEEN {start_year} AND {end_year}
        AND MOD(y.year, 5) = 0
        AND l.labor_status = '{labor_status}'
        {pref_filter}
    GROUP BY y.year
    ORDER BY y.year
    """
    return duckdb.execute(sql).df()
