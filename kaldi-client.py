import requests
import json

url = 'http://localhost:8009/get_text'

payload = json.dumps({ 'audio_path': 'sample_input.wav' })
headers = {
    'content-type': "application/json",
    'cache-control': "no-cache",
    }

for _ in range(10):
    response = requests.request('POST', url, data=payload, headers=headers)
    print(response.text)