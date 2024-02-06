import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()

serper_api_key = os.environ.get("SERP_API_KEY")

def search(query):
    url = "https://google.serper.dev/search"

    payload = json.dumps({
        "q": query
    })

    headers = {
        'X-API-KEY': serper_api_key,
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)

    return response.text


query = "write about the history of the internet"
response = search(query)

response = json.loads(response)
organic_links = [result["link"] for result in response["organic"]]
print('\n\n',organic_links)