from utils.supabase_client import supabase

file_path = "sample_transactions.csv"
bucket_name = "expense-files"

with open(file_path, "rb") as file:
    file_data = file.read()

response = supabase.storage.from_(bucket_name).upload(
    path="test/sample_transactions.csv",
    file=file_data,
    file_options={
        "content-type": "text/csv"
    }
)

print("File uploaded successfully!")
print(response)