class ReturnException(Exception):
    def __init__(self, value):
        self.value = value

class ContinueException(Exception):
    def __init__(self):
        pass

class BreakException(Exception):
    def __init__(self):
        pass
