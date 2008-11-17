import traceback
import sys

class metric(object):
    def __init__(self):
        self.tree = None

    def addMetric(self, values):
        self.tree.addMetric(values)

    def register(self, s, tree):
        if self.tree is None:
            self.tree = tree

        self.gather(tree)
        s.enter(self.interval(), 1, self.register, [s, tree])

    def startup(self):
        pass

    def interval(self):
        return 15

    def gather(self):
        pass

    def shutdown(self):
        pass

