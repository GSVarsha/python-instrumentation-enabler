import falcon
import time
import json
import requests
from falcon import code_to_http_status  # Import this utility

# Simulate application start time
START_TIME = time.time()
VERSION = "1.0.0"

class Home:
    """Handles the root route '/'."""
    def on_get(self, req: falcon.Request, resp: falcon.Response):
        """GET /"""
        resp.status = falcon.HTTP_200
        resp.content_type = falcon.MEDIA_JSON
        resp.text = json.dumps({
            "message": "Welcome to the Simple Falcon API!",
            "version": VERSION,
            "endpoints": ["/", "/info", "/health"]
        })

class Status:
    """Handles the informational route '/info'."""
    def on_get(self, req: falcon.Request, resp: falcon.Response):
        """GET /info"""
        uptime_seconds = int(time.time() - START_TIME)
        
        # Calculate uptime in human-readable format
        days = uptime_seconds // (24 * 3600)
        hours = (uptime_seconds % (24 * 3600)) // 3600
        minutes = (uptime_seconds % 3600) // 60
        seconds = uptime_seconds % 60

        resp.status = falcon.HTTP_200
        resp.content_type = falcon.MEDIA_JSON
        resp.text = json.dumps({
            "name": "simple-falcon-api",
            "version": VERSION,
            "status": "Running",
            "uptime": f"{days}d {hours}h {minutes}m {seconds}s",
            "environment": "development"
        })

class Health:
    """Handles the health check route '/health'."""
    def on_get(self, req: falcon.Request, resp: falcon.Response):
        """GET /health"""
        # A simple health check always returns 200 OK and "UP"
        resp.status = falcon.HTTP_200
        resp.content_type = falcon.MEDIA_JSON
        resp.text = json.dumps({"status": "UP", "message": "Service is operational."})

class Request:
    """
    Handles the '/request' endpoint by proxying an external GET request.
    This simulates the logic requested by the user: requests.get('...') and return JSON.
    """
    def on_get(self, req: falcon.Request, resp: falcon.Response):
        """GET /request"""
        # External URL to fetch data from
        external_url = "https://www.httpbin.org/get"

        # Make the external request with a timeout
        api_resp = requests.get(external_url, timeout=5)
        api_resp.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        # Set the response status and content from the external API
        resp.status = code_to_http_status(api_resp.status_code)
        resp.content_type = falcon.MEDIA_JSON
        resp.text = api_resp.text
