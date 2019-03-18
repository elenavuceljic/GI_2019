import os
from pathlib import Path

unit_tests_dir = Path("Tests/Unit/")


class UnitTestResult(object):

    PASSED = 0
    FAILED = -1

    __result_str = dict()
    __result_str[PASSED] = "Passed"
    __result_str[FAILED] = "Failed"

    def __init__(self, result, name):
        self.__result = result
        self.__name = name

    def get_name(self):
        return self.__name

    def get_result(self):
        return self.__result

    def get_description(self):
        return self.__name + ": " + self.__result_str[self.__result]


def run_algorithm_tests(algorithm):

    tests_dir = unit_tests_dir
    test_files = []
    results = []

    for file in os.listdir(tests_dir):
        test_files.append(tests_dir / file)

    for test_file_name in test_files:

        test_file = open(test_file_name, 'r')
        lines = test_file.readlines()

        name = lines[0].rstrip('\n')
        genome = lines[1].rstrip('\n')

        pattern_line = lines[2].rstrip('\n')
        line_parts = pattern_line.split(':')

        pattern = line_parts[0]
        match_indexes = list(map(int, line_parts[1].split(',')))

        algorithm_result = algorithm.query(genome, pattern)

        if match_indexes != algorithm_result:
            result = UnitTestResult.FAILED
        else:
            result = UnitTestResult.PASSED

        results.append(UnitTestResult(result, name))

    return results


def print_test_results(results):
    for result in results:
        print(result.get_description())
