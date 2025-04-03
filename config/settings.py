import os
from dotenv import load_dotenv

# Load environment variables from `.env` file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

# 🚀 TOR Configuration
TOR_PASSWORD = os.getenv("hashed@02")

# 🔍 VirusTotal API Key (for IOC validation)
VIRUSTOTAL_API_KEY = os.getenv("0a3113ea071cab5b574e9901d7588bfdeda15449d69e856bbf964b4907d9c7de")

# 💾 MongoDB Connection Settings
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "DarkWebDB")

# ✅ Debugging: Print settings (REMOVE in Production)
if __name__ == "__main__":
    print(f"🔹 TOR Password: {TOR_PASSWORD}")
    print(f"🔹 VirusTotal API Key: {VIRUSTOTAL_API_KEY}")
    print(f"🔹 MongoDB URI: {MONGO_URI}")
    print(f"🔹 MongoDB Name: {MONGO_DB_NAME}")
