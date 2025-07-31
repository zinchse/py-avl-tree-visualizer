import random, math
from typing import List
from sortedcollections import SortedList
from AVLTree import AVLTree


def random_unique_list(length: "int") -> "List[int]":
    seen = set()
    res = []
    for i in range(length):
        x = random.randint(1, length)
        if x not in seen:
            res.append(x)
            seen.add(x)
    return res


def test_kth(length: "int" = 10_000, n_removals: "int" = 1_000, max_int: "int" = 10_000) -> "None":
    lst = SortedList(random_unique_list(length))
    tree = AVLTree(lst)

    for k in range(1, len(lst) + 1):
        assert tree.findkth(k).key == lst[k - 1], f"Wrong {k}-th statistics (before removals)!"

    for _ in range(n_removals):
        x = random.randint(1, max_int)
        lst.discard(x)
        tree.remove(x)

    for k in range(1, len(lst) + 1):
        assert tree.findkth(k).key == lst[k - 1], f"Wrong {k}-th statistic (after removals)!"


def test_treesize(length: "int" = 1_000_000) -> "None":
    tree = AVLTree()
    for x in random_unique_list(length):
        tree.insert(x)
    assert tree.height() < 1.44 * math.log(length + 2, 2) - 1, f"Height is too big!"


if __name__ == "__main__":
    test_kth()
    print("OK. Search for kth statistics functions correctly!")
    test_treesize()
    print("OK. Tree's size doesn't explode!")
