import time
import random as r
import string


def linear_search(lst, target, n):
    found = False
    loc = 0

    print(lst)

    while loc < n and not found:
        if target == lst[loc]:
            found = True
        else:
            loc += 1
    return print(f"{found}, {loc}")

def smart_search(lst, target, n):
    slst = sorted(lst)
    found = False
    loc = 0

    while loc < n and not found:
        if target <= slst[loc]:
            found = True
        else:
            loc += 1

    if loc == n or target != slst[loc]:
        loc = None
    return print(f"{found}, {loc}")

def binary_search(lst, target, n):
    slst = sorted(lst)
    found = False
    first = 0
    last = n - 1
    num_srchs = 0

    while first <= last and not found:
        mid = (first + last) // 2
        if target < slst[mid]:
            last = mid - 1
            num_srchs += 1
        elif target > slst[mid]:
            first = mid + 1
            num_srchs += 1
        else:
            found = True
            num_srchs += 1

    if not found:
        mid = None
    return print(f"{found}, Loc = {mid}, searches = {num_srchs}")

# ==================================================================================================================================================================


def bubbleSort(lst, length):
    n = length
    for pass_remaining in range(n - 1, 1, - 1):
        for j in range(0, pass_remaining):
            if lst[j + 1] < lst[j]:
                lst[j], lst[j + 1] = lst[j + 1], lst[j]

    return lst

def selectionSort(lst, length):
    n = length
    for fill_slot in range(n - 1, 1, -1):
        pos_of_max = 0
        for j in range(1, fill_slot):
            if lst[pos_of_max] < lst[j]:
                pos_of_max = j
        lst[fill_slot], lst[pos_of_max] = lst[pos_of_max], lst[fill_slot]

    return lst

def insertionSort(lst, length):
    n = length
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

    while i < len(left) and j < len(right):
        if left[i] < right[j]:
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

def quickSort(array, low, high):
    if low < high:
        piv = partition(array, low, high)

        quickSort(array, low, piv - 1)

        quickSort(array, piv + 1, high)
    return num_lst

def partition(array, low, high):
    pivot = array[high]

    i = low - 1

    for j in range(low, high):
        if array[j] <= pivot:
            i = i + 1
            (array[i], array[j]) = (array[j], array[i])

    (array[i + 1], array[high]) = (array[high], array[i + 1])

    return i + 1
# ==================================================================================================================================================================



if __name__ == "__main__":

    #Search Algorithms
    print("What algorithm type would you like to use\n1. Search Algorithms\n2. Sort Algorithms\n3. Exit")
    user_input_alg_type = int(input("Enter what algorithm you would like to use(1-3): "))
    print()
    if user_input_alg_type == 1:

        num_lst = []
        print("How many numbers do you want in your numbers lst")
        num_lst_input = int(input("Enter number of elements wanted in number list: "))
        print()
        for i in range(1, num_lst_input + 1):
            num = r.randint(0, 100)
            num_lst.append(num)

        char_lst = []
        print("How many characters do you want in your numbers list: ")
        char_lst_input = int(input("Enter number of elements wanted in character list: "))
        print()
        characters = string.ascii_letters + string.digits + string.punctuation
        for i in range(1, char_lst_input + 1):
            char = r.choice(characters)
            char_lst.append(char)

        n_numbers = len(num_lst)
        n_characters = len(char_lst)

        print("What search algorithm would you like to use\n1. Linear Search\n2. Smart Search\n3. Binary Search\n4. Exit")
        alg_input = int(input("Enter what algorithm you would like to use(1-4): "))

        if alg_input == 1:
            print(num_lst)
            print(char_lst)
            print("Choose a integer and then a character to search in the list(linear search)\nInteger: ")
            start = time.time()
            linear_search(num_lst, int(input("Enter: ")), n_numbers)
            seq_time = time.time() - start
            print(f"Execute time: {seq_time: .4f}s")

            print("\nCharacter")
            linear_search(char_lst, str(input("Enter: ")), n_characters)
            print("\n")
        elif alg_input == 2:
            print(num_lst)
            print(char_lst)
            print("Choose a integer to search in the list(smart search)")
            start = time.time()
            smart_search(num_lst, int(input("Enter: ")), n_numbers)
            smrt_time = time.time() - start
            print(f"Execute time: {smrt_time: .4f}s")
            print("\n")
        elif alg_input == 3:
            print(num_lst)
            print(char_lst)
            print("Choose a integer and then a character to search in the list(binary search)\nInteger: ")
            binary_search(num_lst, int(input("Enter: ")), n_numbers)

            print("Character: ")
            binary_search(char_lst, str(input("Enter: ")), n_characters)
        else:
            print()
    elif user_input_alg_type == 2:

        #Sort Algorithms
        num_lst2 = []
        print("How many numbers do you want in your numbers lst")
        num_lst_input = int(input("Enter number of elements wanted in number list: "))
        for i in range(1, num_lst_input + 1):
            num2 = r.randint(0, 100)
            num_lst2.append(num)

        #num_lst2 = [5, 76, 24, 2, 46, 43, 13, 8, 31, 92, 23, 6, 73, 0, 90]
        length = len(num_lst2)
        print(f"Original list: {num_lst2}\n List length: {length}\n")


        print("What search algorithm would you like to use\n1. Bubble Sort\n2. Selection Sort\n3. Insertion Sort\n4. Merge Sort\n 5. Quick Sort\n6. Exit")
        sort_alg_input = int(input("Enter what algorithm you would like to use(1-6): "))

        if sort_alg_input == 1:
            print("Bubble sorted list:\n")
            print(bubbleSort(num_lst2, length))
        elif sort_alg_input == 2:
            print("\nSelection sorted list:\n")
            print(selectionSort(num_lst2, length))
        elif sort_alg_input == 3:
            print("\nInsertion sorted list:\n")
            print(insertionSort(num_lst2, length))
        elif sort_alg_input == 4:
            print("\nMerge sorted list:\n")
            print(mergeSort(num_lst2))
        elif sort_alg_input == 5:
            print("\nQuick sorted list:\n")
            print(quickSort(num_lst2, 0, length - 1))
        else:
            print()
    else:
        print()