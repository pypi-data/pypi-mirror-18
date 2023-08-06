

class RouterResult(object):
    def __init__(self, data, params):
        self.data = data
        self.params = params

    @staticmethod
    def not_match(params={}):
        return RouterResult(None, params)

    @property
    def match(self):
        return self.data is not None
