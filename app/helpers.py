"""""""""""""""""""""""""""""""""

     HELPERS

"""""""""""""""""""""""""""""""""
import copy
from typing import List, Iterator, Set, Dict

from app.exceptions import FileAccessException


def read_file_to_lines(file_path: str) -> List[str]:
    try:
        f = open(file_path, mode="r", encoding="utf-8")
    except OSError as err:
        raise FileAccessException(f"Can't read from file {file_path}. OSError has been raised: {err}")
    return f.readlines()


def string_to_tuple(s: str, pattern) -> tuple:
    return pattern.match(s).groups()


def tuple_to_key_value(lines: Iterator[tuple], k: int, v: int) -> Iterator[tuple]:
    return map(lambda str2str: (int(str2str[k]), str.strip(str2str[v])), lines)


def parse_lines(lines: List[str], pattern) -> Iterator[tuple]:
    return map(lambda line: string_to_tuple(line, pattern), lines)


def string_to_words_set(s: str) -> Set[str]:
    return set(w for w in s.split(" "))


def update_index(ws: Set[str], k: int, index: Dict[str, Set[int]]) -> Dict[str, Set[int]]:
    idx = copy.deepcopy(index)
    for w in ws:
        ids = set(idx.get(w)) if idx.get(w) else set()
        ids.add(k)
        idx.update({w: ids})

    return idx
