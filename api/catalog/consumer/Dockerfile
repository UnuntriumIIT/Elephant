FROM python:3.8-slim AS builder
COPY ./api/catalog/consumer/requirements.txt .

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install --user -r requirements.txt

FROM python:3.8-slim
WORKDIR /code

COPY --from=builder /root/.local /root/.local
COPY ./api/catalog/consumer/catalog_consumer.py .

ENV PATH=/root/.local:$PATH
CMD ["python", "/code/catalog_consumer.py"]
