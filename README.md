# Interactive Search and Sort Algorithms

This repository contains implementations of fundamental search and sort algorithms in Python with an interactive command-line interface.
Overview
This program provides Python implementations of common searching and sorting algorithms with a user-friendly interface that allows for customizable testing. Users can generate random test data and select specific algorithms to run, making it useful for both learning and algorithm comparison.
Features

## Interactive command-line menu system

Random test data generation (numbers and characters)
User-configurable list sizes
Execution time measurement for performance analysis
Clear organization of algorithm types

## Search Algorithms
The following search algorithms are implemented:

### Linear Search

Simple sequential search through an unsorted list
O(n) time complexity
Suitable for small lists or unsorted data


### Smart Search

Modified linear search that first sorts the list
Improves efficiency for certain use cases
Good balance between simplicity and performance


### Binary Search

Efficient search algorithm for sorted lists
O(log n) time complexity
Includes tracking of the number of comparisons made



## Sort Algorithms
The following sorting algorithms are implemented:

### Bubble Sort

Simple comparison-based sorting algorithm
O(n²) time complexity
Repeatedly compares adjacent elements and swaps them if needed


### Selection Sort

In-place comparison sort
O(n²) time complexity
Finds the maximum element and places it at the end in each pass


### Insertion Sort

Simple sorting algorithm that builds the final sorted array one item at a time
O(n²) time complexity in worst case, but efficient for small data sets


### Merge Sort

Efficient, stable, divide and conquer algorithm
O(n log n) time complexity
Divides the array into halves, sorts them recursively, and merges them


### Quick Sort

Efficient divide and conquer sorting algorithm
O(n log n) average time complexity
Uses a pivot element to partition the array



## Usage

### Run the program:
Copypython Algorithms.py

### Follow the interactive menu:

Choose between Search Algorithms or Sort Algorithms
Specify the size of the test data
Select a specific algorithm to run


### For search algorithms:

The program generates random numeric and character lists
You'll be prompted to enter target values to search for
Results show whether the target was found and its position
Some algorithms also display execution time


### For sort algorithms:

The program generates a random numeric list
The selected algorithm sorts the list
The sorted list is displayed



## Implementation Details

All algorithms are implemented from first principles without using Python's built-in sorting or searching functions
Random data generation uses Python's random and string modules
The program demonstrates basic algorithm analysis by measuring execution time for some operations
Includes both recursive implementations (Merge Sort, Quick Sort) and iterative implementations (other algorithms)

Author
Dimitri Montgomery
