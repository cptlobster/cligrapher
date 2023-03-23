


class Graph():
    def __init__(self,
                 data=None,
                 constraints=None):
        if not data:
            data = {}
        self.data = data
        self.constraints = constraints

    def __setattr__(self, key, value):
        self.data[key] = value

    def __getattr__(self, item):
        return self.data[item]

    def __delattr__(self, item):
        del self.data[item]

    def __str__(self):
        return "graph"

    def __repr__(self):
        return "graph"
