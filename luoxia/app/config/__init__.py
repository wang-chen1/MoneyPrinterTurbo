import os
import sys
from pathlib import Path

from loguru import logger

from luoxia.app.config.config import Configuration

CONF = Configuration()

ROOT_DIR = None


def get_project_root():
    global ROOT_DIR
    print("0" * 100)
    if ROOT_DIR:
        print("1" * 100)
        return
    ROOT_DIR = Path(__file__).resolve().parent
    for parent in ROOT_DIR.parents:
        if (
            (parent / ".git").exists()
            or (parent / "pyproject.toml").exists()
            or (parent / "setup.py").exists()
        ):
            return parent
    return ROOT_DIR


def __init_logger():
    _lvl = CONF.default.log_level
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

    def format_record(record):
        # 获取日志记录中的文件全路径
        file_path = record["file"].path
        # 将绝对路径转换为相对于项目根目录的路径
        relative_path = os.path.relpath(file_path, root_dir)
        # 更新记录中的文件路径
        record["file"].path = f"./{relative_path}"
        # 返回修改后的格式字符串
        # 您可以根据需要调整这里的格式
        _format = (
            "<green>{time:%Y-%m-%d %H:%M:%S}</> | "
            + "<level>{level}</> | "
            + '"{file.path}:{line}":<blue> {function}</> '
            + "- <level>{message}</>"
            + "\n"
        )
        return _format

    logger.remove()

    logger.add(
        sys.stdout,
        level=_lvl,
        format=format_record,
        colorize=True,
    )


__init_logger()
get_project_root()
