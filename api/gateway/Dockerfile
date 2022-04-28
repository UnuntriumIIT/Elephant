FROM python:3.8-slim AS builder
COPY ./api/gateway/requirements.txt .

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install --user -r requirements.txt

FROM python:3.8-slim
WORKDIR /code

COPY --from=builder /root/.local /root/.local
COPY ./api/gateway/gateway.py .
ENV FLASK_APP=gateway.py

ENV PATH=/root/.local:$PATH
EXPOSE 5003

CMD [ "python", "-m" , "flask", "run", "--host=gateway", "--port=5003"]
