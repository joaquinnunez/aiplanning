"""
Toy Problem: Missionaries and Cannibals. (Week1)

On one bank of a river are three missionaries and three cannibals.
There is one boat available that can hold up to two people and that
they would like to use to cross the river.
If the cannibals ever outnumber the missionaries on either of the river's
banks, the missionaries will get eaten.
How can the boat be used to safely carry all the missionaries and cannibals
across the river?
Problem: find a sequence of action that brings about another state
"""


class Node(object):
    def __init__(self, current, next):
        if current.river_side == "L":
            self.left = current
            self.right = next
        else:
            self.left = next
            self.right = current

    def goal_test(self):
        return self.pk() == "L:0m,0c-R:3m,3c,b"

    def is_valid(self):
        return self.left.is_valid() and self.right.is_valid()

    def pk(self):
        return "-".join([self.left.pk(), self.right.pk()])

    def __repr__(self):
        return self.pk()

    def next_side(self):
        return self.left.boat and self.right or self.left

    def current_side(self):
        return self.left.boat and self.left or self.right


class RiverSideNode(object):
    def __init__(self, cannibals, missionaries, river_side, boat=""):
        self.cannibals = cannibals
        self.missionaries = missionaries
        self.boat = boat
        self.river_side = river_side

    def pk(self):
        boat = ",{0}".format(self.boat) if self.boat else ""
        return "{0}:{1}m,{2}c{3}".format(self.river_side, self.missionaries, self.cannibals, boat)

    def __repr__(self):
        return self.pk()

    def is_valid(self):
        if self.missionaries > 0:
            return not self.cannibals > self.missionaries
        else:
            return True


def get_first():
    left = RiverSideNode(3, 3, "L", "b")
    right = RiverSideNode(0, 0, "R", "")
    return Node(left, right)


def expand(node):
    """ Computes the possible next nodes """

    next_side = node.next_side()
    current_side = node.current_side()
    new_nodes = []
    # can we move 2 missionaries?
    if current_side.missionaries > 1:
        cside = RiverSideNode(current_side.cannibals, current_side.missionaries - 2, current_side.river_side)
        nside = RiverSideNode(next_side.cannibals, next_side.missionaries + 2, next_side.river_side, "b")
        new_nodes.append(Node(cside, nside))

    # can we move 2 cannibals?
    if current_side.cannibals > 1:
        cside = RiverSideNode(current_side.cannibals - 2, current_side.missionaries, current_side.river_side)
        nside = RiverSideNode(next_side.cannibals + 2, next_side.missionaries, next_side.river_side, "b")
        new_nodes.append(Node(cside, nside))

    # can we move 1 missionary and 1 cannibal?
    # can we move 2 cannibals?
    if current_side.missionaries > 0 and current_side.cannibals > 0:
        cside = RiverSideNode(current_side.cannibals - 1, current_side.missionaries - 1, current_side.river_side)
        nside = RiverSideNode(next_side.cannibals + 1, next_side.missionaries + 1, next_side.river_side, "b")
        new_nodes.append(Node(cside, nside))

    # can we move 1 missionary?
    if current_side.missionaries > 0:
        cside = RiverSideNode(current_side.cannibals, current_side.missionaries - 1, current_side.river_side)
        nside = RiverSideNode(next_side.cannibals, next_side.missionaries + 1, next_side.river_side, "b")
        new_nodes.append(Node(cside, nside))

    # can we move 1 cannibal?
    if current_side.cannibals > 0:
        cside = RiverSideNode(current_side.cannibals - 1, current_side.missionaries, current_side.river_side)
        nside = RiverSideNode(next_side.cannibals + 1, next_side.missionaries, next_side.river_side, "b")
        new_nodes.append(Node(cside, nside))

    return new_nodes


def tree_search(problem, strategy):
    """ Find a solution to the given problem while expanding nodes according to the given strategy """

    # fringe: set of known states; initially just initial state

    fringe = [get_first()]
    counter = 0
    visited = []
    came_from = {}

    while len(fringe) > 0:

        # print(fringe)
        if not fringe:
            raise Exception("Complete tree explored; no goal state found")

        # select node from fringe according to search control strategy
        # the node will not be selected again
        node = fringe.pop()
        visited.append(str(node))
        # print("current node: {0}".format(node))

        # goal test before expansion: to avoid trick problem like "get from Arad to Arad"
        if node.goal_test():
            # success: goal node found
            print("Final node: {0} reached.".format(node))
            print("Counter: {0}".format(counter))
            print(path_to(came_from, str(node)))
            return

        # otherwise: add new nodes to the fringe and continue loop
        for n in expand(node):
            if str(n) not in visited and n.is_valid():
                came_from[str(n)] = str(node)
                fringe.append(n)
        counter += 1


# This was stolen from wikipedia pseudocode :-P
def path_to(came_from, current):
    total_path = [current]
    while current in came_from.keys():
        current = came_from[current]
        total_path.append(current)
    total_path.reverse()
    return " -> ".join(total_path)

if __name__ == "__main__":
    tree_search(None, None)
