#!/usr/bin/env python3
import logging
from sys import version_info
import os

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
    api_key = os.environ.get('NASA_APOD_API_KEY', 'DEMO_KEY')
    api_url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}"
    
    try:
        response = requests.get(api_url, timeout=10)
        
        # Specific check for Rate Limiting
        if response.status_code == 429:
            return "🚀 NASA says we've looked at the stars too much! (Rate limit exceeded. Please try again later.)"
        
        response.raise_for_status()
        data = response.json()
        
        # Extracting data from the JSON response
        title = data.get('title')
        media_url = data.get('url')
        explanation = data.get('explanation')

        # Determine if the content is a video or an image
        if data.get('media_type') == "video":
            media_content = f'<video width="600" style="border-radius: 10px;" controls src="{media_url}"></video>'
        else:
            media_content = f'<img src="{media_url}" style="max-width: 600px; border-radius: 10px;">'

        return f"""
        <div style="max-width: 600px;">
            <h1>{title}</h1>
            {media_content}
            <p style="font-size: 18px; line-height: 1.6; color: #333;">
                {explanation}
            </p>
            <br>
            <a href="/"><button style="padding: 10px 20px; cursor: pointer;">Back to Home</button></a>
        </div>
        """
    except Exception as e:
        return f"failed to fetch data: {e}"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
