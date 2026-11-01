
import streamlit as st
import pandas as pd
import plotly.express as px
import io

from utils.data_processor import load_transactions

from utils.analyzer import (
    calculate_summary,
    calculate_category_expenses,
    calculate_monthly_summary,
    calculate_health_score
)


# -------------------------------
# Page Configuration
# -------------------------------

st.set_page_config(
    page_title="Smart Expense Analyzer",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Smart Expense Analyzer")

st.write(
    "Analyze your income, expenses, and spending habits."
)


# -------------------------------
# File Upload
# -------------------------------

uploaded_file = st.file_uploader(
    "Upload your transactions CSV",
    type=["csv"]
)


if uploaded_file is not None:

    try:

        # Load and clean transactions
        df = load_transactions(uploaded_file)

        # -------------------------------
        # Sidebar Filters
        # -------------------------------

        st.sidebar.header("Filters")

        categories = sorted(
            df["Category"].unique()
        )

        selected_categories = (
            st.sidebar.multiselect(
                "Select categories",
                options=categories,
                default=categories
            )
        )

        min_date = df["Date"].min().date()
        max_date = df["Date"].max().date()

        date_range = st.sidebar.date_input(
            "Select date range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )

        if len(date_range) == 2:

            start_date, end_date = date_range

            filtered_df = df[
                (df["Date"].dt.date >= start_date)
                & (df["Date"].dt.date <= end_date)
                & (df["Category"].isin(
                    selected_categories
                ))
            ]

        else:

            filtered_df = df[
                df["Category"].isin(
                    selected_categories
                )
            ]

        if filtered_df.empty:

            st.warning(
                "No transactions match the filters."
            )

            st.stop()

        # -------------------------------
        # Financial Summary
        # -------------------------------

        summary = calculate_summary(
            filtered_df
        )

        health = calculate_health_score(
            summary
        )

        st.subheader("Financial Summary")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Income",
            f"₹{summary['income']:,.2f}"
        )

        col2.metric(
            "Expenses",
            f"₹{summary['expenses']:,.2f}"
        )

        col3.metric(
            "Net Savings",
            f"₹{summary['savings']:,.2f}"
        )

        col4.metric(
            "Savings Rate",
            f"{summary['savings_rate']:.1f}%"
        )

        # -------------------------------
        # Financial Health
        # -------------------------------

        st.subheader("Financial Health")

        st.metric(
            "Health Score",
            f"{health['score']:.1f}/100",
            health["status"]
        )

        st.progress(
            int(health["score"])
        )

        # -------------------------------
        # Category Expenses
        # -------------------------------

        st.subheader("Category-wise Expenses")

        category_expenses = (
            calculate_category_expenses(
                filtered_df
            )
        )

        if not category_expenses.empty:

            fig = px.pie(
                category_expenses,
                names="Category",
                values="Amount",
                title="Spending by Category"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # -------------------------------
        # Monthly Trends
        # -------------------------------

        st.subheader("Monthly Trends")

        monthly_summary = (
            calculate_monthly_summary(
                filtered_df
            )
        )

        if not monthly_summary.empty:

            fig = px.bar(
                monthly_summary,
                x="Month",
                y=["Income", "Expenses"],
                barmode="group",
                title="Monthly Income vs Expenses"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # -------------------------------
        # Transactions
        # -------------------------------

        st.subheader("Transactions")

        st.dataframe(
            filtered_df.sort_values(
                "Date",
                ascending=False
            ),
            use_container_width=True
        )

        # -------------------------------
        # Download Financial Analysis Report
        # -------------------------------

        st.subheader("Download Report")

        # Create an in-memory Excel file
        output = io.BytesIO()

        # Prepare financial summary data
        summary_df = pd.DataFrame({
            "Metric": [
                "Total Income",
                "Total Expenses",
                "Net Savings",
                "Savings Rate (%)",
                "Financial Health Score",
                "Financial Health Status"
            ],

            "Value": [
                summary["income"],
                summary["expenses"],
                summary["savings"],
                round(summary["savings_rate"], 2),
                round(health["score"], 2),
                health["status"]
            ]
        })

        # Generate Excel workbook
        with pd.ExcelWriter(
            output,
            engine="openpyxl"
        ) as writer:

            # Sheet 1: Financial Summary
            summary_df.to_excel(
                writer,
                sheet_name="Financial Summary",
                index=False
            )

            # Sheet 2: Category-wise Expenses
            category_expenses.to_excel(
                writer,
                sheet_name="Category Expenses",
                index=False
            )

            # Sheet 3: Monthly Income and Expenses
            monthly_summary.to_excel(
                writer,
                sheet_name="Monthly Summary",
                index=False
            )

            # Sheet 4: Transaction Details
            filtered_df.to_excel(
                writer,
                sheet_name="Transactions",
                index=False
            )

        # Download button
        st.download_button(
            label="Download Financial Analysis Report",
            data=output.getvalue(),
            file_name="financial_analysis_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:

        st.error(
            f"Error processing file: {e}"
        )

else:

    st.info(
        "Upload a CSV file to get started."
    )
