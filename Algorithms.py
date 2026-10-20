"""
Search and sort algorithms, written by hand, behind a small menu.

Searches return (position, comparisons): the position of the target in the list they were
given, or None if it isn't there, and how many times the target was compared with an item.
Smart search and binary search need a sorted list; the menu sorts the list first and shows
the sorted list, so every position it prints is a position in a list on the screen.

Sorts put the list in order in place and also return it.

Run it with `python Algorithms.py`, or `python Algorithms.py --seed 7` for the same random
lists every time.
"""

import random as r
import string
import sys
import time


def linear_search(lst, target):
    comparisons = 0
    for loc in range(len(lst)):
        comparisons += 1
        if lst[loc] == target:
            return loc, comparisons
    return None, comparisons


def smart_search(slst, target):
    """Linear search of a sorted list that stops at the first item not smaller than the target."""
    comparisons = 0
    for loc in range(len(slst)):
        comparisons += 1
        if slst[loc] >= target:
            return (loc if slst[loc] == target else None), comparisons
    return None, comparisons


def binary_search(slst, target):
    """Binary search of a sorted list."""
    first = 0
    last = len(slst) - 1
    num_srchs = 0

    while first <= last:
        mid = (first + last) // 2
        num_srchs += 1
        if target < slst[mid]:
            last = mid - 1
        elif target > slst[mid]:
            first = mid + 1
        else:
            return mid, num_srchs
    return None, num_srchs

# ==================================================================================================================================================================


def bubbleSort(lst, length=None):
    n = len(lst) if length is None else length
    for pass_remaining in range(n - 1, 0, -1):
        for j in range(0, pass_remaining):
            if lst[j + 1] < lst[j]:
                lst[j], lst[j + 1] = lst[j + 1], lst[j]

    return lst

def selectionSort(lst, length=None):
    n = len(lst) if length is None else length
    for fill_slot in range(n - 1, 0, -1):
        pos_of_max = 0
        for j in range(1, fill_slot + 1):
            if lst[pos_of_max] < lst[j]:
                pos_of_max = j
        lst[fill_slot], lst[pos_of_max] = lst[pos_of_max], lst[fill_slot]

    return lst

def insertionSort(lst, length=None):
    n = len(lst) if length is None else length
    for i in range(1, n):
        next_elm = lst[i]
        pos = i
        while pos > 0 and lst[pos - 1] > next_elm:
            lst[pos] = lst[pos - 1]
            pos -= 1
        lst[pos] = next_elm

    return lst

def mergeSort(lst):
    n = len(lst)

    if n <= 1:
        return lst
    else:
        mid = n // 2
        left = mergeSort(lst[0:mid])
        right = mergeSort(lst[mid:n])

    i = j = k = 0

    # <= takes the left item on a tie, so equal items keep their order (a stable sort)
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            lst[k] = left[i]
            i += 1
        else:
            lst[k] = right[j]
            j += 1
        k += 1

    while i < len(left):
        lst[k] = left[i]
        i += 1
        k += 1

    while j < len(right):
        lst[k] = right[j]
        j += 1
        k += 1

    return lst

def quickSort(array, low=0, high=None):
    """
    Sorts array[low..high]. The pivot is the middle item, and each partition splits the
    items into less than, equal to, and greater than the pivot, so a sorted list or a list
    with many repeated numbers doesn't make it slow. It recurses into the smaller part and
    loops on the larger, so it never goes more than about log2(n) calls deep.
    """
    if high is None:
        high = len(array) - 1
    while low < high:
        lt, gt = partition(array, low, high)
        if lt - low < high - gt:
            quickSort(array, low, lt - 1)
            low = gt + 1
        else:
            quickSort(array, gt + 1, high)
            high = lt - 1
    return array

