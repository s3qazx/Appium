import json
import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

from config import BASE_DIR


def read_json(file_name, fields=None):
    """读取测试数据；指定 fields 时按字段名顺序生成参数元组。"""
    with (Path(BASE_DIR) / "data" / file_name).open(encoding="utf-8") as file:
        rows = json.load(file)
    if fields is None:
        return rows
    return [tuple(row[field] for field in fields) for row in rows]


class GetLog:
    __log = None

    @classmethod
    def get_log(cls):
        if cls.__log is None:
            log_dir = Path(BASE_DIR) / "log"
            log_dir.mkdir(parents=True, exist_ok=True)
            handler = TimedRotatingFileHandler(
                log_dir / "automation.log",
                when="midnight",
                backupCount=3,
                encoding="utf-8",
            )
            handler.setFormatter(logging.Formatter(
                "%(asctime)s %(levelname)s [%(filename)s(%(funcName)s:%(lineno)d)] - %(message)s"
            ))
            logger = logging.getLogger("appautomation")
            logger.setLevel(logging.INFO)
            logger.addHandler(handler)
            cls.__log = logger
        return cls.__log
