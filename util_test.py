from util import *
from collections import *
import unittest

class Misc(unittest.TestCase):

    def test_flatmap(self):
        self.assertEqual([4, 1, 4, 2, 4, 3], flatmap(lambda x: [4, x], [1, 2, 3]))

    def test_isinit(self):
        self.assertTrue(isint("2"))
        self.assertTrue(isint("123"))
        self.assertTrue(isint("-2"))
        self.assertTrue(isint("+2"))
        self.assertFalse(isint(""))
        self.assertFalse(isint("abc"))

    def test_tokens(self):
        self.assertEqual(["abc", "123", "-345", "def"], tokens("> abc 123 => -345, def"))

    def test_ints(self):
        self.assertEqual([123, -345], ints("> abc 123 => -345, def"))

    def test_initify(self):
        self.assertEqual(["abc", 123, -345, "def"], intify(["abc", "123", "-345", "def"]))

    def test_chunks(self):
        self.assertEqual([["abc", "123"], ["-345", "def"]], chunks(["abc", "123", "-345", "def"], 2))

    def test_digit(self):
        self.assertEqual(4, digit(456, 2))
        self.assertEqual(5, digit(456, 1))
        self.assertEqual(6, digit(456, 0))

    def test_sign(self):
        self.assertEqual(1, sign(2))
        self.assertEqual(0, sign(0))
        self.assertEqual(0, sign(-0))
        self.assertEqual(-1, sign(-2))

    def test_msplit(self):
        self.assertEqual(["1", "2", "3"], msplit("1-2 3", "- "))
        self.assertEqual(["1", "2 3"], msplit("1-2 3", "-"))

    def test_manhattan(self):
        self.assertEqual(13, manhattan((5, 8)))
        self.assertEqual(10, manhattan((1, 2), (5, 8)))
        self.assertEqual(10, manhattan(1, 2, 5, 8))

    def test_lcm(self):
        self.assertEqual(12, lcm(4, 6))

    def test_topsort(self):
        g = {'A': ['ORE'], 'C': ['B', 'A'], 'B': ['ORE'], 'E': ['D', 'A'], 'D': ['C', 'A'], 'FUEL': ['E', 'A']}
        self.assertEqual(['FUEL', 'E', 'D', 'C', 'A', 'B', 'ORE'], top_sort(g, "FUEL"))
        self.assertEqual(['C', 'A', 'B', 'ORE'], top_sort(g, "C"))

    def test_bfs(self):
        g = {'A': ['ORE'], 'C': ['B', 'A'], 'B': ['ORE'], 'E': ['D', 'A'], 'D': ['C', 'A'], 'FUEL': ['E', 'A']}
        self.assertEqual(['FUEL', 'A', 'ORE'], bfs(g, "FUEL", lambda x: x == "ORE"))

    def test_bfs_all_paths(self):
        g = {'A': ['ORE'], 'C': ['B', 'A'], 'B': ['ORE'], 'E': ['D', 'A'], 'D': ['C', 'A'], 'FUEL': ['E', 'A']}
        self.assertEqual([
            ['FUEL', 'A', 'ORE'],
            ['FUEL', 'E', 'A', 'ORE'],
            ['FUEL', 'E', 'D', 'A', 'ORE'],
            ['FUEL', 'E', 'D', 'C', 'B', 'ORE'],
            ['FUEL', 'E', 'D', 'C', 'A', 'ORE']
            ],
                bfs_all_paths(g, "FUEL", lambda x: x == "ORE"))

    def test_astar(self):
        maze = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        graph = maze_to_graph(maze, (0, 0), lambda _, __, ___, x: not x)

        self.assertEqual([(0, 0), (1, 1), (2, 2), (3, 3), (3, 4), (4, 5), (5, 4), (5, 3), (5, 2), (5, 1), (5, 0)], astar(graph, (0, 0), (5, 0)))

    def test_maze_to_graph(self):
        maze = [[0, 1, 0],
                [0, 0, 0],
                [0, 1, 0]]

        self.assertEqual({
            (0, 1): [(0, 0), (0, 2), (1, 1)],
            (0, 0): [(0, 1), (1, 1)],
            (2, 1): [(2, 0), (2, 2), (1, 1)],
            (1, 1): [(0, 1), (2, 1), (0, 0), (0, 2), (2, 0), (2, 2)],
            (2, 0): [(2, 1), (1, 1)],
            (2, 2): [(2, 1), (1, 1)],
            (0, 2): [(0, 1), (1, 1)]},
            maze_to_graph(maze, (0, 0), lambda _, __, ___, x: not x))

    def test_maze_to_graph(self):
        self.assertEqual((123455, 123456), binary_search(0, 10000000, lambda x: x >= 123456))


if __name__ == '__main__':
    unittest.main()
