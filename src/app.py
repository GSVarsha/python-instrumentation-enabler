#!/usr/bin/env python3
import logging
from sys import version_info

from flask import Flask
import requests

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

app = Flask(__name__)

# The Home Route
@app.get('/')
def home():
    return """
    <h1>Welcome to the Space Explorer 🚀</h1>
    <p>Click the button below to fetch a random piece of the universe!</p>
    <a href="/space"><button>Explore Space</button></a>
    """

@app.get("/runtime_version")
def get_runtime_version():
    return {"runtime_version": f"{version_info[0]}.{version_info[1]}.{version_info[2]}"}

# The Requests Route
@app.get('/space')
def get_space_data():
    # Using NASA's Astronomy Picture of the Day API
    api_url = "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY"
    
    try:
        response = requests.get(api_url)
        data = response.json()
        
        # Extracting data from the JSON response
        title = data.get('title')
        img_url = data.get('url')
        explanation = data.get('explanation')
        
        return f"""
        <h1>{title}</h1>
        <img src="{img_url}" style="max-width: 600px; border-radius: 10px;">
        <p style="width: 600px;">{explanation}</p>
        <br>
        <a href="/"><button>Back to Home</button></a>
        """
    except Exception as e:
        return f"failed to fetch data: {e}"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
