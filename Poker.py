""" En esta sección se evaluan las manos en juego"""


def straight(ranks):
    """ Escalera """
    if ranks[0] == 14 and ranks[4] == 2:
        ranks[0] = 1
    if len(set(ranks)) == 5 and (max(ranks) - min(ranks) == 4):
        return True
    return False


def flush(suits):
    """ Color """
    if len(set(suits)) == 1:
        return True
    return False


def kind(n, ranks):
    """ Para determinar repeticiones (par, par doble, poker, etc)"""
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
    """ Determinar los rangos """
    ranks = ["--23456789TJQKA".index(r.number) for r in hand]
    ranks.sort(reverse=True)
    return ranks


def card_suits(hand):
    """ Determinar las pintas """
    return [s.kind for s in hand]


def poker(hands):
    """ Método inicial, se reciben todas las manos en juego"""
    l = []
    for i in range(len(hands)):
        l.append(list(hand_rank(hands[i])))

    a = l.index(max(l))
    m = max(l)
    k = ['Escalera Color', 'Poker', 'Full House', 'Color', 'Escalera', 'Trio', 'Doble Par',
         'Par', 'Carta Alta']
    k = list(reversed(k))
    if m == [8, 14]:
        jugada = 'Escalera Real'
    else:
        jugada = k[m[0]]
    return {"ganador": (a + 1), "jugada": jugada}


def hand_rank(hand):
    """ Evaluacion del rango de la mano """
    ranks = card_ranks(hand)
    suits = card_suits(hand)

    if straight(ranks) and flush(suits):
        """ Escalera real"""
        return (8, max(ranks))
    elif kind(4, ranks):
        """ Poker """
        return (7, kind(4, ranks), kind(1, ranks))
    elif kind(3, ranks) and kind(2, ranks):
        """ Full house """
        return (6, kind(3, ranks), kind(2, ranks))
    elif flush(suits):
        """ Color """
        return (5,) + tuple(ranks)
    elif straight(ranks):
        """ Escalera """
        return (4, max(ranks))
    elif kind(3, ranks):
        """ Trio """
        same = kind(3, ranks)
        return (3, same) + tuple([i for i in ranks if i != same])
    elif two_pair(ranks):
        """ Doble par """
        return (2,) + two_pair(ranks) + (kind(1, ranks),)
    elif kind(2, ranks):
        """ Par """
        same = kind(2, ranks)
        return (1, same) + tuple([i for i in ranks if i != same])
    else:
        """ Carta alta"""
        return (0,) + tuple(ranks)
