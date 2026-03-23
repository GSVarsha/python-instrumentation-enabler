#!/usr/bin/env python3

# from instana.instrumentation.wsgi import InstanaWSGIMiddleware

# import instana

import os
import falcon
import logging

# OpenTelemetry Imports
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

# # Instrumentation Hooks
from opentelemetry.instrumentation.falcon import FalconInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

# Import the utility and service classes from the defined structure
# Note: You must ensure the service/ and routes.py files are in the same directory 
# as this app.py for these imports to work.
from routes import CommonClass
from helpservices import Health, Home, Status, Request
from util import AuthMiddleware

def setup_telemetry():
    # --- OpenTelemetry Initialization ---
    # OTLPSpanExporter() automatically uses OTEL_EXPORTER_OTLP_ENDPOINT from env
    resource = Resource.create({
        SERVICE_NAME: os.getenv("OTEL_SERVICE_NAME", "falcon-app"),
    })

    provider = TracerProvider(resource=resource)
    processor = BatchSpanProcessor(OTLPSpanExporter())
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)

    # --- Apply Auto-Instrumentation ---
    FalconInstrumentor().instrument()
    RequestsInstrumentor().instrument()

setup_telemetry()
# Initialize the Falcon application and apply the middleware
api = falcon.App(middleware=[AuthMiddleware()])

# --- Route Definitions ---

# Home route
api.add_route('/', Home())
# Status/Info route
api.add_route('/info', Status())
# Health check route
api.add_route('/health', Health())
# Route for fetching external data
api.add_route('/request', Request())

# Sink (Smart Proxy) - Catches all other requests
# The regex r'/+' ensures it catches any path that has at least one segment
api.add_sink(CommonClass(), r'/')

# # Wrap the application with the Instana WSGI Middleware
# api = InstanaWSGIMiddleware(api)

# --- Main Server Execution ---

if __name__ == '__main__':
    from wsgiref import simple_server
    import logging

    # logging.basicConfig(level=logging.DEBUG)
    
    HOST = '0.0.0.0'
    PORT = 50071
    
    logging.info(f"Starting Falcon server on http://{HOST}:{PORT}")
    
    httpd = simple_server.make_server(HOST, PORT, api)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logging.info("Server shutting down.")
