
import pandas as pd


REQUIRED_COLUMNS = [
    "Date",
    "Description",
    "Amount",
    "Category"
]


def load_transactions(uploaded_file):
    """
    Load transactions from a CSV file.
    """

    df = pd.read_csv(uploaded_file)

    # Check required columns
    missing_columns = [
        col for col in REQUIRED_COLUMNS
        if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing columns: {missing_columns}"
        )

    # Convert data types
    df["Date"] = pd.to_datetime(
        df["Date"],
        errors="coerce"
    )

    df["Amount"] = pd.to_numeric(
        df["Amount"],
        errors="coerce"
    )

    df["Category"] = (
        df["Category"]
        .astype("string")
        .str.strip()
    )

    # Remove invalid rows
    df = df.dropna(
        subset=["Date", "Amount", "Category"]
    )

    df = df[df["Category"] != ""]

    if df.empty:
        raise ValueError(
            "No valid transactions found."
        )

    return df
