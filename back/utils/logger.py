import traceback

from utils.singleton import SingletonMeta
from os import path
from datetime import datetime


class Logger(metaclass=SingletonMeta):
    def __init__(self):
        self._log_path = ''
        self._log_name = 'log.txt'
        self._path = path.join(self._log_path, self._log_name)

        self._error_levels = ['[Err]', '[War]', '[Inf]']

        self._verbose = False

        with open(self._path, 'w') as file:
            file.write('Start log ' + str(datetime.now()) + '\n')

    def log(self, error_level=0, origin=None, message=''):
        log = self._error_levels[error_level] + '  '
        if origin:
            log += str(type(origin)).split(" '")[1].rstrip("'>")
        else:
            log += 8 * ' '
        log += '  ' + message + '\n'

        if self._verbose:
            traceback.print_stack(limit=5)
            print(log)

        with open(self._path, 'a') as file:
            file.write(log)
