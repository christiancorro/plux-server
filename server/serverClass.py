class ServerClass:
    def __init__(self, A, B):
        self.valueA = A
        self.valueB = B

    def to_dict(self):
        return {"valueA": self.valueA, "valueB": self.valueB}