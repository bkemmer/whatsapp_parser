import polars as pl
import bar_chart_race as bcr
from utils import get_logger
from pathlib import Path
import logging

def run_bcr(df:pl.DataFrame, video_filename_path:str) -> None:
    bcr.bar_chart_race(
            df=df,
            filename=video_filename_path,
            orientation='h',
            sort='desc',
            n_bars=10,
            fixed_order=False,
            fixed_max=True,
            steps_per_period=10,
            period_length=100,
            interpolate_period=False,
            # period_label={'x': .99, 'y': .8, 'font': {'size': 25, 'color': 'blue'}},
            period_template='%B %d, %Y',
            period_summary_func=lambda v, r: {'x': .85, 'y': .2,
                                              's': f'Total de mensages: {v.sum()}',
                                              'size': 11},
            # perpendicular_bar_func='median',
            colors='dark12',
            title='Mensagens por membro do EC07',
            bar_size=.95,
            # bar_textposition='outside',
            # bar_texttemplate='%{x}',
            bar_label_font=12,
            tick_label_font=12,
            # hovertemplate=None,
            scale='linear',
            # bar_kwargs={'opacity': .7},
            # write_html_kwargs=None,
            filter_column_colors=True)

def get_params(configs_dict: dict) -> tuple[pl.DataFrame, Path]:

    logger =  get_logger(logger_name='dataviz_info', log_level=logging.INFO, console=True)

    output_folder = Path(configs_dict['paths']['output_folder'])
    output_folder.mkdir(parents=True, exist_ok=True)

    output_pivot_path = output_folder / configs_dict['paths']['output_pivot_file']

    videos_folder = configs_dict['paths']['videos_folder']
    videos_folder_path = Path(videos_folder)
    videos_folder_path.mkdir(parents=True, exist_ok=True)

    logger.info(f'Trying to read file: {output_pivot_path}')
    df_pivot = pl.read_parquet(output_pivot_path)
    df_pandas = df_pivot.to_pandas().set_index('dt_date')

    return df_pandas, videos_folder_path

def generate_bar_chart_race(configs_dict: dict, project_name:str) -> None:
    df, video_filename_path = get_params(configs_dict)
    video_filename_path_str = str(video_filename_path / f'{project_name}_bcr.mp4')
    run_bcr(df.head(100), video_filename_path_str)
