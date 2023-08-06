from .utils import StringTypes, StringType, classify, _cache_0args

class DTree(list):
    def __init__(self, datatype, datalist=()):
        self.type = datatype
        list.__init__(self, datalist)

d = DTree(1, [1,2])
print d, d.type
