import requests
import tomllib
import json

with open(".streamlit/secrets.toml", "rb") as f:
    secrets = tomllib.load(f)

api_key = secrets.get("NVIDIA_API_KEY", "")
print("API Key:", api_key[:10] + "...")

url = "https://integrate.api.nvidia.com/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# Test different models
models = [
    "meta/llama-3.2-3b-instruct",
    "meta/llama3-8b-instruct",
    "meta/llama-3.1-8b-instruct"
]

for model in models:
    print(f"\n--- Testing Model: {model} ---")
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": "Hello! Reply with exactly one word."}
        ],
        "temperature": 0.3,
        "max_tokens": 10
    }
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30.0)
        print("Status Code:", response.status_code)
        if response.status_code == 200:
            print("Response Content:", response.json()["choices"][0]["message"]["content"])
        else:
            print("Error Response:", response.text)
    except Exception as e:
        print("Exception:", e)
