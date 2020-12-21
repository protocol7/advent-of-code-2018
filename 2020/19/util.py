from collections import deque, defaultdict
from copy import deepcopy
from heapq import heappush, heappop
from re import findall
from itertools import chain
from functools import reduce
from math import gcd

def flatmap(f, items):
    return list(chain.from_iterable(map(f, items)))

# get digit as position n from an int
def digit(number, n):
    return number // 10**n % 10

# partition a list into chunks of lenght n
def chunks(xs, n):
    return [xs[i:i + n] for i in range(0, len(xs), n)]

def pairs(xs):
    return chunks(xs, n)

# find all ints, including negative ones, in a string
def ints(s):
    return list(map(int, findall(r"-?\d+", s)))

# finds all simple strings and digits, including negative ints
def tokens(s):
    return findall(r"[A-Za-z0-9\-]+", s)

# is this string an int?
def isint(s):
    return s.isdigit() or (s and s[0] in ('+', '-') and s[1:].isdigit())

# make ints of everything that looks like one
def intify(xs):
    return [int(x) if isint(x) else x for x in xs]

# turn an str or int into a binary str
# if length is given, left pad to bit string of length
def binary(i, length=0):
    b = "{0:b}".format(int(i))
    if length:
        return b.rjust(length, '0')
    else:
        return b

# split a string at any character in seps
# returns list of strings, excluding any empty substrings
def msplit(s, seps):
    def f(s, seps):
        p = 0
        for i, c in enumerate(s):
            if c in seps:
                yield s[p:i]
                p = i + 1
        yield s[p:]
    return list(filter(lambda s: s, f(s, seps)))

# length of an iterator
def ilen(iter):
    return sum(1 for _ in iter)

# removes value from collections (list, sets) without throwing exception if the value is not in the collection
# does not mutate the provided collection, but rather returns a new collection with the value removed
def safe_remove(v, xs):
    xs = deepcopy(xs)

    if type(xs) == list:
        if v in xs:
            xs.remove(v)
    elif type(xs) == set:
        xs.discard(v)

    return xs

def product(xs):
    return reduce(lambda a, b: a * b, xs)

def sign(i):
    if i > 0:
        return 1
    elif i < 0:
        return -1
    else:
        return 0

# Graphs/geometry

def manhattan(*args):
    if len(args) == 1:
        ax, ay = args[0]
        bx, by = 0, 0
    elif len(args) == 2:
        if type(args[0]) == tuple:
            (ax, ay), (bx, by) = args
        else:
            ax, ay = args
            bx, by = 0, 0
    elif len(args) == 4:
        ax, ay, bx, by = args
    return abs(ax - bx) + abs(ay - by)

# graph is dict of node -> neighbours
# returns dict of node -> best level and dict of node -> best parent
def exhaustive_bfs(graph, start):
    q = deque([start])
    levels = {start: 0}
    parent = {start: None}

    level = 1
    while q:
        v = q.popleft()
        for n in graph[v]:
            if n not in levels:
                q.append(n)
                levels[n] = level
                parent[n] = v
        level += 1
    return levels, parent

# graph is dict of node -> neighbours
# end is predicate function
# returns path from start to end
def bfs(graph, start, end):
    q = deque([[start]])
    seen = set()

    while q:
        path = q.popleft()
        v = path[-1]
        for n in graph[v]:
            p = path + [n]
            if end(n):
                return p
            if n not in seen:
                q.append(p)
                seen.add(n)

# return all paths between start and end
# graph is dict of node -> neighbours
# end is predicate function
# returns list of paths from start to end
def bfs_all_paths(graph, start, end, cyclic=False):
    q = deque([[start]])
    paths = []

    while q:
        path = q.popleft()
        v = path[-1]
        for n in graph[v]:
            if cyclic and n in path:
                continue

            p = path + [n]
            if end(n):
                paths.append(p)
            else:
                q.append(p)
    return paths

# give topological order of graph, starting at "start"
# graph is dict of node -> neighbours
# returns a list of nodes in topological order
def top_sort(graph, start):
    result = []
    seen = set()

    def visit(node):
        if node in graph:
            for n in graph[node]:
                if n not in seen:
                    seen.add(n)
                    visit(n)
        result.insert(0, node) # on the return path, insert in inverse order

    visit(start)

    return result

orthogonal = [(0, -1), (0, 1), (-1, 0), (1, 0)]
adjacent = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]

# iterator over orthogonal coords from x and y
def iter_orthogonal(x, y, grid=None):
    for dx, dy in orthogonal:
        xx = x + dx
        yy = y + dy
        if not grid or in_grid(grid, xx, yy):
            yield xx, yy

