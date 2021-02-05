def straight(ranks):

    if ranks[0] == 14 and ranks[4] == 2:
        ranks[0] = 1
    if len(set(ranks)) == 5 and (max(ranks) - min(ranks) == 4):
        return True
    return False


def flush(suits):

    if len(set(suits)) == 1:
        return True
    return False


def kind(n, ranks):

    for r in ranks:
        if ranks.count(r) == n:
            return r
    return None


def two_pair(ranks):

    hicard = kind(2, ranks)
    locard = kind(2, tuple(reversed(ranks)))

    if hicard != locard:
        return (hicard, locard)
    return False


def card_ranks(hand):
    ranks = ["--23456789TJQKA".index(r.number) for r in hand]
    ranks.sort(reverse=True)
    return ranks


def card_suits(hand):
    return [s.kind for s in hand]


def poker(hands):
    l = []
    for i in range(len(hands)):
        l.append(list(hand_rank(hands[i])))

    a = l.index(max(l))
    m = max(l)
    k = ['Escalera Color', 'Poker', 'Full House', 'Color', 'Escalera', 'Trio', 'Doble Par',
         'Par', 'Carta Alta']
    k = list(reversed(k))
    if (m == [8, 14]):
        jugada = 'Escalera Real'
    else:
        jugada = k[m[0]]
    return {"ganador":(a+1),"jugada":jugada}


def hand_rank(hand):
    ranks = card_ranks(hand)
    suits = card_suits(hand)

    if straight(ranks) and flush(suits):
        return (8, max(ranks))
    elif kind(4, ranks):
        return (7, kind(4, ranks), kind(1, ranks))
    elif kind(3, ranks) and kind(2, ranks):
        return (6, kind(3, ranks), kind(2, ranks))
    elif flush(suits):
        return (5,) + tuple(ranks)
    elif straight(ranks):
        return (4, max(ranks))
    elif kind(3, ranks):
        same = kind(3, ranks)
        return (3, same) + tuple([i for i in ranks if i != same])
    elif two_pair(ranks):
        return (2,) + two_pair(ranks) + (kind(1, ranks),)
    elif kind(2, ranks):
        same = kind(2, ranks)
        return (1, same) + tuple([i for i in ranks if i != same])
    else:
        return (0,) + tuple(ranks)