class Environment:
    def __init__(self, record = {}, parent = None):
        self.record = record
        self.parent = parent

    def define(self, name, value):
        self.record[name] = value

        return value

    def assign(self, name, value):
        env = self.resolve(name)

        if (env is None):
            raise NameError(f"Variable '{name}' is not defined")

        env.record[name] = value

        return value
    
    def lookup(self, name):
        env = self.resolve(name)

        if (env is None):
            raise NameError(f"Variable '{name}' is not defined")

        return env.record[name]

    def resolve(self, name):
        if (name in self.record.keys()):
            return self
        
        if (self.parent is None):
            return None
        
        return self.parent.resolve(name)