'''
The Facade class simply subclass the builtin `dict` class to add a few
convenience flags.
'''
class Facade(dict):
    def __init__(self, *args, **kwargs):
        self.successful = False
        self.empty_results = False
        dict.__init__(self, *args, **kwargs)
