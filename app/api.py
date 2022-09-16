"""""""""""""""""""""""""""""""""

            API

"""""""""""""""""""""""""""""""""
from typing import Dict, Iterator, List, Set, Any

from app.exceptions import FileAccessException
from app.globals import *
from app.helpers import read_file_to_lines, parse_lines, tuple_to_key_value
from app.inverted_index import InvertedIndex


def load_document(file_path: str) -> Dict[int, str]:
    try:
        lines: List[str] = read_file_to_lines(file_path)
        lines_enumerated = map(lambda xs: str(xs[0]) + " " + xs[1], enumerate(lines, start=1))
        lines_parsed: Iterator[tuple] = parse_lines(list(lines_enumerated), WIKI_SAMPLE_LINE_PATERN)
    except FileAccessException as err:
        raise err
    return dict(tuple_to_key_value(lines_parsed, 0, 2))


def load_queries(file_path: str) -> Iterator[Iterator[str]]:
    lines: List[str] = read_file_to_lines(file_path)
    queries: Iterator[str] = map(lambda l: l.split(), lines)

    return queries


def get_inverted_index(articles: Dict[int, str]) -> Dict[str, Set[int]]:
    inverted_index = {}
    for k, v in articles.items():
        ws = set(w for w in v.split())
        for w in ws:
            curr_value = inverted_index.get(w)
            ids = set(curr_value) if curr_value else set()
            ids.add(k)
            inverted_index.update({w: ids})

    return inverted_index


def build_inverted_index(articles: Dict[int, str]) -> InvertedIndex:
    return InvertedIndex(get_inverted_index(articles))
