FROM python:3.8-slim AS builder
COPY ./api/cart/requirements.txt .

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install --user -r requirements.txt

FROM python:3.8-slim
WORKDIR /code

COPY --from=builder /root/.local /root/.local
COPY ./api/cart/cart_api.py .
ENV FLASK_APP=cart_api.py

ENV PATH=/root/.local:$PATH
EXPOSE 5004

CMD [ "python", "-m" , "flask", "run", "--host=cart_api", "--port=5004"]
