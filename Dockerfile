FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install fastapi uvicorn hypercorn apscheduler

CMD ["hypercorn", "main:app", "--reload"]
