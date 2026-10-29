"""Assignment 2: Create a Pandas Series containing ten random numbers.

Run: python pandas_series_assignment.py
Install dependencies: python -m pip install numpy pandas
"""
import numpy as np
import pandas as pd


def make_random_series(count=10, seed=24):
    """Return reproducible random integers from 1 through 99 as a Series."""
    generator = np.random.default_rng(seed)
    numbers = generator.integers(1, 100, size=count)
    return pd.Series(numbers, name="Value")


def add_readable_labels(values):
    """Return the values with meaningful index labels instead of 0, 1, 2..."""
    labels = [f"number_{position}" for position in range(1, len(values) + 1)]
    return pd.Series(values.to_numpy(), index=labels, name="Value")


def show_series_info(values, title):
    print(f"\n{title}")
    print(values)
    print("Data type :", values.dtype)
    print("Shape     :", values.shape)
    print("Size      :", values.size)
    print("Index     :", list(values.index))


def main():
    numbers = make_random_series()
    labeled_numbers = add_readable_labels(numbers)

    show_series_info(numbers, "STEP 1 - Series with default index")
    show_series_info(labeled_numbers, "STEP 2 - Same values with custom labels")

    print("\nSTEP 3 - Basic statistics")
    print("Minimum :", numbers.min())
    print("Maximum :", numbers.max())
    print("Mean    :", round(numbers.mean(), 2))
    print("Sum     :", numbers.sum())

    print("\nSTEP 4 - Values sorted in ascending order (original labels remain attached)")
    print(numbers.sort_values().to_string())

    print("\nSTEP 5 - Access and filter")
    print("First value by position (.iloc[0]):", numbers.iloc[0])
    print("Values greater than 50:")
    filtered = numbers[numbers > 50]
    print(filtered.to_string() if not filtered.empty else "No values greater than 50.")

    print("\nConclusion: A Pandas Series stores values with index labels and supports statistics, sorting, and filtering.")


if __name__ == "__main__":
    main()
