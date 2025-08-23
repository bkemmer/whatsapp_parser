import polars as pl
from datetime import datetime, timedelta
from pathlib import Path

from utils import read_yaml_file, get_logger, CONFIG_FILENAME

logger = get_logger()
configs_dict = read_yaml_file(CONFIG_FILENAME)

map_contacts_filename = configs_dict['paths']['map_contacts_filename']
replace_dict = read_yaml_file(map_contacts_filename)['replace_dict']
print(replace_dict)

input_data_folder = configs_dict['paths']['input_data_folder']
input_data_folder = Path(input_data_folder)
data_input_path = input_data_folder / configs_dict['paths']['data_path']

output_folder = configs_dict['paths']['output_folder']
output_folder = Path(output_folder)
Path(output_folder).mkdir(parents=True, exist_ok=True)

output_file_all_time = output_folder / configs_dict['paths']['output_file_all_time']
output_file_six_months = output_folder / configs_dict['paths']['output_file_six_months']
output_file_last_week = output_folder / configs_dict['paths']['output_file_last_week']
output_pivot_file = output_folder / configs_dict['paths']['output_pivot_file']
output_daily_acc_path = output_folder / configs_dict['paths']['output_daily_acc_path']

skip_words = configs_dict['skip_words']

df = pl.read_parquet(data_input_path)

pattern = '|'.join(skip_words)
df = (
        df
        .with_columns([
            pl.col('dt').dt.year().alias('dt_year'),
            pl.col('dt').dt.date().alias('dt_date'),
            pl.col('name').replace(replace_dict).alias('name'),
        ])
        .with_columns(
            pl.col('name').str.slice(0,17).alias('name')
        )
        .filter(
            ~pl.col("name").str.contains(pattern)
        )
)
print(f"Unique names: {df['name'].unique()}")

df_grp_by_date = (
        df
        .group_by(['dt_date', 'name'])
        .len()
        .sort('dt_date')
        .with_columns(
            pl.col('len').cum_sum().over('name').alias('msgs_acc')
            )
        )
df_grp_by_date.write_excel(output_daily_acc_path)
df_pivot = (
        df_grp_by_date
        .pivot(
            values='msgs_acc',
            index='dt_date',
            on='name',
            )
        .fill_null(strategy="backward")
        .fill_null(strategy="forward")
        )

print(df_pivot)
df_pivot.write_parquet(output_pivot_file)

cutoff_date = datetime.now() - timedelta(days=182)
df_six_months = (
        df
        .filter(pl.col('dt') > cutoff_date)
        .drop('dt_year')
)

df_last_week = (
    df
    .filter(pl.col('dt') > datetime.now() - timedelta(days=7))
)

def group_df(df: pl.DataFrame) -> pl.DataFrame:
    return (
        df
        .group_by('name')
        .len()
        .sort('len', descending=True)
        .rename({"len": "qtde_msgs"})
        .with_columns(
            (pl.col('qtde_msgs') / pl.col('qtde_msgs').sum() * 100).round(1).alias('percentual')
        )
    )

df_grp_six_months = group_df(df_six_months)

df_grp_six_months.write_excel(output_file_six_months)

print(df_grp_six_months)


df_grp_last_week = group_df(df_last_week)

df_grp_last_week.write_excel(output_file_last_week)

print(df_grp_last_week)

df_grp_all_time = group_df(df)
df_grp_all_time.write_excel(output_file_all_time)
print("all time")
print(df_grp_all_time)
