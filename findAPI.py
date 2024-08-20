import json
import requests
from fastapi import FastAPI, HTTPException
from typing import List, Optional
import nest_asyncio
import uvicorn
from pyngrok import ngrok

nest_asyncio.apply()  # Allow nested event loops in Jupyter/Colab

app = FastAPI()

# Path to the JSON file
JSON_FILE_PATH = 'json filepath'

def load_person_data():
    with open(JSON_FILE_PATH, 'r') as file:
        return json.load(file)

data = load_person_data()

def find_matching_person(name: Optional[str] = None, image_url: Optional[str] = None):
    matches = []
    for person in data:
        if (name and name.lower() in person['name'].lower()) or (image_url and person['image'] == image_url):
            matches.append(person)
    return matches

@app.get("/api/persons", response_model=List[dict])
def get_persons():
    return data

@app.get("/api/match")
def match_person(input: str):
    if not input:
        raise HTTPException(status_code=400, detail="No input provided")

    if input.startswith("http://") or input.startswith("https://"):
        profile = find_matching_person(image_url=input)
    else:
        profile = find_matching_person(name=input)

    if profile:
        return profile
    else:
        raise HTTPException(status_code=404, detail="No matching profile found")

# Expose the FastAPI app through ngrok
ngrok.set_auth_token("ngrok token")
public_url = ngrok.connect(8000)
#print(public_url)

uvicorn.run(app, host="0.0.0.0", port=8000)