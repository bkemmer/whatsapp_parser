import yaml
import logging
from datetime import datetime
from pathlib import Path

CONFIG_FILENAME = None
REPLACE_DICT_FILENAME = None

# Basic YAML reading
def read_yaml_file(file_path: str):
    """
    Read a YAML file and return its contents as a dictionary.
    Args:
        file_path (str): Path to the YAML file
    Returns:
        Dict[str, Any]: Parsed YAML content
    Raises:
        FileNotFoundError: If the file doesn't exist
        yaml.YAMLError: If the YAML is malformed
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
            return data if data is not None else {}
    except FileNotFoundError:
        raise FileNotFoundError(f"YAML file not found: {file_path}")
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Error parsing YAML file {file_path}: {e}")


def get_logger(logs_folder:str='logs'):
    # Create a logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.ERROR)  # Only log ERROR and above

    # Create a file handler for error logs
    logs_folder_path = Path(logs_folder)
    logs_folder_path.mkdir(parents=True, exist_ok=True)
    now_str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    error_filename = logs_folder_path / f'error_{now_str}.log'

    error_handler = logging.FileHandler(error_filename)
    error_handler.setLevel(logging.ERROR)

    # Optional: set a format for the log messages
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    error_handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(error_handler)

    return logger

