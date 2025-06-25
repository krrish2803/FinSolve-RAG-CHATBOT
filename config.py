import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
DATA = "./data"
ROLES = ["Finance", "Marketing", "HR", "Engineering", "C-Level", "Employee"]