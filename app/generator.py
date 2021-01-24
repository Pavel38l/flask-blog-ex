class Generator:
    def __init__(self, start=0, step=1):
        self.id = start
        self.step = step

    def next(self):
        self.id += self.step
        return self.id
