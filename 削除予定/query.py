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


def fetch_gender_trend(
    labor_status: str,
    start_year: int,
    end_year: int,
) -> pd.DataFrame:
    """
    男女別の人口推移を返す。

    Returns
    -------
    DataFrame: columns = [year, male, female]
    """
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
    WHERE
        y.year BETWEEN {start_year} AND {end_year}
        AND MOD(y.year, 5) = 0
        AND l.labor_status = '{labor_status}'
    GROUP BY y.year
    ORDER BY y.year
    """
    return duckdb.execute(sql).df()
