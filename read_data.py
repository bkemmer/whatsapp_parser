import polars as pl
from datetime import datetime
from utils import read_yaml_file, get_logger
from pathlib import Path
import logging

error_logger = get_logger(logger_name='read_data_error', log_level=logging.ERROR)
logger =  get_logger(logger_name='read_data_info', log_level=logging.INFO, console=True)

def read_data_from_file(data_path: str):
    with open(data_path, 'r', encoding='utf-8', errors='backslashreplace') as file:
        file.readline()  # Skip the first line
        lines = file.readlines()
        return lines

def get_date_and_msgs(line: str):
        text1 = line.split(' - ')
        dt_str = text1[0]
        name_and_msg = ' '.join(text1[1:])
        dt_obj = datetime.strptime(dt_str, "%m/%d/%y, %H:%M")
        return dt_obj, name_and_msg

def get_name_and_msg(name_and_msg: str):
        text = name_and_msg.split(': ')
        name = text[0]
        msg = ''.join(text[1:])
        return name, msg


def read_data(project_name:str, data_path:str, configs_dict:dict) -> pl.DataFrame:

    outputs_folder = Path(configs_dict['paths']['input_data_folder'])
    project_outputs_folder = outputs_folder / project_name
    project_outputs_folder.mkdir(parents=True, exist_ok=True)

    full_parsed_file = project_outputs_folder / configs_dict['paths']['full_parsed_file']

    lines = read_data_from_file(data_path)

    dt_objs, names, msgs = [], [], []
    for line in lines:
        try:
            dt_obj, name_and_msg = get_date_and_msgs(line)
            name, msg = get_name_and_msg(name_and_msg)
            dt_objs.append(dt_obj)
            names.append(name)
            msgs.append(msg.strip())
        except ValueError as e:
            error_logger.error(f"Error processing line: {line.strip()} - {e}")

    df = pl.DataFrame(
            {
                "dt": dt_objs,
                "name": names,
                "msg": msgs,
            }
        )

    logger.info(f"Dataframe shape: {df.shape}")
    logger.info(df.head())
    df.write_parquet(full_parsed_file)

    print(f"File saved on: {full_parsed_file}")

    return df
