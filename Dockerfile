FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./aiops /app
COPY ./run.sh /run.sh