def partition(array, low, high):
    """Returns (lt, gt): afterwards array[lt..gt] all equal the pivot, smaller items are before, larger after."""
    pivot = array[(low + high) // 2]
    lt, i, gt = low, low, high
    while i <= gt:
        if array[i] < pivot:
            array[lt], array[i] = array[i], array[lt]
            lt += 1
            i += 1
        elif array[i] > pivot:
            array[i], array[gt] = array[gt], array[i]
            gt -= 1
        else:
            i += 1
    return lt, gt
# ==================================================================================================================================================================


SEARCHES = {1: ("Linear search", linear_search), 2: ("Smart search", smart_search), 3: ("Binary search", binary_search)}
SORTS = {1: ("Bubble sort", bubbleSort), 2: ("Selection sort", selectionSort), 3: ("Insertion sort", insertionSort),
         4: ("Merge sort", mergeSort), 5: ("Quick sort", quickSort)}


class InputEnded(Exception):
    pass


def ask(prompt):
    try:
        return input(prompt).strip()
    except EOFError:
        print()
        raise InputEnded


def ask_int(prompt, lo, hi):
    while True:
        s = ask(prompt)
        try:
            n = int(s)
            if lo <= n <= hi:
                return n
        except ValueError:
            pass
        print(f"Expected a whole number from {lo} to {hi}.")


def ask_char(prompt):
    while True:
        s = ask(prompt)
        if len(s) == 1:
            return s
        print("Expected one character.")


def show_search(name, search, lst, target):
    start = time.perf_counter()
    loc, comparisons = search(lst, target)
    took = time.perf_counter() - start
    where = f"found at position {loc}" if loc is not None else "not in the list"
    print(f"{name}: {target!r} {where}, after {comparisons} comparison{'s' * (comparisons != 1)} ({took * 1e6:.1f} microseconds)")


def search_menu():
    n_numbers = ask_int("Enter number of elements wanted in number list (1-100000): ", 1, 100_000)
    num_lst = [r.randint(0, 100) for _ in range(n_numbers)]
    n_characters = ask_int("Enter number of elements wanted in character list (1-100000): ", 1, 100_000)
    characters = string.ascii_letters + string.digits + string.punctuation
    char_lst = [r.choice(characters) for _ in range(n_characters)]

    print("\nWhat search algorithm would you like to use\n1. Linear Search\n2. Smart Search\n3. Binary Search\n4. Back")
    choice = ask_int("Enter what algorithm you would like to use(1-4): ", 1, 4)
    if choice == 4:
        return
    name, search = SEARCHES[choice]
    if search is not linear_search:
        # Smart and binary search need a sorted list, so sort it first and show that list.
        num_lst = mergeSort(num_lst)
        char_lst = mergeSort(char_lst)
        print("Both lists are sorted first, and positions count from 0 in the sorted lists.")
    print(f"\nNumbers: {num_lst}\nCharacters: {char_lst}\n")
    show_search(name, search, num_lst, ask_int("Choose an integer to search for (0-100): ", 0, 100))
    show_search(name, search, char_lst, ask_char("Choose a character to search for: "))


def sort_menu():
    n = ask_int("Enter number of elements wanted in number list (1-100000): ", 1, 100_000)
    num_lst2 = [r.randint(0, 100) for _ in range(n)]
    print(f"Original list: {num_lst2}\n List length: {n}\n")

    print("What sort algorithm would you like to use\n1. Bubble Sort\n2. Selection Sort\n3. Insertion Sort\n4. Merge Sort\n5. Quick Sort\n6. Back")
    choice = ask_int("Enter what algorithm you would like to use(1-6): ", 1, 6)
    if choice == 6:
        return
    name, sort = SORTS[choice]
    if choice <= 3 and n > 5000:
        print(f"{name} makes about {n * n // 2:,} comparisons on {n:,} numbers, so this may take a while.")
    start = time.perf_counter()
    sort(num_lst2)
    took = time.perf_counter() - start
    print(f"\n{name}ed list:\n{num_lst2}\n({took:.4f} s)")


def main(argv):
    if "--seed" in argv:
        r.seed(int(argv[argv.index("--seed") + 1]))
    try:
        while True:
            print("\nWhat algorithm type would you like to use\n1. Search Algorithms\n2. Sort Algorithms\n3. Exit")
            choice = ask_int("Enter what algorithm you would like to use(1-3): ", 1, 3)
            print()
            if choice == 1:
                search_menu()
            elif choice == 2:
                sort_menu()
            else:
                return
    except InputEnded:
        print("The input ended.")


if __name__ == "__main__":
    main(sys.argv[1:])
