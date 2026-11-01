import os
import streamlit as st
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Read from Streamlit Cloud Secrets if environment variables are unavailable
if not SUPABASE_URL:
    SUPABASE_URL = st.secrets.get("SUPABASE_URL")

if not SUPABASE_KEY:
    SUPABASE_KEY = st.secrets.get("SUPABASE_KEY")

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)