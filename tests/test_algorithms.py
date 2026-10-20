"""
Known answers for every sort and search, and runs of the menu as a person would use it.

Run with `python -m pytest tests`.
"""

import functools
import pathlib
import random
import re
import subprocess
import sys
import time

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import Algorithms as A  # noqa: E402

SORTS = {"bubble": A.bubbleSort, "selection": A.selectionSort, "insertion": A.insertionSort,
         "merge": A.mergeSort, "quick": A.quickSort}


@pytest.mark.parametrize("name", SORTS)
@pytest.mark.parametrize("given, expected", [
    ([3, 2, 1], [1, 2, 3]),
    ([2, 1], [1, 2]),
    ([1, 2, 3], [1, 2, 3]),
    (list(range(10)), list(range(10))),
    ([], []),
    ([7], [7]),
    ([5, 1, 5, 0, 1, 5], [0, 1, 1, 5, 5, 5]),
    (list("hello"), list("ehllo")),
])
def test_sort_known_answers(name, given, expected):
    lst = given[:]
    assert SORTS[name](lst) == expected
    assert lst == expected  # in place


@pytest.mark.parametrize("name", SORTS)
def test_sorts_random_lists_like_the_menu(name):
    rng = random.Random(331)
    for n in (2, 3, 10, 100):
        for _ in range(200):
            lst = [rng.randint(0, 100) for _ in range(n)]
            assert SORTS[name](lst[:]) == sorted(lst)


@functools.total_ordering
class Card:
    """Compares by number only, so equal numbers can be told apart by their tag."""
    def __init__(self, number, tag):
        self.number, self.tag = number, tag
    def __eq__(self, other):
        return self.number == other.number
    def __lt__(self, other):
        return self.number < other.number


def test_merge_sort_is_stable():
    cards = [Card(n, tag) for tag, n in enumerate([3, 1, 3, 2, 1, 3])]
    out = A.mergeSort(cards)
    assert [(c.number, c.tag) for c in out] == [(1, 1), (1, 4), (2, 3), (3, 0), (3, 2), (3, 5)]


@pytest.mark.parametrize("lst", [list(range(5000)), list(range(5000, 0, -1)),
                                 [random.Random(2).randint(0, 100) for _ in range(200_000)]],
                         ids=["sorted 5,000", "reversed 5,000", "menu numbers 200,000"])
def test_quick_sort_inputs_that_once_ran_out_of_stack(lst):
    expected = sorted(lst)
    assert A.quickSort(lst) == expected


@pytest.mark.parametrize("lst, target, expected", [
    ([30, 10, 20], 30, (0, 1)),
    ([30, 10, 20], 20, (2, 3)),
    ([30, 10, 20], 99, (None, 3)),
    ([], 5, (None, 0)),
    (list("abc"), "c", (2, 3)),
])
def test_linear_search(lst, target, expected):
    assert A.linear_search(lst, target) == expected


@pytest.mark.parametrize("slst, target, expected", [
    ([10, 20], 15, (None, 2)),      # stops at 20 without finding 15
    ([10, 20, 30], 20, (1, 2)),
    ([10, 20, 30], 99, (None, 3)),
    ([10, 20, 30], 5, (None, 1)),
    (list("abc"), "b", (1, 2)),
])
def test_smart_search(slst, target, expected):
    assert A.smart_search(slst, target) == expected


@pytest.mark.parametrize("slst, target, expected", [
    ([10, 20, 30], 30, (2, 2)),
    ([10, 20, 30], 20, (1, 1)),
    ([10, 20, 30], 15, (None, 2)),
    (list(range(0, 2000, 2)), 1000, (500, 9)),
    ([], 1, (None, 0)),
])
def test_binary_search(slst, target, expected):
    assert A.binary_search(slst, target) == expected


def test_searches_agree_on_random_lists():
    rng = random.Random(7)
    for _ in range(2000):
        lst = [rng.randint(0, 100) for _ in range(rng.randint(0, 30))]
        target = rng.randint(0, 100)
        slst = sorted(lst)
        loc, _ = A.linear_search(lst, target)
        assert (loc is not None) == (target in lst) and (loc is None or lst[loc] == target)
        for search in (A.smart_search, A.binary_search):
            loc, _ = search(slst, target)
            assert (loc is not None) == (target in slst) and (loc is None or slst[loc] == target)


def test_smart_search_makes_no_more_comparisons_than_linear_on_the_same_sorted_list():
    rng = random.Random(9)
    for _ in range(500):
        slst = sorted(rng.randint(0, 100) for _ in range(50))
        target = rng.randint(0, 100)
        assert A.smart_search(slst, target)[1] <= A.linear_search(slst, target)[1]


# ---- the menu, run as a separate program -------------------------------------------------------

def run(lines, pause=None):
    """Types lines into the program; with pause=(i, s), waits s seconds before line i."""
    p = subprocess.Popen([sys.executable, "Algorithms.py", "--seed", "1"], cwd=ROOT, text=True,
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for i, line in enumerate(lines):
        if pause and pause[0] == i:
            time.sleep(pause[1])
        p.stdin.write(line + "\n")
        p.stdin.flush()
    out, _ = p.communicate(timeout=60)
    return p.returncode, out


@pytest.mark.parametrize("choice", ["1", "2", "3", "4", "5"])
def test_menu_sorts_every_algorithm(choice):
    code, out = run(["2", "25", choice, "3"])
    assert code == 0, out
    sorted_line = out.split("sorted list:\n")[1].splitlines()[0]
    numbers = [int(x) for x in re.findall(r"\d+", sorted_line)]
    assert len(numbers) == 25 and numbers == sorted(numbers)


def test_menu_smart_search_shows_the_sorted_list_and_reports_a_missing_number():
    code, out = run(["1", "20", "20", "2", "101", "50", "~", "3"])
    assert code == 0, out
    numbers = [int(x) for x in re.findall(r"\d+", out.split("Numbers: ")[1].splitlines()[0])]
    assert numbers == sorted(numbers)
    assert "Expected a whole number from 0 to 100." in out  # 101 was asked again
    line = next(l for l in out.splitlines() if "Smart search: 50 " in l)
    assert ("not in the list" in line) == (50 not in numbers)
    if 50 in numbers:
        assert numbers[int(re.search(r"position (\d+)", line)[1])] == 50


def test_menu_survives_bad_input_and_the_end_of_input():
    code, out = run(["two", "9", "2", "x"])
    assert code == 0, out
    assert out.count("Expected a whole number from 1 to 3.") == 2
    assert "Traceback" not in out and out.rstrip().endswith("The input ended.")


def test_menu_time_leaves_out_the_typing():
    code, out = run(["1", "10", "10", "1", "50", "a", "3"], pause=(4, 1.5))
    assert code == 0, out
    times = [float(t) for t in re.findall(r"\(([\d.]+) microseconds\)", out)]
    assert len(times) == 2 and max(times) < 100_000  # under 0.1 s, though 1.5 s passed before typing
