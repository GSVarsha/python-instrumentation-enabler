#!/usr/bin/env python3
import instana

import logging
import os
from sys import version_info

from flask import Flask
import requests

# OpenTelemetry Imports
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

# # Instrumentation Hooks
# from opentelemetry.instrumentation.flask import FlaskInstrumentor
# from opentelemetry.instrumentation.requests import RequestsInstrumentor

def setup_telemetry(app):
    # --- OpenTelemetry Initialization ---
    # OTLPSpanExporter() automatically uses OTEL_EXPORTER_OTLP_ENDPOINT from env
    resource = Resource.create({
        SERVICE_NAME: os.getenv("OTEL_SERVICE_NAME", "space-explorer-app"),
    })

    provider = TracerProvider(resource=resource)
    processor = BatchSpanProcessor(OTLPSpanExporter())
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)

    # # --- Apply Auto-Instrumentation ---
    # FlaskInstrumentor().instrument_app(app)
    # RequestsInstrumentor().instrument()

# Initialize Flask
app = Flask(__name__)
setup_telemetry(app)

# Create a tracer for custom spans
tracer = trace.get_tracer(__name__)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

@app.get("/")
def home():
    return """
    <h1>Welcome to the Space Explorer 🚀</h1>
    <p>Click the button below to fetch a random piece of the universe!</p>
    <a href="/space"><button>Explore Space</button></a>
    """

@app.get("/runtime_version")
def get_runtime_version():
    return {"runtime_version": f"{version_info[0]}.{version_info[1]}.{version_info[2]}"}

@app.get("/space")
def get_space_data():
    # We wrap the core logic in a custom span to track business logic separately
    with tracer.start_as_current_span("fetch-nasa-data") as span:
        print(tracer, type(tracer))
        api_key = os.environ.get("NASA_APOD_API_KEY", "DEMO_KEY")
        api_url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}"
        
        # Adding an attribute to our span for better filtering in the backend
        span.set_attribute("nasa.api_url", api_url)

        try:
            # This call is automatically instrumented by RequestsInstrumentor
            response = requests.get(api_url, timeout=10)

            if response.status_code == 429:
                span.set_status(trace.Status(trace.StatusCode.ERROR, "Rate Limited"))
                return "🚀 NASA says we've looked at the stars too much! (Rate limit exceeded.)"

            response.raise_for_status()
            data = response.json()

            title = data.get("title")
            media_url = data.get("url")
            explanation = data.get("explanation")

            if data.get("media_type") == "video":
                media_content = f'<video width="600" style="border-radius: 10px;" controls src="{media_url}"></video>'
            else:
                media_content = f'<img src="{media_url}" style="max-width: 600px; border-radius: 10px;">'

            return f"""
            <div style="max-width: 600px;">
                <h1>{title}</h1>
                {media_content}
                <p style="font-size: 18px; line-height: 1.6; color: #333;">{explanation}</p>
                <br>
                <a href="/"><button style="cursor: pointer;">Back to Home</button></a>
            </div>
            """
        except Exception as e:
            logger.error(f"Error fetching space data: {e}")
            span.record_exception(e)
            return f"failed to fetch data: {e}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
