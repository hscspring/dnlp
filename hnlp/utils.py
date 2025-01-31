from collections import namedtuple
from collections.abc import Sequence
from functools import wraps
from itertools import chain
from addict import Dict as ADict
from pathlib import Path
from typing import Any
import re
import pnlp


name_split_reg = re.compile(r"[-_]")


def build_class_name(name: str):
    return "".join(map(str.capitalize, name_split_reg.split(name)))


def check_dir(path: str):
    p = Path(path)
    if not path or not p.is_dir():
        raise ValueError(f"hnlp: {path} should be a path.")


def check_file(path: str):
    p = Path(path)
    if not path or not p.is_file():
        raise ValueError(f"hnlp: {path} should be a file.")


def build_config_from_json(json_path: str):
    js = pnlp.read_json(json_path)
    # like argparse.Namespace
    Config = namedtuple("Config", js.keys())
    return Config(**js)


def build_pretrained_config_from_json(pretrained_config, json_path: str):
    js = pnlp.read_json(json_path)
    return pretrained_config(**js)


def get_attr(typ: type, attr: str, default: Any):
    if not hasattr(typ, attr):
        return default
    return getattr(typ, attr)


def check_parameter(func):
    @wraps(func)
    def wrapper(config):
        config = ADict(config)
        return func(config)

    return wrapper


def unfold(lst: Sequence) -> list:
    while lst and isinstance(lst[0], Sequence):
        lst = list(chain(*lst))
    return lst
