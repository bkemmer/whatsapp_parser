import polars as pl
from datetime import datetime
from utils import read_yaml_file, get_logger, CONFIG_FILENAME
from pathlib import Path

logger = get_logger()
configs_dict = read_yaml_file(CONFIG_FILENAME)

input_data_folder = configs_dict['paths']['input_data_folder']
input_data_folder = Path(input_data_folder)

data_raw_input_path = input_data_folder / configs_dict['paths']['data_raw_input_path']
data_path = input_data_folder / configs_dict['paths']['data_path']

def read_data(data_path: str):
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

lines = read_data(data_raw_input_path)

dt_objs, names, msgs = [], [], []
for line in lines:
    try:
        dt_obj, name_and_msg = get_date_and_msgs(line)
        name, msg = get_name_and_msg(name_and_msg)
        dt_objs.append(dt_obj)
        names.append(name)
        msgs.append(msg.strip())
    except ValueError as e:
        logger.error(f"Error processing line: {line.strip()} - {e}")

df = pl.DataFrame(
        {
            "dt": dt_objs,
            "name": names,
            "msg": msgs,
        }
    )
print(df.head())
print(f"shape: {df.shape}")
df.write_parquet(data_path)

print(f"File saved on: {data_path}")

