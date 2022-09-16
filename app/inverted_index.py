import copy
import json
from collections.abc import Iterable
from typing import Dict, Set

from app.exceptions import FileAccessException

"""""""""""""""""""""""""""""""""

     INVERTED INDEX CLASS

"""""""""""""""""""""""""""""""""


class InvertedIndex:
    def __init__(self, word_to_docs_mapping: Dict[str, Set[int]]):
        self.__index = word_to_docs_mapping
        self.__keys = set(word_to_docs_mapping.keys())

    def index(self):
        return copy.deepcopy(self.__index)

    def query(self, words: Iterable) -> Set[int]:
        def get_result(ws: Set[str], output: Set[int]):
            if len(ws) == 0 or len(output) == 0:
                return output
            else:
                curr_w = ws.pop()
                curr_w_ids = self.__index.get(curr_w)
                updated_output = output.intersection(curr_w_ids)
                return get_result(ws, updated_output)

        words_set = set(words)

        if self.__keys.intersection(words_set) != words_set:
            return set()
        else:
            init_w = words_set.pop()
            return get_result(words_set, self.__index.get(init_w))

    def __to_json(self):
        index = dict(map(lambda item: (item[0], list(item[1])), self.__index.items()))
        return json.dumps(index)

    def dump(self, filepath):
        try:
            with open(filepath, mode="w", encoding="utf-8") as out:
                out.write(self.__to_json())
        except OSError as err:
            raise FileAccessException(f"Can't write to file {filepath}. OSError has been raised: {err}")

    @classmethod
    def load(cls, filepath):
        try:
            with open(filepath, mode="r", encoding="utf-8") as json_file:
                index_json = json.loads(json_file.read())
            index = dict(map(lambda item: (item[0], set(item[1])), index_json.items()))
        except OSError as err:
            raise FileAccessException(f"Can't read from file {filepath}. OSError has been raised: {err}")

        return cls(index)