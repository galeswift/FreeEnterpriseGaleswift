def byte_string(bytes_iterable):
    return ' '.join([f'{b:02X}' for b in bytes_iterable])

def value_byte_string(val, byte_length):
    byte_vals = []
    while len(byte_vals) < byte_length:
        byte_vals.append(val & 0xFF)
        val >>= 8
    return byte_string(byte_vals)


class Distribution:
    def __init__(self, named_weights=None, **kw_named_weights):
        self._thresholds = []
        self._sum = 0

        if named_weights is None:
            named_weights = kw_named_weights

        for name in named_weights:
            self._sum += named_weights[name]
            self._thresholds.append( (name, self._sum) )

    def choose(self, rnd):
        v = rnd.random() * self._sum
        for threshold in self._thresholds:
            if v < threshold[1]:
                return threshold[0]
        return None

    def choose_many(self, rnd, count):
        counts = {}
        for i in range(count):
            v = self.choose(rnd)
            counts.setdefault(v, 0)
            counts[v] += 1
        return counts


# awkward spot for it, but it needs to go somewhere
WILDISH_BOOST_MATRIX = {
    1: [(1, 7/8)],
    2: [(1, 1/8), (2, 6/8)],
    3: [(2, 2/8), (3, 5/8)],
    4: [(3, 3/8), (4, 4/8)],
    5: [(4, 4/8), (5, 3/8)],
    6: [(5, 5/8), (6, 2/8)],
    7: [(6, 6/8), (7, 1/8)],
    8: [(7, 7/8), (8, 1)],
}

STANDARDISH_BOOST_MATRIX = {
    1: [(1, 6/8)],
    2: [(1, 2/8), (2, 6/8)],
    3: [(2, 2/8), (3, 5/8)],
    4: [(3, 3/8), (4, 4/8)],
    5: [(4, 4/8), (5, 5/8)],
    6: [(5, 3/8), (6, 6/8)],
    7: [(6, 2/8), (7, 7/8)],
    8: [(7, 1/8), (8, 1)],
}

SEMIBOOST_MATRIX = {
    1: [(1, 15/16)],
    2: [(1, 1/16), (2, 14/16)],
    3: [(2, 2/16), (3, 13/16)],
    4: [(3, 3/16), (4, 12/16)],
    5: [(4, 4/16), (5, 11/16)],
    6: [(5, 5/16), (6, 10/16)],
    7: [(6, 6/16), (7, 9/16)],
    8: [(7, 7/16), (8, 1)],
}

# adjustment matrix for locations with miabs under weighted distributions
ADJUST_MIABS_MATRIX = { 
    1: [(1, 1), (2, 1/4)],
    2: [(2, 3/4), (3, 1/4)],
    3: [(3, 3/4), (4, 1/2)],
    4: [(4, 1/2), (5, 1/2)],
    5: [(5, 1/2), (6, 3/4)],
    6: [(6, 1/4), (7, 3/4)],
    7: [(7, 1/4), (8, 3/4)],
    8: [(8, 1/4)],
}

def get_boosted_weights(weights, adjustment):
    boosted_weights = {i : 0 for i in range(1,9)}
    if adjustment == 'wildish':
        active_weights = WILDISH_BOOST_MATRIX
    elif adjustment == 'standardish':
        active_weights = STANDARDISH_BOOST_MATRIX 
    elif adjustment == 'semipro':
        active_weights = SEMIBOOST_MATRIX
    elif adjustment == 'miab_areas':
        active_weights = ADJUST_MIABS_MATRIX

    for i in boosted_weights:
        for chunk in active_weights[i]:
            boosted_weights[i] += weights[chunk[0]] * chunk[1]

    return boosted_weights