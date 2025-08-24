import polars as pl
import bar_chart_race as bcr
from utils import get_logger
from etl import get_pivoted_df
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

def get_videos_folder_path(project_name:str, configs_dict: dict) -> Path:

    outputs_folder = Path(configs_dict['paths']['outputs_folder'])
    outputs_folder.mkdir(parents=True, exist_ok=True)

    videos_folder = configs_dict['paths']['videos_folder']
    videos_folder_path = Path(videos_folder) / project_name
    videos_folder_path.mkdir(parents=True, exist_ok=True)

    return videos_folder_path

def generate_bar_chart_race(df:pl.DataFrame, configs_dict: dict, project_name:str, verbose:bool) -> None:

    logger =  get_logger(logger_name='dataviz_info', log_level=logging.INFO, console=True)
    df_pivot = get_pivoted_df(df)
    df_pandas = df_pivot.to_pandas().set_index('dt_date')
    video_filename_path = get_videos_folder_path(project_name, configs_dict)
    video_filename_path_str = str(video_filename_path / f'{project_name}_bcr.mp4')
    # FIXME: remove limit
    run_bcr(df_pandas.head(100), video_filename_path_str)
