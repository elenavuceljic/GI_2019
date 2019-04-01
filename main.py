from index_hash import IndexHash
from index_sorted import IndexSorted
from suffix_array import SuffixArray
from suffix_tree import SuffixTree
from benchmark import benchmark_run
import os
from pathlib import Path


def rstrip(line):
    return line.rstrip('\n')


algorithms = [IndexHash(), IndexSorted(), SuffixArray(), SuffixTree()]

tests_dir = Path("Tests/Performance/")
tests_results_dir = Path("Tests/Results/")
test_files = []

for file in os.listdir(tests_dir):
    test_files.append(tests_dir / file)

for test_file_name in test_files:

    test_file = open(test_file_name, 'r')
    lines = test_file.readlines()

    genome = ''.join(map(rstrip, lines[2:]))
    patterns = [x for x in lines[1].rstrip('\n').split(',')]

    index = test_files.index(test_file_name)

    for algorithm in algorithms:
        test_results_file_path = tests_results_dir / (algorithm.get_name() + str(index) + ".txt")
        test_results_file = open(test_results_file_path, "w+")
        test_results_file.write(benchmark_run(algorithm, genome, patterns, algorithm.get_name(), 1))
