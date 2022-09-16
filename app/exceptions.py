"""""""""""""""""""""""""""""""""

     EXCEPTIONS

"""""""""""""""""""""""""""""""""


class FileAccessException(Exception):
    def __init(self, *args):
        if args:
            self.__message = args[0]
        else:
            self.__message = None

    def __str__(self):
        if self.__message:
            return "FileAccessError, {0}".format(self.__message)
        else:
            return "FileAccessError has been raised"
