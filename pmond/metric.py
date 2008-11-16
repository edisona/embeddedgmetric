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
            
        try:
            self.gather(tree)
        except KeyboardInterrupt:
            sys.exit(1)
        except Exception,e:
            print "Got exception in " + self.__class__.__name__
            traceback.print_exc()
        s.enter(self.interval(), 1, self.register, [s, tree])
        #s.enter(5, 1, self.register, [s, tree])

    def startup(self):
        pass

    def interval(self):
        return 15

    def gather(self):
        pass

    def shutdown(self):
        pass

