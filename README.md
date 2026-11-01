# Smart Expense Analyzer

A web-based application that analyzes financial transactions and provides insights into income, expenses, savings, and spending patterns.

## Features

- Upload transaction data using CSV files.
- Calculate total income, expenses, net savings, and savings rate.
- Evaluate financial health using a health score.
- Visualize category-wise expenses and monthly financial trends.
- Filter transactions by category and date range.
- Download financial analysis reports in Excel format.
- Store uploaded CSV files in Supabase Storage.

## Tech Stack

- **Language:** Python
- **Frontend:** Streamlit
- **Data Processing:** Pandas
- **Visualization:** Plotly
- **Cloud Storage:** Supabase
- **Containerization:** Docker
- **Deployment:** Streamlit Community Cloud

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Pai-Pratheeksha/Smart_Expense_Analyzer.git
cd Smart_Expense_Analyzer
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

**Windows**
```bash
venv\Scripts\activate
```

**Linux/macOS**
```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_publishable_key
```

### 5. Run the application

```bash
streamlit run app.py
```

## Docker

Build the Docker image:

```bash
docker build -t smart-expense-analyzer .
```

Run the container:

```bash
docker run -p 8501:8501 smart-expense-analyzer
```

Access the application at `http://localhost:8501`.

## Project Structure

```text
Smart_Expense_Analyzer/
├── app.py
├── utils/
│   ├── data_processor.py
│   ├── analyzer.py
│   └── supabase_client.py
├── sample_transactions.csv
├── requirements.txt
├── Dockerfile
├── .dockerignore
└── README.md
```

## License

This project is intended for educational and personal use.
