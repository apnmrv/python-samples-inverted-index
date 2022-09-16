"""""""""""""""""""""""""""""""""

            CLI

"""""""""""""""""""""""""""""""""
import argparse

from app.api import *
from app.inverted_index import *
from app.globals import *


def cmd_build(_args):
    init_dataset_file_path = _args.dataset
    dump_file_path = _args.index
    try:
        raw_index = load_document(init_dataset_file_path)
        index = build_inverted_index(raw_index)
        index.dump(dump_file_path)
    except FileAccessException as err:
        print(err)


def cmd_query(_args):
    dump_file_path = _args.index
    query_file_path = _args.query_file
    try:
        index = InvertedIndex.load(dump_file_path)
        queries: Iterator[Iterator[str]] = load_queries(query_file_path)
        query_results = map(lambda q: index.query(set(q)), list(queries))
        for r in query_results:
            output_string = ",".join([str(i) for i in sorted(r)])
            print(output_string)

    except FileAccessException as err:
        print(err)


parser = argparse.ArgumentParser(prog='inverted_index')


subparsers = parser.add_subparsers(title='subcommands',
                                   description='valid subcommands',
                                   help='subcommands')
parser_build = subparsers.add_parser('build',
                                     help='takes a Wikipedia dump as input, '
                                          'constructs an inverted index and saves it to disk')

parser_build.add_argument('--dataset',
                          type=str,
                          default=DEFAULT_INIT_DATASET_FILE_PATH,
                          help='path to dataset to build Inverted Index')

parser_build.add_argument('--index',
                          type=str,
                          default=DEFAULT_INDEX_DUMP_FILE_PATH,
                          help='path for Inverted Index dump')

parser_build.set_defaults(func=cmd_build)

parser_query = subparsers.add_parser('query',
                                     help='find common articles for words in each query from the query file')
parser_query.add_argument('--index',
                          type=str,
                          default=DEFAULT_INDEX_DUMP_FILE_PATH,
                          help='path to load Inverted Index')
parser_query.add_argument('--query-file',
                          type=str,
                          default=DEFAULT_QUERY_FILE_PATH,
                          help='path to query_file with collection of queries to run against Inverted Index')

parser_query.set_defaults(func=cmd_query)

args = parser.parse_args()

args.func(args)
