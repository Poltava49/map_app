import json
from typing import Any
from src.db import DataBase


def check_cached(url: str, params: dict[str, Any]) -> bool: 
    db = DataBase()
    if db.get_cahce() == None:
        return False
    else: 
        return True


def read_from_cache(url, params): 
    # json.loads(str) -> dict
    # json.dump(dict) -> str


def write_to_cache(
    request_url=url,
    request_params=params,
    resposne_status_code=response.status_code,
    is_file=True,
    content=response.content,
): ...
