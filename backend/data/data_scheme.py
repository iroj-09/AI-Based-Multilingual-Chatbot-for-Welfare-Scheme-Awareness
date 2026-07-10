import os
import requests
from dotenv import load_dotenv
import json

load_dotenv()

API_KEY = os.getenv("MYSCHEME_API_KEY")

headers = {
    "accept": "application/json",
    "origin": "https://www.myscheme.gov.in",
    "user-agent": "Mozilla/5.0",
    "x-api-key": API_KEY
}

params = {
    "lang": "en",
    "q": '[{"identifier":"schemeCategory","value":"Agriculture,Rural & Environment"}]',
    "keyword": "",
    "sort": "",
    "from": 0,
    "size": 100
}

url = "https://api.myscheme.gov.in/search/v6/schemes"

response = requests.get(url, headers=headers, params=params)

print(response.status_code)

data = response.json()

items = data["data"]["hits"]["items"]


slugs=[]

for offset in range(0,852,100):

    params["from"]=offset

    response=requests.get(url,headers=headers,params=params)

    data=response.json()

    for item in data["data"]["hits"]["items"]:
        slugs.append(item["fields"]["slug"])

schemes = []

base_url = "https://api.myscheme.gov.in/schemes/v6/public/schemes"

for slug in slugs:
    params = {
        "slug": slug,
        "lang": "en"
    }
    response = requests.get(base_url, headers=headers, params=params)
    schemes.append(response.json())
    
    
with open("./backend/data/schemes.json", "w", encoding="utf-8") as f:
    json.dump(schemes, f, ensure_ascii=False, indent=4) 
    
    