# iterator over adjacent coords from x and y
# if grid (list of lists) is provided, only coords in bound of the grid will be returned
def iter_adjacent(x, y, grid=None):
    for dx, dy in adjacent:
        xx = x + dx
        yy = y + dy
        if not grid or in_grid(grid, xx, yy):
            yield xx, yy

# check if coordinate is in grid. grid is list of lists
def in_grid(grid, x, y):
    return x >= 0 and y >= 0 and y < len(grid) and x < len(grid[y])

# get the value in grid (list of lists). Return default if x, y is out of bounds
def grid_get(grid, x, y, default=None):
    if in_grid(grid, x, y):
        return grid[y][x]
    else:
        return default

# convert grid (list of lists) into a dict (x, y) -> value
def grid_to_dict(grid):
    d = dict()
    for y, row in enumerate(grid):
        for x, v in enumerate(row):
            d[(x, y)] = v
    return d

# maze = [[0, 0], [0, 1]]
# is_neighbour is a predicate to check if one can navigate from one node to
# another
# is_neighbour(current_coord, current_value, neighbour_coord, neighbour_value)
# result in graph of dict of node -> neighbours
#
# Example, maze where false values are navigatable
# maze_to_graph(maze, start, lambda _, __, ___, x: not x)
#
def maze_to_graph(maze, start, is_neighbour):
    q = [start]
    seen = set([start])
    g = defaultdict(list)
    w = len(maze[0])
    h = len(maze)

    while q:
        c = heappop(q)
        cx, cy = c

        for nx, ny in iter_adjacent(cx, cy, maze):
            n = nx, ny

            if is_neighbour(c, maze[cy][cx], n, maze[ny][nx]):
                g[c].append(n)

                if n not in seen:
                    heappush(q, n)
                    seen.add(n)
    return g

# finds a path between start and goal
# graph is dict of node -> neighbours
# node and neighbours are (x, y) tuples, as is start and goal
def astar(graph, start, goal):
    q = [(0, [start])]
    seen = set([start])

    while q:
        cost, path = heappop(q)
        c = path[-1]

        if c == goal:
            return path

        for n in graph[c]:
            if n not in seen:
                priority = cost + 1 + manhattan(n, goal)
                heappush(q, (priority, path + [n]))
                seen.add(n)

# check(i), return True if i is too large
# returns the largest value where check is false, and the smallest where check
# is true (just to remember to think about the one-off :)
def binary_search(lo, hi, check):
    blo = check(lo)
    bhi = check(hi)
    if blo == bhi:
        assert False, "lo and hi both %s" % blo

    while True:
        x = (lo + hi) // 2
        if check(x):
            if not check(x-1):
                return (x-1, x)
            hi = x
        else:
            lo = x

# Simple memoize implementation, use with @Memoize
class Memoize:
    def __init__(self, f):
        self.f = f
        self.memo = {}

    def __call__(self, *args):
        if not args in self.memo:
            self.memo[args] = self.f(*args)
        #Warning: You may wish to do a deepcopy here if returning objects
        return self.memo[args]

# Maths

# least common multiple
def lcm(*args):
    if len(args) == 2:
        a, b = args
        return abs(a*b) // gcd(a, b)
    elif len(args) > 2:
        return reduce(lcm, args)

# find the smallest number x, such that x % n = a for each n and a in nx, ax
# ax thus is a list of mod remainders
# note that remainders in ax should be negative
#
# Adapted from https://rosettacode.org/wiki/Chinese_remainder_theorem#Python_3.6
def chinese_remainder(nx, ax):
    prod = product(nx)

    s = 0
    for n, a in zip(nx, ax):
        p = prod // n

        s += a * mul_inv(p, n) * p

    return s % prod

# return x, such that (a * x) % m == 1, 0 <= x <= m
def mul_inv(a, m):
    m0 = m
    x0, x1 = 0, 1

    if m == 1:
        return 1

    while a > 1:
        q = a // m
        a, m = m, a % m
        x0, x1 = x1 - q * x0, x0

    if x1 < 0:
        x1 += m0

    return x1

# for a dict where values are list of possible options, this will reduce that down to the one unique option for each item.
# for example, given a dict of:
# {
#   0: [1, 2, 3],
#   1: [2],
#   2: [2, 3]
# }
#
# will give:
# {
#   0: [1],
#   1: [2],
#   2: [2]
# }
#
# keys can be any value
def reduce_unique_options(d):
    d = deepcopy(d)

    def all1(xs):
        return all(len(x) == 1 for x in xs)

    # reduce by looking at cases where there is only one available option. do this until only one remain for each
    while not all1(d.values()):
        for v in d.values():
            if len(v) == 1:

                # delete from all values, except self
                for k, vv in d.items():
                    if vv != v:
                        d[k] = safe_remove(v[0], vv)

    return d

