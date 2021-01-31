from Card import CardClass
import random


class DeckClass:
    ranks = ("2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A")
    suits = ("c", "d", "h", "s")

    def __init__(self):
        self.cards = []
        for rank in DeckClass.ranks:
            for suit in DeckClass.suits:
                self.cards.append(CardClass(rank + suit))

    def __str__(self):

        return str([item for item in self.cards])
        # return str(self.cards)

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self, how_many=1):

        return [(self.cards.pop()) for i in range(how_many)]

    def put(self, cards):
        for card in cards:
            self.cards.insert(0, card)
