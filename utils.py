import yaml
import logging
from datetime import datetime
from pathlib import Path


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
        with open(file_path, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)
            return data if data is not None else {}
    except FileNotFoundError:
        raise FileNotFoundError(f"YAML file not found: {file_path}")
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Error parsing YAML file {file_path}: {e}")


def get_logger(
    logger_name: str,
    logs_folder: str = "logs",
    log_level: int = logging.ERROR,
    file: bool = True,
    console: bool = False,
) -> logging.Logger:
    # Create a logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)

    now_str = datetime.now().strftime("%Y%m%d")
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    if file:
        # Create a file handler for error logs
        logs_folder_path = Path(logs_folder) / now_str
        logs_folder_path.mkdir(parents=True, exist_ok=True)
        if log_level == logging.ERROR:
            fname = logs_folder_path / f"{logger_name}_error.log"
        else:
            fname = logs_folder_path / f"{logger_name}.log"
        file_handler = logging.FileHandler(fname)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    if console:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger
