"""
Runs the first version (the tag `first-version`) and this version on the same random lists and
writes what each got wrong to results/compare.md.

    python evaluation/compare.py

The first version's searches print their answers instead of returning them, so this reads what
they print. Its quick sort ends in a NameError; the list is checked as the error left it.
"""

import contextlib
import importlib.util
import io
import pathlib
import random
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
LISTS = 10_000


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def printed(f, *args):
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        f(*args)
    return out.getvalue().strip().splitlines()[-1]


def first_sorts(A):
    def quick(lst):
        try:
            A.quickSort(lst, 0, len(lst) - 1)
        except NameError:
            pass
        return lst
    return {"Bubble sort": lambda l: A.bubbleSort(l, len(l)), "Selection sort": lambda l: A.selectionSort(l, len(l)),
            "Insertion sort": lambda l: A.insertionSort(l, len(l)), "Merge sort": A.mergeSort, "Quick sort": quick}


def revised_sorts(A):
    return {"Bubble sort": A.bubbleSort, "Selection sort": A.selectionSort, "Insertion sort": A.insertionSort,
            "Merge sort": A.mergeSort, "Quick sort": A.quickSort}


def first_found(A, search, lst, target):
    """(said found, position) from what the first version printed; positions are in its sorted copy."""
    line = printed(search, lst, target, len(lst))
    found, rest = line.split(", ", 1)
    loc = rest.split(",")[0].replace("Loc = ", "")
    return found == "True", None if loc == "None" else int(loc)


def main():
    with tempfile.TemporaryDirectory() as tmp:
        first_path = pathlib.Path(tmp) / "first.py"
        first_path.write_text(subprocess.run(["git", "show", "first-version:Algorithms.py"], cwd=ROOT,
                                             capture_output=True, text=True, check=True).stdout)
        first, revised = load(first_path, "first"), load(ROOT / "Algorithms.py", "revised")

        rows = []
        rng = random.Random(331)
        lists = [[rng.randint(0, 100) for _ in range(10)] for _ in range(LISTS)]
        for (name, f1), f2 in zip(first_sorts(first).items(), revised_sorts(revised).values()):
            bad1 = sum(f1(l[:]) != sorted(l) for l in lists)
            bad2 = sum(f2(l[:]) != sorted(l) for l in lists)
            rows.append((f"{name}: lists left out of order", bad1, bad2))

        rng = random.Random(332)
        cases = []
        for _ in range(LISTS):
            lst = [rng.randint(0, 100) for _ in range(10)]
            cases.append((lst, rng.randint(0, 100)))
        missing = [(l, t) for l, t in cases if t not in l]
        said1 = sum(first_found(first, first.smart_search, l, t)[0] for l, t in missing)
        said2 = sum(revised.smart_search(sorted(l), t)[0] is not None for l, t in missing)
        rows.append((f"Smart search: missing numbers called found (of {len(missing):,})", said1, said2))

        # Every list here has distinct numbers, so a position names exactly one number.
        rng = random.Random(333)
        shown = [(l, rng.choice(l)) for l in (rng.sample(range(101), 10) for _ in range(LISTS))]
        for name in ("smart_search", "binary_search"):
            wrong1 = 0
            for lst, t in shown:
                _, loc = first_found(first, getattr(first, name), lst, t)
                wrong1 += loc is None or lst[loc] != t
            # The revised menu shows the sorted list, so its positions are checked in that list.
            wrong2 = 0
            for lst, t in shown:
                s = sorted(lst)
                loc, _ = getattr(revised, name)(s, t)
                wrong2 += loc is None or s[loc] != t
            label = name.replace("_", " ").capitalize()
            rows.append((f"{label}: position points at another number in the list shown (of {LISTS:,})", wrong1, wrong2))

        sweep = []
        for n in (100, 1000):
            lists = [rng.sample(range(10 * n), n) for _ in range(50)]
            lin = smart = 0
            for lst in lists:
                t = rng.choice(lst)
                lin += revised.linear_search(lst, t)[1]
                # the first version's own smart search, given numbers that count every comparison made,
                # including those of the sorted() it calls first
                Counted.n = 0
                printed(first.smart_search, [Counted(v) for v in lst], Counted(t), n)
                smart += Counted.n
            sweep.append((n, round(lin / len(lists)), round(smart / len(lists))))

    lines = ["# The first version against this one", "",
             f"{LISTS:,} random lists of 10 numbers from 0 to 100, as the menu makes them.", "",
             "| Check | First version | This version |", "| --- | --- | --- |"]
    lines += [f"| {label} | {a:,} | {b:,} |" for label, a, b in rows]
    lines += ["", "Comparisons to find a number that is in the list (50 lists each):", "",
              "| Items | Linear search | First version's smart search (sort, then scan) |", "| --- | --- | --- |"]
    lines += [f"| {n:,} | {lin:,} | {smart:,} |" for n, lin, smart in sweep]
    text = "\n".join(lines) + "\n"
    (ROOT / "results").mkdir(exist_ok=True)
    (ROOT / "results" / "compare.md").write_text(text)
    print(text)


class Counted:
    """A number that counts how many times it is compared."""
    n = 0

    def __init__(self, v):
        self.v = v

    def _other(self, o):
        Counted.n += 1
        return o.v if isinstance(o, Counted) else o

    def __lt__(self, o): return self.v < self._other(o)
    def __le__(self, o): return self.v <= self._other(o)
    def __gt__(self, o): return self.v > self._other(o)
    def __ge__(self, o): return self.v >= self._other(o)
    def __eq__(self, o): return self.v == self._other(o)
    def __ne__(self, o): return self.v != self._other(o)
    __hash__ = None


if __name__ == "__main__":
    sys.exit(main())
