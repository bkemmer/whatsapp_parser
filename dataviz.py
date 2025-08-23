import polars as pl
import bar_chart_race as bcr
from utils import read_yaml_file, CONFIG_FILENAME
from pathlib import Path

configs_dict = read_yaml_file(CONFIG_FILENAME)

output_folder = configs_dict['paths']['output_folder']
output_folder = Path(output_folder)
output_pivot_path = output_folder / configs_dict['paths']['output_pivot_file']

videos_folder = configs_dict['paths']['videos_folder']
videos_folder_path = Path(videos_folder)
videos_folder_path.mkdir(parents=True, exist_ok=True)

video_filename = configs_dict['paths']['video_filename']
video_filename_path = videos_folder_path / video_filename

print(f'Trying to read file: {output_pivot_path}')
df_pivot = pl.read_parquet(output_pivot_path)
df_pandas = df_pivot.to_pandas().set_index('dt_date')

bcr.bar_chart_race(
        df=df_pandas,
        filename=str(video_filename_path),
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
