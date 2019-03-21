import abc

class AlgorithmWithIndexStructure(object):

    @abc.abstractmethod
    def initWithText(self):
        pass

    @abc.abstractmethod
    def query(self, text, pattern):
        pass
