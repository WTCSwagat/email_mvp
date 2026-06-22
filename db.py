
import os

from dotenv import load_dotenv
from supabase import create_client
load_dotenv()
client = create_client(url=os.getenv("SUPABASE_URL"), key=os.getenv("SUPABASE_KEY"))