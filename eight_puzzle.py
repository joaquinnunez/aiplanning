"""
Toy Problem: Sliding-Block Puzzle
- problem description:
- states: location of each tile and the blank (9!/2 = 181440 states)
- initial state: any (reachable) state, e.g. one shown on left (worst case: solution requires at least 31 steps)
- actions: good formulation: move blank left/right/up/down
- goal test: goal state (shown right)
- step cost: 1
"""

import copy
import heapq

LEFT = "l"
RIGHT = "r"
UP = "u"
DOWN = "d"

GOAL = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
GOAL_TILES = {}
for j, row in enumerate(GOAL):
    for i, val in enumerate(row):
        GOAL_TILES[val] = (i, j)


class Puzzle(object):
    """ """
    def __init__(self, initial, last_move, n_moves):
        self.data = initial
        self.tiles = {}
        self.compute_tiles_positions()
        self.last_move = last_move
        self.n_moves = n_moves

    def compute_tiles_positions(self):
        for j, row in enumerate(self.data):
            for i, val in enumerate(row):
                self.tiles[val] = (i, j)
                if self.data[j][i] == 0:
                    self.x, self.y = i, j

    def get_tile(self, x, y):
        return self.data[y][x]

    def set_tile(self, x, y, value):
        self.data[y][x] = value
        if value == 0:
            self.x = x
            self.y = y

    def __str__(self):
        result = []
        for row in self.data:
            result.append(", ".join([str(val) for val in row]))
        return "\n".join(result) + "\n"

    def heuristic(self):
        """ Heuristics for the Eight-Puzzle
            - h1: number of misplaced tiles
            - h2: Manhattan block distance
        """
        value = 0
        for j, row in enumerate(self.data):
            for i, val in enumerate(row):
                # for each misplaced tile, we add 1, and the value of the manhattan distance
                if self.data[j][i] != GOAL[j][i]:
                    value += 1
                    # md = abs(self.tiles[val][0] - GOAL_TILES[val][0]) + abs(self.tiles[val][1] - GOAL_TILES[val][1])
                    # value += md
        return value

    def __lt__(self, other):
        return self.heuristic() + self.n_moves < other.heuristic() + other.n_moves

    def can_move(self, to):
        return (to == LEFT and self.x > 0) or (to == RIGHT and self.x < 2) or (to == UP and self.y > 0) or (to == DOWN and self.y < 2)

    def id(self):
        result = []
        for row in self.data:
            for value in row:
                result.append(str(value))
        return "".join(result)

    def goal_test(self):
        return self.id() == "012345678"


class Action(object):
    """ """
    def move(self, puzzle, to):
        npuzzle = copy.deepcopy(puzzle)
        if to == LEFT:
            tile_value = npuzzle.get_tile(npuzzle.x - 1, npuzzle.y)
            npuzzle.set_tile(npuzzle.x, npuzzle.y, tile_value)
            npuzzle.set_tile(npuzzle.x - 1, npuzzle.y, 0)
        elif to == RIGHT:
            tile_value = npuzzle.get_tile(npuzzle.x + 1, npuzzle.y)
            npuzzle.set_tile(npuzzle.x, npuzzle.y, tile_value)
            npuzzle.set_tile(npuzzle.x + 1, npuzzle.y, 0)
        elif to == UP:
            tile_value = npuzzle.get_tile(npuzzle.x, npuzzle.y - 1)
            npuzzle.set_tile(npuzzle.x, npuzzle.y, tile_value)
            npuzzle.set_tile(npuzzle.x, npuzzle.y - 1, 0)
        elif to == DOWN:
            tile_value = npuzzle.get_tile(npuzzle.x, npuzzle.y + 1)
            npuzzle.set_tile(npuzzle.x, npuzzle.y, tile_value)
            npuzzle.set_tile(npuzzle.x, npuzzle.y + 1, 0)
        else:
            raise Exception("Would you like to break the npuzzle?")
        npuzzle.last_move = to
        npuzzle.n_moves += 1
        npuzzle.compute_tiles_positions()
        return npuzzle


def expand(puzzle):

    previous = {UP: DOWN, DOWN: UP, RIGHT: LEFT, LEFT: RIGHT}
    states = []
    a = Action()
    for move_to in [LEFT, RIGHT, UP, DOWN]:
        if puzzle.last_move != previous[move_to] and puzzle.can_move(move_to):
            p = a.move(puzzle, move_to)
            states.append(p)
    return states


def path_to(came_from, current):
    total_path = [current]
    while current in came_from.keys():
        current = came_from[current]
        total_path.append(current)
    total_path.reverse()
    return " -> ".join(total_path)

if __name__ == "__main__":
    # initial = [[3, 2, 0], [4, 5, 7], [1, 8, 6]]
    initial = [[8, 1, 7], [4, 5, 6], [2, 0, 3]]
    # initial = [[1, 6, 4], [8, 7, 0], [3, 2, 5]]
    node = Puzzle(initial, None, 0)
    graph_search = True
    came_from = {}
    fringe = []

    if graph_search:
        memory = set()

    heapq.heappush(fringe, node)
    while fringe:

        # select node from heap priority queue the node will not be selected again
        node = heapq.heappop(fringe)
        # print("Current node:\n{0}".format(node))

        # goal test before expansion: to avoid trick problem like "get from Arad to Arad"
        if node.goal_test():
            # success: goal node found
            print("Moves: {0}".format(node.n_moves))
            print(path_to(came_from, node.id()))
            break

        if graph_search:
            memory.add(node.id())

        # otherwise: add new nodes to the fringe and continue loop
        # print("Successors:")
        for n in expand(node):
            if not graph_search or (graph_search and n.id() not in memory):
                came_from[n.id()] = node.id()
                heapq.heappush(fringe, n)
                # print("N:{0} - h:{1} - c:{2}".format(n.id(), n.heuristic(), n.n_moves))

        # a = raw_input()
