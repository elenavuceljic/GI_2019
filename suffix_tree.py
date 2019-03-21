from main import AlgorithmWithIndexStructure
from unit_test import *


class SuffixTree(AlgorithmWithIndexStructure):

    class Node(object):
        def __init__(self, lab, offset=-1):
            self.lab = lab  # label on path leading to this node
            self.offset = offset  # suffix offset in text
            self.out = {}  # outgoing edges; maps characters to nodes

        def getLeavesOffsets(self):
            if self.offset != -1:
                # node is a leaf, returns suffix offset
                return [self.offset]
            else:
                # node is internal, propagates function call further down the tree
                return sorted([el for c in self.out for el in self.out[c].getLeavesOffsets()])

    def __init__(self):
        self.__root = self.Node(None)
        self.__text = ""

    def initWithText(self):
        self.__root.out[self.__text[0]] = self.Node(self.__text, 0)  # trie for just longest suf
        # add the rest of the suffixes, from longest to shortest
        for i in range(1, len(self.__text)):
            # start at root; we’ll walk down as far as we can go
            cur = self.__root
            j = i
            while j < len(self.__text):
                if self.__text[j] in cur.out:
                    child = cur.out[self.__text[j]]
                    lab = child.lab
                    # Walk along edge until we exhaust edge label or
                    # until we mismatch
                    k = j + 1
                    while k - j < len(lab) and self.__text[k] == lab[k - j]:
                        k += 1
                    if k - j == len(lab):
                        cur = child  # we exhausted the edge
                        j = k
                    else:
                        # we fell off in middle of edge
                        c_exist, c_new = lab[k - j], self.__text[k]
                        # create “mid”: new node bisecting edge
                        mid = self.Node(lab[:k - j])
                        mid.out[c_new] = self.Node(self.__text[k:], i)
                        # original child becomes mid’s child
                        mid.out[c_exist] = child
                        # original child’s label is curtailed
                        child.lab = lab[k - j:]
                        # mid becomes new child of original parent
                        cur.out[self.__text[j]] = mid
                else:
                    # Fell off tree at a node: make new edge hanging off it
                    cur.out[self.__text[j]] = self.Node(self.__text[j:], i)

    def followPath(self, pattern):
        cur = self.__root
        i = 0
        while i < len(pattern):
            c = pattern[i]
            if c not in cur.out:
                return None  # fell off at a node
            child = cur.out[pattern[i]]
            lab = child.lab
            j = i + 1
            while j - i < len(lab) and j < len(pattern) and pattern[j] == lab[j - i]:
                j += 1
            if j - i == len(lab):
                cur = child  # exhausted edge
                i = j
            elif j == len(pattern):
                return child  # exhausted query string in middle of edge
            else:
                return None  # fell off in the middle of the edge
        return cur  # exhausted query string at internal node

    def query(self, text, pattern):
        self.__text = text + '$'
        self.__root = self.Node(None)

        self.initWithText()

        node = self.followPath(pattern)
        return node.getLeavesOffsets()


# Run tests
test_results = run_algorithm_tests(SuffixTree())
print_test_results(test_results)
