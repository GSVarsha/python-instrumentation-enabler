FROM public.ecr.aws/docker/library/python:3.10-slim-bookworm

# Copy application files
COPY src/. /app
WORKDIR /app

RUN python -m pip install -r requirements.txt

EXPOSE 8080

CMD [ "python", "app.py" ]
