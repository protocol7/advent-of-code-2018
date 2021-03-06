from collections import deque
from itertools import chain, imap
from heapq import heappush, heappop
from re import findall

def flatmap(f, items):
    return chain.from_iterable(imap(f, items))

# get digit as position n from an int
def digit(number, n):
    return number // 10**n % 10

# partition a list into chunks of lenght n
def chunks(xs, n):
    return [xs[i:i + n] for i in range(0, len(xs), n)]

# find all ints, including negative ones, in a string
def ints(s):
    return map(int, findall(r"-?\d+", s))

# finds all simple strings and digits, including negative ints
def tokens(s):
    return findall(r"[A-Za-z0-9\-]+", s)

# is this string an int?
def isint(s):
    return s.isdigit() or (s and s[0] in ('+', '-') and s[1:].isdigit())

# make ints of everything that looks like one
def intify(xs):
    return [int(x) if isint(x) else x for x in xs]

def sign(i):
    if i > 0:
        return 1
    elif i < 0:
        return -1
    else:
        return 0

def manhattan(*args):
    if len(args) == 2:
        (ax, ay), (bx, by) = args
    elif len(args) == 4:
        ax, ay, bx, by = args
    return abs(ax - bx) + abs(ay - by)

# graph is dict of node -> neighbours
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

# give topological order of graph, starting at "start"
# graph is dict of node -> neighbours
# returns a list of nodes in topological order
def top_sort(graph, start):
    result = []
    seen = set()

    def visit(node):
        for n in graph[node]:
            if n not in seen:
                seen.add(n)
                visit(n)
        result.insert(0, node) # on the return path, insert in inverse order

    visit(start)

    return result

adjacent = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]

# maze = [[0, 0], [0, 1]]
def astar(maze, start, goal):
    q = [(0, [start])]
    seen = set([start])

    while q:
        cost, path = heappop(q)
        c = path[-1]

        if c == goal:
            return path

        cx, cy = c
        for dx, dy in adjacent:
            n = cx + dx, cy + dy
            nx, ny = n

            if nx < 0 or ny < 0 or nx >= len(maze[0]) or ny >= len(maze):
                continue

            if not maze[ny][nx]:
                if n not in seen:
                    priority = cost + 1 + manhattan(n, goal)
                    heappush(q, (priority, path + [n]))
                seen.add(n)
