"""Assignment 1: Create and explore a one-dimensional NumPy array (1 to 10).

Run: python numpy_array_assignment.py
Install dependency: python -m pip install numpy
"""
import numpy as np


def build_array_from_list():
    """Create the required array from an explicit Python list."""
    return np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])


def build_array_with_range():
    """Generate the same sequence; the stop value (11) is excluded."""
    return np.arange(1, 11)


def show_array_details(values, heading):
    """Display the array and attributes requested in the lab manual."""
    print(f"\n{heading}")
    print("Array          :", values)
    print("Data type      :", values.dtype)
    print("Shape          :", values.shape)
    print("Dimensions     :", values.ndim)
    print("Number of items:", values.size)


def main():
    array_from_list = build_array_from_list()
    array_from_range = build_array_with_range()

    show_array_details(array_from_list, "METHOD 1 - np.array()")
    show_array_details(array_from_range, "METHOD 2 - np.arange()")

    print("\nDo both methods give the same array?", np.array_equal(array_from_list, array_from_range))
    print("\nVectorized operations")
    print("Each value doubled :", array_from_list * 2)
    print("Each value plus 100:", array_from_list + 100)
    print("Sum                :", array_from_list.sum())
    print("Mean               :", array_from_list.mean())

    print("\nIndexing and slicing")
    print("First element      :", array_from_list[0])
    print("Last element       :", array_from_list[-1])
    print("First five elements:", array_from_list[:5])
    print("Every second value :", array_from_list[::2])

    print("\nConclusion: NumPy arrays support convenient vectorized numerical operations and expose useful attributes.")


if __name__ == "__main__":
    main()
