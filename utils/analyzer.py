
import pandas as pd


def calculate_summary(df):
    """
    Calculate income, expenses, savings,
    and savings rate.
    """

    income = df.loc[
        df["Amount"] > 0, "Amount"
    ].sum()

    expenses = abs(
        df.loc[
            df["Amount"] < 0, "Amount"
        ].sum()
    )

    savings = income - expenses

    savings_rate = (
        (savings / income) * 100
        if income > 0 else 0
    )

    return {
        "income": income,
        "expenses": expenses,
        "savings": savings,
        "savings_rate": savings_rate
    }


def calculate_category_expenses(df):
    """
    Calculate expenses for each category.
    """

    expense_df = df[
        df["Amount"] < 0
    ].copy()

    expense_df["Amount"] = (
        expense_df["Amount"].abs()
    )

    category_expenses = (
        expense_df.groupby("Category")["Amount"]
        .sum()
        .reset_index()
    )

    return category_expenses


def calculate_monthly_summary(df):
    """
    Calculate monthly income and expenses.
    """

    df = df.copy()

    df["Month"] = (
        df["Date"].dt.to_period("M").astype(str)
    )

    income_df = df[df["Amount"] > 0]

    expense_df = df[df["Amount"] < 0].copy()

    expense_df["Amount"] = (
        expense_df["Amount"].abs()
    )

    monthly_income = (
        income_df.groupby("Month")["Amount"]
        .sum()
        .rename("Income")
    )

    monthly_expenses = (
        expense_df.groupby("Month")["Amount"]
        .sum()
        .rename("Expenses")
    )

    monthly_summary = pd.concat(
        [monthly_income, monthly_expenses],
        axis=1
    ).fillna(0).reset_index()

    return monthly_summary


def calculate_health_score(summary):
    """
    Calculate a simple financial health score
    based on savings rate.
    """

    savings_rate = summary["savings_rate"]

    score = min(
        max(savings_rate, 0),
        100
    )

    if score >= 30:
        status = "Good"

    elif score >= 15:
        status = "Moderate"

    else:
        status = "Needs Improvement"

    return {
        "score": score,
        "status": status
    }
