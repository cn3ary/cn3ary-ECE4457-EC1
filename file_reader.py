# You need to implement the "get" and "head" functions.
import os.path
from os import path
class FileReader:
    def __init__(self):
        pass

    def get(self, filepath, cookies):
        """
        Returns a binary string of the file contents, or None.
        """
        f = open(filepath, 'rb')
        data = f.read()
        f.close()
        return data

    def head(self, filepath, cookies):
        """
        Returns the size to be returned, or None.
        """
        f = open(filepath, 'rb')
        binary = f.read()
        if binary is None:
            return None
        return len(binary)
