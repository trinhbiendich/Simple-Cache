import hashlib
import json
import os
from os import path


class Cache:
    def __init__(self, config):
        self.name = config["name"]
        self.path = config["path"]
        self.ext = config["ext"]

    def _load_cache(self):
        if self.get_cache_dir() is not None and path.exists(self.get_cache_dir()):
            f = open(self.get_cache_dir(), "r")
            my_string = f.read()
            f.close()
            return json.loads(my_string)
        return None

    def get_cache_dir(self):
        if self._check_cache_dir():
            file_name = self.name.lower()
            return path.join(self.path, hashlib.md5(file_name.encode()).hexdigest()) + self.ext
        return None

    def _check_cache_dir(self):
        if not path.isdir(self.path):
            if not os.mkdir(self.path, True):
                raise Exception('Unable to create cache directory ' + self.path)
        else:
            os.chmod(self.path, 0o777)
            if not os.access(self.path, os.R_OK) or not os.access(self.path, os.W_OK):
                raise Exception(self.path + ' must be readable and writeable')
        return True

    def store(self, key, data):
        saved_data = self._load_cache()
        if saved_data is None:
            saved_data = {}
        saved_data[key] = data
        f = open(self.get_cache_dir(), "w")
        f.write(json.dumps(saved_data))
        f.close()
        return self

    def retrieve(self, key):
        saved_data = self._load_cache()
        if saved_data is None or key not in saved_data:
            return None
        return saved_data[key]

    def erase(self, key):
        saved_data = self._load_cache()
        if saved_data is None or key not in saved_data:
            raise Exception("can't delete " + key)
        del saved_data[key]
        f = open(self.get_cache_dir(), "w")
        f.write(json.dumps(saved_data))
        f.close()
        return True
