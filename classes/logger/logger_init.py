import logging
import logging.config
from configparser import ConfigParser
from pathlib import Path


def get_config_file_path() -> Path:
    return Path(__file__).with_name("logger-conf.ini")


def set_app_logger(config_path: Path) -> logging.Logger:
    config = ConfigParser()
    config.read(config_path)
    logging.config.fileConfig(fname=config_path)
    return logging.getLogger("appLogger")


logger = set_app_logger(get_config_file_path())
