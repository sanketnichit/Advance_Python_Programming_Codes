# Advance Python Programming — Lab Assignments

These original Python scripts follow the practical goals in the three supplied lab manuals.

## Assignments

1. **`numpy_array_assignment.py`** — creates values 1–10 using `np.array()` and `np.arange()`; prints `dtype`, `shape`, `ndim`, and `size`; compares the arrays; demonstrates vectorized operations, indexing, and slicing.
2. **`pandas_series_assignment.py`** — creates a reproducible Series of ten random integers; demonstrates a default index and custom labels; prints attributes and summary statistics; sorts and filters the values.
3. **`customer_churn_eda_assignment.py`** — generates a reproducible synthetic churn dataset with intentional quality issues; explores and cleans it; summarizes churn patterns and correlations; saves raw/cleaned CSV files and four charts.

## Setup

Python 3.8+ is recommended. Install the dependencies once:

```bash
python -m pip install numpy pandas matplotlib
```

Run from this directory:

```bash
python numpy_array_assignment.py
python pandas_series_assignment.py
python customer_churn_eda_assignment.py
```

The first two scripts print results to the terminal. The third saves CSV files and PNG charts in `churn_eda_output/`.

**Note:** The churn dataset is synthetically generated for practice; it is not real customer data.
