import requests
import json
from pprint import pprint

API_KEY = "2b10reEl4ESP60OUh0FhIcyu"  # Set you API_KEY here
PROJECT = "all" # try "weurope" or "canada"
api_endpoint = f"https://my-api.plantnet.org/v2/identify/{PROJECT}?api-key={API_KEY}"

url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent'

def gemini(prompt):
    headers = {
        'Content-Type': 'application/json',
    }
    params = {
        'key': 'AIzaSyBXgsFwAI340Jn1j69gr15X3rXKTK0rXk0',
    }
    
    json_data = {
        'contents': [
            {
                'parts': [
                    {
                        'text': prompt,
                    },
                ],
            },  
        ],  
    }

    response = requests.post(
        url,
        params=params,
        headers=headers,
        json=json_data,
    )

    return(response.json()['candidates'][0]['content']['parts'][0]['text'])

def getPlant(img_path):
    img_data = open(img_path, 'rb')

    data = {
        'organs': ['auto']
    }

    files = [
        ('images', (img_path, img_data))
    ]

    req = requests.Request('POST', url=api_endpoint, files=files, data=data)
    prepared = req.prepare()

    s = requests.Session()
    response = s.send(prepared)
    json_result = json.loads(response.text)

    return json_result['results'][0]['species']['scientificNameWithoutAuthor'], json_result['results'][0]['species']['commonNames'][0] 

