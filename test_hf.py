import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-small"
headers = {"Authorization": f"Bearer {os.getenv('HF_API_KEY')}"}

payload = {"inputs": "Hello, how are you?"}
response = requests.post(API_URL, headers=headers, json=payload)

print("Status Code:", response.status_code)
try:
    print("Response:", response.json())
except:
    print("Raw Response:", response.text)
