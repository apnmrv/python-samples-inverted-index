"""""""""""""""""""""""""""""""""

     GLOBALS

"""""""""""""""""""""""""""""""""

import re
from typing import Pattern

WIKI_SAMPLE_LINE_PATERN: Pattern[str] = re.compile("^(\d+?)(\s+?)(.+)$")
DEFAULT_INDEX_DUMP_FILE_PATH: str = 'index_dump.txt'
DEFAULT_INIT_DATASET_FILE_PATH: str = 'init_text_sample.txt'
DEFAULT_QUERY_FILE_PATH: str = 'query.txt'
