import bisect
import sys

from unit_test import *
from main import AlgorithmWithIndexStructure

class IndexSorted(AlgorithmWithIndexStructure):

    def __init__(self):
        self.__text = ""
        self.__pattern = ""
        self.__pattern_len = 0
        self.__index = []

    def initWithText(self):
        self.__index = []
        for i in range(len(self.__text) - self.__pattern_len + 1):
            self.__index.append((self.__text[i:i + self.__pattern_len], i))  # add <substr, offset> pair
        self.__index.sort()  # sort pairs

    def query(self, text, pattern):

        self.__text = text
        self.__pattern = pattern
        self.__pattern_len = len(self.__pattern)

        self.initWithText()

        st = bisect.bisect_left(self.__index, (self.__pattern[:self.__pattern_len], -1))  # binary search
        en = bisect.bisect_right(self.__index, (self.__pattern[:self.__pattern_len], sys.maxsize))  # binary search

        hits = self.__index[st:en]  # this range of elements corresponds to the hits

        return [h[1] for h in hits]  # return just the offsets


# Run tests
test_results = run_algorithm_tests(IndexSorted())
print_test_results(test_results)
