import os
import time


class Toolbox:
    """Contains useful tools"""

    def get_data_directory(self) -> str:
        """Returns the absolute path of the data directory
        :return: The location of the data
        :rtype: str
        """
        parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_directory = os.path.join(parent, 'data' + os.sep)
        return data_directory


def timeit(method):
    """Time the duration it takes to execute a method, use it as a
    decorator."""

    def timed(*args, **kw) -> str:
        """The timer code
        :param args: Arguments
        :param kw: Keywords
        :return: The time it took to execute the method
        :rtype: str
        """
        start_time = time.time()
        result = method(*args, **kw)
        end_time = time.time()

        print(f'{method.__name__}, {end_time - start_time} seconds')
        return result

    return timed
