

class CardClass:
    def __init__(self, name):
        self.name = name
        self.number = name[0]
        self.kind = name[1]
        self.revealed = False
        self.selected = False

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()
