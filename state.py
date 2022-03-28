
class State:

    def __init__(self, state, parent, move, depth, cost, key):

        self.state = state # List yang berisi urutan nomor sekarang.

        self.parent = parent # State parent.

        self.move = move # Move sebelumnya

        self.depth = depth

        self.cost = cost

        self.key = key

        if self.state:
            self.map = ''.join(str(e) for e in self.state)

    def __eq__(self, other):
        return self.map == other.map

    def __lt__(self, other):
        return self.map < other.map
