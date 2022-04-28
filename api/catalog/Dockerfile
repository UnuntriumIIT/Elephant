FROM python:3.8-slim AS builder
COPY ./api/catalog/requirements.txt .

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install --user -r requirements.txt

FROM python:3.8-slim
WORKDIR /code

COPY --from=builder /root/.local /root/.local
COPY ./api/catalog/catalog_api.py .
ENV FLASK_APP=catalog_api.py
ENV MONGO_CONN_STR=mongodb://root:example@mongo:27017/

ENV PATH=/root/.local:$PATH
EXPOSE 5001
CMD [ "python", "-m" , "flask", "run", "--host=catalog_api", "--port=5001"]
