FROM public.ecr.aws/docker/library/python:3.10-slim-bookworm

WORKDIR /app

# 1. Copy only requirements first to leverage Docker cache
COPY src/requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

# 2. Copy the rest of the application code
COPY src/ .

EXPOSE 8080

CMD [ "python", "app.py" ]
