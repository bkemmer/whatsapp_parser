import polars as pl
from datetime import datetime
from pathlib import Path
import logging
from utils import get_logger
from dateutil.relativedelta import relativedelta


def group_df(df: pl.DataFrame) -> pl.DataFrame:
    return (
        df.group_by("name")
        .len()
        .sort("len", descending=True)
        .rename({"len": "qtde_msgs"})
        .with_columns(
            (pl.col("qtde_msgs") / pl.col("qtde_msgs").sum() * 100)
            .round(1)
            .alias("perc")
        )
    )


def get_pivoted_df(df: pl.DataFrame):
    df_grp_by_date = (
        df.group_by(["dt_date", "name"])
        .len()
        .sort("dt_date")
        .with_columns(pl.col("len").cum_sum().over("name").alias("msgs_acc"))
    )
    df_pivot = (
        df_grp_by_date.pivot(
            values="msgs_acc",
            index="dt_date",
            on="name",
        )
        .fill_null(strategy="backward")
        .fill_null(strategy="forward")
    )
    return df_pivot


def relativedelta_to_string(rd: relativedelta) -> str:
    text = "period"
    if rd.years > 0:
        text += f"_{rd.years}y"
    if rd.months > 0:
        text += f"_{rd.months}m"
    if rd.days > 0:
        text += f"_{rd.days}d"
    return text


def anonymize_df(df: pl.DataFrame) -> pl.DataFrame:
    unique_names_list = list(df["name"].unique())
    anon_dict = {
        k: f"user{v}"
        for k, v in zip(unique_names_list, range(1, len(unique_names_list) + 1))
    }
    df = df.with_columns(pl.col("name").replace(anon_dict).alias("name"))
    print(df["name"].unique())
    return df


def transform(
    df: pl.DataFrame,
    project_name: str,
    replace_dict: dict | None,
    configs_dict: dict,
    start_date: datetime | None,
    period: relativedelta | None,
    anon: bool,
    verbose: bool,
) -> None:
    logger = get_logger(logger_name="etl_info", log_level=logging.INFO, console=True)

    filename = project_name

    outputs_folder = configs_dict["paths"]["outputs_folder"]
    outputs_folder_path = Path(outputs_folder) / project_name
    outputs_folder_path.mkdir(parents=True, exist_ok=True)

    truncate_names_chars = int(configs_dict["configs"]["truncate_names_chars"])

    skip_words = configs_dict["skip_words"]
    pattern = "|".join(skip_words)

    exprs = [pl.col("dt").dt.date().alias("dt_date")]
    if replace_dict:
        exprs = exprs + [pl.col("name").replace(replace_dict).alias("name")]

    df = (
        df.with_columns(exprs)
        .filter(~pl.col("name").str.contains(pattern))
        .with_columns(pl.col("name").str.slice(0, truncate_names_chars).alias("name"))
    )
    if verbose:
        logger.info(f"Unique names: {df['name'].unique()}")

    if anon:
        df = anonymize_df(df)

    if period:
        cutoff_date = datetime.now() - period
        df = df.filter(pl.col("dt") > cutoff_date)
        filename = f"{filename}_{relativedelta_to_string(period)}"

    if start_date:
        df = df.filter(pl.col("dt") > start_date)
        filename = f"{filename}_{start_date.strftime('%Y%m%d')}"

    if verbose:
        logger.info(df.head())

    df.write_parquet(outputs_folder_path / f"{filename}.parquet")
    df.write_excel(outputs_folder_path / f"{filename}.xlsx")

    return df
