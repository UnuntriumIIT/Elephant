FROM python:3.8-slim AS builder
COPY ./api/cart/consumer/requirements.txt .

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install --user -r requirements.txt

FROM python:3.8-slim
WORKDIR /code

COPY --from=builder /root/.local /root/.local
COPY ./api/cart/consumer/cart_consumer.py .

ENV PATH=/root/.local:$PATH
CMD ["python", "/code/cart_consumer.py"]
