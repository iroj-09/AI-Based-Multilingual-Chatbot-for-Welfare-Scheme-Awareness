import json
import os
import time
import requests
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()

API_KEY = os.getenv("MYSCHEME_API_KEY")

headers = {
    "accept": "application/json",
    "origin": "https://www.myscheme.gov.in",
    "user-agent": "Mozilla/5.0",
    "x-api-key": API_KEY
}

with open(r".\backend\data\schemes.json", "r", encoding="utf-8") as f:
    schemes = json.load(f)
    

for scheme in tqdm(schemes):

    scheme_id = scheme["data"]["_id"]

    url = f"https://api.myscheme.gov.in/schemes/v6/public/schemes/{scheme_id}/documents"

    response = requests.get(
        url,
        headers=headers,
        params={"lang": "en"},
        timeout=30
    )

    if response.status_code == 200:
        scheme["documents"] = response.json()
    else:
        scheme["documents"] = None
        print(f"Failed: {scheme_id}")

    time.sleep(0.2)
    
    
with open("./backend/data/schemes_with_documents.json", "w", encoding="utf-8") as f:
    json.dump(schemes, f, indent=4, ensure_ascii=False)