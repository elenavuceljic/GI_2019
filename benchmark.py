from main import AlgorithmWithIndexStructure
import time
import threading
import psutil
import os
import copy
import gc
import sys


class BenchmarkResult(object):

    def __init__(self, algorithm_name, text, pattern_set, init_time, patterns_query_time, used_memory):
        self.__algorithm_name = algorithm_name
        self.__text = text
        self.__pattern_set = pattern_set
        self.__init_time = init_time
        self.__patterns_query_time = patterns_query_time
        self.__used_memory = used_memory

    def get_algorithm_name(self):
        return self.__algorithm_name

    def get_text(self):
        return self.__text

    def get_pattern_set(self):
        return self.__pattern_set

    def get_total_execution_time(self):
        return self.__init_time + self.__patterns_query_time

    def get_patterns_query_time(self):
        return self.__patterns_query_time

    def get_init_time(self):
        return self.__init_time

    def get_memory_usage(self):
        return self.__used_memory

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "--------------------------------------------------------------"\
               "\n" + self.__algorithm_name + " benchmark results \n\n" \
               "Used memory (bytes): \t" + str(self.__used_memory) + "\n" + \
               "Text init time: \t\t" + str(self.__init_time) + "\n" + \
               "Total query time: \t\t" + str(self.__patterns_query_time) + "\n" \
               "Total execution time: \t" + str(self.get_total_execution_time()) + "\n" \
               "--------------------------------------------------------------" \



class MemoryMonitor(threading.Thread):

    def __init__(self, refresh_rate):
        threading.Thread.__init__(self)
        self.daemon = True
        self.__thread_running = threading.Event()
        self.__max_memory = 0
        self.__sleep_time = refresh_rate
        self.__process = psutil.Process(os.getpid())

    def run(self):
        gc.collect()
        initial_memory_usage = self.__process.memory_info().rss

        while self.__thread_running.isSet():
            current_memory_usage = self.__process.memory_info().rss - initial_memory_usage
            self.__max_memory = max(current_memory_usage, self.__max_memory)
            time.sleep(self.__sleep_time)

    def start_monitoring(self):
        self.__thread_running.set()
        self.start()

    def finish_monitoring(self):
        self.__thread_running.clear()
        return self.__max_memory

    def getName(self):
        return "MonitorThread #" + threading.Thread.getName(self)


class DummyAlgorithm(AlgorithmWithIndexStructure):

    @staticmethod
    def __allocate_memory(size):
        x = bytearray(size//2)
        y = copy.deepcopy(x)
        del x
        return y

    def initWithText(self, text):
        self.__allocate_memory(512000000)
        time.sleep(3)

    def query(self, pattern):
        self.__allocate_memory(256000000)
        time.sleep(1)


def benchmark_run(algorithm, text, patterns, title, iterations=1, memory_monitor_resolution=0.01):

    print("Running benchmark tests for " + title)

    min_init_time = sys.maxsize + 1
    min_total_query_time = sys.maxsize + 1
    min_memory_all = sys.maxsize + 1

    for i in range(iterations):

        print("\n---------- Test iteration " + str(i+1) + " ----------")
        alg_object = copy.deepcopy(algorithm)

        print("Building index structure...")

        mem_monitor = MemoryMonitor(memory_monitor_resolution)
        mem_monitor.start_monitoring()

        init_time_start = time.time()
        alg_object.initWithText(text)
        init_time = time.time() - init_time_start

        min_init_time = min(min_init_time, init_time)

        total_query_time = 0

        for pattern in patterns:

            print("Query pattern \"" + pattern + "\"...")

            time_start = time.time()
            alg_object.query(pattern)
            time_pattern = time.time() - time_start

            total_query_time += time_pattern

        min_total_query_time = min(min_total_query_time, total_query_time)
        min_memory_all = min(min_memory_all, mem_monitor.finish_monitoring())

        del alg_object

    return BenchmarkResult(title, text, patterns, min_init_time, min_total_query_time, min_memory_all)


# Unit test for benchmark_run function

# Use a simulated exact match algorithm
dummy_algorithm = DummyAlgorithm()

# Simulate initial memory usage
bytearray(64000)

results = benchmark_run(dummy_algorithm, "ACCTCGATCCGATCG", ["ATTG", "CCA"], "DummyAlgorithm", 5)

print("\n" + str(results))
