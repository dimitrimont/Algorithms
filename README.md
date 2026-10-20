# Search and sort algorithms

Three searches and five sorts, written by hand in Python, behind a small menu that fills lists
with random numbers and characters to try them on. It was a class assignment in spring 2025, and
was revised in October 2026.

The tag `first-version` is the program as first uploaded.

## Run it

With Python 3.9 or later:

```bash
python Algorithms.py              # the menu
python Algorithms.py --seed 7     # the same random lists every time
python -m pip install pytest && python -m pytest tests   # 74 known-answer tests
python evaluation/compare.py      # both versions on the same 10,000 lists
```

The menu keeps going until you choose Exit, and asks again when you type something it can't use.

## The algorithms

Each search returns where it found the target, or `None`, and how many times it compared the
target with an item.

| Search | Needs a sorted list | Comparisons for n items |
| --- | --- | --- |
| Linear search | No | up to n |
| Smart search: a linear search that stops at the first item not smaller than the target | Yes | up to n, fewer when the target is missing |
| Binary search | Yes | about log2 n |

For smart and binary search, the menu sorts both lists first and shows you the sorted lists, so
the positions it prints are positions in lists on the screen. The time it prints covers the
search alone.

| Sort | Comparisons for n items | Notes |
| --- | --- | --- |
| Bubble sort | about n²/2 | |
| Selection sort | about n²/2 | Moves the largest remaining item to the end of each pass. |
| Insertion sort | about n²/4 on a random list | Fast on a list that is nearly sorted. |
| Merge sort | about n log2 n | Stable: equal items keep their order. |
| Quick sort | about n log2 n on average | Middle pivot, split three ways around it. |

## The first version against this one

From `python evaluation/compare.py`: 10,000 random lists of 10 numbers from 0 to 100, as the menu
makes them.

| Check | First version | This version |
| --- | --- | --- |
| Bubble sort: lists left out of order | 917 | 0 |
| Selection sort: lists left out of order | 8,914 | 0 |
| Insertion sort: lists left out of order | 0 | 0 |
| Merge sort: lists left out of order | 0 | 0 |
| Quick sort: lists left out of order | 9,630 | 0 |
| Smart search: missing numbers called found (of 9,035) | 8,147 | 0 |
| Smart search: position points at another number in the list shown | 8,998 | 0 |
| Binary search: position points at another number in the list shown | 8,998 | 0 |

What was wrong, and what changed:

- **The sort menu crashed before sorting.** It filled the list with `num`, a name that only the
  search menu defines, so every sort of one number or more stopped with a `NameError`. None of
  the five sorts ever ran from the menu. It now fills the list it means to.
- **Bubble sort skipped its last pass.** `range(n - 1, 1, -1)` stops at 2, so the first two items
  were never compared at the end: `[3, 2, 1]` came back `[2, 1, 3]`, and no two-item list was
  sorted. The range now runs down to 1.
- **Selection sort skipped a slot, and never looked at each slot's own item.** The search for the
  largest item stopped one place short, so a large item already in its slot was swapped away. An
  already sorted `0` to `9` came back `[0, 9, 1, 2, 3, 4, 5, 6, 7, 8]`, and lists of 100 were
  wrong 98% of the time. Both ranges now include the slot.
- **Quick sort crashed on its first small piece.** It returned `num_lst`, another name only the
  search menu defines, so the first call on a piece of one item stopped with a `NameError` and
  left the list part sorted. Fixing that alone wasn't enough: with the last item as the pivot, an
  already sorted list of 1,000, or 200,000 of the menu's numbers (many repeats), went deeper than
  Python allows. It now takes the middle item as the pivot, splits the items into less, equal and
  greater, and recurses into the smaller side only.
- **Smart search said it found numbers that weren't there.** It stopped at the first item not
  smaller than the target and reported `True` even when that item was a different number: 8,147
  of 9,035 missing numbers were "found". It now reports a find only when the item equals the
  target.
- **Positions pointed into a list nobody saw.** Smart and binary search sorted a copy and gave
  positions in the copy, while the menu showed the unsorted list. The menu now sorts first and
  shows that list.
- **"Smart" search was the slowest search.** Sorting first takes about n log2 n comparisons, so at
  1,000 items it made 9,171 comparisons to linear search's 565. It now expects a sorted list, as
  binary search does, and on the same sorted list it never makes more comparisons than linear
  search.
- **The time included the typing.** The clock started before the program asked for the target,
  so a two-second pause read as "Execute time: 2.2074s". It now times the search alone.
- **Merge sort wasn't stable.** On a tie it took the item from the right half. It now takes the
  left one, so equal items keep their order (the old README already said it was stable).
- **Searches printed instead of returning.** They returned the value of `print`, which is `None`,
  and linear search reported position `n` for a missing number. They now return the position or
  `None`, and the comparison count; the menu does the printing.
- **Any wrong key crashed the menu**, and it ran once per launch. It now loops, asks again, and
  stops cleanly when the input ends.

## The tests

`tests/test_algorithms.py` checks every sort against known answers (including empty lists, one
item, repeats and characters) and against 800 random lists each, quick sort on the lists that once
ran out of stack, merge sort's stability, each search's position and comparison count on known
lists, and the three searches against each other on 2,000 random lists. Four tests run the menu
as a separate program and type into it, including one that waits 1.5 seconds before typing and
checks that the printed time leaves the wait out.

## Author

Dimitri Montgomery
