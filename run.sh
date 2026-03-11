#!/usr/bin/env bash

# The `opentelemetry-bootstrap -a install` command reads through the list of packages installed in your active `site-packages` folder, and
# installs the corresponding instrumentation libraries for these packages, if applicable.
# flask -> opentelemetry-instrumentation-flask
echo -e "Setting up the opentelemetry-bootstrap ..."
uv run opentelemetry-bootstrap -a install

export OTEL_SERVICE_NAME="otel-to-instana-varsha"

# Before OpenTelemetry Python 1.40.0 logs auto instrumentation was disabled by default and implemented in the opentelemetry-sdk package. 
# Setting OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED to true would have enabled it.
# export OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true

export FLASK_APP=app.py
# export FLASK_RUN_HOST=0.0.0.0
# export FLASK_RUN_PORT=8080

echo -e "Instrumenting the app..."

# The OpenTelemetry Python agent (opentelemetry-instrument) will use monkey patching to modify functions in these libraries at runtime.
uv run opentelemetry-instrument \
    --logs_exporter otlp \
    --traces_exporter console,otlp \
    --metrics_exporter otlp \
    flask run -p 8080 -h 0.0.0.0
