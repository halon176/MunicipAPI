FROM python:3.10

LABEL org.opencontainers.image.source="https://github.com/halon176/MunicipAPI"

RUN mkdir /municipapi_app

WORKDIR municipapi_app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD gunicorn src.main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
