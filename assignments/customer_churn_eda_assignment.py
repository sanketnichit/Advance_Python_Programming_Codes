"""Assignment 3: Explore, clean, analyze, and visualize customer churn data.

This creates a reproducible synthetic telecom-style dataset, injects data-quality
issues, explores and cleans the data, analyzes churn patterns, and saves CSV
outputs and four chart images in churn_eda_output/.

Run: python customer_churn_eda_assignment.py
Install dependencies: python -m pip install numpy pandas matplotlib
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUTPUT_DIR = Path("churn_eda_output")


def generate_churn_data(rows=1200, seed=37):
    """Generate synthetic customer records with intentional data-quality issues."""
    rng = np.random.default_rng(seed)
    contract = rng.choice(["Month-to-month", "One year", "Two year"], rows, p=[0.55, 0.23, 0.22])
    tenure = rng.integers(1, 73, size=rows)
    monthly_charges = np.round(rng.uniform(20, 120, size=rows), 2)
    internet = rng.choice(["DSL", "Fiber optic", "No"], rows, p=[0.36, 0.48, 0.16])
    gender = rng.choice(["Female", "Male"], rows)
    senior = rng.choice([0, 1], rows, p=[0.84, 0.16])

    # Churn probability is intentionally higher for month-to-month and short-tenure customers.
    probability = np.full(rows, 0.12)
    probability += np.where(contract == "Month-to-month", 0.36, 0.0)
    probability += np.where(tenure < 12, 0.18, 0.0)
    probability += np.where(internet == "Fiber optic", 0.05, 0.0)
    churn = np.where(rng.random(rows) < np.clip(probability, 0.03, 0.88), "Yes", "No")

    df = pd.DataFrame({
        "CustomerID": [f"C{number:05d}" for number in range(1, rows + 1)],
        "Gender": gender,
        "SeniorCitizen": senior,
        "Contract": contract,
        "InternetService": internet,
        "Tenure": tenure,
        "MonthlyCharges": monthly_charges,
        "TotalCharges": np.round(tenure * monthly_charges, 2).astype(str),
        "Churn": churn,
    })

    for column, count in [("Tenure", 12), ("InternetService", 10), ("TotalCharges", 18)]:
        positions = rng.choice(df.index, size=count, replace=False)
        df.loc[positions, column] = np.nan

    bad_positions = rng.choice(df.index, size=8, replace=False)
    df.loc[bad_positions, "TotalCharges"] = "not recorded"

    for position in rng.choice(df.index, size=25, replace=False):
        df.loc[position, "Churn"] = " Yes " if df.loc[position, "Churn"] == "Yes" else " no "
    for position in rng.choice(df.index, size=18, replace=False):
        df.loc[position, "InternetService"] = " Fiber optic "

    # Add exact duplicate customer rows to make duplicate removal demonstrable.
    df = pd.concat([df, df.iloc[:15]], ignore_index=True)
    return df


def explore_data(df, title):
    print(f"\n{'=' * 65}\n{title}\n{'=' * 65}")
    print("Rows and columns:", df.shape)
    print("\nColumn data types:\n", df.dtypes.to_string())
    print("\nMissing values by column:\n", df.isna().sum().to_string())
    print("\nExact duplicate rows:", int(df.duplicated().sum()))
    print("\nSummary statistics:")
    print(df.describe(include="all").to_string())


def clean_data(raw):
    """Clean a copy of the data while preserving the raw DataFrame."""
    clean = raw.copy()

    for column in ["Gender", "Contract", "InternetService", "Churn"]:
        clean[column] = clean[column].astype("string").str.strip()

    clean["Gender"] = clean["Gender"].str.title()
    clean["Churn"] = clean["Churn"].str.title()
    clean["InternetService"] = clean["InternetService"].str.title()
    clean["Contract"] = clean["Contract"].replace({"One Year": "One year", "Two Year": "Two year"})

    for column in ["SeniorCitizen", "Tenure", "MonthlyCharges", "TotalCharges"]:
        clean[column] = pd.to_numeric(clean[column], errors="coerce")

    initial_count = len(clean)
    clean = clean.drop_duplicates().copy()
    print(f"\nRemoved duplicate rows: {initial_count - len(clean)}")

    for column in ["SeniorCitizen", "Tenure", "MonthlyCharges", "TotalCharges"]:
        if clean[column].isna().any():
            median = clean[column].median()
            clean[column] = clean[column].fillna(median if pd.notna(median) else 0)

    for column in ["Gender", "Contract", "InternetService", "Churn"]:
        if clean[column].isna().any():
            modes = clean[column].mode(dropna=True)
            replacement = modes.iloc[0] if not modes.empty else "Unknown"
            clean[column] = clean[column].fillna(replacement)

    clean["SeniorCitizen"] = clean["SeniorCitizen"].round().astype(int)
    clean["Tenure"] = clean["Tenure"].round().astype(int)
    return clean


def analyze_patterns(df):
    print("\n" + "=" * 65 + "\nCHURN PATTERN ANALYSIS\n" + "=" * 65)
    print(f"Overall churn rate: {df['Churn'].eq('Yes').mean() * 100:.2f}%")

    churn_flag = df["Churn"].eq("Yes").astype(int)
    for column in ["Contract", "InternetService"]:
        rates = df.assign(_churn=churn_flag).groupby(column, observed=False)["_churn"].mean().mul(100)
        print(f"\nChurn rate by {column} (%):\n{rates.round(2).to_string()}")

    print("\nAverage tenure by churn status:\n", df.groupby("Churn", observed=False)["Tenure"].mean().round(2).to_string())
    print("\nAverage monthly charges by churn status:\n", df.groupby("Churn", observed=False)["MonthlyCharges"].mean().round(2).to_string())
    numeric = df[["SeniorCitizen", "Tenure", "MonthlyCharges", "TotalCharges"]]
    print("\nCorrelation between numeric features:\n", numeric.corr().round(2).to_string())


def create_charts(df, output_dir=OUTPUT_DIR):
    """Save the four visualizations described in the lab manual."""
    output_dir.mkdir(parents=True, exist_ok=True)

    counts = df["Churn"].value_counts().reindex(["No", "Yes"], fill_value=0)
    fig, ax = plt.subplots(figsize=(7, 4.5))
    counts.plot(kind="bar", ax=ax)
    ax.set(title="Overall Churn Distribution", xlabel="Churn", ylabel="Number of Customers")
    ax.tick_params(axis="x", rotation=0)
    fig.tight_layout()
    fig.savefig(output_dir / "01_churn_distribution.png", dpi=150)
    plt.close(fig)

    rate = df.assign(_churn=df["Churn"].eq("Yes").astype(int)).groupby("Contract", observed=False)["_churn"].mean().mul(100)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    rate.plot(kind="bar", ax=ax)
    ax.set(title="Churn Rate by Contract Type", xlabel="Contract", ylabel="Churn Rate (%)")
    ax.tick_params(axis="x", rotation=15)
    fig.tight_layout()
    fig.savefig(output_dir / "02_churn_by_contract.png", dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 4.5))
    for label in ["No", "Yes"]:
        ax.hist(df.loc[df["Churn"] == label, "Tenure"], bins=18, alpha=0.6, label=f"Churn = {label}")
    ax.set(title="Tenure Distribution by Churn Status", xlabel="Tenure (months)", ylabel="Number of Customers")
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_dir / "03_tenure_by_churn.png", dpi=150)
    plt.close(fig)

    numeric = df[["SeniorCitizen", "Tenure", "MonthlyCharges", "TotalCharges"]].corr()
    fig, ax = plt.subplots(figsize=(6.5, 5.5))
    image = ax.imshow(numeric, vmin=-1, vmax=1, cmap="coolwarm")
    ax.set_xticks(range(len(numeric.columns)), numeric.columns, rotation=35, ha="right")
    ax.set_yticks(range(len(numeric.columns)), numeric.columns)
    for row in range(len(numeric.columns)):
        for col in range(len(numeric.columns)):
            ax.text(col, row, f"{numeric.iloc[row, col]:.2f}", ha="center", va="center", fontsize=9)
    ax.set_title("Correlation Between Numeric Features")
    fig.colorbar(image, ax=ax, label="Correlation")
    fig.tight_layout()
    fig.savefig(output_dir / "04_numeric_correlation.png", dpi=150)
    plt.close(fig)
    print(f"\nSaved four charts to: {output_dir.resolve()}")


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    raw_data = generate_churn_data()
    raw_path = OUTPUT_DIR / "customer_churn_raw.csv"
    raw_data.to_csv(raw_path, index=False)
    explore_data(raw_data, "RAW DATA EXPLORATION")

    cleaned_data = clean_data(raw_data)
    cleaned_path = OUTPUT_DIR / "customer_churn_cleaned.csv"
    cleaned_data.to_csv(cleaned_path, index=False)
    explore_data(cleaned_data, "CLEANED DATA CHECK")
    print("\nMissing values remaining:", int(cleaned_data.isna().sum().sum()))
    print("Duplicate rows remaining:", int(cleaned_data.duplicated().sum()))

    analyze_patterns(cleaned_data)
    create_charts(cleaned_data)
    print(f"Raw CSV     : {raw_path.resolve()}")
    print(f"Cleaned CSV : {cleaned_path.resolve()}")
    print("\nConclusion: EDA identifies data issues before cleaning and helps reveal churn patterns.")
    print("Note: This is synthetic practice data, not real customer records.")


if __name__ == "__main__":
    main()
