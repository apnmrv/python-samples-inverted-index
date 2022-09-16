# Inverted Index 
## CLI application

Builds an inverted index from an input text file and resolves search queries against it.

- to build an inverted index ( word -> line numbers it is encountered ) from an input text file
```shell
$ python inverted_index.py build --dataset [PATH_TO_INTPUT_TEXT_FILE] --index [PATH_FOR_INDEX_OUTPUT]   
```

- to resolve a query ( list of words -> line numbers they are all encountered )
```shell
$ python inverted_index.py query --index [PATH_TO_PREBUILD_INDEX_FILE] --query-file [PATH_TO_QUERY_FILE]
```
